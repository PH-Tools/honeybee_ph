# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to convert a standard HBJSON Model over to WUFI Objects"""

from honeybee.model import Model as HB_Model
from honeybee.room import Room as HB_Room
from honeybee.face import Face as HB_Face
from honeybee.aperture import Aperture as HB_Aperture
from honeybee_energy.construction.opaque import OpaqueConstruction as HB_OpaqueConstruction
from honeybee_energy.construction.window import WindowConstruction as HB_WindowConstruction
from ladybug_geometry.geometry3d.face import Face3D

from honeybee_ph.model import ModelPhProperties
from honeybee_ph.room import RoomPhProperties
from honeybee_ph.face import FacePhProperties
from honeybee_ph.aperture import AperturePhProperties
from ladybug_geometry_ph.geometry3d_ph.pointvector import PHX_Vertix, Point3DPHProperties
from honeybee_energy_ph.construction.opaque import PHX_OpaqueConstruction, OpaqueConstructionPHProperties
from honeybee_energy_ph.construction.window import PHX_WindowConstruction, WindowConstructionPHProperties
from to_WUFI_XML.wufi import Project, Variant


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


def _add_PH_properties_to_obj(_lbt_obj):
    """Add a new '*.properties._PH' to certain LBT Objects, if it doesn't already exist.

    Arguments:
    ----------
        * _lbt_obj (Any LBT, HB or PHX Object):

    Returns:
    --------
        * The input object, with PH Properties added, if it is one of the allowed types.
    """

    if hasattr(_lbt_obj.properties, "PH"):
        return _lbt_obj

    if isinstance(_lbt_obj, HB_Model):
        _lbt_obj.properties._PH = ModelPhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_Room):
        _lbt_obj.properties._PH = RoomPhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_Face):
        _lbt_obj.properties._PH = FacePhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, PHX_Vertix):
        _lbt_obj.properties._PH = Point3DPHProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_Aperture):
        _lbt_obj.properties._PH = AperturePhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_OpaqueConstruction):
        _lbt_obj.properties._PH = OpaqueConstructionPHProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_WindowConstruction):
        _lbt_obj.properties._PH = WindowConstructionPHProperties(_lbt_obj)

    return _lbt_obj


def _add_PH_Properties_to_HB_Obj_vertices(_hb_obj: HB_Face | HB_Aperture) -> HB_Face | HB_Aperture:
    """Adds '*.properties._PH' to all the Face's Vertices. This requires swapping out the
        LBT Point3D vertices for new PHX_Point3D vertices which have a slot for .properties and
        room for ._PH on the properties.

    Arguments:
    ----------
        * _hb_obj (HB_Face | HB_Aperture): The HB Object to add the ._PH properties to the vertices of.

    Returns:
    --------
        * (HB_Face | HB_Aperture): The input HB Object, with ._PH properties slot added to its Vertices.
    """

    hb_obj = _hb_obj.duplicate()

    # -- Create a new PHX Vertix with a properties._PH for each LBT Vert in the Face Geometry
    # ------------------------------------------------------------------
    new_phx_vertices = [_add_PH_properties_to_obj(PHX_Vertix(v.x, v.y, v.z)) for v in hb_obj.vertices]

    # -- Re-set the boundary / vertices of the HB-Face._geometry (Face3D)
    # -- This is adapted from ladybug_geometry.geometry3D.face.Face3D.__copy__()
    # -- I don't love this. If Face3D __copy__ changes someday, it won't happen here. Grrr...
    _new_lbt_face3D = Face3D(tuple(new_phx_vertices), hb_obj.geometry.plane)
    hb_obj.geometry._transfer_properties(_new_lbt_face3D)
    _new_lbt_face3D._holes = hb_obj.geometry._holes
    _new_lbt_face3D._polygon2d = hb_obj.geometry._polygon2d
    _new_lbt_face3D._mesh2d = hb_obj.geometry._mesh2d
    _new_lbt_face3D._mesh3d = hb_obj.geometry._mesh3d

    # Re-Set the face geometry to the new Geom with the PHX Vertices
    hb_obj._geometry = _new_lbt_face3D

    return hb_obj


def add_PH_Properties(_hb_model: HB_Model) -> HB_Model:
    """Walks through the HB Model, adding '*.properties._PH' as needed to the HB Objects.

    If the user did not set PH Properties when building the LBT Model, this is needed
    so that all the LBT objects have a slot for PH-related data to be stored.

    Arguments:
    ----------
        * hb_model (HB_Model): The Honeybee Model to operate on.

    Returns:
    --------
        * (HB_Model): The input model, with all it's child objects adjusted to allow for .properties._PH.
    """

    _hb_model = _add_PH_properties_to_obj(_hb_model)

    for room in _hb_model.rooms:
        room = _add_PH_properties_to_obj(room)

        new_faces = []
        for hb_face in room.faces:
            # -- Convert the Face's Construction
            hb_const = hb_face.properties.energy.construction
            phx_const = PHX_OpaqueConstruction.from_hb_construction(hb_const)
            phx_const = _add_PH_properties_to_obj(phx_const)
            hb_face.properties.energy.construction = phx_const

            # -- Convert any Aperture Constructions
            for aperture in hb_face.apertures:
                hb_ap_const = aperture.properties.energy.construction
                phx_ap_const = PHX_WindowConstruction.from_hb_construction(hb_ap_const)
                phx_ap_const = _add_PH_properties_to_obj(phx_ap_const)
                aperture.properties.energy.construction = phx_ap_const

            # -- Convert the base Face Geometry
            face = _add_PH_Properties_to_HB_Obj_vertices(hb_face)
            face = _add_PH_properties_to_obj(face)

            # -- Convert over all the Face's Apertures
            new_apertures = []
            for aperture in face.apertures:
                aperture = _add_PH_Properties_to_HB_Obj_vertices(aperture)
                aperture = _add_PH_properties_to_obj(aperture)
                new_apertures.append(aperture)
            face._apertures = new_apertures

            new_faces.append(face)

        room._faces = tuple(new_faces)

    return _hb_model
