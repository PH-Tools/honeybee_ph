# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used to merge Honeybee-Rooms together"""
from typing import List
from honeybee import room, face
from honeybee.boundarycondition import Outdoors, Ground
from honeybee_energy.boundarycondition import Adiabatic


def get_room_exposed_faces(_hb_room: room.Room) -> List[face.Face3D]:
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

    exposed_faces = []
    for hb_room in _hb_rooms:
        exposed_faces += get_room_exposed_faces(hb_room)

    new_room = room.Room(
        identifier=reference_room.properties.ph.ph_bldg_segment.name,
        faces=exposed_faces,
    )

    # -- Set the new Room's properties.ph to match the 'reference' room
    dup_ph_prop = reference_room._properties.ph.duplicate(
        new_room._properties.ph, include_spaces=False)
    setattr(new_room._properties, '_ph', dup_ph_prop)

    # -- Then, collect all the spaces from the input rooms and add to the NEW room
    # -- DEVELOPER NOTE: this has to be done AFTER the duplicate()
    # -- call, otherwise not all the spaces will transfer over properly.
    for hb_room in _hb_rooms:
        for existing_space in hb_room.properties.ph.spaces:
            # -- Preserve the original HB-Room's energy and ph properties over
            # -- on the space. We need to do this cus' the HB-Room is being removed
            # -- and we want to presever HVAC and program info for the spaces.
            existing_space.properties._energy = hb_room.properties._energy.duplicate(
                new_host=existing_space)
            existing_space.properties._ph = hb_room.properties._ph.duplicate(
                new_host=existing_space)
            new_room.properties.ph.add_new_space(existing_space)

    return new_room
