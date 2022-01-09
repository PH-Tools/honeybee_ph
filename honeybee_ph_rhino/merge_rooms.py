# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to merged / join together Honeybee Rooms into a single new Honeybee Room."""

import honeybee.room
import honeybee.face
from honeybee.boundarycondition import Outdoors, Ground
from honeybee_energy.boundarycondition import Adiabatic


def get_room_exposed_faces(_hb_room):
    # type: (honeybee.room.Room) -> list[honeybee.face.Face]
    """Returns a list of the exposed Honeybee Faces of a Honeybee Room. Exposed 
    faces are faces with a Boundary Condition of: 'Outdoors', 'Ground' or 'Adiabatic'.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room to get the faces of.

    Returns:
    --------
        * list[honeybee.face.Face]: The list of Exposed Honeybee Faces.
    """

    exposed_faces = []
    for original_face in _hb_room.faces:
        if not isinstance(original_face.boundary_condition, (Outdoors, Ground, Adiabatic)):
            continue

        new_face = original_face.duplicate()

        # TODO: This should not be needed? Why isn't duplicate() working right and duping the properties?
        new_face._properties._energy = original_face.properties.energy.duplicate()
        new_face._properties._radiance = original_face.properties.radiance.duplicate()
        new_face._properties._ph = original_face.properties.ph.duplicate()

        exposed_faces.append(new_face)

    return exposed_faces


def merge(_room_list, _room_name):
    # type: (list[honeybee.room.Room], str) -> tuple[honeybee.room.Room, list[honeybee.face.Face]]
    """Merges two or more Honeybee Rooms into a single Honeyebee Room. This will 
    ignore any 'interior' Honeybee-Faces with a 'Surface' boundary condition and will only
    keep the 'exposed' Honeybee Faces to build the new Honeybee Room from.

    Arguments:
    ----------
        * _room_list (list[honeybee.room.Room]): A list of the Honeybee Rooms to merge.
        * _room_name (str): The name to give to the new Honeybee Room.

    Returns:
    --------
        * honeybee.room.Room: The new Honeybee Room.
    """

    exposed_faces = []
    for room in _room_list:
        exposed_faces += get_room_exposed_faces(room)

    new_room = honeybee.room.Room(
        identifier=_room_name,
        faces=exposed_faces,
    )

    return (new_room, exposed_faces)
