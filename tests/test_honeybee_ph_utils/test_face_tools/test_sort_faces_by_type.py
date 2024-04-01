from honeybee.boundarycondition import Ground, Outdoors
from honeybee.face import Face, Face3D
from honeybee.facetype import AirBoundary, Floor, RoofCeiling, Wall
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_ph_utils.face_tools import sort_hb_faces_by_type


def faces_are_same(f1, f2):
    """Check if two faces are the same."""
    return (
        f1.geometry == f2.geometry
        and f1.type == f2.type
        and f1.display_name == f2.display_name
    )


def test_sort_hb_faces_by_type():
    f1 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=RoofCeiling(),
        boundary_condition=Outdoors(),
    )
    f2 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=Wall(),
        boundary_condition=Outdoors(),
    )
    f3 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=Floor(),
        boundary_condition=Outdoors(),
    )
    f4 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=AirBoundary(),
        boundary_condition=Outdoors(),
    )
    f5 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=AirBoundary(),
        boundary_condition=Outdoors(),
    )
    f6 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 1, 0)]),
        type=AirBoundary(),
        boundary_condition=Outdoors(),
    )
    f7 = Face(
        identifier="test",
        geometry=Face3D(boundary=[Point3D(0, 0, 0), Point3D(0, 1, 0), Point3D(1, 1, 0)]),
        type=AirBoundary(),
        boundary_condition=Outdoors(),
    )

    sorted_faces = sort_hb_faces_by_type([f1, f2, f3, f4, f5, f6, f7])
    assert len(sorted_faces) == 4


def test_sort_faces_by_type():
    # Test case 1: Empty list of faces
    f1 = Face.from_vertices(
        "f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )

    faces = [f1]
    sorted_faces = sort_hb_faces_by_type(faces)
    assert len(sorted_faces) == 1
    assert faces_are_same(sorted_faces[0][0], f1)


def test_sort_faces_by_type_all_same():
    # Test case 2: faces with the same type
    f1 = Face.from_vertices(
        "f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )
    f2 = Face.from_vertices(
        "f2", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )
    f3 = Face.from_vertices(
        "f3", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )

    faces = [f1, f2, f3]
    sorted_faces = sort_hb_faces_by_type(faces)
    assert len(sorted_faces) == 1
    assert faces_are_same(sorted_faces[0][0], f1)
    assert faces_are_same(sorted_faces[0][1], f2)
    assert faces_are_same(sorted_faces[0][2], f3)


def test_sort_faces_by_type_all_different():
    # Test case 2: faces with the same type
    f1 = Face.from_vertices(
        "f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )
    f2 = Face.from_vertices(
        "f2", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Floor()
    )
    f3 = Face.from_vertices(
        "f3", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=RoofCeiling()
    )

    faces = [f1, f2, f3]
    sorted_faces = sort_hb_faces_by_type(faces)
    assert len(sorted_faces) == 3
    assert faces_are_same(sorted_faces[0][0], f1)
    assert faces_are_same(sorted_faces[1][0], f2)
    assert faces_are_same(sorted_faces[2][0], f3)


def test_sort_faces_by_type_mixed():
    # Test case 2: faces with the same type
    f1 = Face.from_vertices(
        "f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )
    f2 = Face.from_vertices(
        "f2", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Floor()
    )
    f3 = Face.from_vertices(
        "f3", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=RoofCeiling()
    )
    f4 = Face.from_vertices(
        "f4", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], type=Wall()
    )

    faces = [f1, f2, f3, f4]
    sorted_faces = sort_hb_faces_by_type(faces)
    assert len(sorted_faces) == 3
    assert faces_are_same(sorted_faces[0][0], f1)
    assert faces_are_same(sorted_faces[0][1], f4)
    assert faces_are_same(sorted_faces[1][0], f2)
    assert faces_are_same(sorted_faces[2][0], f3)
