# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used to cleanup / optimize Honeybee-Rooms before outputting to WUFI"""

from re import A
from typing import List

from honeybee import room, face
from honeybee.boundarycondition import Outdoors, Ground
from honeybee_energy.boundarycondition import Adiabatic
from honeybee.room import Room

from honeybee_energy_ph.load import ph_equipment
from PHX.model import project


def _get_room_exposed_faces(_hb_room: room.Room) -> List[face.Face3D]:
    """Returns a list of the exposed Honeybee Faces of a Honeybee Room. Exposed
    faces are faces with a Boundary Condition of: 'Outdoors', 'Ground' or 'Adiabatic'.

    Arguments:
    ----------
        * _hb_room (room.Room): The Honeybee Room to get the faces of.

    Returns:
    --------
        * list[face.Face]: The list of Exposed Honeybee Faces.
    """

    exposed_faces = []
    for original_face in _hb_room.faces:
        if not isinstance(original_face.boundary_condition, (Outdoors, Ground, Adiabatic)):
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


def _add_hb_room_occupancy_to_existing_room(rm_1: Room, rm_2: Room) -> Room:
    """Merges the HBE "People" from one HBE-Room with another HBE-Room.

    Arguments:
    ----------
        * rm_1 (room.Room): A Honeybee Room
        * rm_2 (room.Room): A Honeybee Room

    Returns:
    --------
        * (room.Room) A Honeybee Room
    """

    new_ppl = rm_1.properties.energy.people.duplicate()

    # -- Combine the HB Values
    weighted_val_1 = rm_1.properties.energy.people.people_per_area * rm_1.floor_area
    weighted_val_2 = rm_2.properties.energy.people.people_per_area * rm_2.floor_area
    total_floor_area = rm_1.floor_area + rm_2.floor_area
    weighted_total_val = weighted_val_1 + weighted_val_2
    new_ppl.people_per_area = weighted_total_val / total_floor_area

    # -- Combine the PH Values
    new_ppl.properties.ph.number_bedrooms += int(
        rm_2.properties.energy.people.properties.ph.number_bedrooms)
    new_ppl.properties.ph.number_people += int(
        rm_2.properties.energy.people.properties.ph.number_people)

    rm_1.properties.energy.people = new_ppl

    return rm_1


def _add_hb_room_elec_equip_to_existing_room(rm_1: Room, rm_2: Room) -> Room:
    """
    Merges the electric equipment from one Honeybee Room to another.

    Arguments:
    ----------
        * rm_1 (room.Room): A Honeybee Room
        * rm_2 (room.Room): A Honeybee Room

    Returns:
    --------
        * (room.Room) A Honeybee Room
    """
    # -------------------------------------------------------------------------
    #
    # TODO: Combine the Honeybee Room's HBE Elec Equip Values
    #
    #

    # -------------------------------------------------------------------------
    # -- Combine the PH Elec. Equip it is the same item (same identifier / key)
    equip_coll_1 = rm_1.properties.energy.electric_equipment.properties.ph.equipment_collection
    equip_coll_2 = rm_2.properties.energy.electric_equipment.properties.ph.equipment_collection

    for equip_key, equip in equip_coll_2:
        try:
            equip_coll_1[equip_key].quantity += 1
        except KeyError:
            equip_coll_1.add_equipment(equip)

    return rm_1


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
    # -- Merge the hb_rooms' Occupancy properties
    for hb_room in _hb_rooms:
        new_room = _add_hb_room_occupancy_to_existing_room(new_room, hb_room)

    # -------------------------------------------------------------------------
    # -- Merge the hb_rooms' Elec. Equipment (appliances)
    for hb_room in _hb_rooms:
        new_room = _add_hb_room_elec_equip_to_existing_room(new_room, hb_room)

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
                vert = polygon.vertices[i] = unique_vertix_dict[vert.__hash__()]
            except KeyError:
                unique_vertix_dict[vert.__hash__()] = vert

    return _variant
