# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Grasshopper Component Interface for Get FloorSegment Data."""

try:
    from System import Object
except ImportError:
    pass  # Outside .NET

try:
    from typing import List, Tuple, Any, Optional, Dict
except ImportError:
    pass  # IronPython 2.7

from collections import namedtuple, defaultdict
from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.gh_compo_io.ghio_spc_vent import SpacePhVentFlowRates


# -- Temporary dataclasses to organize input data


class VentilationData(object):

    def __init__(self, _v_sup, _v_eta, _v_tran):
        self.v_sup = _v_sup
        self.v_eta = _v_eta
        self.v_tran = _v_tran


class FloorSegmentData(object):

    def __init__(self, _name, _number, _full_name, _vent_rates, _geometry, _weighting_factor):
        # type: (str, str, str, Any, Optional[SpacePhVentFlowRates], float) -> None
        self.name = _name
        self.number = _number
        self.full_name = _full_name
        self.vent_rates = _vent_rates
        self.geometry = _geometry
        self.weighting_factor = _weighting_factor


# -- Component Interface

class IGetFloorSegData(object):

    def __init__(self, _IGH, _group_by_name, _input_geom):
        # type: (gh_io.IGH, bool, List) -> None
        self.IGH = _IGH
        self.group_by_name = _group_by_name
        self.floor_segment_data = self.handle_user_input(_input_geom, '_floor_seg_geom')

    def handle_user_input(self, _input_geom, _input_node_name):
        # type: (List, str) -> List[FloorSegmentData]
        """Try and read in all the user-supplied input data for the GH-Component input node and organize the data.

        Will try and read in all the inputs of whatever type and get as much
        data as possible. If the input objects are Rhino objects, will try and
        read in any UserText attribute data from the Rhino scene. All data is
        organized into FloorSegmentData objects before output.

        Arguments:
        ----------
            * _input_geom (List[Any]): A list of the user-supplied input data / Geometry.
            * _input_node_name (str): The name of the GH-Component input node to read input data from.

        Returns:
        --------
            * (List[FloorSegmentData]): A list of FloorSegmentData objects with user inputs organized.
        """

        if not isinstance(_input_geom, (list, tuple, set)):
            _input_geom = [_input_geom]

        # -- Get the GH-Component Input Object Attribute UserText values (if any)
        input_index_number = self.IGH.gh_compo_find_input_index_by_name(_input_node_name)
        input_guids = self.IGH.gh_compo_get_input_guids(input_index_number)
        input_data = self.IGH.get_rh_obj_UserText_dict(input_guids)

        # -- Build the FloorSegmentData objects, organize all the attributes.
        floor_segment_input_data = []  # type: (List[FloorSegmentData])
        for data_dict, geom in zip(input_data, _input_geom):
            segment_vent_data = VentilationData(
                float(data_dict.get('V_sup', 0.0))/3600,
                float(data_dict.get('V_eta', 0.0))/3600,
                float(data_dict.get('V_trans', 0.0))/3600
            )

            segment_data = FloorSegmentData(
                _name=data_dict.get('Object Name', ''),
                _number=data_dict.get('Room_Number', ''),
                _full_name='{}-{}'.format(
                    data_dict.get('Room_Number'),
                    data_dict.get('Object Name')
                ),
                _vent_rates=segment_vent_data,
                _geometry=geom,
                _weighting_factor=float(data_dict.get('TFA_Factor', 1.0)),
            )

            floor_segment_input_data.append(segment_data)

        return floor_segment_input_data

    def create_output(self):
        # type: () -> Tuple
        """Sort out all the data and create the Output DataTrees.

        Arguments:
        ----------
            * (None):

        Returns:
        --------
            * (Tuple[DataTree, DataTree, DataTree, DataTree]):
        """

        # -- Output Trees
        flr_seg_srfcs_ = self.IGH.Grasshopper.DataTree[Object]()
        flr_seg_weighting_factors_ = self.IGH.Grasshopper.DataTree[float]()
        flr_seg_names_ = self.IGH.Grasshopper.DataTree[str]()
        flr_seg_numbers_ = self.IGH.Grasshopper.DataTree[str]()
        flr_seg_vent_rates_ = self.IGH.Grasshopper.DataTree[SpacePhVentFlowRates]()
        pth = self.IGH.Grasshopper.Kernel.Data.GH_Path
        NameGroupItem = namedtuple(
            'NameGroupItem', ['breps', 'name', 'number', 'weight', 'vent_rates'])

        # -- Break out the data into the output Trees
        if self.group_by_name:
            name_groups = defaultdict(list)  # type: (Dict[str, List[NameGroupItem]])
            for flr_seg in self.floor_segment_data:

                new_entry = NameGroupItem(
                    flr_seg.geometry,
                    str(flr_seg.name).upper(),
                    str(flr_seg.number).upper(),
                    flr_seg.weighting_factor,
                    flr_seg.vent_rates
                )
                name_groups[flr_seg.full_name].append(new_entry)

            for i, name_group in enumerate(name_groups.values()):
                for item in name_group:
                    flr_seg_srfcs_.Add(item.breps, pth(i))
                    flr_seg_weighting_factors_.Add(item.weight, pth(i))
                    flr_seg_names_.Add(item.name, pth(i))
                    flr_seg_numbers_.Add(item.number, pth(i))
                    flr_seg_vent_rates_.Add(
                        SpacePhVentFlowRates(
                            item.vent_rates.v_sup,
                            item.vent_rates.v_eta,
                            item.vent_rates.v_tran
                        ), pth(i)
                    )
        else:
            for i, flr_seg in enumerate(self.floor_segment_data):
                flr_seg_srfcs_.Add(flr_seg.geometry, pth(i))
                flr_seg_names_.Add(flr_seg.name, pth(i))
                flr_seg_numbers_.Add(flr_seg.number, pth(i))
                flr_seg_vent_rates_.Add(
                    SpacePhVentFlowRates(
                        flr_seg.vent_rates.v_sup,
                        flr_seg.vent_rates.v_eta,
                        flr_seg.vent_rates.v_tran
                    ), pth(i)
                )

        return flr_seg_srfcs_, flr_seg_weighting_factors_, flr_seg_names_, flr_seg_numbers_, flr_seg_vent_rates_
