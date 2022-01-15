# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create 'Space' objects from Rhino/Grasshopper inputs."""

from functools import partial
from collections import defaultdict
from functools import reduce
from honeybee_ph_rhino import gh_io
from honeybee_ph import space


def create_volumes(_floor_segments, _heights):
    # type (list, list) -> list[space.SpaceVolume]
    """Create new SpaceVolume objects for a list of SpaceFloorSegments.

    Arguments:
    ----------
        * _floor_segments (list[space.SpaceFloorSegments]): A list of the SpaceFloorSegments to create
            SpaceVolume objects from.
        * _heights (list[float]): A list of the heights for each of the SpaceVolumes.

    Returns:
    --------
        * list[space.SpaceVolume]: A list of SpaceVolume objects created.
    """

    volumes = []
    for i, flr_seg in enumerate(_floor_segments):
        new_volume = space.SpaceVolume()

        new_volume.floor.floor_segments.append(flr_seg)

        # default height = 2.5m
        new_volume.avg_ceiling_height = gh_io.clean_get(_heights, i, 2.5)

        volumes.append(new_volume)
    return volumes


def create_spaces(_volumes, _space_names, _space_numbers):
    # type: (list[space.SpaceVolume], list[str], list[str]) -> list[space.Space]
    """Create new Space objects for a list of SpaceVolumes input.

    Arguments:
    ----------
        * _volumes (list[SpaceVolume]): A list of the SpaceVolume objects to create Spaces from.
        * _space_names (list[str]): A list of the space names like "Kitchen", "Restroom", etc..
        * _space_numnbers (list[str]): A list of the space numbers like "101", "102", etc.

    Returns:
    --------
        * list[space.Space]: A list of the Space objects created.
    """

    spaces = []
    for i, volume in enumerate(_volumes):
        new_space = space.Space()

        new_space.volumes.append(volume)
        new_space.name = gh_io.clean_get(
            _space_names, i, 'unnamed_room_{}'.format(i))
        new_space.number = gh_io.clean_get(_space_numbers, i, '00')

        spaces.append(new_space)

    return spaces


def merge_spaces(IGH, space_1, space_2):
    # type: (gh_io.IGH, space.Space, space.Space) -> space.Space
    """Combine two Spaces into a single new space.

    Arguments:
    ----------
        * IGH: The Grasshopper Interface object
        * space_1 (space.Space):
        * space_2 (space.Space):

    Return:
    -------
        space.Space: 
    """

    # TODO: Merge Spaces, join Floor Surfaces, etc...

    return space.Space()


def merge_spaces_by_name(IGH, _spaces):
    # type: (gh_io.IGH, list[space.Space]) -> list[space.Space]
    """Group spaces by their fullnames and merge each group together

    Arguments:
    ----------
        * gh_io.IGH: The Grasshopper Interface Object.
        * _spaces (list[space.Space]): A list of Space objects to try and group/merge.

    Returns:
    --------
        * list[space.Space] A list of new Space objects.
    """

    # -- Group the spaces by full-name. ie: "101-Kitchen", etc
    space_groups = defaultdict(list)
    for space in _spaces:
        space_groups[space.full_name].append(space)

    # -- Merge the groups of spaces together
    # -- Note: Pass the IGH to merge ahead of time uing partial since
    # -- reduce requires a two-argument function.
    _merge_with_IGH = partial(merge_spaces, IGH)
    spaces_ = []
    for space_group in space_groups.values():
        spaces_.append(reduce(_merge_with_IGH, space_group))

    return spaces_
