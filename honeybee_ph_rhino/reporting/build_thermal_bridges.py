# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""""""

try:
    from typing import List, Dict, Tuple
except ImportError:
    pass  # Python 2.7

try:
    from System import Object
    from System.Drawing import Color
except ImportError:
    pass  # Outside .NET

try:
    from Rhino.Geometry import Curve
    from Rhino.DocObjects import ObjectAttributes
except ImportError:
    pass  # Outside Rhino

from collections import defaultdict, OrderedDict

from ladybug_rhino.fromgeometry import from_polyline3d, from_linesegment3d
from honeybee import model

from honeybee_energy_ph.construction import thermal_bridge
from honeybee_ph_rhino import gh_io


def _build_tb_attributes(IGH, _outline_color, _outline_weight):
    # type: (gh_io.IGH, Color, float) -> ObjectAttributes
    """Return a new Rhino ObjectAttributes object with color and line-weight set.

    Arguments:
    ----------
        * IGH (gh_io.IGH):
        * _outline_color (Color):
        * _outline_weight (float):

    Returns:
    --------
        * (ObjectAttributes)
    """
    new_attr_obj = IGH.Rhino.DocObjects.ObjectAttributes()

    new_attr_obj.ObjectColor = _outline_color
    new_attr_obj.PlotColor = _outline_color
    new_attr_obj.ColorSource = IGH.Rhino.DocObjects.ObjectColorSource.ColorFromObject
    new_attr_obj.PlotColorSource = IGH.Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject

    new_attr_obj.PlotWeight = _outline_weight
    new_attr_obj.PlotWeightSource = IGH.Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject

    new_attr_obj.DisplayOrder = 1  # 1 = Front, -1 = Back

    return new_attr_obj


def _get_tbs_grouped_by_name(_hb_model):
    # type: (model.Model) -> Dict[str, List[thermal_bridge.PhThermalBridge]]
    """Return a Dict with the HBPH TB Objects grouped by 'display_name'

    Arguments:
    ----------
        * _hb_model (model.Model): The Honeybee model object to use as the source.

    Returns:
    --------
        * Dict[str, List[thermal_bridge.PhThermalBridge]]
    """

    if not _hb_model:
        return {}

    # -- Get each unique TB in the model, organized by Identifier
    tb_dict_all = {}
    for room in _hb_model.rooms:
        for k, hbph_tb in room.properties.ph.ph_bldg_segment.thermal_bridges.items():
            tb_dict_all[k] = hbph_tb

    # -- Group the TBs by their 'display_name'
    tb_dict_grouped = defaultdict(list)
    for hbph_tb in tb_dict_all.values():
        tb_dict_grouped[hbph_tb.display_name].append(hbph_tb)

    # -- Order the dict by display_name
    tb_dict_sorted = OrderedDict()
    for k in sorted(tb_dict_grouped.keys()):
        tb_dict_sorted[k] = tb_dict_grouped[k]

    return tb_dict_sorted


def _get_tb_geometry(_hbph_tb):
    # type: (thermal_bridge.PhThermalBridge) -> Curve
    """Get the TB Geometry as a Rhino.Geometry.Curve (LineCurve or PolylineCurve)

    Arguments:
    ----------
        * _hbph_tb (thermal_bridge.PhThermalBridge):

    Returns:
    --------
        * (Curve)
    """
    try:
        return from_polyline3d(_hbph_tb.geometry)
    except:
        return from_linesegment3d(_hbph_tb.geometry)


def get_tb_data(_IGH, _hb_model, _outline_color, _outline_weight):
    # type: (gh_io.IGH, model.Model, Color, float) -> Tuple
    """Return a Tuple of the geometry and attribute DataTrees with the TB data.

    Arguments:
    ----------
        * IGH (gh_io.IGH):
        * _hb_model (model.Model):
        * _outline_color (System.Drawing.Color):
        * _outline_weight (float):

    Returns:
    --------
        * Tuple[Grasshopper.DataTree, Grasshopper.DataTree]
    """

    # --- Group all the Model's TBs by their 'display_name'
    tb_dict = _get_tbs_grouped_by_name(_hb_model)

    # -- Build the output Trees
    tb_geom_tree = _IGH.Grasshopper.DataTree[Curve]()
    tb_attr_tree = _IGH.Grasshopper.DataTree[ObjectAttributes]()
    tb_names_tree = _IGH.Grasshopper.DataTree[str]()
    tb_lengths_tree = _IGH.Grasshopper.DataTree[float]()

    for i, items in enumerate(tb_dict.items()):
        tb_name, tb_list = items
        gh_path = _IGH.Grasshopper.Kernel.Data.GH_Path(i)

        # -- TB Geom and Rhino ObjectAttributes
        for tb in tb_list:
            tb_geom_tree.Add(_get_tb_geometry(tb), gh_path)
            tb_attr_tree.Add(_build_tb_attributes(
                _IGH, _outline_color, _outline_weight), gh_path)

        # -- TB Data
        tb_names_tree.Add(tb_name, gh_path)
        tb_lengths_tree.Add(sum(tb.length for tb in tb_list), gh_path)

    return tb_names_tree, tb_geom_tree, tb_attr_tree, tb_lengths_tree
