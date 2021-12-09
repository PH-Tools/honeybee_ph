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
from ladybug_geometry_ph.geometry3d_ph.pointvector import PH_Point3D, Point3DPhProperties
from honeybee_energy_ph.construction.opaque import PH_OpaqueConstruction, OpaqueConstructionPhProperties
from honeybee_energy_ph.construction.window import PH_WindowConstruction, WindowConstructionPhProperties
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


def _add_PH_properties_to_obj(_lbt_obj):
    """Add a new '._ph' to LBT Object with a '.properties', if it doesn't already exist.

    Arguments:
    ----------
        * _lbt_obj (Any LBT, HB or PH Object):

    Returns:
    --------
        * The input object, with *.properties._ph added, if it is one of the supported types.
    """

    if not hasattr(_lbt_obj, 'properties'):
        raise MissingPropertiesError(_lbt_obj)

    if hasattr(_lbt_obj.properties, "ph"):
        return _lbt_obj

    if isinstance(_lbt_obj, HB_Model):
        _lbt_obj.properties._ph = ModelPhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_Room):
        _lbt_obj.properties._ph = RoomPhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_Face):
        _lbt_obj.properties._ph = FacePhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, PH_Point3D):
        _lbt_obj.properties._ph = Point3DPhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_Aperture):
        _lbt_obj.properties._ph = AperturePhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_OpaqueConstruction):
        _lbt_obj.properties._ph = OpaqueConstructionPhProperties(_lbt_obj)
    elif isinstance(_lbt_obj, HB_WindowConstruction):
        _lbt_obj.properties._ph = WindowConstructionPhProperties(_lbt_obj)

    return _lbt_obj


def _add_PH_Properties_to_HB_Obj_vertices(_hb_obj: HB_Face | HB_Aperture) -> HB_Face | HB_Aperture:
    """Adds '*.properties._PH' to all the Face's Vertices. This requires swapping out the
        LBT Point3D vertices for new ph_Point3D vertices which have a slot for .properties and
        room for ._ph on the properties.

    Arguments:
    ----------
        * _hb_obj (HB_Face | HB_Aperture): The HB Object to add the ._ph properties to the vertices of.

    Returns:
    --------
        * (HB_Face | HB_Aperture): The input HB Object, with ._ph properties slot added to its Vertices.
    """

    hb_obj = _hb_obj.duplicate()

    # -- Create a new PH Vertix with a properties._ph for each LBT Vert in the Face Geometry
    # ------------------------------------------------------------------
    new_ph_vertices = [_add_PH_properties_to_obj(
        PH_Point3D(v.x, v.y, v.z)) for v in hb_obj.vertices]

    # -- Re-set the boundary / vertices of the HB-Face._geometry (Face3D)
    # -- This is adapted from ladybug_geometry.geometry3D.face.Face3D.__copy__()
    # -- I don't love this. If Face3D __copy__ changes someday, it won't happen here. Grrr...
    _new_lbt_face3D = Face3D(tuple(new_ph_vertices), hb_obj.geometry.plane)
    hb_obj.geometry._transfer_properties(_new_lbt_face3D)
    _new_lbt_face3D._holes = hb_obj.geometry._holes
    _new_lbt_face3D._polygon2d = hb_obj.geometry._polygon2d
    _new_lbt_face3D._mesh2d = hb_obj.geometry._mesh2d
    _new_lbt_face3D._mesh3d = hb_obj.geometry._mesh3d

    # Re-Set the face geometry to the new Geom with the PH Vertices
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
        * (HB_Model): The input model, with all it's child objects adjusted to allow for .properties._ph.
    """

    _hb_model = _add_PH_properties_to_obj(_hb_model)

    for room in _hb_model.rooms:
        room = _add_PH_properties_to_obj(room)

        new_faces = []
        for hb_face in room.faces:
            # -- Convert the Face's Construction to PH_Construction
            hb_const = hb_face.properties.energy.construction
            ph_const = PH_OpaqueConstruction.from_hb_construction(hb_const)
            ph_const = _add_PH_properties_to_obj(ph_const)
            hb_face.properties.energy.construction = ph_const

            # -- Convert any Aperture Constructions
            for aperture in hb_face.apertures:
                hb_ap_const = aperture.properties.energy.construction
                ph_ap_const = PH_WindowConstruction.from_hb_construction(
                    hb_ap_const)
                ph_ap_const = _add_PH_properties_to_obj(ph_ap_const)
                aperture.properties.energy.construction = ph_ap_const

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
