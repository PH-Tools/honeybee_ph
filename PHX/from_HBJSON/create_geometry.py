# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for building PHX-Geometry from Ladybug / Honeybee Geometry."""

from honeybee import aperture, face, shade
from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
from ladybug_geometry.geometry3d.plane import Plane
from PHX.model import geometry


def create_PHX_Vertix_from_lbt_Point3D(_lbt_Point3D: Point3D) -> geometry.PhxVertix:
    """Returns a new PhxVertix object with attributes based on an LBT-Point3D."""
    return geometry.PhxVertix(
        _lbt_Point3D.x,
        _lbt_Point3D.y,
        _lbt_Point3D.z
    )


def create_PhxVector_from_lbt_Vector3D(_lbt_vector3d: Vector3D) -> geometry.PhxVector:
    """Return a new PhxVector with attributes based on an LBT-Vector3D."""
    return geometry.PhxVector(
        _lbt_vector3d.x,
        _lbt_vector3d.y,
        _lbt_vector3d.z,
    )


def create_PhxPlane_from_lbt_Plane(_lbt_plane: Plane) -> geometry.PhxPlane:
    """Return a new PhxPlane with attributes based on an LBT-Plane"""
    return geometry.PhxPlane(
        create_PhxVector_from_lbt_Vector3D(_lbt_plane.n),
        create_PHX_Vertix_from_lbt_Point3D(_lbt_plane.o),
        create_PhxVector_from_lbt_Vector3D(_lbt_plane.x),
        create_PhxVector_from_lbt_Vector3D(_lbt_plane.y)
    )


def create_PhxPolygon_from_hb_aperture(_hb_aperture: aperture.Aperture) -> geometry.PhxPolygon:
    """Return a new PHX-Polygon based on a honeybee-aperture.

    Arguments:
    ----------
        * _hb_aperture (aperture.Aperture): The Honeybee-Aperture to base the PHX Polygon on.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon object.
    """
    phx_polygon = geometry.PhxPolygon()

    phx_polygon.display_name = _hb_aperture.display_name
    phx_polygon.area = _hb_aperture.geometry.area
    phx_polygon.normal_vector = create_PhxVector_from_lbt_Vector3D(_hb_aperture.normal)

    for v in _hb_aperture.vertices:
        phx_polygon.add_vertix(create_PHX_Vertix_from_lbt_Point3D(v))
    phx_polygon.plane = create_PhxPlane_from_lbt_Plane(_hb_aperture.geometry.plane)

    return phx_polygon


def create_PhxPolygon_from_hb_face(_hb_face: face.Face) -> geometry.PhxPolygon:
    """Return a new PHX-Polygon based on a honeybee-face.

    Arguments:
    ----------
        * _hb_face (face.Face): The Honeybee Face to base the new Polygon on.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon object.
    """
    phx_polygon = geometry.PhxPolygon()

    phx_polygon.display_name = _hb_face.display_name
    phx_polygon.area = _hb_face.geometry.area
    phx_polygon.normal_vector = create_PhxVector_from_lbt_Vector3D(_hb_face.normal)

    for v in _hb_face.vertices:
        phx_polygon.add_vertix(create_PHX_Vertix_from_lbt_Point3D(v))
    phx_polygon.plane = create_PhxPlane_from_lbt_Plane(_hb_face.geometry.plane)

    return phx_polygon


def create_PhxPolygon_from_hb_shade(_hb_shade: shade.Shade) -> geometry.PhxPolygon:
    """Returns a new PHX-Polygon based on a honeybee-shade.

    Arguments:
    ----------
        * _hb_shade (shade.Shade): The Honeybee Shade to build the new PHX-Polygon from.

    Returns:
    --------
        * geometry.Polygon: The new PHX-Polygon created from the Honeybee-Shade.

    """
    phx_polygon = geometry.PhxPolygon()

    phx_polygon.normal_vector = create_PhxVector_from_lbt_Vector3D(_hb_shade.normal)

    for v in _hb_shade.vertices:
        phx_polygon.add_vertix(create_PHX_Vertix_from_lbt_Point3D(v))
    phx_polygon.plane = create_PhxPlane_from_lbt_Plane(_hb_shade.geometry.plane)

    return phx_polygon
