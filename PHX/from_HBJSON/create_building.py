# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create a new PhxBuilding from Honeybee-Rooms"""

from typing import List, Union, Dict

from honeybee import room, aperture, face

from PHX.model import building, constructions, components
from PHX.from_HBJSON import create_rooms, create_geometry
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceOpacity, ComponentColor, ComponentFaceType


def _hb_face_opacity_to_phx_enum(_hb_face: face.Face) -> ComponentFaceOpacity:
    mapping = {
        "Wall": ComponentFaceOpacity.OPAQUE,
        "RoofCeiling": ComponentFaceOpacity.OPAQUE,
        "Floor": ComponentFaceOpacity.OPAQUE,
        "AirBoundary": ComponentFaceOpacity.AIRBOUNDARY,
    }
    return mapping[str(_hb_face.type)]


def _hb_face_type_to_phx_enum(_hb_face:  face.Face) -> ComponentFaceType:
    mapping = {
        'Wall': ComponentFaceType.WALL,
        'Floor': ComponentFaceType.FLOOR,
        'RoofCeiling': ComponentFaceType.ROOF_CEILING,
        'AirBoundary': ComponentFaceType.AIR_BOUNDARY,
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


def create_component_from_hb_aperture(
        _host_compo: components.PhxComponentOpaque,
        _hb_aperture: aperture.Aperture,
        _hb_room: room.Room,
        _window_type_dict: Dict[str, constructions.PhxConstructionWindow]) -> building.PhxComponentAperture:
    """Create a new Transparent (window) Component based on a Honeybee Aperture.

    Arguments:
    ----------
        * _host (components.PhxComponentOpaque): The Aperture's parent opaque component.
        * _hb_aperture (aperture.Aperture): The Honeybee-Aperture to use as the source.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.
        * _window_type_dict (Dict[str, constructions.PhxConstructionWindow]): The Window Type dict.

    Returns:
    --------
        * componets.PhxComponentAperture: A new Transparent (window) Component.
    """
    phx_ap = building.PhxComponentAperture(_host=_host_compo)
    phx_ap.display_name = _hb_aperture.display_name
    phx_ap.exposure_interior = _hb_room.properties.ph.id_num
    phx_ap.window_type = _window_type_dict[_hb_aperture.properties.energy.construction.identifier]
    phx_ap.window_type_id_num = _hb_aperture.properties.energy.construction.properties.ph.id_num

    # -- Polygons
    phx_ap.add_polygons(
        create_geometry.create_PhxPolygon_from_hb_aperture(_hb_aperture))

    return phx_ap


def create_components_from_hb_face(_hb_face: face.Face,
                                   _hb_room: room.Room,
                                   _assembly_dict: Dict[str, constructions.PhxConstructionOpaque],
                                   _window_type_dict: Dict[str, constructions.PhxConstructionWindow]) -> components.PhxComponentOpaque:
    """Returns a new Opaque Component (and any child components) based on a Honeybee Face,

    Arguments:
    ----------
        * _hb_face (face.Face): The Honeybee-Face to use as the source.
        * _hb_room (room.Room)L The Honeybee-Room to use as the source.
        * _assembly_dict (Dict[str, constructions.PhxConstructionOpaque]): The Assembly Type dict.
        * _window_type_dict (Dict[str, constructions.PhxConstructionWindow]): The Window Type dict.

    Returns:
    --------
        * building.Component: The new Opaque Component.
    """

    opaque_compo = components.PhxComponentOpaque()
    opaque_compo.display_name = _hb_face.display_name
    opaque_compo.assembly = _assembly_dict[_hb_face.properties.energy.construction.identifier]
    opaque_compo.assembly_type_id_num = _hb_face.properties.energy.construction.properties.ph.id_num

    opaque_compo.face_type = _hb_face_type_to_phx_enum(_hb_face)
    opaque_compo.face_opacity = _hb_face_opacity_to_phx_enum(_hb_face)
    opaque_compo.exposure_exterior = _hb_ext_exposure_to_phx_enum(_hb_face)
    opaque_compo.exposure_interior = _hb_room.properties.ph.id_num
    opaque_compo.color_interior = _hb_int_color_to_phx_enum(_hb_face)
    opaque_compo.color_exterior = _hb_ext_color_to_phx_enum(_hb_face)

    # -- Create Polygon
    phx_polygon = create_geometry.create_PhxPolygon_from_hb_face(_hb_face)
    opaque_compo.add_polygons(phx_polygon)

    # -- Create Child Apertures, register the Aperature with the Parent Compo
    for hb_aperture in _hb_face.apertures:
        phx_compo_aperture = create_component_from_hb_aperture(
            opaque_compo, hb_aperture, _hb_room, _window_type_dict)
        phx_polygon.add_child_poly_id(phx_compo_aperture.polygon_ids)
        opaque_compo.add_aperture(phx_compo_aperture)

    return opaque_compo


def create_components_from_hb_room(_hb_room: room.Room,
                                   _assembly_dict: Dict[str, constructions.PhxConstructionOpaque],
                                   _window_type_dict: Dict[str, constructions.PhxConstructionWindow],
                                   ) -> List[components.PhxComponentOpaque]:
    """Create new Opaque and Transparent PHX-Components based on Honeybee-Room Faces.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeybee-Room to use as the source.
        * _assembly_dict (Dict[str, constructions.PhxConstructionOpaque]): The Assembly Type dict.
        * _assembly_dict (Dict[str, constructions.PhxConstructionWindow]): The Window Type dict.

    Returns:
    --------
        * list[components.PhxComponentOpaque]: A list of the new opaque PhxComponents.
    """
    return [
        create_components_from_hb_face(
            hb_face, _hb_room, _assembly_dict, _window_type_dict)
        for hb_face in _hb_room
    ]


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
    new_zone.display_name = _hb_room.display_name

    # -- Sort the room order by full_name
    sorted_spaces = sorted(_hb_room.properties.ph.spaces,
                           key=lambda x: x.full_name)

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
