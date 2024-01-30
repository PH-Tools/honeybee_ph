from math import radians
from honeybee.face import Face
from honeybee_ph_utils.face_tools import sort_hb_faces_by_co_planar


def test_sort_two_planar_faces_by_co_planar():
    tolerance = 0.001
    angle_tolerance_degrees = 1.0
    angle_tolerance_radians = radians(angle_tolerance_degrees)

    # Define two co-planar faces
    face1 = Face.from_vertices("face_1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face2 = Face.from_vertices("face_2", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face3 = Face.from_vertices("face_3", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])

    # # Sort the faces by co-planarity
    sorted_faces = sort_hb_faces_by_co_planar(
        [face1, face2, face3], tolerance, angle_tolerance_radians
    )

    # Check that the faces are in the same group
    assert len(sorted_faces) == 1
    assert face1 in sorted_faces[0]
    assert face2 in sorted_faces[0]
    assert face3 in sorted_faces[0]


def test_sort_two_non_planar_faces_by_co_planar():
    tolerance = 0.001
    angle_tolerance_degrees = 1.0
    angle_tolerance_radians = radians(angle_tolerance_degrees)

    # Define two co-planar faces
    face1 = Face.from_vertices("face_1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face2 = Face.from_vertices("face_2", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face3 = Face.from_vertices("face_3", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])

    # Rotate face2 so it is pointing a different direction than face1
    face2.rotate(
        axis=face2.geometry.plane.y,
        angle=angle_tolerance_degrees + 0.1,  # Ensure it is just outside the tolerance
        origin=face2.geometry.plane.o,
    )

    # # Sort the faces by co-planarity
    sorted_faces = sort_hb_faces_by_co_planar(
        [face1, face2, face3], tolerance, angle_tolerance_radians
    )

    # Check that the faces are in the same group
    assert len(sorted_faces) == 2
    assert face1 in sorted_faces[0]
    assert face2 in sorted_faces[1]
    assert face3 in sorted_faces[0]
