# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create new SpaceFloor objects based on Rhino / Grasshopper inputs"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython

from collections import defaultdict

from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.make_spaces import floor_segment
from honeybee_ph import space


def gather_neighbor_group_ids(IGH, _flr_segments):
    # type: (gh_io.IGH, list[space.SpaceFloorSegment]) -> tuple[dict[int, set[int]], list[space.SpaceFloorSegment]]
    """Returns a dict of sets of 'Neighbor' (touching) FloorSegment ids.

    Arguments:
    ----------
        * IGH (gh_io.IGH): Honeybee-PH Grasshopper Interface Object.
        * _flr_segments (list[space.SpaceFloorSegment]): A list of the SpaceFloorSegment objects

    Returns:
    -------
        [0] dict[int, set[int]]: A dict of sets of floor-segment ids.
        [1] list[space.SpaceFloorSegment]: A list of any surfaces that cause and error 
            during Merge. If no errors, this list will be empty. 
    """

    error_surfaces = []
    neighbor_group_ids = defaultdict(set)
    # -- Try and merge the SpaceFloorSegments two at a time
    for floor_seg_a in _flr_segments:
        for floor_seg_b in _flr_segments:
            if floor_seg_a == floor_seg_b:
                continue
            input_geometry = [floor_seg_a.geometry, floor_seg_b.geometry]
            try:
                merge_result = IGH.merge_Face3D(input_geometry)
            except:
                error_surfaces += input_geometry
                merge_result = input_geometry

            if len(merge_result) < len(input_geometry):
                # Merge worked, so record the neighbor group ids in the list
                for _k, _v in neighbor_group_ids.items():
                    if id(floor_seg_a) in _v or id(floor_seg_b) in _v:
                        neighbor_group_ids[_k].add(id(floor_seg_a))
                        neighbor_group_ids[_k].add(id(floor_seg_b))
                        break
                else:
                    neighbor_group_ids[id(floor_seg_a)].add(id(floor_seg_a))
                    neighbor_group_ids[id(floor_seg_a)].add(id(floor_seg_b))

    # -- If any FloorSegment groups can't be merged at all
    for floor_seg in _flr_segments:
        for gr in neighbor_group_ids.values():
            if id(floor_seg) in gr:
                break
        else:
            neighbor_group_ids[id(floor_seg)].add(id(floor_seg))

    return (neighbor_group_ids, error_surfaces)


def group_floor_segments_by_neighbor(_neighbor_group_id_groups, _flr_segments):
    # type: (dict[int, set[int]], list[space.SpaceFloorSegment]) -> list[list[space.SpaceFloorSegment]]
    """Group the FloorSegments if they are 'touching'

    Arguments:
    ----------
        * _neighbor_group_id_goups (dict[int, set[int]]): A dict of the floor segment ids grouped.
        * _flr_segments (list[space.SpaceFloorSegment]): A list of the floor segments.

    Returns:
    --------
        * list[list[space.SpaceFloorSegment]]: A list of lists of the touching SpaceFloorSegment Objecst.
    """

    # -- Sort by Neighbor Group results
    floors_sorted_by_neighbor = defaultdict(list)
    for floor in _flr_segments:
        for _k, group_list_ids in _neighbor_group_id_groups.items():
            if id(floor) in group_list_ids:
                floors_sorted_by_neighbor[_k].append(floor)

    return floors_sorted_by_neighbor.values()


def build_floors_from_segments(IGH, _flr_segments):
    # type: (gh_io.IGH, list[space.SpaceFloorSegment]) -> tuple[list[space.SpaceFloor], list[space.SpaceFloorSegment]]
    """Create new SpaceFloor objects from the SpaceFloor Segments. This will attempt to 
        group and merge SpaceFloorSegments if they are touching one another.

    Arguments:
    ----------
        * IGH (gh_io.IGH): Honeybee-PH Grasshopper Interface Object.
        * _flr_segments (list[space.SpaceFloorSegment]): A list of the SpaceFloorSegment
            Objects to use to build the SpaceFloors from.

    Returns:
    --------
        [0] list[space.SpaceFloor]: A list of the new SpaceFloor objects.
        [1] list[space.SpaceFloorSegment]: A list of any surfaces that cause and error 
            during Merge. If no errors, this list will be empty.
    """

    error_surfaces = []
    new_floors = []
    # -- If its just a single FloorSegment
    if len(_flr_segments) == 1:
        new_floor = space.SpaceFloor()
        for seg in _flr_segments:
            new_floor.add_floor_segment(seg)
            new_floor.geometry = seg.geometry.duplicate()
        new_floors.append(new_floor)
    else:
        # -- Sort out the 'neighbor' (ie: touching) SpaceFloorSegment groups
        neighbor_group_ids, error_surfaces = gather_neighbor_group_ids(
            IGH, _flr_segments)
        neighbor_group_flr_segs = group_floor_segments_by_neighbor(
            neighbor_group_ids, _flr_segments)

        # -- Build new Floors for each of the neighbor groups
        for flr_seg_group in neighbor_group_flr_segs:
            grp_face_3Ds = [seg.geometry for seg in flr_seg_group]
            new_flr_seg_geometry = IGH.merge_Face3D(grp_face_3Ds)
            new_floor = space.SpaceFloor()

            for seg in flr_seg_group:
                new_floor.add_floor_segment(seg)
            new_floor.geometry = new_flr_seg_geometry[0][0].duplicate()
            new_floors.append(new_floor)

    return (new_floors, error_surfaces)


def space_floor_from_rh_geom(IGH, _flr_segment_geom):
    # type: (gh_io.IGH, list[Any]) -> tuple[list[space.SpaceFloor], list[space.SpaceFloorSegment]]
    """Return a list of new SpaceFloors built from a list of Rhino floor-segment Geometry.

    Arguments:
    ----------
        * IGH (gh_io.IGH): Honeybee-PH Grasshopper Interface Object.
        * _flr_segment_geom (list[Any]): A list of the Rhino Geometry representing the FloorSegments.

    Returns:
    --------
        [0] list[space.SpaceFloor]: A list of the SpaceFloor objects built from the Rhino Geometry.
        [1] list[space.SpaceFloorSegment]: A list of any surfaces that cause and error 
            during Merge. If no errors, this list will be empty. 
    """

    # -- Build the new SpaceFloorSegments from the Rhino Geometry
    flr_segments = floor_segment.create_floor_segment_from_rhino_geom(
        IGH, _flr_segment_geom)

    # -- Build the new SpaceFloors from the new SpaceFloorSegments
    new_floors, error_surfaces = build_floors_from_segments(IGH, flr_segments)

    return (new_floors, error_surfaces)
