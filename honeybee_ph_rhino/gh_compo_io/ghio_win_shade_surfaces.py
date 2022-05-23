# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for creating window shading surfaces."""

from honeybee import room, aperture
from ladybug_rhino.fromgeometry import from_face3d
from ladybug_geometry.geometry3d import Face3D

try:
    import Rhino.Geometry as rg
except ImportError:
    pass

try:
    from typing import List, Optional, Collection
except ImportError:
    pass


def create_punched_geometry(_hb_rooms):
    # type: (Collection[room.Room]) -> List[rg.Brep]
    """Return a list of all of the 'punched' surfaces from the HB-Model."""

    envelope_surfaces_punched = []
    for hb_room in _hb_rooms:
        for face in hb_room.faces:
            rh_geom = from_face3d(face.punched_geometry)  # type: Optional[rg.Brep]

            if rh_geom:
                rh_geom.SetUserString('display_name', face.display_name)
                envelope_surfaces_punched.append(rh_geom)

    return envelope_surfaces_punched


def create_inset_aperture_surface(_aperture):
    # type: (aperture.Aperture) -> Optional[rg.Brep]
    """Return Rhino.Geometry.Brep of an aperture's face, inset."""
    inset_face = from_face3d(
        _aperture.geometry.move(
            _aperture.geometry.normal.reverse() * _aperture.properties.ph.inset_dist
        )
    )  # type: Optional[rg.Brep]

    if inset_face:
        inset_face.SetUserString('display_name', _aperture.display_name)

    return inset_face


def create_inset_aperture_surfaces(_hb_rooms):
    # type: (Collection[room.Room]) -> List[rg.Brep]
    """Return a list of aperture Rhino.Geometry.Brep surfaces, inset."""

    inset_window_surfaces = []
    for room in _hb_rooms:
        for face in room.faces:
            for aperture in face.apertures:
                inset_window_surfaces.append(create_inset_aperture_surface(aperture))
    return inset_window_surfaces


def create_window_reveal(_hb_aperture):
    # type: (aperture.Aperture) -> List[rg.Brep]
    """Return a list of the Aperture 'reveal' surfaces."""

    extrusion_vector = _hb_aperture.normal.reverse() * _hb_aperture.properties.ph.inset_dist
    return [
        from_face3d(Face3D.from_extrusion(seg, extrusion_vector))
        for seg in _hb_aperture.geometry.boundary_segments
    ]


def create_window_reveals(_hb_rooms):
    # type: (Collection[room.Room]) -> List[rg.Brep]
    """Return a list of all the aperture 'reveals' in the Honeybee-Model"""

    reveals = []
    for room in _hb_rooms:
        for face in room.faces:
            for aperture in face.apertures:
                reveals.extend(create_window_reveal(aperture))
    return reveals
