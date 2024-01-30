from honeybee.face import Face
from honeybee_ph_utils.face_tools import find_connected_HB_Faces


def test_find_connected_HB_Faces_single_face():
    # Define a single face
    face1 = Face.from_vertices("f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])

    # Check that the function returns a single component containing the face
    assert find_connected_HB_Faces([face1], 0.01) == [[face1]]


def test_find_connected_HB_Faces_two_faces():
    # Define two touching faces
    face1 = Face.from_vertices("f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face2 = Face.from_vertices("f2", [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)])

    # Check that the function returns a single component containing both faces
    assert find_connected_HB_Faces([face1, face2], 0.01) == [[face1, face2]]


def test_find_connected_HB_Faces_three_faces():
    # Define three touching faces
    face1 = Face.from_vertices("f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face2 = Face.from_vertices("f2", [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)])
    face3 = Face.from_vertices("f3", [(0, 0, 0), (0, 0, 1), (1, 0, 1), (1, 0, 0)])

    # Check that the function returns a single component containing all three faces
    assert find_connected_HB_Faces([face1, face2, face3], 0.01) == [
        [face1, face2, face3]
    ]


def test_find_connected_HB_Faces_two_connected_faces():
    # Define two touching faces
    face1 = Face.from_vertices("f1", [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)])
    face2 = Face.from_vertices("f2", [(0, 0, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1)])

    # Define a non-touching face
    face3 = Face.from_vertices("f3", [(1, 1, 1), (1, 2, 1), (1, 2, 2), (1, 1, 2)])

    # Check that the function returns two components, one containing face1 and face2, and one containing face3
    assert find_connected_HB_Faces([face1, face2, face3], 0.01) == [
        [face1, face2],
        [face3],
    ]
