# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for getting / sorting all the Honeybee-Model Envelope Surfaces."""

try:
    from typing import Tuple, Dict, List
except ImportError:
    pass  # Python 2.7

try:
    from System import Object
    from System.Drawing import Color
except ImportError:
    pass  # Outside .NET

try:
    from Rhino.DocObjects import ObjectAttributes
except ImportError:
    pass  # Outside Rhino

from collections import defaultdict, OrderedDict

from honeybee import model, face
from ladybug_rhino.fromgeometry import from_face3d

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


def _get_hb_face_groups_from_model(_hb_model):
    # type: (model.Model) -> Dict[str, List[face.Face]]
    """Return a dict with Honeybee-Faces grouped by their Construction-Name."""

    face_groups = defaultdict(list)

    for hb_room in _hb_model.rooms:
        for hb_face in hb_room.faces:
            hb_face_constr_name = hb_face.properties.energy.construction.display_name
            hb_face_constr_name = hb_face_constr_name.strip()
            face_groups[hb_face_constr_name].append(hb_face)

    return face_groups


def _get_all_construction_names(_hb_model):
    # type: (model.Model) -> List[str]
    """Returns a sorted list of all the construction names found in the Honeybee-Model."""
    hb_cont_names = set()
    for hb_room in _hb_model.rooms:
        for hb_face in hb_room.faces:
            hb_cont_names.add(hb_face.properties.energy.construction.display_name)
    return sorted(list(hb_cont_names))


def get_env_data(_IGH, _hb_model, _highlight_srfc_color, _highlight_outline_color,
                 _highlight_outline_weight, _default_srfc_color, _default_outline_color,
                 _default_outline_weight):
    # type: (gh_io.IGH, model.Model, Color, Color, float, Color, Color, float) -> Tuple
    """Returns a tuple of the DataTrees with all the Surface Data and geometry from the HB-Model.

    Arguments:
    ----------
        * _IGH (gh_io.IGH): The Grasshopper Interface
        * _hb_model (model.Model): The Honeybee Model to use as the source.
        * _highlight_srfc_color (System.Drawing.Color): The color to use for the Mesh surfaces
        * _highlight_outline_color (System.Drawing.Color): The color to use for the Mesh outlines
        * _highlight_outline_weight (float): The plot-weight to use for the Mesh outlines.
        * _default_srfc_color (System.Drawing.Color): 
        * _default_outline_color (System.Drawing.Color): 
        * _default_outline_weight (float): 

    Returns:
    --------
        * (Tuple[DataTree, DataTree, DataTree, DataTree]): 
    """

    # -- Output Trees
    face_const_names_ = _IGH.Grasshopper.DataTree[str]()
    face_geometry_ = _IGH.Grasshopper.DataTree[Object]()
    face_rh_attributes_ = _IGH.Grasshopper.DataTree[ObjectAttributes]()
    face_areas_ = _IGH.Grasshopper.DataTree[float]()
    pth = _IGH.Grasshopper.Kernel.Data.GH_Path

    # -- Build the RH AttributeObjects
    rh_attr_srfc_highlight = _create_rh_attr_object(
        _IGH, _highlight_srfc_color, 0)
    rh_attr_srfc_default = _create_rh_attr_object(
        _IGH, _default_srfc_color, 0)
    rh_attr_curve_highlight = _create_rh_attr_object(
        _IGH, _highlight_outline_color, _highlight_outline_weight)
    rh_attr_curve_default = _create_rh_attr_object(
        _IGH, _default_outline_color, _default_outline_weight)

    # -- Get all the exterior surfaces from the Model
    hb_face_groups = _get_hb_face_groups_from_model(_hb_model)

    # -- Create the mesh surfaces and edges from the HB-Faces
    for i, const_name in enumerate(_get_all_construction_names(_hb_model)):

        face_const_names_.Add(const_name, pth(i))
        face_areas_.Add(sum(f.area for f in hb_face_groups[const_name]), pth(i))

        for hb_room in _hb_model.rooms:
            for hb_face in hb_room.faces:

                # -- Choose the right colors
                if hb_face.properties.energy.construction.display_name == const_name:
                    srfc_color = rh_attr_srfc_highlight
                    crv_color = rh_attr_curve_highlight
                else:
                    srfc_color = rh_attr_srfc_default
                    crv_color = rh_attr_curve_default

                # -- Surface
                mesh = _IGH.ghpythonlib_components.MeshColours(
                    from_face3d(hb_face.geometry), srfc_color.ObjectColor)
                face_geometry_.Add(mesh, pth(i))
                face_rh_attributes_.Add(srfc_color, pth(i))

                # -- Boundary Edges
                msh_edges = _IGH.ghpythonlib_components.MeshEdges(mesh).naked_edges
                msh_boundary = _IGH.ghpythonlib_components.JoinCurves(
                    msh_edges, preserve=False)
                face_geometry_.Add(msh_boundary, pth(i))
                face_rh_attributes_.Add(crv_color, pth(i))

    return (face_const_names_, face_geometry_, face_rh_attributes_, face_areas_)
