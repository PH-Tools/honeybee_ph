# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to Add Spaces onto Honeybee Rooms."""

from collections import namedtuple

from honeybee_ph import space
from honeybee import room


class HostRoomNotFoundError(Exception):
    def __init__(self, _spaces):
        self.space_list = ["{}, ".format(space_data.space.full_name)
                           for space_data in _spaces]
        self.message = 'Error: Host Honeybee-Rooms not found for the spaces: {}'.format(
            self.space_list)
        super(HostRoomNotFoundError, self).__init__(self.message)


SpaceData = namedtuple('SpaceData', ['space', 'reference_points'])


def add_spaces_to_honeybee_rooms(_spaces, _hb_rooms):
    # type: (list[space.Space], list[room.Room]) -> list[room.Room]
    """Sorts a list of Spaces, checks which are 'in' which HB-Room, and adds the space to that room.

    Arguments:
    ----------
        * _spaces (list[space.Space]) A list of Spaces.
        * _hb_rooms (list[room.Room]): A list of Honeybee Rooms.

    Returns:
    --------
        (list[room.Room]): A list of Honeybee rooms with Spaces added to them. 
    """

    # -- Organize the spaces into a dict and pull out the reference points
    # -- This is done to avoide re-collecting the points at each is_point_inside
    # -- check and so that 'del' can be used to speed up the hosting checks.
    spaces_dict = {}
    for space in _spaces:
        spaces_dict[id(space)] = SpaceData(space, [pt for pt in space.reference_points])

    # -- Duplicate HB Rooms to ensure no confilcts
    hb_rooms = [rm.duplicate() for rm in _hb_rooms]

    # -- Add the spaces to the host-rooms
    new_rooms = []
    for room in hb_rooms:

        # -- See if any of the Space Reference points are inside the Room Geometry
        for space_data_id, space_data in spaces_dict.items():
            for pt in space_data.reference_points:
                if room.geometry.is_point_inside(pt):
                    sp = space_data.space
                    sp.host = room
                    room.properties.ph.add_new_space(sp)

                    # -- to speed up further checks
                    del spaces_dict[space_data_id]
                    break

        new_rooms.append(room)

    # -- There should not be any spaces left in the dict if all were
    # -- hosted properly. Raise warning error if any are un-hosted?
    if spaces_dict:
        raise HostRoomNotFoundError(spaces_dict.values())

    return new_rooms
