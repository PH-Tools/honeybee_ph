# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for Calculating Window PHPP-Style shading dimension"""

try:
    from typing import Any, Sequence, Tuple, Optional, List
except ImportError:
    pass  # IronPython 2.7

import Rhino.Geometry

import math

from honeybee import aperture
from ladybug_geometry.geometry3d import line, pointvector
from ladybug_rhino.fromgeometry import from_linesegment3d, from_vector3d, from_point3d
from honeybee_ph_rhino import gh_io


class PhppShadingDims:
    """Dataclass for holding shading dimension info"""

    def __init__(self):
        # Horizon
        self.h_hori = None  # type: Optional[float]
        self.d_hori = None  # type: Optional[float]
        self.checkline_hori = None  # type: Optional[Rhino.Geometry.Line]

        # Side Reveal
        self.o_reveal = None  # type: Optional[float]
        self.d_reveal = None  # type: Optional[float]
        self.checkline_r1 = None  # type: Optional[Rhino.Geometry.Line]
        self.checkline_r2 = None  # type: Optional[Rhino.Geometry.Line]

        # Overhangs
        self.o_over = None  # type: Optional[float]
        self.d_over = None  # type: Optional[float]
        self.checkline_over = None  # type: Optional[Rhino.Geometry.Line]

    def __str__(self):
        return "{}({})".format(
            str(self.__class__.__name__),
            ", ".join(["{}={}".format(k, v) for k, v in vars(self).items()])
        )


def calc_shading_dims(_aperture, _shading_objs, _IGH, _limit=99):
    # type: (aperture.Aperture, Sequence, gh_io.IGH, int) -> PhppShadingDims
    """Returns a PhppShadingDims object with all the shading dimensions found."""

    dims = PhppShadingDims()

    if not _shading_objs:
        return dims

    # ----------------------------------------------------------------------
    # Find the relevant geometry in the scene and figures out the critical dimensions from the window
    dims.h_hori, dims.d_hori, dims.checkline_hori = find_horizon_shading(
        _aperture, _shading_objs, _IGH, _limit)
    dims.d_over, dims.o_over, dims.checkline_over = find_overhang_shading(
        _aperture, _shading_objs, _IGH, _limit)
    dims.o_reveal, dims.d_reveal, dims.checkline_r1, dims.checkline_r2 = find_reveal_shading(
        _aperture, _shading_objs, _IGH, _limit)

    return dims


# TODO: Refactor glazing edge finder as generic func


def _get_top_glazing_edge(_aperture):
    # type (aperture.Aperture) -> Rhino.Geometry.LineCurve
    """Returns the center point of the top glazing edge of an HB-Aperture."""

    # -- Find the top edge of the HB-Aperture
    edge = line.LineSegment3D.from_end_points(
        _aperture.geometry.upper_right_corner,
        _aperture.geometry.upper_left_corner
    )
    vect_towards_center = _aperture.geometry.centroid - edge.midpoint
    vect_towards_center = vect_towards_center.normalize()

    # -- Try and get the bottom Ph-Frame, if there is one
    # -- Move the bottom edge 'up' the width of the frame, or 0.1m if None
    ph_frame = _aperture.properties.energy.construction.properties.ph.ph_frame
    if ph_frame:
        dist = ph_frame.top.width
    else:
        dist = 0.1
    edge = edge.move(vect_towards_center * dist)

    # -- move the bottom edge 'in' the inset distance as well
    edge = edge.move(_aperture.normal.normalize() *
                     _aperture.properties.ph.inset_dist * -1)
    return from_linesegment3d(edge)


def _get_bottom_glazing_edge(_aperture):
    # type (aperture.Aperture) ->  Rhino.Geometry.LineCurve
    """Returns the center point of the bottom glazing edge of an HB-Aperture."""

    # -- Find the bottom edge of the HB-Aperture
    edge = line.LineSegment3D.from_end_points(
        _aperture.geometry.lower_left_corner,
        _aperture.geometry.lower_right_corner
    )
    vect_towards_center = _aperture.geometry.centroid - edge.midpoint
    vect_towards_center = vect_towards_center.normalize()

    # -- Try and get the bottom Ph-Frame, if there is one
    # -- Move the bottom edge 'up' the width of the frame, or 0.1m if None
    ph_frame = _aperture.properties.energy.construction.properties.ph.ph_frame
    if ph_frame:
        dist = ph_frame.bottom.width
    else:
        dist = 0.1
    edge = edge.move(vect_towards_center * dist)

    # -- move the bottom edge 'in' the inset distance as well
    edge = edge.move(_aperture.normal.normalize() *
                     _aperture.properties.ph.inset_dist * -1)
    return from_linesegment3d(edge)


def _get_left_glazing_edge(_aperture):
    # type (aperture.Aperture) ->  Rhino.Geometry.LineCurve
    """Returns the center point of the left glazing edge of an HB-Aperture."""

    # -- Find the bottom edge of the HB-Aperture
    edge = line.LineSegment3D.from_end_points(
        _aperture.geometry.upper_left_corner,
        _aperture.geometry.lower_left_corner
    )
    vect_towards_center = _aperture.geometry.centroid - edge.midpoint
    vect_towards_center = vect_towards_center.normalize()

    # -- Try and get the bottom Ph-Frame, if there is one
    # -- Move the bottom edge 'up' the width of the frame, or 0.1m if None
    ph_frame = _aperture.properties.energy.construction.properties.ph.ph_frame
    if ph_frame:
        dist = ph_frame.left.width
    else:
        dist = 0.1
    edge = edge.move(vect_towards_center * dist)

    # -- move the bottom edge 'in' the inset distance as well
    edge = edge.move(_aperture.normal.normalize() *
                     _aperture.properties.ph.inset_dist * -1)
    return from_linesegment3d(edge)


def _get_right_glazing_edge(_aperture):
    # type (aperture.Aperture) ->  Rhino.Geometry.LineCurve
    """Returns the center point of the right glazing edge of an HB-Aperture."""

    # -- Find the bottom edge of the HB-Aperture
    edge = line.LineSegment3D.from_end_points(
        _aperture.geometry.lower_right_corner,
        _aperture.geometry.upper_right_corner
    )
    vect_towards_center = _aperture.geometry.centroid - edge.midpoint
    vect_towards_center = vect_towards_center.normalize()

    # -- Try and get the bottom Ph-Frame, if there is one
    # -- Move the bottom edge 'up' the width of the frame, or 0.1m if None
    ph_frame = _aperture.properties.energy.construction.properties.ph.ph_frame
    if ph_frame:
        dist = ph_frame.right.width
    else:
        dist = 0.1
    edge = edge.move(vect_towards_center * dist)

    # -- move the bottom edge 'in' the inset distance as well
    edge = edge.move(_aperture.normal.normalize() *
                     _aperture.properties.ph.inset_dist * -1)
    return from_linesegment3d(edge)


def _get_glazing_center(_aperture):
    # type (aperture.Aperture) -> Rhino.Geometry.Point3d
    """Return the center point of the glazing surface of an HB-Aperture.

    This will be a point in the center, put pushed 'in' the "inset_dist" amount.
    """

    return from_point3d(
        _aperture.geometry.centroid.move(
            _aperture.normal.normalize() * _aperture.properties.ph.inset_dist * -1)
    )


def find_horizon_shading(_aperture, _shading_objs, _IGH, _limit=99):
    # type: (aperture.Aperture, Sequence, gh_io.IGH, int) -> Tuple[Optional[float], Optional[float], Rhino.Geometry.LineCurve]
    """
    Returns a tuple of the Horizon shading dims and the preview checkline.

    Arguments:
    ----------
        _aperture: The HB Aperture object to determine the values for
        _shading_objs: (list) A list of possible shading objects to test against
        _IGH: (gh_io.IGH) The GH IO interface
        _limit: (float) A number (m) to limit the shading search to. Default = 99m

    Returns:
    --------
        Tuple
            [0] h_hori: Distance (m) out from the glazing surface of any horizontal shading objects found
            [1] d_hori: Distance (m) up from the base of the window to the top of any horizontal shading objects found
            [2] check_line: (Rhino.Geometry.Line) Preview line for checking results.
    """
    surface_normal = from_vector3d(_aperture.normal)

    # -----------------------------------------------------------------------
    # Find Starting Point (the bottom middle glazing-edge)
    bottom_glazing_edge = _get_bottom_glazing_edge(_aperture)
    shading_origin = _IGH.ghpythonlib_components.CurveMiddle(bottom_glazing_edge)
    up_vector = _IGH.ghpythonlib_components.VectorXYZ(0, 0, 1).vector

    # -----------------------------------------------------------------------
    # Find if there are any intersection shading objects. If so, put them in a list
    line_horizontal = _IGH.ghpythonlib_components.LineSDL(
        shading_origin, surface_normal, _limit)
    horizon_shading_objs = [shading_obj
                            for shading_obj in _shading_objs
                            if _IGH.ghpythonlib_components.BrepXCurve(shading_obj, line_horizontal).points != None
                            ]

    # -----------------------------------------------------------------------
    # Find any intersection Curves with the shading objects
    line_vertical = _IGH.ghpythonlib_components.LineSDL(
        shading_origin, up_vector, _limit)
    intersection_surface = _IGH.ghpythonlib_components.SumSurface(
        line_horizontal, line_vertical)
    intersection_curve = []
    intersection_points = []

    for shading_obj in horizon_shading_objs:
        if _IGH.ghpythonlib_components.BrepXBrep(shading_obj, intersection_surface).curves != None:
            intersection_curve.append(_IGH.ghpythonlib_components.BrepXBrep(
                shading_obj, intersection_surface))
    for pnt in intersection_curve:
        pts = _IGH.ghpythonlib_components.ControlPoints(pnt).points
        if pts:
            intersection_points.append(pts)

    # -----------------------------------------------------------------------
    # Run the "Top-Corner-Finder" if there are any intersecting objects...
    if intersection_points:
        # Find the top/closets point for each of the objects that could possibly shade
        key_points = []
        for pnt in intersection_points:
            rays = []
            angles = []
            if pnt:
                for k in range(len(pnt)):
                    rays.append(_IGH.ghpythonlib_components.Vector2Pt(
                        shading_origin, pnt[k], False).vector)
                    angles.append(_IGH.ghpythonlib_components.Angle(
                        surface_normal, rays[k]).angle)
                key_points.append(pnt[angles.index(max(angles))])

        # Find the relevant highest / closest point
        rays = []
        angles = []
        for i in range(len(key_points)):
            rays.append(_IGH.ghpythonlib_components.Vector2Pt(
                surface_normal, key_points[i], False).vector)
            angles.append(_IGH.ghpythonlib_components.Angle(
                surface_normal, rays[i]).angle)
        key_point = key_points[angles.index(max(angles))]

        # Use the point it finds to deliver the Height and Distance for the PHPP Shading Calculator
        h_hori = key_point.Z - shading_origin.Z  # Vertical distance
        hypotenuse = _IGH.ghpythonlib_components.Length(
            _IGH.ghpythonlib_components.Line(shading_origin, key_point))
        d_hori = math.sqrt(hypotenuse**2 - h_hori**2)
        check_line = _IGH.ghpythonlib_components.Line(shading_origin, key_point)
    else:
        h_hori = None
        d_hori = None
        check_line = line_horizontal

    return h_hori, d_hori, check_line


def find_overhang_shading(_aperture, _shading_objs, _IGH, _limit=99):
    # type: (aperture.Aperture, Sequence, gh_io.IGH, int) -> Tuple[Optional[float], Optional[float], Rhino.Geometry.LineCurve]

    # Figure out the glass surface (inset a bit) and then
    # find the origin point for all the subsequent shading calcs (top, middle)
    top_glazing_edge = _get_top_glazing_edge(_aperture)
    origin_point = _IGH.ghpythonlib_components.CurveMiddle(top_glazing_edge)

    # In order to also work for windows which are not vertical, find the
    # 'direction' from the glazing origin and the top/middle ege point
    glazing_center = _get_glazing_center(_aperture)
    UpVector = _IGH.ghpythonlib_components.Vector2Pt(
        glazing_center, origin_point, True).vector

    # -----------------------------------------------------------------------
    # First, need to filter the scene to find the objects that are 'above'
    # the window. Create a 'test plane' that is _extents (99m) tall and 0.5m past the wall surface, test if
    # any objects intersect that plane. If so, add them to the set of things
    # test in the next step
    depth = float(_aperture.properties.ph.inset_dist) + 0.5
    edge1 = _IGH.ghpythonlib_components.LineSDL(origin_point, UpVector, _limit)
    edge2 = _IGH.ghpythonlib_components.LineSDL(
        origin_point, from_vector3d(_aperture.geometry.normal), depth)
    intersectionTestPlane = _IGH.ghpythonlib_components.SumSurface(edge1, edge2)

    OverhangShadingObjs = (x for x in _shading_objs if _IGH.ghpythonlib_components.BrepXBrep(
        intersectionTestPlane, x).curves != None)

    # -----------------------------------------------------------------------
    # Using the filtered set of shading objects, find the 'edges' of shading
    # geom and then decide where the maximums shading point is
    # Create a new 'test' plane coming off the origin (99m in both directions this time).
    # Test to find any intersection shading objs and all their curves/points with this plane
    HorizontalLine = _IGH.ghpythonlib_components.LineSDL(
        origin_point, from_vector3d(_aperture.geometry.normal), _limit)
    VerticalLine = _IGH.ghpythonlib_components.LineSDL(origin_point, UpVector, _limit)

    IntersectionSurface = _IGH.ghpythonlib_components.SumSurface(
        HorizontalLine, VerticalLine)
    IntersectionCurves = (_IGH.ghpythonlib_components.BrepXBrep(obj, IntersectionSurface).curves
                          for obj in OverhangShadingObjs
                          if _IGH.ghpythonlib_components.BrepXBrep(obj, IntersectionSurface).curves != None)
    IntersectionPointsList = (_IGH.ghpythonlib_components.ControlPoints(
        crv).points for crv in IntersectionCurves)
    IntersectionPoints = (
        pt for list_of_pts in IntersectionPointsList for pt in list_of_pts)

    # -----------------------------------------------------------------------
    # If there are any intersection Points found, choose the right one to use to calc shading....
    # Find the top/closets point for each of the objects that could possibly shade
    smallest_angle_found = 2 * math.pi
    key_point = None

    for pt in IntersectionPoints:
        if pt == None:
            continue

        # Protect against Zero-Length error

        ray = _IGH.ghpythonlib_components.Vector2Pt(origin_point, pt, False).vector
        if ray.Length < 0.001:
            continue

        this_ray_angle = _IGH.ghpythonlib_components.Angle(
            from_vector3d(_aperture.geometry.normal), ray).angle
        if this_ray_angle < 0.001:
            continue

        if this_ray_angle <= smallest_angle_found:
            smallest_angle_found = this_ray_angle
            key_point = pt

    # -----------------------------------------------------------------------
    # Use the 'key point' found to deliver the Height and Distance for the PHPP Shading Calculator
    if not key_point:
        d_over = None
        o_over = None
        CheckLine = VerticalLine
    else:
        d_over = key_point.Z - origin_point.Z  # Vertical distance
        Hypot = _IGH.ghpythonlib_components.Length(
            _IGH.ghpythonlib_components.Line(origin_point, key_point))
        # Horizontal distance
        o_over = math.sqrt(Hypot**2 - d_over**2)
        CheckLine = _IGH.ghpythonlib_components.Line(origin_point, key_point)

    return d_over, o_over, CheckLine


def find_reveal_shading(_aperture, _shading_objs, _IGH, _limit=99):
    # type: (aperture.Aperture, Sequence, gh_io.IGH, int) -> Tuple[Optional[float], Optional[float], Rhino.Geometry.LineCurve, Rhino.Geometry.LineCurve]

    # Get the starting reference points, edges
    glazing_center = _get_glazing_center(_aperture)
    glazing_edge_left = _get_left_glazing_edge(_aperture)
    glazing_edge_right = _get_right_glazing_edge(_aperture)
    aperture_normal_vector = from_vector3d(_aperture.geometry.normal)

    # Create the Intersection Surface for each side
    Side1_OriginPt = _IGH.ghpythonlib_components.CurveMiddle(glazing_edge_left)
    Side1_NormalLine = _IGH.ghpythonlib_components.LineSDL(
        Side1_OriginPt, aperture_normal_vector, _limit)
    Side1_Direction = _IGH.ghpythonlib_components.Vector2Pt(
        glazing_center, Side1_OriginPt, False).vector
    Side1_HorizLine = _IGH.ghpythonlib_components.LineSDL(
        Side1_OriginPt, Side1_Direction, _limit)
    Side1_IntersectionSurface = _IGH.ghpythonlib_components.SumSurface(
        Side1_NormalLine, Side1_HorizLine)

    # Side2_OriginPt = SideMidPoints[1] #ghc.CurveMiddle(self.Edge_Left)
    Side2_OriginPt = _IGH.ghpythonlib_components.CurveMiddle(glazing_edge_right)
    Side2_NormalLine = _IGH.ghpythonlib_components.LineSDL(
        Side2_OriginPt, aperture_normal_vector, _limit)
    Side2_Direction = _IGH.ghpythonlib_components.Vector2Pt(
        glazing_center, Side2_OriginPt, False).vector
    Side2_HorizLine = _IGH.ghpythonlib_components.LineSDL(
        Side2_OriginPt, Side2_Direction, _limit)
    Side2_IntersectionSurface = _IGH.ghpythonlib_components.SumSurface(
        Side2_NormalLine, Side2_HorizLine)

    # Find any Shader Objects and put them all into a list
    Side1_RevealShaderObjs = []
    testStartPt = _IGH.ghpythonlib_components.Move(glazing_center, _IGH.ghpythonlib_components.Amplitude(
        aperture_normal_vector, 0.1)).geometry  # Offsets the test line just a bit
    # extend a line off to side 1
    Side1_TesterLine = _IGH.ghpythonlib_components.LineSDL(
        testStartPt, Side1_Direction, _limit)
    for i in range(len(_shading_objs)):
        if _IGH.ghpythonlib_components.BrepXCurve(_shading_objs[i], Side1_TesterLine).points != None:
            Side1_RevealShaderObjs.append(_shading_objs[i])

    Side2_RevealShaderObjs = []
    # extend a line off to side 2
    Side2_TesterLine = _IGH.ghpythonlib_components.LineSDL(
        testStartPt, Side2_Direction, _limit)
    for i in range(len(_shading_objs)):
        if _IGH.ghpythonlib_components.BrepXCurve(_shading_objs[i], Side2_TesterLine).points != None:
            Side2_RevealShaderObjs.append(_shading_objs[i])

    # ---------------------------------------------------------------------------
    # Calc Shading reveal dims
    NumShadedSides = 0
    if len(Side1_RevealShaderObjs) != 0:
        Side1_o_reveal = CalcRevealDims(
            _aperture, Side1_RevealShaderObjs, Side1_IntersectionSurface, Side1_OriginPt, Side1_Direction, _IGH)[0]
        Side1_d_reveal = CalcRevealDims(
            _aperture, Side1_RevealShaderObjs, Side1_IntersectionSurface, Side1_OriginPt, Side1_Direction, _IGH)[1]
        Side1_CheckLine = CalcRevealDims(
            _aperture, Side1_RevealShaderObjs, Side1_IntersectionSurface, Side1_OriginPt, Side1_Direction, _IGH)[2]
        NumShadedSides = NumShadedSides + 1
    else:
        Side1_o_reveal = None
        Side1_d_reveal = None
        Side1_CheckLine = Side1_HorizLine

    if len(Side2_RevealShaderObjs) != 0:
        Side2_o_reveal = CalcRevealDims(
            _aperture, Side2_RevealShaderObjs, Side2_IntersectionSurface, Side2_OriginPt, Side2_Direction, _IGH)[0]
        Side2_d_reveal = CalcRevealDims(
            _aperture, Side2_RevealShaderObjs, Side2_IntersectionSurface, Side2_OriginPt, Side2_Direction, _IGH)[1]
        Side2_CheckLine = CalcRevealDims(
            _aperture, Side2_RevealShaderObjs, Side2_IntersectionSurface, Side2_OriginPt, Side2_Direction, _IGH)[2]
        NumShadedSides = NumShadedSides + 1
    else:
        Side2_o_reveal = None
        Side2_d_reveal = None
        Side2_CheckLine = Side2_HorizLine

    #
    #
    #
    # TODO: how to handel asymmetrical reveals????

    # (Side1_o_reveal + Side2_o_reveal )/ max(1,NumShadedSides)
    o_reveal = Side1_o_reveal
    # (Side1_d_reveal + Side2_d_reveal )/ max(1,NumShadedSides)
    d_reveal = Side1_d_reveal

    #
    #
    #
    #
    #

    return o_reveal, d_reveal, Side1_CheckLine, Side2_CheckLine


def CalcRevealDims(_aperture, _shader_objs, _intersection_surface, _reference_pt, _direction_vector, _IGH):
    # type: (aperture.Aperture, Sequence, Any, Rhino.Geometry.Point3d, Rhino.Geometry.Vector3d, gh_io.IGH) -> Tuple[float, float, Rhino.Geometry.LineCurve]

    # Test shading objects for their edge points
    Side_IntersectionCurve = []
    Side_IntersectionPoints = []
    for i in range(len(_shader_objs)):  # This is the list of shading objects to filter
        if _IGH.ghpythonlib_components.BrepXBrep(_shader_objs[i], _intersection_surface).curves != None:
            Side_IntersectionCurve.append(_IGH.ghpythonlib_components.BrepXBrep(
                _shader_objs[i], _intersection_surface).curves)
    for i in range(len(Side_IntersectionCurve)):
        for k in range(len(_IGH.ghpythonlib_components.ControlPoints(Side_IntersectionCurve[i]).points)):
            Side_IntersectionPoints.append(
                _IGH.ghpythonlib_components.ControlPoints(Side_IntersectionCurve[i]).points[k])

    # Find the top/closets point for each of the objects that could possibly shade
    Side_KeyPoints = []
    Side_Rays = []
    Side_Angles = []
    for i in range(len(Side_IntersectionPoints)):
        if _reference_pt != Side_IntersectionPoints[i]:
            Ray = _IGH.ghpythonlib_components.Vector2Pt(
                _reference_pt, Side_IntersectionPoints[i], False).vector
            Angle = math.degrees(_IGH.ghpythonlib_components.Angle(
                from_vector3d(_aperture.geometry.normal), Ray).angle)
            if Angle < 89.9:
                Side_Rays.append(Ray)
                Side_Angles.append(float(Angle))
                Side_KeyPoints.append(Side_IntersectionPoints[i])
    Side_KeyPoint = Side_KeyPoints[Side_Angles.index(min(Side_Angles))]
    Side_KeyRay = Side_Rays[Side_Angles.index(min(Side_Angles))]

    # use the Key point found to calculate the Distances for the PHPP Shading Calculator
    Side_Hypot = _IGH.ghpythonlib_components.Length(
        _IGH.ghpythonlib_components.Line(_reference_pt, Side_KeyPoint))
    Deg = (_IGH.ghpythonlib_components.Angle(_direction_vector,
           Side_KeyRay).angle)  # note this is in Radians
    Side_o_reveal = math.sin(Deg) * Side_Hypot
    Side_d_reveal = math.sqrt(Side_Hypot**2 - Side_o_reveal**2)
    Side_CheckLine = _IGH.ghpythonlib_components.Line(_reference_pt, Side_KeyPoint)

    return (Side_o_reveal, Side_d_reveal, Side_CheckLine)
