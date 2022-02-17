# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to build PHX-Variant from Honeybee Rooms"""

from honeybee import room
from PHX import project, certification, ground
from from_HBJSON import create_building, create_geometry, create_hvac


def add_geometry_from_hb_rooms(_variant: project.Variant, _hb_room: room.Room) -> None:
    """Create geometry from a Honeybee-Room and add the geometry to the PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the Geometry to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source for the geometry.

    Returns:
    --------
        * None
    """

    for hb_face in _hb_room.faces:
        # Dev Note: To get the right IDs, have to generate the Children Polys first.
        for aperture in hb_face.apertures:
            _variant.graphics3D.add_polygons(
                create_geometry.create_PHX_Polyon_from_hb_aperture(aperture))

        _variant.graphics3D.add_polygons(
            create_geometry.create_PHX_Polyon_from_hb_face(hb_face))


def add_building_from_hb_room(_variant: project.Variant, _hb_room: room.Room, group_components: bool = False) -> None:
    """Create the  PHX-Building with all Components and Zones based on a Honeybee-Room.

    Arguments:
    ----------
        * _variaint (project.Variant): The PHX-Variant to add the building to.
        * _hb_room (room.Room): The honeybee-Room to use as the source.
        * group_components (bool): defauly=False. Set to true to have the converter
            group the components by assembly-type.

    Returns:
    --------
        * None
    """
    _variant.building.add_components(
        create_building.create_components_from_hb_room(_hb_room))
    _variant.building.add_zones(
        create_building.create_zones_from_hb_room(_hb_room))

    if group_components:
        _variant.building.group_components_by_assembly()


def add_phius_certification_from_hb_room(_variant: project.Variant, _hb_room: room.Room) -> None:
    """Copy PHX-Phius Certification from a Honeybee-Rooom over to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the PHX-Phius Certification to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    _variant.ph_data.ph_certificate_criteria = _hb_room.properties.ph.ph_bldg_segment.ph_certification.certification_criteria
    _variant.ph_data.ph_selection_target_data = _hb_room.properties.ph.ph_bldg_segment.ph_certification.localization_selection_type
    _variant.ph_data.annual_heating_demand = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_heating_demand
    _variant.ph_data.annual_cooling_demand = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_cooling_demand
    _variant.ph_data.peak_heating_load = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_heating_load
    _variant.ph_data.peak_cooling_load = _hb_room.properties.ph.ph_bldg_segment.ph_certification.PHIUS2021_cooling_load

    return None


def add_PH_Building_from_hb_room(_variant: project.Variant, _hb_room: room.Room) -> None:
    """Create and add a PHX PH-Building to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the PH-Building to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """
    ph_building = certification.PH_Building()

    ph_building.building_category = _hb_room.properties.ph.ph_bldg_segment.usage_type.number
    ph_building.occupancy_type = _hb_room.properties.ph.ph_bldg_segment.occupancy_type.number
    ph_building.building_status = _hb_room.properties.ph.ph_bldg_segment.ph_certification.building_status.number
    ph_building.building_type = _hb_room.properties.ph.ph_bldg_segment.ph_certification.building_type.number
    ph_building.num_of_units = _hb_room.properties.ph.ph_bldg_segment.num_dwelling_units
    ph_building.num_of_floors = _hb_room.properties.ph.ph_bldg_segment.num_floor_levels

    # TODO: Foundations. For now: set to None
    none_foundation = ground.Foundation()
    ph_building.foundations.append(none_foundation)

    # Not clear why this is a list in the WUFI file? When would there be more than one?
    _variant.ph_data.ph_buildings.append(ph_building)

    return None


def add_climate_from_hb_room(_variant: project.Variant, _hb_room: room.Room) -> None:
    """Copy PHX-Climate info from a Honeybee-Room over to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the climate data to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """
    ud_climate = _hb_room.properties.ph.ph_bldg_segment.climate

    # -- Basics
    _variant.climate.ph_climate_location.daily_temp_swing = ud_climate.summer_daily_temperature_swing
    _variant.climate.ph_climate_location.avg_wind_speed = ud_climate.average_wind_speed

    # -- Location
    _variant.climate.ph_climate_location.location.latitude = ud_climate.location.latitude
    _variant.climate.ph_climate_location.location.longitude = ud_climate.location.longitude
    _variant.climate.ph_climate_location.location.weather_station_elevation = ud_climate.location.weather_station_elevation
    _variant.climate.ph_climate_location.location.climate_zone = ud_climate.location.longitude
    _variant.climate.ph_climate_location.location.hours_from_UTC = ud_climate.location.hours_from_UTC

    # -- Ground
    _variant.climate.ph_climate_location.ground.ground_thermal_conductivity = ud_climate.ground.ground_thermal_conductivity
    _variant.climate.ph_climate_location.ground.ground_heat_capacitiy = ud_climate.ground.ground_heat_capacitiy
    _variant.climate.ph_climate_location.ground.ground_density = ud_climate.ground.ground_density
    _variant.climate.ph_climate_location.ground.depth_groundwater = ud_climate.ground.depth_groundwater
    _variant.climate.ph_climate_location.ground.flow_rate_groundwater = ud_climate.ground.flow_rate_groundwater

    # -- Monthly Values
    _variant.climate.ph_climate_location.monthly_temperature_air = ud_climate.monthly_temperature_air.values
    _variant.climate.ph_climate_location.monthly_temperature_dewpoint = ud_climate.monthly_temperature_dewpoint.values
    _variant.climate.ph_climate_location.monthly_temperature_sky = ud_climate.monthly_temperature_sky.values

    _variant.climate.ph_climate_location.monthly_radiation_north = ud_climate.monthly_radiation_north.values
    _variant.climate.ph_climate_location.monthly_radiation_east = ud_climate.monthly_radiation_east.values
    _variant.climate.ph_climate_location.monthly_radiation_south = ud_climate.monthly_radiation_south.values
    _variant.climate.ph_climate_location.monthly_radiation_west = ud_climate.monthly_radiation_west.values
    _variant.climate.ph_climate_location.monthly_radiation_global = ud_climate.monthly_radiation_global.values

    # -- Peak Load Values
    _variant.climate.ph_climate_location.peak_heating_1.temp = ud_climate.peak_heating_1.temp
    _variant.climate.ph_climate_location.peak_heating_1.rad_north = ud_climate.peak_heating_1.rad_north
    _variant.climate.ph_climate_location.peak_heating_1.rad_east = ud_climate.peak_heating_1.rad_east
    _variant.climate.ph_climate_location.peak_heating_1.rad_south = ud_climate.peak_heating_1.rad_south
    _variant.climate.ph_climate_location.peak_heating_1.rad_west = ud_climate.peak_heating_1.rad_west
    _variant.climate.ph_climate_location.peak_heating_1.rad_global = ud_climate.peak_heating_1.rad_global

    _variant.climate.ph_climate_location.peak_heating_2.temp = ud_climate.peak_heating_2.temp
    _variant.climate.ph_climate_location.peak_heating_2.rad_north = ud_climate.peak_heating_2.rad_north
    _variant.climate.ph_climate_location.peak_heating_2.rad_east = ud_climate.peak_heating_2.rad_east
    _variant.climate.ph_climate_location.peak_heating_2.rad_south = ud_climate.peak_heating_2.rad_south
    _variant.climate.ph_climate_location.peak_heating_2.rad_west = ud_climate.peak_heating_2.rad_west
    _variant.climate.ph_climate_location.peak_heating_2.rad_global = ud_climate.peak_heating_2.rad_global

    _variant.climate.ph_climate_location.peak_cooling_1.temp = ud_climate.peak_cooling_1.temp
    _variant.climate.ph_climate_location.peak_cooling_1.rad_north = ud_climate.peak_cooling_1.rad_north
    _variant.climate.ph_climate_location.peak_cooling_1.rad_east = ud_climate.peak_cooling_1.rad_east
    _variant.climate.ph_climate_location.peak_cooling_1.rad_south = ud_climate.peak_cooling_1.rad_south
    _variant.climate.ph_climate_location.peak_cooling_1.rad_west = ud_climate.peak_cooling_1.rad_west
    _variant.climate.ph_climate_location.peak_cooling_1.rad_global = ud_climate.peak_cooling_1.rad_global

    _variant.climate.ph_climate_location.peak_cooling_2.temp = ud_climate.peak_cooling_2.temp
    _variant.climate.ph_climate_location.peak_cooling_2.rad_north = ud_climate.peak_cooling_2.rad_north
    _variant.climate.ph_climate_location.peak_cooling_2.rad_east = ud_climate.peak_cooling_2.rad_east
    _variant.climate.ph_climate_location.peak_cooling_2.rad_south = ud_climate.peak_cooling_2.rad_south
    _variant.climate.ph_climate_location.peak_cooling_2.rad_west = ud_climate.peak_cooling_2.rad_west
    _variant.climate.ph_climate_location.peak_cooling_2.rad_global = ud_climate.peak_cooling_2.rad_global

    return None


def add_hvac_systems_from_hb_rooms(_variant: project.Variant, _hb_room: room.Room) -> None:
    """Add new HVAC (Ventilation, DHW, etc) Systems to the Variant based on the HB-Rooms.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the new hvac systems to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    for space in _hb_room.properties._ph.spaces:
        # -- Build the ventilator
        # -- Use the normal Ideal Air unique key, but remove the name so can group
        vent_key = str(space.host.properties.energy.hvac._IdealAirSystem__key()[1:])

        if _variant.mech_systems.equipment_in_collection(vent_key):
            # -- If the ventilator already exists, just use that one.
            space_ventilator = _variant.mech_systems.get_mech_equipment_by_key(vent_key)
        else:
            # -- otherwise, build a new PH-Ventilator from the HB-hvac
            space_ventilator = create_hvac.build_phx_ventilator(space)
            _variant.mech_systems.add_new_mech_equipment(vent_key, space_ventilator)

        # -- Set the space host-room's ventilator-ID-number to match the new ventilator
        space.host.properties.energy.hvac.properties.ph.ventilator_id_num = space_ventilator.id_num

    return None


def from_hb_room(_hb_room: room.Room, group_components: bool = False) -> project.Variant:
    """Create a new PHX-Variant based on a single PH/Honeybee Room.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeybee room to base the Variant on.
        * group_components (bool): default=False. Set to true to have the converter
            group the components by assembly-type.

    Returns:
    --------
        * A new Variant object.
    """

    new_variant = project.Variant()

    # -- Keep all the ID numbers aligned
    new_variant.id_num = project.Variant._count
    _hb_room.properties.ph.id_num = new_variant.id_num
    new_variant.name = _hb_room.display_name

    # -- Build the Variant Elements (order matters)
    add_hvac_systems_from_hb_rooms(new_variant, _hb_room)
    add_geometry_from_hb_rooms(new_variant, _hb_room)
    add_building_from_hb_room(new_variant, _hb_room, group_components)
    add_phius_certification_from_hb_room(new_variant, _hb_room)
    add_PH_Building_from_hb_room(new_variant, _hb_room)
    add_climate_from_hb_room(new_variant, _hb_room)

    return new_variant
