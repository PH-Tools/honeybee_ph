from dataclasses import dataclass
import pytest
from ladybug_geometry.geometry3d import Face3D, Point3D, Plane
from dataclasses import dataclass


@pytest.fixture
def floor_segment_geometry():

    @dataclass
    class Data:
        flr_segment_1: Face3D
        flr_segment_2: Face3D

    boundary_1 = [
        Point3D(0, 0, 0),
        Point3D(10, 0, 0),
        Point3D(10, 10, 0),
        Point3D(0, 10, 0),
    ]
    plane_1 = Plane()
    face_1 = Face3D(boundary_1, plane_1)

    boundary_2 = [
        Point3D(0, 0, 0),
        Point3D(10, 0, 0),
        Point3D(10, 10, 0),
        Point3D(0, 10, 0),
    ]
    plane_2 = Plane()
    face_2 = Face3D(boundary_2, plane_2)

    return Data(
        face_1,
        face_2
    )
