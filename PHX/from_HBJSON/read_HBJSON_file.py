# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for importing / translating Honeybee Models into WUFI-JSON """

# -- Dev Note: Required to import all the base packages to run the __init__ startup routines
# -- which ensures that .ph properties slot is added to all HB Objects. This must be done before
# -- running read_hb_json to ensure there is a place for all the .ph properties to go.
# -- Dev Note: Do not remove --
import honeybee
import honeybee_ph
import honeybee_energy
import honeybee_energy_ph
import ladybug_geometry
import ladybug_geometry_ph
# -- Dev Note: Do not remove --

import json
import pathlib
from typing import Dict

from honeybee import model
from honeybee import face

# from honeybee_energy_ph.properties.construction.opaque import PH_OpaqueConstruction
# from honeybee_energy_ph.properties.construction.window import PH_WindowConstruction
from ladybug_geometry_ph.geometry3d_ph import pointvector


class HBJSONModelReadError(Exception):
    def __init__(self, _in):
        self.message = f"Error: Can only convert a Honeybee 'Model' to WUFI XML.\n"\
            "Got a Honeybee object of type: {_in}."

        super(HBJSONModelReadError, self).__init__(self.message)


def convert_face_3d(_lbt_geom: face.Face3D) -> face.Face3D:
    """Convert Ladybug face.Face3D vertices into PH-Vertices which have a .properties

    Arguments:
    ----------
        * _lbt_geometry (face.Face3D): A Labybug face.Face3D object to convert the vertices of.

    Returns:
    --------
        * face.Face3D: A new face.Face3D with all of it's vertices converted to PH-Style with a .properties.ph
    """

    # -- Create new PH Vertices from the HB-Vertices
    new_ph_vertices = [pointvector.PH_Point3D(v.x, v.y, v.z) for v in _lbt_geom.vertices]

    # -- Re-set the boundary / vertices of the HB-Face._geometry (face.Face3D)
    # -- This is adapted from ladybug_geometry.geometry3D.face.face.Face3D.__copy__()
    # -- I don't love this. If face.Face3D __copy__ changes someday, it won't happen here. Grrr...
    _new_lbt_face3D = face.Face3D(tuple(new_ph_vertices), _lbt_geom.plane)

    # -- Unlcear if we need these or how to update them?
    # _lbt_geom._transfer_properties(_new_lbt_face3D)
    # _new_lbt_face3D._holes = _lbt_geom._holes
    # _new_lbt_face3D._polygon2d = _lbt_geom._polygon2d
    # _new_lbt_face3D._mesh2d = _lbt_geom._mesh2d
    # _new_lbt_face3D._mesh3d = _lbt_geom._mesh3d

    return _new_lbt_face3D


def convert_model_LBT_geometry(_model: model.Model) -> model.Model:
    """Walk through the entire HB-Model and convert LBT geometry as needed so that
    they all have a '.properties.ph' slot on them if they need it. This function 
    will also convert over all the LBT-Vertices to PH-Vertices so that things like 
    the ID-Number can be tracked.

    Arguments:
    ----------
        * _model (model.Model): The Honeybee Model to operate on.

    Returns:
    --------
        * model.Model: The Honeybee Model with properties and objects modified as needed.
    """

    new_rooms = []
    for room in _model.rooms:
        new_room = room.duplicate()
        new_faces = []
        for hb_face in new_room.faces:
            # -- convert face's geometry
            new_hb_face = hb_face.duplicate()
            new_hb_face._geometry = convert_face_3d(hb_face.geometry)

            new_apertures = []
            for aperture in hb_face.apertures:
                # -- convert aperture's geometry
                new_aperture = aperture.duplicate()
                new_aperture._geometry = convert_face_3d(aperture.geometry)
                new_apertures.append(new_aperture)

            new_hb_face._apertures = new_apertures
            new_faces.append(new_hb_face)

        new_room._faces = new_faces
        new_rooms.append(new_room)

    _model._rooms = new_rooms

    # -- convert the orphaned-shades
    new_shades = []
    for shade in _model.orphaned_shades:
        new_shade = shade.duplicate()
        new_shade._geometry = convert_face_3d(new_shade.geometry)
        new_shades.append(new_shade)

    _model._orphaned_shades = new_shades

    return _model


def read_hb_json_from_file(_file_address: pathlib.Path) -> Dict:
    """Read in the HBJSON file and return it as a python dictionary.

    Arguments:
    ----------
        _file_address (pathlib.Path): A valid file path for the HBJSON file to read.

    Returns:
    --------
        Dict: The HBJSON dictionary, read in from the HBJSON file.
    """

    with open(_file_address) as json_file:
        data = json.load(json_file)

    if data.get('type', None) != 'Model':
        raise HBJSONModelReadError(data.get('type', None))
    else:
        return data


def convert_hbjson_dict_to_hb_model(_data: Dict) -> model.Model:
    """Convert an HBJSON python dictionary into an HB-Model, do some cleanup and PHX conversions.

    Arguments:
    ----------
        _data (Dict): An HBJSON dictionary with all the model information.

    Returns:
    --------
        model.Model: A Honeybee Model, rebuilt from the HBJSON file.
    """

    # -- Clean up the model, add the .ph properties
    new_hb_model = model.Model.from_dict(_data)
    new_hb_model = convert_model_LBT_geometry(new_hb_model)

    return new_hb_model
