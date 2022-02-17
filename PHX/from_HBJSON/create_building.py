# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to build PHX-Building from Honeybee Rooms"""
from typing import Any, Optional, List

from honeybee import room, aperture, face
from PHX.model import building
from PHX.from_HBJSON import create_rooms


def get_wufi_enum(_schema_nm: str, _key: str, _default: Any, _sub_schema: Optional[str] = None) -> int:
    """Convert Honeybe attribute values into corresponding WUFI integer enums.

    Arguments:
    ----------
        * _schema_nm (str): The primary schema-key to lookup
        * _key (str): The secondary key to look up in the designated schema-dict.
        * default (Any): The default value to return if no schema is found mathcing
            the key(s) input
        * _sub_schema (str | None): The secondary key to lookup within the designated
            schema.

    Returns:
    --------
        * int: The WUFI integer corresponding to the input key(s) or the default
            value is none found in the schema.
    """

    schemas = {
        'face_type': {  # <---- _schema_nm
            "Wall": 1,  # <---- _key
            "RoofCeiling": 1,
            "Floor": 1,
            "AirBoundary": 3,
        },
        'exposure_ext': {
            "Outdoors": -1,
            "Ground": -2,
            "Surface": -3,
        },
        'color_interior': {
            "Wall": {  # <------ _sub_schema
                "Outdoors": 1,
                "Surface": 3,
                "Ground": 1,
            },
            "RoofCeiling": {
                "Outdoors": 8,
                "Surface": 6,
                "Ground": 12,
            },
            "Floor": {
                "Outdoors": 5,
                "Surface": 5,
                "Ground": 12,
            },
        },
        'color_exterior': {
            "Wall": {
                "Outdoors": 2,
                "Surface": 3,
                "Ground": 12,
            },
            "RoofCeiling": {
                "Outdoors": 7,
                "Surface": 6,
                "Ground": 12,
            },
            "Floor": {
                "Outdoors": 5,
                "Surface": 5,
                "Ground": 12,
            },
        },
    }

    schema = schemas.get(_schema_nm, {})
    if _sub_schema:
        schema = schema.get(_sub_schema, {})

    return schema.get(_key, _default)


def create_component_from_aperture(_aperture: aperture.Aperture, _hb_room: room.Room) -> building.Component:
    """Create a new Transparent (window) Component based on a Honeybee Aperture.

    Arguments:
    ----------
        * _aperture (aperture.Aperture): The Honeybee-Aperture to use as the source.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * building.Component: A new Transparent (window) Component.
    """
    new_compo = building.Component()

    new_compo.name = _aperture.display_name
    new_compo.id_num = building.Component._count

    new_compo.type = 2  # Transparent

    new_compo.exposure_exterior = get_wufi_enum(
        "exposure_ext", str(_aperture.boundary_condition), 1)
    new_compo.exposure_interior = _hb_room.properties.ph.id_num
    new_compo.color_interior = 4  # Window
    new_compo.color_exterior = 4  # Window
    new_compo.window_type_id_num = _aperture.properties.energy.construction.properties.ph.id_num

    new_compo.polygon_ids = [_aperture.properties.ph.id_num]

    return new_compo


def create_component_from_opaque_face(_hb_face: face.Face, _hb_room: room.Room) -> building.Component:
    """Returns a new Opaque Component based on a Honeybee Face,

    Arguments:
    ----------
        * _hb_face (face.Face): The Honeybee-Face to use as the source.
        * _hb_room (room.Room)L The Honeybee-Room to use as the source.

    Returns:
    --------
        * building.Component: The new Opaque Component.
    """
    new_compo = building.Component()

    new_compo.name = _hb_face.display_name
    new_compo.id_num = building.Component._count
    new_compo.assembly_type_id_num = _hb_face.properties.energy.construction.properties.ph.id_num

    new_compo.type = get_wufi_enum("face_type", str(_hb_face.type), 1)
    new_compo.exposure_exterior = get_wufi_enum(
        "exposure_ext", str(_hb_face.boundary_condition), 1)
    new_compo.exposure_interior = _hb_room.properties.ph.id_num
    new_compo.color_interior = get_wufi_enum(
        "color_interior", str(_hb_face.boundary_condition), 1, str(_hb_face.type))
    new_compo.color_exterior = get_wufi_enum(
        "color_exterior", str(_hb_face.boundary_condition), 1, str(_hb_face.type))
    new_compo.polygon_ids = [_hb_face.properties.ph.id_num]

    return new_compo


def create_components_from_hb_room(_hb_room: room.Room) -> List[building.Component]:
    """Create new Opaque and Transparent PHX-Components based on Honeybee-Room Faces.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeybee-Room to use as the source.

    Returns:
    --------
        * list[building.Component]: A list of the new PHX-Components.
    """
    compos = []
    for hb_face in _hb_room:
        for aperture in hb_face.apertures:
            compos.append(create_component_from_aperture(aperture, _hb_room))

        compos.append(create_component_from_opaque_face(hb_face, _hb_room))

    return compos


def create_zones_from_hb_room(_hb_room: room.Room) -> building.Zone:
    """Create a new PHX-Zone based on a honeybee-Room.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeybee-Room to use as the source.

    Returns:
    --------
        * building.Zone: The new PHX-Zone object.
    """
    new_zone = building.Zone()

    new_zone.id_num = building.Zone._count
    new_zone.name = _hb_room.display_name

    # -- Sort the room order by full_name
    sorted_spaces = sorted(_hb_room.properties.ph.spaces, key=lambda x: x.full_name)

    # -- Create a new WUFI-RoomVentilation for each space
    new_zone.wufi_rooms = [create_rooms.create_room_from_space(sp)
                           for sp in sorted_spaces]

    # -- Set Zone properties
    new_zone.volume_gross = _hb_room.volume
    new_zone.weighted_net_floor_area = sum(
        (rm.weighted_floor_area for rm in new_zone.wufi_rooms))
    new_zone.volume_net = sum((rm.net_volume for rm in new_zone.wufi_rooms))

    return new_zone
