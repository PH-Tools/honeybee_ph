# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to Add Spaces onto Honeybee Rooms."""

from collections import namedtuple

from honeybee_ph import space
from honeybee import room
from honeybee_ph_rhino import gh_io
from ladybug_rhino.fromgeometry import from_point3d
from ladybug_rhino.togeometry import to_point3d


SpaceData = namedtuple('SpaceData', ['space', 'reference_points'])


def offset_space_reference_points(IGH, _space, _dist=0):
    # type (gh_io.IGH, space.Space) -> space.Space
    """Move the Space's floor segments 'up' in the world-Z some distance. This is
        useful since if the reference point is directly 'on' the honeybee-Room's floor 
        surface, sometimes it will not test as 'inside' correctly. Tolerance issue?

    Arguments:
    ----------
        * IGH (gh_io.IGH): The Grasshopper interface object.
        * _space (space.Space): A Space to operate on.
        * _dist (float): A distance to offset the reference point.

    Returns:
    --------
        * space.Space: A copy of the input Space with the floor-segment reference 
            points modified.
    """

    if _dist == 0:
        return _space

    new_space = _space.duplicate()
    for volume in new_space.volumes:
        for seg in volume.floor._floor_segments:
            seg.reference_point = to_point3d(
                IGH.grasshopper_components.Move(
                    from_point3d(seg.reference_point),
                    IGH.grasshopper_components.UnitZ(_dist)).geometry
            )
    return new_space


def add_spaces_to_honeybee_rooms(_spaces, _hb_rooms, _inherit_names=False):
    # type: (list[space.Space], list[room.Room], bool) -> tuple[list[room.Room], list[SpaceData]]
    """Sorts a list of Spaces, checks which are 'in' which HB-Room, and adds the space to that room.

    Arguments:
    ----------
        * _spaces (list[space.Space]) A list of Spaces.
        * _hb_rooms (list[room.Room]): A list of Honeybee Rooms.
        * _inherit_names (bool) default=False. Set True to override all space names
            with the name of the parent Honeybee-Room.

    Returns:
    --------
        (list[room.Room]): A list of Honeybee rooms with Spaces added to them. 
    """

    # -- Organize the spaces into a dict and pull out the reference points
    # -- This is done to avoid re-collecting the points at each is_point_inside
    # -- check and so that 'del' can be used to speed up the hosting checks.
    spaces_dict = {}
    for space in _spaces:
        spaces_dict[id(space)] = SpaceData(space, [pt for pt in space.reference_points])

    # -- Duplicate HB Rooms to ensure no conflicts
    hb_rooms = [rm.duplicate() for rm in _hb_rooms]

    # -- Add the spaces to the host-rooms
    new_rooms = []
    for room in hb_rooms:

        # -- See if any of the Space Reference points are inside the Room Geometry
        for space_data_id, space_data in spaces_dict.items():
            for pt in space_data.reference_points:
                if not room.geometry.is_point_inside(pt):
                    continue

                sp = space_data.space
                sp.host = room

                # -- If 'inherit names', simplify the spaces so that
                # -- there is only a single space inside of the HB-Room
                # -- and it will inherit its name from the parent HB-Room.
                if _inherit_names:
                    sp.name = room.display_name
                    room.properties.ph.merge_new_space(sp)
                else:
                    room.properties.ph.add_new_space(sp)

                # -- to speed up further checks
                del spaces_dict[space_data_id]
                break

        new_rooms.append(room)

    # -- There should not be any spaces left in the dict if all were
    # -- hosted properly. Raise warning error if any are un-hosted?
    un_hosted_spaces = []
    if spaces_dict:
        for space in spaces_dict.values():
            un_hosted_spaces.append(space)

    return new_rooms, un_hosted_spaces
