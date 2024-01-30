import pytest
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.pointvector import Point3D

from honeybee_ph_utils.polygon2d_tools import merge_lbt_face_polygons

TOL = 0.1


def test_merge_two_face3Ds_overlapping_merge_into_one() -> None:
    f1 = Face3D(
        [Point3D(0, 0, 0), Point3D(10, 0, 0), Point3D(10, 10, 0), Point3D(0, 10, 0)],
        Plane(Point3D(0, 0, 1), Point3D(0, 0, 0)),
    )

    f2 = Face3D(
        [Point3D(0, 8, 0), Point3D(20, 8, 0), Point3D(20, 18, 0), Point3D(0, 18, 0)],
        Plane(Point3D(0, 0, 1), Point3D(0, 8, 0)),
    )

    merged_polygon2D = merge_lbt_face_polygons([f1, f2], TOL)
    assert len(merged_polygon2D) == 1
    assert merged_polygon2D[0].area == pytest.approx(280, abs=TOL)
    assert len(merged_polygon2D[0].vertices) == 6


def test_merge_two_face3Ds_separated_do_not_merge() -> None:
    f1 = Face3D(
        [Point3D(0, 0, 0), Point3D(10, 0, 0), Point3D(10, 10, 0), Point3D(0, 10, 0)],
        Plane(Point3D(0, 0, 1), Point3D(0, 0, 0)),
    )

    f2 = Face3D(
        [Point3D(0, 15, 0), Point3D(20, 15, 0), Point3D(20, 25, 0), Point3D(0, 25, 0)],
        Plane(Point3D(0, 0, 1), Point3D(0, 15, 0)),
    )

    merged_polygon2D = merge_lbt_face_polygons([f1, f2], TOL)
    assert len(merged_polygon2D) == 2
    assert merged_polygon2D[0].area == pytest.approx(100, abs=TOL)
    assert merged_polygon2D[1].area == pytest.approx(200, abs=TOL)
    assert len(merged_polygon2D[0].vertices) == 4
    assert len(merged_polygon2D[1].vertices) == 4
