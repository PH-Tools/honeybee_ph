import math

import pytest
from ladybug_geometry.geometry3d.plane import Plane
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_ph_utils.polygon2d_tools import counterclockwise_angle_between_2_Planes
from honeybee_ph_utils.vector3d_tools import vector_equal

TOL = 0.001


def test_radians_angle_between_coincident_planes():
    # Test case 1: Parallel planes
    plane1 = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0))
    assert vector_equal(plane1.x, Vector3D(1, 0, 0), TOL)

    plane2 = plane1.duplicate()
    assert vector_equal(plane2.x, Vector3D(1, 0, 0), TOL)

    angle = counterclockwise_angle_between_2_Planes(plane1, plane2, TOL)
    assert angle == pytest.approx(0)


def test_radians_angle_between_90_degree_planes():
    # Test case 1: Parallel planes
    plane1 = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0))
    assert vector_equal(plane1.x, Vector3D(1, 0, 0), TOL)

    plane2 = plane1.rotate(plane1.n, math.radians(90), plane1.o)
    assert vector_equal(plane2.x, Vector3D(0, 1, 0), TOL)

    angle = counterclockwise_angle_between_2_Planes(
        plane1,
        plane2,
        TOL,
    )
    assert angle == pytest.approx(math.radians(90))


def test_radians_angle_between_45_degree_planes():
    # Test case 1: Parallel planes
    plane1 = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0))
    assert vector_equal(plane1.x, Vector3D(1, 0, 0), TOL)

    plane2 = plane1.rotate(plane1.n, math.radians(45), plane1.o)
    print("{:.12f}".format(plane2.x.x))
    assert vector_equal(plane2.x, Vector3D(0.707106781187, 0.707106781187, 0), TOL)  # type: ignore

    angle = counterclockwise_angle_between_2_Planes(
        plane1,
        plane2,
        TOL,
    )
    assert angle == pytest.approx(math.radians(45))


def test_angle_between_planes_with_different_normals():
    plane1 = Plane(Vector3D(0, 0, 1), Point3D(0, 0, 0))
    assert vector_equal(plane1.x, Vector3D(1, 0, 0), TOL)

    plane2 = Plane(Vector3D(0, 1, 0), Point3D(1, 1, 0))
    assert vector_equal(plane2.x, Vector3D(1, -0, 0), TOL)

    with pytest.raises(Exception):
        counterclockwise_angle_between_2_Planes(plane1, plane2, TOL)
