# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for getting / sorting all the Honeybee-Model Thermal Bridges."""

try:
    from typing import List, Dict, Tuple, Set
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

from ladybug_rhino.fromgeometry import from_polyline3d, from_linesegment3d, from_face3d
from honeybee import model

from honeybee_energy_ph.construction import thermal_bridge
from honeybee_ph_rhino import gh_io


def _create_rh_attr_object(_IGH, _color, _weight):
    # type: (gh_io.IGH, Color, float) -> ObjectAttributes
    """Return a new Rhino.DocObjects.ObjectAttributes object with specified settings."""

    new_attr_obj = _IGH.Rhino.DocObjects.ObjectAttributes()

    new_attr_obj.ObjectColor = _color
    new_attr_obj.PlotColor = _color
    new_attr_obj.ColorSource = _IGH.Rhino.DocObjects.ObjectColorSource.ColorFromObject
    new_attr_obj.PlotColorSource = _IGH.Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject

    new_attr_obj.PlotWeight = _weight
    new_attr_obj.PlotWeightSource = _IGH.Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject

    # new_attr_obj.DisplayOrder = 0  # 1 = Front, -1 = Back

    return new_attr_obj


def _get_all_tb_groups_from_model(_hb_model):
    # type: (model.Model) -> Dict[str, List[thermal_bridge.PhThermalBridge]]
    """Return a Dict of all the unique TB objects found in the Model, grouped by display_name."""

    # -- First, get every unique TB object in the model
    all_tbs = {}
    for hb_room in _hb_model.rooms:
        for tb_key, tb in hb_room.properties.ph.ph_bldg_segment.thermal_bridges.items():
            all_tbs[tb_key] = tb

    # Now group the TBs by name
    tb_groups = defaultdict(list)
    for tb in all_tbs.values():
        tb_groups[tb.display_name].append(tb)

    return tb_groups


def _get_all_tb_names(_hb_model):
    # type: (model.Model) -> List[str]
    """Return a list of all the unique TB object display_names found in the model."""

    tb_names = set()
    for hb_room in _hb_model.rooms:
        for tb in hb_room.properties.ph.ph_bldg_segment.thermal_bridges.values():
            tb_names.add(tb.display_name)

    return sorted(list(tb_names))


def _get_tb_geometry(_hbph_tb):
    # type: (thermal_bridge.PhThermalBridge) -> Curve
    """Get the TB Geometry as a Rhino.Geometry.Curve (LineCurve or PolylineCurve)

    Arguments:
    ----------
        * _hbph_tb (thermal_bridge.PhThermalBridge):

    Returns:
    --------
        * (Rhino.Geometry.Curve)
    """
    try:
        return from_polyline3d(_hbph_tb.geometry)
    except:
        return from_linesegment3d(_hbph_tb.geometry)


def get_tb_data(_IGH, _hb_model, _highlight_outline_color, _highlight_outline_weight,
                _default_srfc_color, _default_outline_color, _default_outline_weight):
    # type: (gh_io.IGH, model.Model, Color, float, Color, Color, float) -> Tuple
    """Return a Tuple of the geometry and attribute DataTrees with the TB data.

    Arguments:
    ----------
        * _IGH (gh_io.IGH): The Grasshopper Interface
        * _hb_model (model.Model): The Honeybee Model to use as the source.
        * _highlight_outline_color (System.Drawing.Color): The color to use for the TB Curve outlines
        * _highlight_outline_weight (float): The plot-weight to use for the TB Curve outlines.
        * _default_srfc_color (System.Drawing.Color): 
        * _default_outline_color (System.Drawing.Color): 
        * _default_outline_weight (float): 


    Returns:
    --------
        * Tuple[Grasshopper.DataTree, Grasshopper.DataTree]
    """

    # -- Build the output Trees
    tb_geom_tree_ = _IGH.Grasshopper.DataTree[Object]()
    tb_attr_tree_ = _IGH.Grasshopper.DataTree[ObjectAttributes]()
    tb_names_tree_ = _IGH.Grasshopper.DataTree[str]()
    tb_lengths_tree_ = _IGH.Grasshopper.DataTree[float]()
    pth = _IGH.Grasshopper.Kernel.Data.GH_Path

    if not _hb_model:
        return tb_names_tree_, tb_geom_tree_, tb_attr_tree_, tb_lengths_tree_

    # -- Build the RH AttributeObjects
    rh_attr_srfc_default = _create_rh_attr_object(
        _IGH, _default_srfc_color, 0)
    rh_attr_curve_highlight = _create_rh_attr_object(
        _IGH, _highlight_outline_color, _highlight_outline_weight)
    rh_attr_curve_default = _create_rh_attr_object(
        _IGH, _default_outline_color, _default_outline_weight)

    # -- Build the background building Mesh geometry which gets added to each output branch
    bldg_srfc_geom = []
    bldg_srfc_attrs = []

    for hb_room in _hb_model.rooms:
        for hb_face in hb_room.faces:
            # -- Surface
            mesh = _IGH.ghpythonlib_components.MeshColours(
                from_face3d(hb_face.geometry), rh_attr_srfc_default.ObjectColor)
            bldg_srfc_geom.append(mesh)
            bldg_srfc_attrs.append(rh_attr_srfc_default)

            # -- Boundary Edges
            msh_edges = _IGH.ghpythonlib_components.MeshEdges(mesh).naked_edges
            msh_boundary = _IGH.ghpythonlib_components.JoinCurves(
                msh_edges, preserve=False)
            bldg_srfc_geom.append(msh_boundary)
            bldg_srfc_attrs.append(rh_attr_curve_default)

    # -- Get all the TB objects from the model
    tb_groups = _get_all_tb_groups_from_model(_hb_model)

    # -- Build the thermal bridge curve geometry (with background meshes)
    for i, tb_name in enumerate(_get_all_tb_names(_hb_model)):

        # -- TB Geom and Rhino ObjectAttributes
        for tb in tb_groups[tb_name]:
            # -- Add the background model geom to each branch
            tb_geom_tree_.AddRange(bldg_srfc_geom, pth(i))
            tb_attr_tree_.AddRange(bldg_srfc_attrs, pth(i))

            # -- Add the new TB highlight Geometry
            tb_geom_tree_.Add(_get_tb_geometry(tb), pth(i))
            tb_attr_tree_.Add(rh_attr_curve_highlight, pth(i))

        # -- TB Data
        tb_names_tree_.Add(tb_name, pth(i))
        tb_lengths_tree_.Add(sum(tb.length for tb in tb_groups[tb_name]), pth(i))

    return tb_names_tree_, tb_geom_tree_, tb_attr_tree_, tb_lengths_tree_
