# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Tools for working with Ladybug.geometry2d.Polygon2D objects."""

import math
from copy import copy

try:
    from typing import List
except ImportError:
    pass  # Python 2.7

try:
    from ladybug_geometry.geometry2d.pointvector import Point2D, Vector2D
    from ladybug_geometry.geometry2d.polygon import Polygon2D
    from ladybug_geometry.geometry3d.face import Face3D
    from ladybug_geometry.geometry3d.plane import Plane
except ImportError as e:
    raise ImportError("Failed to import ladybug_geometry: " + str(e))

try:
    from honeybee_ph_utils import vector3d_tools
except ImportError as e:
    raise ImportError("Failed to import honeybee_ph_utils: " + str(e))


def counterclockwise_angle_between_2_Planes(_plane1, _plane2, _tolerance):
    # type: (Plane, Plane, float) -> float
    """Return the counterclockwise angle (in radians) between two Plane's X-Axes."""

    if not vector3d_tools.vector_equal(_plane1.n, _plane2.n, _tolerance):
        msg = (
            "Error: Cannot calculate the angle between planes with different normal vectors ."
            "Normal vector: {} is not equal to: {}".format(_plane1.n, _plane2.n)
        )
        raise Exception(msg)

    angle_in_radians = vector3d_tools.angle_between_2D_vectors(_plane1.x, _plane2.x)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_in_radians)

    # Determine the sign of the angle using the cross product
    cross_prod = vector3d_tools.cross_product(_plane1.x, _plane2.x)
    if vector3d_tools.dot_product(cross_prod, _plane1.n) < 0:
        angle_degrees = 360 - angle_degrees

    return math.radians(angle_degrees)


def move_vector_between_two_points(_point1, _point2):
    # type: (Point2D, Point2D) -> Vector2D
    """Return a Vector2D from _point1 to _point2."""

    mv_x = _point1.x - _point2.x
    mv_y = _point1.y - _point2.y
    move_vec = Vector2D(mv_x, mv_y)  # type: ignore
    return move_vec


def translate_polygon2D(_polygon2D, _starting_plane, _target_plane, _tolerance):
    # type: (Polygon2D, Plane, Plane, float) -> Polygon2D
    """Translate (move, rotate) one Polygon2D from its own Plane into another."""

    # ------------------------------------------------------------------------
    # -- Create a Vector2D from the Polygon2D's origin to the _new_plane's
    # -- origin within the new-plane's space.
    target_plane_origin_pt = copy(_target_plane.xyz_to_xy(_target_plane.o))
    polygon2D_origin_pt_in_target_plane_space = copy(_target_plane.xyz_to_xy(_starting_plane.o))

    # ------------------------------------------------------------------------
    # -- Move the starting Polygon2D into the _new_plane's space
    move_vec = move_vector_between_two_points(polygon2D_origin_pt_in_target_plane_space, target_plane_origin_pt)
    moved_polygon2D = _polygon2D.move(move_vec)

    # ------------------------------------------------------------------------
    # -- Rotate the moved Polygon2D to align with the _new_plane's space
    angle_in_radians = counterclockwise_angle_between_2_Planes(
        _target_plane,
        _starting_plane,
        _tolerance,
    )
    rotated_polygon = moved_polygon2D.rotate(angle=angle_in_radians, origin=polygon2D_origin_pt_in_target_plane_space)

    return rotated_polygon


def get_lbt_Face3D_polygon2Ds(_lbt_face3Ds):
    # type: (List[Face3D]) -> List[Polygon2D]
    """Return the LBT-Face3D Polygon2Ds."""

    return [copy(f.polygon2d) for f in _lbt_face3Ds]


def get_lbt_Face3D_planes(_lbt_face3Ds):
    # type: (List[Face3D]) -> List[Plane]
    """Return the LBT-Face3D Planes."""

    return [copy(f.plane) for f in _lbt_face3Ds]


def merge_polygon_2ds(_lbt_polygon_2ds, _tolerance):
    # type: (List[Polygon2D], float) -> List[Polygon2D]
    """Merge together a list of Polygon2Ds."""

    try:
        merged_polygon2Ds = Polygon2D.boolean_union_all(_lbt_polygon_2ds, _tolerance)
    except Exception as e:
        merged_polygon2Ds = _lbt_polygon_2ds

    return merged_polygon2Ds


def merge_lbt_face_polygons(_lbt_face3Ds, _tolerance):
    # type: (List[Face3D], float) -> List[Polygon2D]
    """Merge together the Polygon2Ds of a list of LBT-Face3Ds."""

    lbt_face3D_polygon2Ds = get_lbt_Face3D_polygon2Ds(_lbt_face3Ds)
    lbt_face3D_planes = get_lbt_Face3D_planes(_lbt_face3Ds)
    reference_plane = _lbt_face3Ds[0].plane

    try:
        # ---------------------------------------------------------------------
        # -- Get all the LBT-Face3D Polygon2Ds in the same Plane-space
        translated_polygon2Ds = []  # type: List[Polygon2D]
        for face3D_poly_2D, face3D_plane in zip(lbt_face3D_polygon2Ds, lbt_face3D_planes):
            translated_polygon2Ds.append(translate_polygon2D(face3D_poly_2D, face3D_plane, reference_plane, _tolerance))

        # ---------------------------------------------------------------------
        # -- Try and merge all the new Polygon2Ds together into a single one.
        merged_polygon2Ds = Polygon2D.boolean_union_all(translated_polygon2Ds, _tolerance)
    except Exception as e:
        merged_polygon2Ds = list(lbt_face3D_polygon2Ds)

    return merged_polygon2Ds
