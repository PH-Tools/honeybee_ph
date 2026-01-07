# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Tools for working with Honeybee.face.Face objects."""

import logging
import math
from collections import defaultdict

try:
    from typing import List, Sequence, TypeVar, Union
except ImportError:
    pass  # IronPython 2.7

try:
    T = TypeVar("T", bound="Union[face.Face, shade.Shade]")
except Exception:
    pass  # IronPython 2.7

try:
    from honeybee import face, shade
except ImportError:
    raise ImportError("Failed to import honeybee")

try:
    from ladybug_geometry.geometry3d import pointvector
    from ladybug_geometry.geometry3d.plane import Plane
except ImportError:
    raise ImportError("Failed to import ladybug_geometry")

logger = logging.getLogger(__name__)


def _hb_face_type_unique_key(_hb_face):
    # type: (face.Face | shade.Shade) -> str
    """Return a unique key for an HB-Face's type considering the type, construction, and bc."""
    return "{}_{}_{}".format(
        getattr(_hb_face, "type", "shade"),
        getattr(_hb_face, "boundary_condition", "shade"),
        _hb_face.properties.energy.construction.display_name,  # type: ignore
    )


def sort_hb_faces_by_type(_faces):
    # type: (Sequence[T]) -> List[List[T]]
    """Group HB-Faces by their type."""
    logger.debug("sort_hb_faces_by_type(_faces=[{}])".format(len(_faces)))

    d = defaultdict(list)
    for face in _faces:
        key = _hb_face_type_unique_key(face)
        d[key].append(face.duplicate())

    logger.debug("Returning: [{}] Groups".format(len(d.values())))
    return list(d.values())


def sort_hb_faces_by_co_planar(_faces, _tolerance, _angle_tolerance_radians):
    # type: (List[T], float, float) -> List[List[T]]
    """Group HB-Faces with their co-planar neighbors.
    Args:
        _faces: (List[Face | Shade]) A list of HB-Faces to sort.
        _tolerance: (Model units) The tolerance value for co-planarity test, in model units.
        _angle_tolerance: (Radians) The tolerance for co-planarity, in radians.
    Returns:
        (List[List[Face | Shade]]) A list of lists of HB-Faces that are co-planar.
    """
    logger.debug(
        "sort_hb_faces_by_co_planar(_faces=[{}], _tolerance={:.4f}, _angle_tolerance_radians={:.4f})".format(
            len(_faces), _tolerance, _angle_tolerance_radians
        )
    )

    groups = {}  # type: dict[Plane, List[T]]
    for face in _faces:
        for group_plane, group_faces in groups.items():
            if face.geometry.plane.is_coplanar_tolerance(group_plane, _tolerance, _angle_tolerance_radians):
                group_faces.append(face)
                break
        else:
            groups[face.geometry.plane] = [face]

    # for k in sorted(groups.keys(), key=lambda p: p.n.x):
    #     logger.debug("Group {}".format(k.n))
    #     for face in groups[k]:
    #         face_type = getattr(face, "type", "shade")
    #         const_name = getattr(face.properties, "energy").construction.display_name
    #         logger.debug("  {} | {} | {}".format(face.display_name, face_type, const_name))

    logger.debug("Returning: [{}] Groups".format(len(groups.values())))
    return list(groups.values())


def points_are_coincident(_pt1, _pt2, _tolerance):
    # type: (pointvector.Point3D, pointvector.Point3D, float) -> bool
    """Return True if two Point3D objects are coincident within the tolerance."""
    return _pt1.distance_to_point(_pt2) < _tolerance


def hb_faces_are_touching(_face_2, _face_1, _tolerance):
    # type: (face.Face, face.Face, float) -> bool
    """Return True if the faces are 'touching' one another within the tolerance."""

    for v in _face_1.vertices:
        if _face_2.geometry.is_point_on_face(v, _tolerance):
            return True
        elif any([points_are_coincident(v, v2, _tolerance) for v2 in _face_2.vertices]):
            return True
    return False


def find_connected_HB_Faces(_hb_faces, _tolerance):
    # type: (List[face.Face], float) -> List[List[face.Face]]
    """Finds 'connected' HB-Faces.

    Args:
        _hb_faces List[Face | Shade]: A list of Honeybee face or shades to search for connected components.
        _tolerance: A tolerance value for determining whether two faces are touching.

    Returns:
        A list of lists, where each inner list contains a connected component of touching faces.
    """

    """Initialize an empty set called visited to keep track of which faces have 
    been visited during the search, and an empty list called components to store 
    the connected component groups."""
    logger.debug("find_connected_HB_Faces(_hb_faces=[{}], _tolerance={:.4f})".format(len(_hb_faces), _tolerance))

    visited = set()
    components = []

    def depth_first_search(node, component):
        # type: (face.Face, List[face.Face]) -> None
        """Define a recursive function that takes a starting face node
        and a list component to store the connected component.
        The function adds the starting face to the visited set and the component list,
        and then recursively calls itself on all neighboring faces that are not
        in the visited set and are touching the starting face within
        a given tolerance _tolerance.
        """
        visited.add(node)
        component.append(node)

        for _neighbor_face in _hb_faces:
            if _neighbor_face not in visited and hb_faces_are_touching(node, _neighbor_face, _tolerance):
                depth_first_search(_neighbor_face, component)

    """Loop over all the faces in the input list _hb_faces. If a face has not 
    been visited yet, create an empty list called 'component', call the 'depth_first_search'
    function with the face and the new component list, and append the 'component' list 
    to the master components list."""
    for hb_face in _hb_faces:
        if hb_face not in visited:
            component = []
            depth_first_search(hb_face, component)
            components.append(component)

    # for component in components:
    #     logger.debug("Component with {} faces:".format(len(component)))
    #     for face in component:
    #         face_type = getattr(face, "type", "shade")
    #         const_name = getattr(face.properties, "energy").construction.display_name
    #         logger.debug("  {} | {} | {}".format(face.display_name, face_type, const_name))

    logger.debug("Returning: [{}] Groups".format(len(components)))
    return components


def group_hb_faces(_hb_faces, _tolerance, _angle_tolerance_degrees):
    # type: (Sequence[T], float, float) -> List[List[T]]
    """Sort HB-Faces into groups of similar, planar, connected faces.

    Args:
        _hb_faces: (List[Face | Shade]) A list of HB-Faces to sort.
        _tolerance: (Model units) The tolerance value for co-planarity test, in model units.
        _angle_tolerance_degrees: (Degrees) The tolerance for co-planarity, in degrees.
    Returns:
        (List[List[Face | Shade]]) A list of lists of HB-Faces that are similar, planar, and connected.
    """
    logger.debug("group_hb_faces()")

    face_groups_by_type = sort_hb_faces_by_type(_hb_faces)

    face_groups_coplanar = []
    angle_tolerance_radians = math.radians(_angle_tolerance_degrees)
    for face_group in face_groups_by_type:
        face_groups_coplanar.extend(sort_hb_faces_by_co_planar(face_group, _tolerance, angle_tolerance_radians))

    face_groups_connected = []
    for face_group in face_groups_coplanar:
        face_groups_connected.extend(find_connected_HB_Faces(face_group, _tolerance))

    return face_groups_connected
