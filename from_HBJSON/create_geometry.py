# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions for building PHX-Geometry from Ladybug / Honeybee Geometry."""

from honeybee import aperture, face
from ladybug_geometry_ph.geometry3d_ph import pointvector
from PHX import geometry


def create_PHX_Vertix_from_LBT_P3D(_lbt_Point3D: pointvector.PH_Point3D) -> geometry.Vertix:
    """Returns a new PHX Vertix object with attributes based on a Ladybug_PH PH_Point3D.

    Arguments:
    ----------
        * _lbt_Point3D (pointvector.PH_Point3D): The PH_Point3D to base the new Vertix on.

    Returns:
    --------
        * geometry.Vertix: The new PHX Vertix object.
    """

    new_pt = geometry.Vertix()
    new_pt.id_num = geometry.Vertix._count
    _lbt_Point3D.properties._ph.id_num = new_pt.id_num

    new_pt.x = _lbt_Point3D.x
    new_pt.y = _lbt_Point3D.y
    new_pt.z = _lbt_Point3D.z

    return new_pt


def create_PHX_Polyon_from_hb_aperture(_hb_aperture: aperture.Aperture) -> geometry.Polygon:
    """

    Arguments:
    ----------
        * _hb_aperture (aperture.Aperture): The Honeybee-Aperture to base the PHX Polygon on.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon object.
    """
    new_polygon = geometry.Polygon()

    new_polygon.id_num = geometry.Polygon._count
    _hb_aperture.properties._ph.id_num = new_polygon.id_num
    new_polygon.normal_vector = _hb_aperture.normal
    new_polygon.vertices = [create_PHX_Vertix_from_LBT_P3D(v)
                            for v in _hb_aperture.vertices]

    return new_polygon


def create_PHX_Polyon_from_hb_face(_hb_face: face.Face) -> geometry.Polygon:
    """

    Arguments:
    ----------
        * _hb_face (face.Face): The Honeybee Face to base the new Polygon on.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon object.
    """
    new_polygon = geometry.Polygon()

    new_polygon.id_num = geometry.Polygon._count
    _hb_face.properties._ph.id_num = new_polygon.id_num
    new_polygon.normal_vector = _hb_face.normal
    new_polygon.vertices = [create_PHX_Vertix_from_LBT_P3D(v) for v in _hb_face.vertices]
    new_polygon.child_polygon_ids = [aperture.properties.ph.id_num
                                     for aperture in _hb_face.apertures]

    return new_polygon
