# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create SpaceFloorSegment objects from Rhino/Grasshopper inputs."""

try:
    from typing import Any
except ImportError:
    pass  # IronPython

try:
    from itertools import izip as zip
except ImportError:
    pass  # Python 3

from collections import namedtuple

from honeybee_ph_rhino import gh_io

# -- Temporary dataclasses to organize input data
VentilationData = namedtuple('VentilationData', ['v_sup', 'v_eta', 'v_trans'])
FloorSegmentData = namedtuple(
    'FloorSegmentData', ['name', 'number', 'full_name', 'ventilation_flow_rates', 'geometry'])


def handle_floor_seg_user_input(IGH, _input_objects, _input_name):
    # type: (gh_io.IGH, list, str) -> list[FloorSegmentData]
    """Try and read in all the user-supplied input data for the GH-Component input ndoe and organize the data.

    Will try and read in all the inputs of whatever type and get as much data as possibe. If the input objects
    are Rhino objects, will try and read in any UserText attribute data from the Rhino scene. All data is organized
    into FloorSegmentData objects before output.

    Arguments:
    ----------
        * IGH (gh_io.IGH): The Grasshopper Interface object.
        * _input_objects (list[]): A list of the user-supplied input data / Geometry.
        * _input_name (str): The name of the GH-Component input node to read input data from.

    Returns:
    --------
        * list[FloorSegmentData]: A list of FloorSegmentData objects with user inputs organized.
    """

    if not isinstance(_input_objects, (list, tuple, set)):
        _input_objects = [_input_objects]

    # -- Get the GH-Component Input Object Attribute UserText values (if any)
    input_index_number = IGH.gh_compo_find_input_index_by_name(_input_name)
    input_guids = IGH.gh_compo_get_input_guids(input_index_number)
    input_data = IGH.get_rh_obj_UserText_dict(input_guids)

    # -- Build the FloorSegmentData objects, organize all the attributes.
    floor_segment_input_data = []
    for data_dict, geom in zip(input_data, _input_objects):
        segment_vent_data = VentilationData(
            data_dict.get('V_sup'),
            data_dict.get('V_eta'),
            data_dict.get('V_trans')
        )

        segment_data = FloorSegmentData(
            data_dict.get('Object Name'),
            data_dict.get('Room_Number'),
            '{}-{}'.format(data_dict.get('Object Name'),
                           data_dict.get('Room_Number')),
            segment_vent_data,
            geom
        )

        floor_segment_input_data.append(segment_data)

    return floor_segment_input_data

# TODO: verify this can be removed safely?
# def create_floor_segments(_flr_seg_input_data, _weighting_factors):
#     # type: (list[FloorSegmentData], list[float]) -> list[space.SpaceFloorSegment]
#     flr_segments = []
#     for i, data in enumerate(_flr_seg_input_data):
#         new_flr_segment = space.SpaceFloorSegment()

#         # -- In case the weighting factors klen doesn't match
#         # -- first try and use the input at index=0, then the default (1.0)
#         try:
#             seg_weighting_fac = _weighting_factors[i]
#         except IndexError:
#             try:
#                 seg_weighting_fac = _weighting_factors[0]
#             except IndexError:
#                 seg_weighting_fac = 1.0

#         new_flr_segment.weighting_factor = seg_weighting_fac
#         new_flr_segment.geometry = data.geometry

#         flr_segments.append(new_flr_segment)

#     return flr_segments
