# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to convert a standard HBJSON Model over to WUFI Objects"""

from honeybee.model import Model as HB_Model
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry_ph.geometry3d_ph.pointvector import PH_Point3D
from honeybee_energy_ph.construction.opaque import PH_OpaqueConstruction
from honeybee_energy_ph.construction.window import PH_WindowConstruction
from to_WUFI_XML.wufi import Project, Variant


class MissingPropertiesError(Exception):
    def __init__(self, _lbt_obj):
        self.message = (f'Error: LBT Object "{_lbt_obj}" does not have a .properties attribute?\n'
                        'Can not add the .ph to missing .properties attribute.')
        super().__init__(self.message)


def convert_HB_model_to_WUFI_Project(_hb_model: HB_Model) -> Project:
    """Return a complete WUFI Project object with values based on the HB Model

    Arguments:
    ----------
        * _hb_model (HB_Model): The Honeybee Model to base the WUFI Project on

    Returns:
    --------
        * (Project): The new WUFI Project object. 
    """

    project = Project()
    project.add_opaque_assemblies_from_HB_model(_hb_model)
    project.add_transparent_assemblies_from_HB_Model(_hb_model)
    project.variants = [Variant.from_room(room) for room in _hb_model.rooms]

    return project


def convert_Face3D(_lbt_geom: Face3D) -> Face3D:
    """Convert Ladybug Face3D vertices into PH-Vertices which have a .properties

    Arguments:
    ----------
        * _lbt_geometry (Face3D): A Labybug Face3D object to convert the vertices of.

    Returns:
    --------
        * Face3D: A new Face3D with all of it's vertices converted to PH-Style with a .properties.ph
    """

    # -- Create new PH Vertices from the HB-Vertices
    new_ph_vertices = [PH_Point3D(v.x, v.y, v.z) for v in _lbt_geom.vertices]

    # -- Re-set the boundary / vertices of the HB-Face._geometry (Face3D)
    # -- This is adapted from ladybug_geometry.geometry3D.face.Face3D.__copy__()
    # -- I don't love this. If Face3D __copy__ changes someday, it won't happen here. Grrr...
    _new_lbt_face3D = Face3D(tuple(new_ph_vertices), _lbt_geom.plane)

    # -- Unlcear if we need these or how to update them?
    # _lbt_geom._transfer_properties(_new_lbt_face3D)
    # _new_lbt_face3D._holes = _lbt_geom._holes
    # _new_lbt_face3D._polygon2d = _lbt_geom._polygon2d
    # _new_lbt_face3D._mesh2d = _lbt_geom._mesh2d
    # _new_lbt_face3D._mesh3d = _lbt_geom._mesh3d

    return _new_lbt_face3D


def add_PH_Properties_to_model(_model: HB_Model) -> HB_Model:
    """Walk through the entire HB-Model and convert HB-Objects as needed so that
    they all have a '.properties.ph' slot on them if they need it. This function 
    will also convert over all the LBT-Vertices to PH-Vertices so that things like 
    the ID-Number can be tracked.

    Arguments:
    ----------
        * _model (HB_Model): The Honeybee Model to oeprate on.

    Returns:
    --------
        * HB_Model: The Honeybee Model with properties and objects modified as needed.
    """

    new_rooms = []
    for room in _model.rooms:
        new_room = room.duplicate()
        new_faces = []
        for hb_face in new_room.faces:
            # -- convert face's construction
            hb_const = hb_face.properties.energy.construction
            if not hasattr(hb_const, 'properties'):
                ph_const = PH_OpaqueConstruction.from_hb_construction(hb_const)
                hb_face.properties.energy.construction = ph_const

            # -- convert face's geometry
            new_hb_face = hb_face.duplicate()
            new_hb_face._geometry = convert_Face3D(hb_face.geometry)

            new_apertures = []
            for aperture in hb_face.apertures:
                # -- convert aperture's construction
                hb_const = aperture.properties.energy.construction
                if not hasattr(hb_const, 'properties'):
                    ph_const = PH_WindowConstruction.from_hb_construction(hb_const)
                    aperture.properties.energy.construction = ph_const

                # -- convert aperture's geometry
                new_aperture = aperture.duplicate()
                new_aperture._geometry = convert_Face3D(aperture.geometry)
                new_apertures.append(new_aperture)

            new_hb_face._apertures = new_apertures
            new_faces.append(new_hb_face)

        new_room._faces = new_faces
        new_rooms.append(new_room)

    _model._rooms = new_rooms

    return _model
