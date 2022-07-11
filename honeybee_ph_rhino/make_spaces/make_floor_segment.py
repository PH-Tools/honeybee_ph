# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions to create SpaceFloorSegment objects from Rhino/Grasshopper inputs."""

try:
    from typing import Any, List
except ImportError:
    pass  # IronPython

from ladybug_rhino.fromgeometry import from_point3d, from_face3d
from ladybug_geometry.geometry3d import face, pointvector

from honeybee_ph import space
from honeybee_ph_rhino import gh_io


def calc_reference_point(IGH, _face3D):
    # type: (gh_io.IGH, face.Face3D) -> pointvector.Point3D
    """Find the 'reference point' for a Face3D.

    For rectangular Face3D objects, this is the center point. For irregular shaped Face3D
    objects ('L', 'T', 'O', etc...) this will use the Rhino 'PullPoint' to project the 
    center to the nearest surface edge. This ensure thats the reference point is always
    'on' the Face3D itself.

    Arguments:
    ----------
        * IGH (gh_io.IGH): The Grasshopper Interface object.
        * _face3D (face.Face3D): The Ladybug Face3D object for the SpaceFloorSegment.

    Returns:
    -------
        * (pointvector.Point3D): The Reference Point found.
    """

    # -- Find the normal centerpoint of the surface
    face_cent_rh_pt = from_point3d(_face3D.center)
    face_rh = from_face3d(_face3D)
    new_cp = IGH.ghpythonlib_components.PullPoint(face_cent_rh_pt, face_rh).closest_point

    return pointvector.Point3D(new_cp.X, new_cp.Y, new_cp.Z)


def create_floor_segment_from_rhino_geom(IGH, _flr_segment_geom, _weighting_factors):
    # type: (gh_io.IGH, List[Any], List[float]) -> List[space.SpaceFloorSegment]
    """Return a list of SpaceFloorSegments created from Rhino geometry.

    Arguments:
    ----------
        * IGH (gh_io.IGH): The Grasshopper Interface Object.
        * _flr_segment_geom (List[Any]): A list of Rhino Geometry representing
            the floor-segments.
        * _weighting_factors (List[float]): A List of the weighting-factors (0.0-1.0)
            to apply to the floor segments. Note: the length of this list should match the 
            _flr_segment_geom length.

    Returns:
    --------
        * list[space.SpaceFloorSegment]: A list of the new SpaceFloorSegments 
            created from the input Rhino geometry.
    """

    # -- Convert the input surfaces to LBT Geom
    # -- Note: convert_to_LBT_geom() returns a list of lists since the
    # -- to_face3d might return a list of triangulated srfcs sometimes.
    lbt_face_3ds = IGH.convert_to_LBT_geom(_flr_segment_geom)

    # TODO: probably need to type check of validate that they are all
    # Face3Ds here before moving on? Give useful warnings.

    # -- Check weighting factors
    assert len(lbt_face_3ds) == len(_weighting_factors), "Error: input lists of floor"\
        "segments and weighting factor lengths do not match?"

    # -- Create new SpaceFloorSegments for each surface input
    flr_segments = []
    for i, face_3d_list in enumerate(lbt_face_3ds):
        for face_3d in face_3d_list:
            new_segment = space.SpaceFloorSegment()
            new_segment.geometry = face_3d
            new_segment.reference_point = calc_reference_point(IGH, face_3d)
            new_segment.weighting_factor = _weighting_factors[i]
            flr_segments.append(new_segment)

    return flr_segments
