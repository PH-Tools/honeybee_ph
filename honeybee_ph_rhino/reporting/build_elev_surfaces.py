try:
    from typing import Tuple, List
except ImportError:
    pass  # IronPython 2.7

try:
    from itertools import izip
except ImportError:
    import zip as izip  # Python 3

try:
    from System import Object
    from System.Drawing import Color
except ImportError:
    pass  # Outside .NET

try:
    from Grasshopper import DataTree
except ImportError:
    pass  # Outside Grasshopper

try:
    from Rhino.Geometry import TextJustification
    from Rhino.DocObjects import ObjectAttributes
except ImportError:
    pass  # Outside Rhino

import math
from ladybug_rhino.fromgeometry import from_face3d, from_plane, from_point3d
from honeybee import boundarycondition

from honeybee import model
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


def _get_exterior_env_surfaces(_hb_model):
    # type: (model.Model) -> List

    envelope_surfaces = []
    for room in _hb_model.rooms:
        for face in room.faces:
            if isinstance(face.boundary_condition, boundarycondition.Surface):
                continue
            envelope_surfaces.append(from_face3d(face.geometry))

    return envelope_surfaces


def _to_mesh(_IGH, _srfc, _color):
    return _IGH.ghpythonlib_components.MeshColours(_srfc, _color)


def _merge_rh_srfc(_IGH, _rh_surfaces):
    # type: (gh_io.IGH, List) -> List
    joined_breps = _IGH.ghpythonlib_components.BrepJoin(_rh_surfaces).breps
    if not isinstance(joined_breps, list):
        joined_breps = [joined_breps]
    merged_breps = _IGH.ghpythonlib_components.MergeFaces(joined_breps).breps

    if not isinstance(merged_breps, list):
        merged_breps = [merged_breps]

    for brep in merged_breps:
        brep.Edges.MergeAllEdges((math.pi)/2)

    return merged_breps


def _get_edges(_IGH, _rh_breps):
    # type: (gh_io.IGH, List) -> List
    if not isinstance(_rh_breps, list):
        _rh_breps = [_rh_breps]

    edges = []
    for brep in _rh_breps:
        e = _IGH.ghpythonlib_components.DeconstructBrep(brep).edges
        c = _IGH.ghpythonlib_components.JoinCurves(e, True)
        edges.append(c)

    return edges


def _get_window_surfaces(_IGH, _hb_model):
    # type: (gh_io.IGH, model.Model) -> Tuple[List, List]
    win_surfaces = []
    win_planes = []
    for room in _hb_model.rooms:
        for face in room.faces:
            for aperture in face.apertures:
                win_srfc = from_face3d(aperture.geometry)
                win_srfc.SetUserString('display_name', aperture.display_name)
                win_surfaces.append(win_srfc)
                win_cp = from_point3d(aperture.geometry.center)
                win_plane = from_plane(aperture.geometry.plane)
                move_vec = _IGH.ghpythonlib_components.Vector2Pt(
                    win_plane.Origin, win_cp, False).vector
                centered_plane = _IGH.ghpythonlib_components.Move(
                    win_plane, move_vec).geometry
                win_planes.append(centered_plane)

    return win_surfaces, win_planes


def make(_IGH, _hb_model):
    # type: (gh_io.IGH, model.Model) -> Tuple[DataTree, DataTree]

    # -- Output Trees
    env_geom_ = _IGH.Grasshopper.DataTree[Object]()
    env_geom_attrs_ = _IGH.Grasshopper.DataTree[Object]()

    c_light_grey = Color.FromArgb(255, 240, 240, 240)
    c_black = Color.FromArgb(255, 0, 0, 0)

    # -- Build the Envelope Surfaces
    rh_surfaces = _get_exterior_env_surfaces(_hb_model)
    rh_merged_surfaces = _merge_rh_srfc(_IGH, rh_surfaces)
    rh_merged_edges = _get_edges(_IGH, rh_merged_surfaces)
    for srfc in rh_merged_surfaces:
        env_geom_.Add(_to_mesh(_IGH, srfc, c_light_grey))
        env_geom_attrs_.Add(_create_rh_attr_object(_IGH, c_light_grey, .10))

    # -- Add the edges
    for edge_list in rh_merged_edges:
        for e in edge_list:
            env_geom_.Add(e)
            env_geom_attrs_.Add(_create_rh_attr_object(_IGH, c_black, 0.10))

    # -- Add the windows
    rh_win_surfaces, rh_win_planes = _get_window_surfaces(_IGH, _hb_model)
    for srfc, srfc_plane in izip(rh_win_surfaces, rh_win_planes):
        srfc_edge_lists = _get_edges(_IGH, srfc)
        for srfc_edge in srfc_edge_lists:
            # -- Add the window outline curve
            env_geom_.Add(srfc_edge)
            env_geom_attrs_.Add(_create_rh_attr_object(_IGH, c_black, 0.25))

        # -- Add the a Text label object for the Window
        txt_obj = _IGH.Rhino.Geometry.TextEntity()
        txt_obj.Text = srfc.GetUserString('display_name')
        txt_obj.Plane = srfc_plane
        txt_obj.TextHeight = 0.18
        txt_obj.Justification = TextJustification.MiddleCenter
        for crv in txt_obj.Explode():
            env_geom_.Add(crv)
            env_geom_attrs_.Add(_create_rh_attr_object(_IGH, c_black, 0.01))

    return env_geom_, env_geom_attrs_
