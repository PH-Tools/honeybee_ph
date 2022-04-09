# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used to cleanup / optimize Honeybee-Rooms before outputting to WUFI"""

from typing import List, Union, Tuple
from functools import partial

from honeybee import room, face
from honeybee.boundarycondition import Outdoors, Ground
from honeybee_energy.boundarycondition import Adiabatic
from honeybee_energy.load import infiltration, people, equipment

from PHX.model import project

HB_BC = Union[Outdoors, Ground, Adiabatic]


def _get_room_exposed_faces(_hb_room: room.Room, _bc_types: Tuple = (Outdoors, Ground, Adiabatic)) -> List[face.Face3D]:
    """Returns a list of the Honeybee Faces within the set of HB-Boundary Conditions specified.

    Arguments:
    ----------
        * _hb_room (room.Room): The Honeybee Room to get the faces of.
        * _type (tuple[HB_BC]): A tuple of the allowable HB-Boundary Conditions.
            default = (Outdoors, Ground, Adiabatic)

    Returns:
    --------
        * list[face.Face]: The list of Exposed Honeybee Faces.
    """

    exposed_faces = []
    for original_face in _hb_room.faces:
        if not isinstance(original_face.boundary_condition, _bc_types):
            continue

        new_face = original_face.duplicate()
        new_face._properties._duplicate_extension_attr(original_face._properties)

        # TODO: Verify this next isn't needed anymore:
        # # -- Duplicate any extensions like .ph, .energy or .radiance
        # for extension_name in original_face.properties._extension_attributes:
        #     original_extension = getattr(original_face._properties, f'_{extension_name}')
        #     new_extension = original_extension.duplicate()
        #     setattr(new_face._properties, f'_{extension_name}', new_extension)

        exposed_faces.append(new_face)

    return exposed_faces


def _get_room_exposed_face_area(_hb_room: room.Room, _bc_types: Tuple) -> float:
    """Returns the total area of the 'exposed' faces in a HB-Room."""
    return sum(f.area for f in _get_room_exposed_faces(_hb_room, _bc_types))


def merge_occupancies(_hb_rooms: List[room.Room]) -> people.People:
    """Returns a new HB-People-Obj with it's values set from a list of input HB-Rooms.

    Arguments:
    ----------
        * _hb_rooms (List[room.Room]): A list of the HB-Rooms to build the merged
            HB-People object from.

    Return:
    ------- 
        * (people.People): A new Honeybee People object with values merged from the HB-Rooms.
    """

    # Tally up all the values from all the rooms
    total_hb_people = 0.0
    total_ph_bedrooms = 0.0
    total_ph_people = 0.0
    for room in _hb_rooms:
        hb_ppl_obj = room.properties.energy.people  # alias
        total_ph_bedrooms += int(hb_ppl_obj.properties.ph.number_bedrooms)
        total_ph_people += int(hb_ppl_obj.properties.ph.number_people)
        total_hb_people += hb_ppl_obj.people_per_area * room.floor_area

    # Build up the new object's attributes
    total_floor_area = sum(rm.floor_area for rm in _hb_rooms)
    new_hb_ppl = _hb_rooms[0].properties.energy.people.duplicate()
    new_hb_ppl.people_per_area = total_hb_people / total_floor_area
    new_hb_ppl.properties.ph.number_bedrooms = total_ph_bedrooms
    new_hb_ppl.properties.ph.number_people = total_ph_people

    return new_hb_ppl


def merge_infiltrations(_hb_rooms: List[room.Room]) -> infiltration.Infiltration:
    """Returns a new HB-Infiltration-Obj with it's values set from a list of input HB-Rooms.

    Arguments:
    ----------
        * _hb_rooms (List[room.Room]): A list of the HB-Rooms to build the merged
            HB-Infiltration object from.

    Return:
    ------- 
        * (infiltration.Infiltration): A new Honeybee Infiltration object 
            with values merged from the HB-Rooms.
    """
    # For Phius, infiltration-exposed surfaces include all, including 'Ground'
    # unlike for Honeybee where only 'Outdoors' count as 'exposed'
    get_rm_infil_exposed_face_area = partial(
        _get_room_exposed_face_area, _bc_types=(Outdoors, Ground))

    # Calculate the total airflow per room, total exposed area per room
    total_m3_s = 0.0
    total_exposed_area = 0.0
    for room in _hb_rooms:
        room_infil_exposed_area = get_rm_infil_exposed_face_area(room)
        room_infil_m3_s = room_infil_exposed_area * \
            room.properties.energy.infiltration.flow_per_exterior_area

        total_exposed_area += room_infil_exposed_area
        total_m3_s += room_infil_m3_s

    # -- Set the new Infiltration Object's attr to the weighted average
    new_infil = _hb_rooms[0].properties.energy.infiltration.duplicate()
    new_infil.flow_per_exterior_area = total_m3_s / total_exposed_area

    return new_infil


def merge_elec_equip(_hb_rooms: List[room.Room]) -> equipment.ElectricEquipment:
    """Returns a new HB-ElectricEquipment-Obj with it's values set from a list of input HB-Rooms.

    Arguments:
    ----------
        * _hb_rooms (List[room.Room]): A list of the HB-Rooms to build the merged
            HB-ElectricEquipment object from.

    Return:
    ------- 
        * (equipment.ElectricEquipment): A new Honeybee ElectricEquipment object 
            with values merged from the HB-Rooms.
    """

    # -- Collect all the unique PH-Equipment in all the rooms.
    # -- Increase the quantity for each duplicate piece of equipment found.
    ph_equipment = {}
    for room in _hb_rooms:
        for equip_key, equip in room.properties.energy.electric_equipment.properties.ph.equipment_collection.items():
            try:
                ph_equipment[equip_key].quantity += 1
            except KeyError:
                ph_equipment[equip_key] = equip

    # -- Calculate the total Watts of elec-equipment, total floor-area
    total_floor_area = sum(rm.floor_area for rm in _hb_rooms)
    total_watts = sum(
        (rm.floor_area * rm.properties.energy.electric_equipment.watts_per_area) for rm in _hb_rooms)

    # -- Build a new HB-Elec-Equip with all the PH-Equipment in it.
    new_hb_equip = _hb_rooms[0].properties.energy.electric_equipment.duplicate()
    new_hb_equip.watts_per_area = total_watts / total_floor_area
    new_hb_equip.properties.ph.equipment_collection.remove_all_equipment()
    for ph_item in ph_equipment.values():
        new_hb_equip.properties.ph.equipment_collection.add_equipment(ph_item)

    return new_hb_equip


def merge_rooms(_hb_rooms: List[room.Room]) -> room.Room:
    """Merge together a group of Honeybee Rooms into a new single HB Room.

    This will
    ignore any 'interior' Honeybee-Faces with a 'Surface' boundary condition and will only
    keep the 'exposed' Honeybee Faces with boundary_conditions of 'Outdoors', 'Ground'
    and 'Adiabatic' to build the new Honeybee Room from.

    Arguments:
    ----------
        * _hb_rooms (list[room.Room]):

    Returns:
    --------
        * room.Room: The new Honeybee Room.
    """
    reference_room = _hb_rooms[0]

    # -------------------------------------------------------------------------
    # -- Get only the 'exposed' faces to build a new HB-Room with
    exposed_faces = []
    for hb_room in _hb_rooms:
        exposed_faces += _get_room_exposed_faces(hb_room)

    new_room = room.Room(
        identifier=reference_room.properties.ph.ph_bldg_segment.name,
        faces=exposed_faces,
    )

    # -------------------------------------------------------------------------
    # -- Set the new Merged-Room's properties.ph and
    # -- properties.energy to match the 'reference' room to start with
    dup_ph_prop = reference_room._properties.ph.duplicate(
        new_room._properties.ph, include_spaces=False)
    setattr(new_room._properties, '_ph', dup_ph_prop)

    dup_energy_prop = reference_room._properties.energy.duplicate(
        new_room._properties.energy)
    setattr(new_room._properties, '_energy', dup_energy_prop)

    # -------------------------------------------------------------------------
    # -- Then, collect all the spaces from the input rooms and add to the NEW room
    # -- NOTE: this has to be done AFTER the duplicate()
    # -- call, otherwise not all the spaces will transfer over properly.
    # -- NOTE: Skip the reference room so it isn't counted twice.
    for hb_room in _hb_rooms[1:]:
        for existing_space in hb_room.properties.ph.spaces:
            # -- Preserve the original HB-Room's energy and ph properties over
            # -- on the space. We need to do this cus' the HB-Room is being removed
            # -- and we want to presever HVAC and program info for the spaces.
            existing_space.properties._energy = hb_room.properties._energy.duplicate(
                new_host=existing_space)
            existing_space.properties._ph = hb_room.properties._ph.duplicate(
                new_host=existing_space)
            new_room.properties.ph.add_new_space(existing_space)

    # -------------------------------------------------------------------------
    # -- Merge the hb_rooms' load values
    new_room.properties.energy.infiltration = merge_infiltrations(_hb_rooms)
    new_room.properties.energy.people = merge_occupancies(_hb_rooms)
    new_room.properties.energy.electric_equipment = merge_elec_equip(_hb_rooms)

    # -------------------------------------------------------------------------
    # -- TODO: Can I merge together the surfaces as well?
    # -- For larger models, I think this will be important.... hmm....

    # -- Organize the surfaces by -> assembly / exposure / orientation (normal)

    return new_room


def weld_vertices(_variant: project.Variant) -> project.Variant:
    """
    Used to try and weld/unify the vertices of a variant.

    This is helpful to reduce the complexity / number of variants in a large
    model so that WUFI can actually open it.

    Arguments:
    ----------
        * _variant (project.Variant): The Variant object to weld the vertices for.

    Returns:
    --------
        * (project.Variant): The variant, with its vertix objects welded.

    """

    unique_vertix_dict = {}
    for polygon in _variant.graphics3D.polygons:
        for i, vert in enumerate(polygon.vertices):
            try:
                vert = polygon.vertices[i] = unique_vertix_dict[vert.unique_key]
            except KeyError:
                unique_vertix_dict[vert.unique_key] = vert

    return _variant
