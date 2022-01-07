# # -*- coding: utf-8 -*-
# # -*- Python Version: 2.7 -*-

# """Functions to create new FloorSegments and Floors based on Rhino Geometry input"""

# from collections import defaultdict
# from collections import namedtuple

# from honeybee.room import Room
# from honeybee.face import Face
# import honeybee_ph.space
# from honeybee_ph_rhino import gh_io
# from honeybee_ph_rhino.create_spaces import FloorSegmentData, VentilationData

# FlrSegGroup = namedtuple(
#     'FlrSegGroup', ['hb_room', 'flr_seg_input_data', 'floor_segments'])


# def sort_flr_srfcs_by_hb_room(_floor_surfaces_data, _hb_rooms):
#     # type: (list[FloorSegmentData], list[Room]) -> list[FlrSegGroup]
#     """Sorts the floor surfaces based on which HB Room they are 'in'

#     Uses the HB Room's 'is_point_inside()' method and tests against each floor surface's
#     centroid. So note that the entire surface might not be 'in' the room - just
#     the centroid.

#     Arguments:
#     ----------
#         * _floor_surfaces_data (list[FloorSegmentData]):
#         * _hb_rooms (list[Room]): A list of Honeybee Rooms to test the floor segments against.

#     Returns:
#     --------
#         * rooms (list[RoomInputData]]): List of data with floorsegments organized
#             by which honeybee room they are 'in'.
#     """

#     # -- Convert the list to a dict so can remove items during iteration (trying to help speed up)
#     _floor_surfaces_dict = {id(srfc): srfc for srfc in _floor_surfaces_data}

#     rooms = []
#     for room in _hb_rooms:
#         if not room:
#             continue

#         room_data = FlrSegGroup(room, [], [])
#         for k, flr_segment_dict in _floor_surfaces_dict.items():
#             for face in flr_segment_dict.geometry:
#                 if room.geometry.is_point_inside(face.centroid):
#                     room_data.flr_seg_input_data.append(flr_segment_dict)
#                     del _floor_surfaces_dict[k]  # -- to help speed up later 'in' tests

#         rooms.append(room_data)

#     # -- If any are left in the dict, throw Exception
#     if _floor_surfaces_dict:
#         for _ in _floor_surfaces_dict.values():
#             raise Exception(
#                 "Error: Cannot find a host Honeybee room for the floor"
#                 'segment: "{}"?\nPlease make sure it is inside a Honeybee-Room?'.format(
#                     _.name)
#             )

#     return rooms


# def add_default_floor_surfaces(IGH, _flr_segment_groups):
#     # type: (gh_io.IGH, list[FlrSegGroup]) -> list[FlrSegGroup]
#     """If no user-input Space floor surfaces are found for a HB Room, create a new floor using inset.

#     Arguments:
#     ----------
#         * IGH (gh_io.IGH): The Grasshopper Interface Object
#         * _input_rm_data (dict[str, FloorSegmentData]): The room dicts to operate on.

#     Returns:
#     --------
#         * list[FlrSegGroup]: A list of the FloorSegmentGroup objects.
#     """

#     def _get_hb_room_floor_surfaces(_hb_room):
#         # type: (Room) -> list[Face]
#         """Return a list of only the 'Floor' surfaces of a Honeybee Room"""
#         floors = []
#         for face in _hb_room.faces:
#             if "FLOOR" in str(face.type).upper():
#                 floors.append(face)

#         if not floors:
#             raise Exception('Error: No Floor found on Honeybee Room: ""'.format(
#                 _hb_room.display_name))

#         return floors

#     def _create_inset_floor_surface(_floor_face3Ds, _inset_distance=0.1):
#         # type: (list[Face], float) -> list[Face]
#         """Return a new inset floor Face, based on a list of existing floor Faces."""
#         new_floors = []
#         for srfc in _floor_face3Ds:
#             inset_rh_srfc = IGH.inset_LBT_face(srfc, _inset_distance)
#             try:
#                 for _ in inset_rh_srfc:
#                     new_floors.extend(_)
#             except:
#                 new_floors.extend(inset_rh_srfc)
#         return new_floors

#     for flr_seg_group in _flr_segment_groups:
#         if len(flr_seg_group.flr_seg_input_data) == 0:
#             # -- No floor segments on the room, so build a defaults floor segment.
#             room_floor_surfaces = _get_hb_room_floor_surfaces(flr_seg_group.hb_room)
#             inset_floor_surfaces = _create_inset_floor_surface(room_floor_surfaces, 0.1)

#             flr_seg_group.flr_seg_input_data.append(FloorSegmentData(
#                 flr_seg_group.hb_room.display_name, 00, VentilationData(0, 0, 0), inset_floor_surfaces))

#     return _flr_segment_groups


# def convert_inputs_to_FloorSegments(_flr_segment_groups):
#     # type: (list[FlrSegGroup]) -> list[FlrSegGroup]
#     """Convert the user-input floor surfaces into FloorSegment objects

#     Arguments:
#     ----------
#         * _flr_segment_groups list[FlrSegGroup]:

#     Returns:
#     --------
#         * (list[FlrSegGroup]):
#     """

#     for flr_segment_group in _flr_segment_groups:
#         for flr_seg_data in flr_segment_group.flr_seg_input_data:
#             new_flr_seg = honeybee_ph.space.SpaceFloorSegment()

#             new_flr_seg.weighting_factor = getattr(flr_seg_data, "weighting_factor", 1.0)
#             new_flr_seg.geometry = getattr(flr_seg_data, "geometry", None)

#             flr_segment_group.floor_segments.append(new_flr_seg)

#     return _flr_segment_groups


# def group_FloorSegments_by_room_name(_room_dicts):
#     # type: (dict) -> dict
#     """Sort / Combine User-Input FloorSegments based on their Object-Name & Room-Number

#     Arguments:
#     ----------
#         * _room_dicts (dict): The room dictionaries to look at

#     Returns:
#     --------
#         * (dict): The room dict, with floor surfaces combined based on room name / number
#     """

#     for room_dict in _room_dicts.values():
#         room_dict["FloorSegments"] = {}
#         for v in room_dict["floor_surfaces"].values():

#             if v.display_name in room_dict["FloorSegments"]:
#                 room_dict["FloorSegments"][v.display_name].append(v)
#             else:
#                 room_dict["FloorSegments"][v.display_name] = [v]

#         del room_dict["floor_surfaces"]

#     return _room_dicts


# def find_neighbors(IGH, _floor_segment_list):
#     # type: (gh_io.IGH, list) -> dict
#     """See if any FloorSegments in the inut list are 'neighbors.' Returns a dict
#     of the FloorSegments, sorted by 'neighbor-group.'

#     Arguments:
#     ----------
#         * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
#         * _floor_segment_list (list[FloorSegments])

#     Returns:
#     --------
#         * (dict): ie - {10947: set(FloorSegment_1, FloorSegment_2, ...), 10948: set(...), ... }
#     """
#     neighbor_groups = defaultdict(set)

#     # -- If its just a single FloorSegment
#     if len(_floor_segment_list) == 1:
#         neighbor_groups[id(_floor_segment_list[0])].add(id(_floor_segment_list[0]))

#     # -- If its a group of FloorSegments, see if any can be merged
#     for floor_seg_a in _floor_segment_list:
#         for floor_seg_b in _floor_segment_list:
#             if floor_seg_a == floor_seg_b:
#                 continue
#             input_geometry = [floor_seg_a.geometry, floor_seg_b.geometry]

#             merge_result = IGH.merge_Face3D(input_geometry)

#             if len(merge_result) < len(input_geometry):
#                 # Merge worked, so record the neighbor group in the list
#                 for _k, _v in neighbor_groups.items():
#                     if id(floor_seg_a) in _v or id(floor_seg_b) in _v:
#                         neighbor_groups[_k].add(id(floor_seg_a))
#                         neighbor_groups[_k].add(id(floor_seg_b))
#                         break
#                 else:
#                     neighbor_groups[id(floor_seg_a)].add(id(floor_seg_a))
#                     neighbor_groups[id(floor_seg_a)].add(id(floor_seg_b))

#     # -- If any FloorSegment groups can't be merged at all
#     for floor_seg in _floor_segment_list:
#         for gr in neighbor_groups.values():
#             if id(floor_seg) in gr:
#                 break
#         else:
#             neighbor_groups[id(floor_seg)].add(id(floor_seg))

#     return neighbor_groups


# def sort_FloorSegments_by_neighbor(IGH, _floor_segment_list):
#     # type: (gh_io.IGH, list) -> dict
#     """Sorts all the FloorSegment Objects by 'Neighbor-Group' (if touching)

#     Arguments:
#     ----------
#         * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
#         * _floor_segment_list (list[FloorSegments])

#     Returns:
#     --------
#         * (dict): ie - {10947: set(FloorSegment_1, FloorSegment_2, ...), 10948: set(...), ... }
#     """

#     neighbor_groups = find_neighbors(IGH, _floor_segment_list)

#     # -- Sort by Neighbor Group results
#     floors_sorted_by_neighbor = defaultdict(list)
#     for floor in _floor_segment_list:
#         for _k, group_list_ids in neighbor_groups.items():
#             if id(floor) in group_list_ids:
#                 floors_sorted_by_neighbor[_k].append(floor)

#     return floors_sorted_by_neighbor


# def create_Floors_from_FloorSegments(IGH, _room_dicts):
#     # type: (gh_io, dict) -> dict
#     """Creates new Floor Objects for the input FloorSegments. Sorts and groups
#     new Floors by name / number and if the FloorSegments are 'touching'

#     Arguments:
#     ----------
#         * IGH (gh_io.IGH): The PyPH Grasshopper Interface Object
#         * _room_dicts (dict): The Room dict to operate on

#     Returns:
#     --------
#         * (dict): The room dicts, with the Floor Objects added to the 'Floor' key
#     """

#     for v in _room_dicts.values():
#         v["Floors"] = {}

#         for space_id, space_floor_segments_list in v["FloorSegments"].items():
#             v["Floors"][space_id] = []
#             results = sort_FloorSegments_by_neighbor(IGH, space_floor_segments_list)

#             for floor_segment_group in results.values():

#                 new_floor = honeybee_ph.space.SpaceFloor()
#                 for floor_segment in floor_segment_group:
#                     new_floor.add_new_floor_segment(floor_segment)

#                 v["Floors"][space_id].append(new_floor)

#         del v["FloorSegments"]

#     return _room_dicts
