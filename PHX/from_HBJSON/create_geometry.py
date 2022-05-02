# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for building PHX-Geometry from Ladybug / Honeybee Geometry."""

from honeybee import aperture, face, shade
from ladybug_geometry_ph.geometry3d_ph import pointvector
from ladybug_geometry.geometry3d.pointvector import Vector3D
from PHX.model import geometry


def create_PHX_Vertix_from_LBT_P3D(_lbt_Point3D: pointvector.PH_Point3D) -> geometry.PhxVertix:
    """Returns a new PHX Vertix object with attributes based on a Ladybug_PH PH_Point3D.

    Arguments:
    ----------
        * _lbt_Point3D (pointvector.PH_Point3D): The PH_Point3D to base the new Vertix on.

    Returns:
    --------
        * geometry.Vertix: The new PHX Vertix object.
    """

    new_pt = geometry.PhxVertix()
    new_pt.id_num = geometry.PhxVertix._count
    _lbt_Point3D.properties._ph.id_num = new_pt.id_num

    new_pt.x = _lbt_Point3D.x
    new_pt.y = _lbt_Point3D.y
    new_pt.z = _lbt_Point3D.z

    return new_pt


def create_PhxVector_from_lbt_vec3D(_lbt_vector3d: Vector3D) -> geometry.PhxVector:
    return geometry.PhxVector(
        _lbt_vector3d.x,
        _lbt_vector3d.y,
        _lbt_vector3d.z,
    )


def create_PHX_Polyon_from_hb_aperture(_hb_aperture: aperture.Aperture) -> geometry.PhxPolygon:
    """Return a new PHX-Polygon based on a honeybee-aperture.

    Arguments:
    ----------
        * _hb_aperture (aperture.Aperture): The Honeybee-Aperture to base the PHX Polygon on.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon object.
    """
    new_polygon = geometry.PhxPolygon()

    new_polygon.id_num = geometry.PhxPolygon._count  # TODO: WHY?
    new_polygon.display_name = _hb_aperture.display_name
    new_polygon.area = _hb_aperture.geometry.area
    new_polygon.normal_vector = create_PhxVector_from_lbt_vec3D(_hb_aperture.normal)

    for v in _hb_aperture.vertices:
        new_polygon.add_vertix(create_PHX_Vertix_from_LBT_P3D(v))

    # -- reset the hb-face num to keep everything aligned
    _hb_aperture.properties._ph.id_num = new_polygon.id_num

    return new_polygon


def create_PHX_Polyon_from_hb_face(_hb_face: face.Face) -> geometry.PhxPolygon:
    """Return a new PHX-Polygon based on a honeybee-face.

    Arguments:
    ----------
        * _hb_face (face.Face): The Honeybee Face to base the new Polygon on.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon object.
    """
    new_polygon = geometry.PhxPolygon()

    new_polygon.id_num = geometry.PhxPolygon._count  # TODO: WHY?
    new_polygon.display_name = _hb_face.display_name
    new_polygon.area = _hb_face.geometry.area
    new_polygon.normal_vector = create_PhxVector_from_lbt_vec3D(_hb_face.normal)

    for v in _hb_face.vertices:
        new_polygon.add_vertix(create_PHX_Vertix_from_LBT_P3D(v))

    for aperture in _hb_face.apertures:
        new_polygon.add_child_poly_id(aperture.properties.ph.id_num)

    # -- reset the hb-face num to keep everything aligned
    _hb_face.properties._ph.id_num = new_polygon.id_num

    return new_polygon


def create_PHX_Polygon_from_hb_shade(_hb_shade: shade.Shade) -> geometry.PhxPolygon:
    """Returns a new PHX-Polygon based on a honeybee-shade.

    Arguments:
    ----------
        * _hb_shade (shade.Shade): The Honeybee Shade to build the new PHX-Polygon from.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon created from the Honeybee-Shade.

    """
    new_polygon = geometry.PhxPolygon()

    new_polygon.id_num = geometry.PhxPolygon._count  # TODO: WHY?
    _hb_shade.properties.ph.id_num = new_polygon.id_num
    new_polygon.normal_vector = create_PhxVector_from_lbt_vec3D(
        _hb_shade.normal)
    for v in _hb_shade.vertices:
        new_polygon.add_vertix(create_PHX_Vertix_from_LBT_P3D(v))

    return new_polygon
