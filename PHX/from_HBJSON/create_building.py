# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create a new PhxBuilding from Honeybee-Rooms"""

from typing import List, Union

from honeybee import room, aperture, face

from PHX.model import building
from PHX.from_HBJSON import create_rooms, create_geometry
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceType, ComponentColor


def _hb_face_type_to_phx_enum(_hb_face: face.Face) -> ComponentFaceType:
    mapping = {
        "Wall": ComponentFaceType.OPAQUE,
        "RoofCeiling": ComponentFaceType.OPAQUE,
        "Floor": ComponentFaceType.OPAQUE,
        "AirBoundary": ComponentFaceType.AIRBOUNDARY,
    }
    return mapping[str(_hb_face.type)]


def _hb_ext_exposure_to_phx_enum(_hb_face: Union[face.Face, aperture.Aperture]) -> ComponentExposureExterior:
    mapping = {
        "Outdoors": ComponentExposureExterior.EXTERIOR,
        "Ground": ComponentExposureExterior.GROUND,
        "Surface": ComponentExposureExterior.SURFACE,
    }
    return mapping[str(_hb_face.boundary_condition)]


def _hb_int_color_to_phx_enum(_hb_face: face.Face) -> ComponentColor:
    mapping = {
        "Wall": {
            "Outdoors": ComponentColor.EXT_WALL_OUTER,
            "Surface": ComponentColor.INNER_WALL,
            "Ground": ComponentColor.SURFACE_GROUND_CONTACT,
        },
        "RoofCeiling": {
            "Outdoors": ComponentColor.SLOPED_ROOF_OUTER,
            "Surface": ComponentColor.CEILING,
            "Ground": ComponentColor.SURFACE_GROUND_CONTACT,
        },
        "Floor": {
            "Outdoors": ComponentColor.FLOOR,
            "Surface": ComponentColor.FLOOR,
            "Ground": ComponentColor.SURFACE_GROUND_CONTACT,
        },
    }
    return mapping[str(_hb_face.type)][str(_hb_face.boundary_condition)]


def _hb_ext_color_to_phx_enum(_hb_face: face.Face) -> ComponentColor:
    mapping = {
        "Wall": {
            "Outdoors": ComponentColor.EXT_WALL_OUTER,
            "Surface": ComponentColor.INNER_WALL,
            "Ground": ComponentColor.EXT_WALL_OUTER,
        },
        "RoofCeiling": {
            "Outdoors": ComponentColor.SLOPED_ROOF_INNER,
            "Surface": ComponentColor.CEILING,
            "Ground": ComponentColor.SURFACE_GROUND_CONTACT,
        },
        "Floor": {
            "Outdoors": ComponentColor.FLOOR,
            "Surface": ComponentColor.FLOOR,
            "Ground": ComponentColor.SURFACE_GROUND_CONTACT,
        },
    }
    return mapping[str(_hb_face.type)][str(_hb_face.boundary_condition)]


def create_component_from_hb_aperture(_aperture: aperture.Aperture, _hb_room: room.Room) -> building.PhxComponent:
    """Create a new Transparent (window) Component based on a Honeybee Aperture.

    Arguments:
    ----------
        * _aperture (aperture.Aperture): The Honeybee-Aperture to use as the source.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * building.Component: A new Transparent (window) Component.
    """
    new_compo = building.PhxComponent()

    new_compo.display_name = _aperture.display_name
    new_compo.id_num = building.PhxComponent._count

    new_compo.face_type = ComponentFaceType.TRANSPARENT
    new_compo.exposure_exterior = _hb_ext_exposure_to_phx_enum(_aperture)
    new_compo.exposure_interior = _hb_room.properties.ph.id_num
    new_compo.color_interior = ComponentColor.WINDOW
    new_compo.color_exterior = ComponentColor.WINDOW
    new_compo.window_type_id_num = _aperture.properties.energy.construction.properties.ph.id_num

    # -- Polygons
    phx_polygon = create_geometry.create_PhxPolygon_from_hb_aperture(_aperture)
    new_compo.add_polygons(phx_polygon)

    return new_compo


def create_components_from_hb_face(_hb_face: face.Face, _hb_room: room.Room) -> List[building.PhxComponent]:
    """Returns a new Opaque Component based on a Honeybee Face,

    Arguments:
    ----------
        * _hb_face (face.Face): The Honeybee-Face to use as the source.
        * _hb_room (room.Room)L The Honeybee-Room to use as the source.

    Returns:
    --------
        * building.Component: The new Opaque Component.
    """
    new_compos: List[building.PhxComponent] = []

    new_compo_opaque = building.PhxComponent()

    new_compo_opaque.display_name = _hb_face.display_name
    new_compo_opaque.id_num = building.PhxComponent._count
    new_compo_opaque.assembly_type_id_num = _hb_face.properties.energy.construction.properties.ph.id_num

    new_compo_opaque.face_type = _hb_face_type_to_phx_enum(_hb_face)
    new_compo_opaque.exposure_exterior = _hb_ext_exposure_to_phx_enum(_hb_face)
    new_compo_opaque.exposure_interior = _hb_room.properties.ph.id_num
    new_compo_opaque.color_interior = _hb_int_color_to_phx_enum(_hb_face)
    new_compo_opaque.color_exterior = _hb_ext_color_to_phx_enum(_hb_face)

    # -- Create Polygon
    phx_polygon = create_geometry.create_PhxPolygon_from_hb_face(_hb_face)
    new_compo_opaque.add_polygons(phx_polygon)

    new_compos.append(new_compo_opaque)

    # -- Create Children, register their Poly-Ids with the Parent
    for hb_aperture in _hb_face.apertures:
        phx_compo_aperture = create_component_from_hb_aperture(hb_aperture, _hb_room)
        phx_polygon.add_child_poly_id(phx_compo_aperture.polygon_ids)
        new_compos.append(phx_compo_aperture)

    return new_compos


def create_components_from_hb_room(_hb_room: room.Room) -> List[building.PhxComponent]:
    """Create new Opaque and Transparent PHX-Components based on Honeybee-Room Faces.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeybee-Room to use as the source.

    Returns:
    --------
        * list[building.Component]: A list of the new PHX-Components.
    """
    compos: List[building.PhxComponent] = []
    for hb_face in _hb_room:
        compos += create_components_from_hb_face(hb_face, _hb_room)

    return compos


def create_zones_from_hb_room(_hb_room: room.Room) -> building.PhxZone:
    """Create a new PHX-Zone based on a honeybee-Room.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeybee-Room to use as the source.

    Returns:
    --------
        * building.Zone: The new PHX-Zone object.
    """
    new_zone = building.PhxZone()

    new_zone.id_num = building.PhxZone._count
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

    # Set the zone's occupancy based on the merged HB room
    new_zone.res_occupant_quantity = _hb_room.properties.energy.people.properties.ph.number_people
    new_zone.res_number_bedrooms = _hb_room.properties.energy.people.properties.ph.number_bedrooms

    return new_zone
