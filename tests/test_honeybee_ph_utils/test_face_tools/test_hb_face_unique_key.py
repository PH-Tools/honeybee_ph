from honeybee.boundarycondition import Ground, Outdoors
from honeybee.face import Face, Face3D
from honeybee.facetype import AirBoundary, Floor, RoofCeiling, Wall
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_ph_utils.face_tools import _hb_face_type_unique_key


def test_hb_face_type_unique_key():
    f1 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=RoofCeiling(),
        boundary_condition=Outdoors(),
    )
    face_1_name = _hb_face_type_unique_key(f1)
    assert face_1_name != None


def test_different_types_hb_face_type_unique_key():
    f1 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=RoofCeiling(),
        boundary_condition=Outdoors(),
    )
    face_1_name = _hb_face_type_unique_key(f1)
    assert face_1_name != None

    f2 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=Wall(),
        boundary_condition=Outdoors(),
    )
    face_2_name = _hb_face_type_unique_key(f2)
    assert face_2_name != None
    assert face_1_name != face_2_name

    f3 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=Floor(),
        boundary_condition=Outdoors(),
    )
    face_3_name = _hb_face_type_unique_key(f3)
    assert face_3_name != None
    assert face_1_name != face_3_name
    assert face_2_name != face_3_name

    f4 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=AirBoundary(),
        boundary_condition=Outdoors(),
    )
    face_4_name = _hb_face_type_unique_key(f4)
    assert face_4_name != None
    assert face_1_name != face_4_name
    assert face_2_name != face_4_name
    assert face_3_name != face_4_name


def test_different_BCs_hb_face_type_unique_key():
    f1 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=RoofCeiling(),
        boundary_condition=Outdoors(),
    )
    face_1_name = _hb_face_type_unique_key(f1)
    assert face_1_name != None

    f2 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=RoofCeiling(),
        boundary_condition=Ground(),
    )
    face_2_name = _hb_face_type_unique_key(f2)
    assert face_2_name != None
    assert face_1_name != face_2_name
