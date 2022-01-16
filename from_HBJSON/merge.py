# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to merge Honeybee-Rooms together"""

from honeybee import room, face
from honeybee.boundarycondition import Outdoors, Ground
from honeybee_energy.boundarycondition import Adiabatic


def get_room_exposed_faces(_hb_room: room.Room) -> list[face.Face3D]:
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


def merge_rooms(_hb_rooms: list[room.Room]) -> room.Room:
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

    # -- Set the new Room's properties based on the reference room
    new_room._properties._duplicate_extension_attr(reference_room._properties)

    # Properties, Spaces, etc....

    return new_room
