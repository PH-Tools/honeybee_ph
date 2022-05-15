# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to build PHX-Variant from Honeybee Rooms"""

from typing import Dict

from honeybee import room

from honeybee_ph import location
from honeybee_energy_ph.properties.load import equipment
from PHX.model import project, certification, ground, climate, constructions
from PHX.from_HBJSON import create_building, create_hvac, create_shw, create_elec_equip


def add_building_from_hb_room(_variant: project.PhxVariant,
                              _hb_room: room.Room,
                              _assembly_dict: Dict[str, constructions.PhxConstructionOpaque],
                              _window_type_dict: Dict[str, constructions.PhxConstructionWindow],
                              group_components: bool = False) -> None:
    """Create the  PHX-Building with all Components and Zones based on a Honeybee-Room.

    Arguments:
    ----------
        * _variaint (project.Variant): The PHX-Variant to add the building to.
        * _hb_room (room.Room): The honeybee-Room to use as the source.
        * _assembly_dict (Dict[str, constructions.PhxConstructionOpaque]): The Assembly Type dict.
        * _window_type_dict (Dict[str, constructions.PhxConstructionWindow]): The Window Type dict.
        * group_components (bool): default=False. Set to true to have the converter
            group the components by assembly-type.

    Returns:
    --------
        * None
    """
    _variant.building.add_components(
        create_building.create_components_from_hb_room(_hb_room, _assembly_dict, _window_type_dict))
    _variant.building.add_zones(
        create_building.create_zones_from_hb_room(_hb_room))

    if group_components:
        _variant.building.merge_opaque_components_by_assembly()
        _variant.building.merge_aperture_components_by_assembly()


def add_phius_certification_from_hb_room(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Copy PHX-Phius Certification from a Honeybee-Room over to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the PHX-Phius Certification to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    hbph_cert = _hb_room.properties.ph.ph_bldg_segment.ph_certification  # alias

    _variant.ph_certification.certification_criteria.ph_certificate_criteria = hbph_cert.certification_criteria
    _variant.ph_certification.certification_criteria.ph_selection_target_data = hbph_cert.localization_selection_type
    _variant.ph_certification.certification_criteria.annual_heating_demand = hbph_cert.PHIUS2021_heating_demand
    _variant.ph_certification.certification_criteria.annual_cooling_demand = hbph_cert.PHIUS2021_cooling_demand
    _variant.ph_certification.certification_criteria.peak_heating_load = hbph_cert.PHIUS2021_heating_load
    _variant.ph_certification.certification_criteria.peak_cooling_load = hbph_cert.PHIUS2021_cooling_load

    return None


def add_PH_Building_from_hb_room(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Create and add a PHX PH-Building to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the PH-Building to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """
    ph_building = certification.PhxPHBuilding()

    ph_building.building_category = _hb_room.properties.ph.ph_bldg_segment.usage_type.number
    ph_building.occupancy_type = _hb_room.properties.ph.ph_bldg_segment.occupancy_type.number
    ph_building.building_status = _hb_room.properties.ph.ph_bldg_segment.ph_certification.building_status.number
    ph_building.building_type = _hb_room.properties.ph.ph_bldg_segment.ph_certification.building_type.number
    ph_building.num_of_units = _hb_room.properties.ph.ph_bldg_segment.num_dwelling_units
    ph_building.num_of_floors = _hb_room.properties.ph.ph_bldg_segment.num_floor_levels

    # TODO: Foundations. For now: set to None
    ph_building.add_foundation(ground.PhxFoundation())

    # Set the airtightness for Building
    ph_building.airtightness_q50 = _hb_room.properties.energy.infiltration.flow_per_exterior_area * 3600

    # Not clear why this is a list in the WUFI file? When would there be more than one?
    _variant.ph_certification.add_ph_building(ph_building)

    return None


def add_climate_from_hb_room(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Copy PHX-Climate info from a Honeybee-Room over to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the climate data to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    ud_climate: location.Climate = _hb_room.properties.ph.ph_bldg_segment.climate

    # -- Basics
    _variant.location.climate.daily_temp_swing = ud_climate.summer_daily_temperature_swing
    _variant.location.climate.avg_wind_speed = ud_climate.average_wind_speed

    # -- Location
    _variant.location.site.latitude = ud_climate.location.latitude
    _variant.location.site.longitude = ud_climate.location.longitude
    _variant.location.site.elevation = ud_climate.location.weather_station_elevation
    _variant.location.site.climate_zone = ud_climate.location.climate_zone
    _variant.location.site.hours_from_UTC = ud_climate.location.hours_from_UTC

    # -- Ground
    _variant.location.ground.ground_thermal_conductivity = ud_climate.ground.ground_thermal_conductivity
    _variant.location.ground.ground_heat_capacity = ud_climate.ground.ground_heat_capacity
    _variant.location.ground.ground_density = ud_climate.ground.ground_density
    _variant.location.ground.depth_groundwater = ud_climate.ground.depth_groundwater
    _variant.location.ground.flow_rate_groundwater = ud_climate.ground.flow_rate_groundwater

    # -- Monthly Values
    _variant.location.climate.monthly_temperature_air = ud_climate.monthly_temperature_air.values
    _variant.location.climate.monthly_temperature_dewpoint = ud_climate.monthly_temperature_dewpoint.values
    _variant.location.climate.monthly_temperature_sky = ud_climate.monthly_temperature_sky.values

    _variant.location.climate.monthly_radiation_north = ud_climate.monthly_radiation_north.values
    _variant.location.climate.monthly_radiation_east = ud_climate.monthly_radiation_east.values
    _variant.location.climate.monthly_radiation_south = ud_climate.monthly_radiation_south.values
    _variant.location.climate.monthly_radiation_west = ud_climate.monthly_radiation_west.values
    _variant.location.climate.monthly_radiation_global = ud_climate.monthly_radiation_global.values

    # -- Peak Load Values
    _variant.location.climate.peak_heating_1.temp = ud_climate.peak_heating_1.temp
    _variant.location.climate.peak_heating_1.rad_north = ud_climate.peak_heating_1.rad_north
    _variant.location.climate.peak_heating_1.rad_east = ud_climate.peak_heating_1.rad_east
    _variant.location.climate.peak_heating_1.rad_south = ud_climate.peak_heating_1.rad_south
    _variant.location.climate.peak_heating_1.rad_west = ud_climate.peak_heating_1.rad_west
    _variant.location.climate.peak_heating_1.rad_global = ud_climate.peak_heating_1.rad_global

    _variant.location.climate.peak_heating_2.temp = ud_climate.peak_heating_2.temp
    _variant.location.climate.peak_heating_2.rad_north = ud_climate.peak_heating_2.rad_north
    _variant.location.climate.peak_heating_2.rad_east = ud_climate.peak_heating_2.rad_east
    _variant.location.climate.peak_heating_2.rad_south = ud_climate.peak_heating_2.rad_south
    _variant.location.climate.peak_heating_2.rad_west = ud_climate.peak_heating_2.rad_west
    _variant.location.climate.peak_heating_2.rad_global = ud_climate.peak_heating_2.rad_global

    _variant.location.climate.peak_cooling_1.temp = ud_climate.peak_cooling_1.temp
    _variant.location.climate.peak_cooling_1.rad_north = ud_climate.peak_cooling_1.rad_north
    _variant.location.climate.peak_cooling_1.rad_east = ud_climate.peak_cooling_1.rad_east
    _variant.location.climate.peak_cooling_1.rad_south = ud_climate.peak_cooling_1.rad_south
    _variant.location.climate.peak_cooling_1.rad_west = ud_climate.peak_cooling_1.rad_west
    _variant.location.climate.peak_cooling_1.rad_global = ud_climate.peak_cooling_1.rad_global

    _variant.location.climate.peak_cooling_2.temp = ud_climate.peak_cooling_2.temp
    _variant.location.climate.peak_cooling_2.rad_north = ud_climate.peak_cooling_2.rad_north
    _variant.location.climate.peak_cooling_2.rad_east = ud_climate.peak_cooling_2.rad_east
    _variant.location.climate.peak_cooling_2.rad_south = ud_climate.peak_cooling_2.rad_south
    _variant.location.climate.peak_cooling_2.rad_west = ud_climate.peak_cooling_2.rad_west
    _variant.location.climate.peak_cooling_2.rad_global = ud_climate.peak_cooling_2.rad_global

    return None


def add_local_pe_conversion_factors(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Copy local Site->Source conversion factors from a Honeybee-Room over to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the factor data to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """
    for factor in _hb_room.properties.ph.ph_bldg_segment.source_energy_factors:
        new_phx_factor = climate.PhxPEFactor()
        new_phx_factor.fuel_name = factor.fuel_name
        new_phx_factor.value = factor.value
        new_phx_factor.unit = factor.unit
        _variant.location.energy_factors.pe_factors[new_phx_factor.fuel_name] = new_phx_factor
    return


def add_local_co2_conversion_factors(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Copy local Site->CO2e conversion factors from a Honeybee-Room over to a PHX-Variant.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the factor data to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    for factor in _hb_room.properties.ph.ph_bldg_segment.co2e_factors:
        new_phx_factor = climate.PhxCO2Factor()
        new_phx_factor.fuel_name = factor.fuel_name
        new_phx_factor.value = factor.value
        new_phx_factor.unit = factor.unit
        _variant.location.energy_factors.co2_factors[new_phx_factor.fuel_name] = new_phx_factor
    return


def add_ventilation_systems_from_hb_rooms(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Add new HVAC (Ventilation, etc) Systems to the Variant based on the HB-Rooms.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the new hvac systems to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    for space in _hb_room.properties._ph.spaces:
        # -- Get the HBE-PH Ventilation system from the space's host room
        # -- Note: in the case of a merged room, the space host may not be the same
        # -- as _hb_room, so always refer back to the space.host to be sure.
        vent_sys = space.host.properties.energy.hvac.properties.ph.ventilation_system

        if not vent_sys:
            continue

        # -- Get or Build the PHX Ventilation system
        # -- If the ventilator already exists, just use that one.
        phx_subsystem = _variant.mech_systems.get_mech_subsystem_by_key(
            vent_sys.key)
        if not phx_subsystem:
            # -- otherwise, build a new PH-Ventilator from the HB-hvac
            phx_subsystem = create_hvac.build_phx_ventilation_sys(vent_sys)
            _variant.mech_systems.add_new_mech_subsystem(
                vent_sys.key, phx_subsystem)

        vent_sys.id_num = phx_subsystem.id_num

    return None


def add_heating_systems_from_hb_rooms(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Add a new PHX-Heating SubSystem to the Variant based on the HB-Rooms.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the new hvac systems to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    for space in _hb_room.properties._ph.spaces:
        # -- Get the HBE-PH Heating Systems from the space's host room
        # -- Note: in the case of a merged room, the space host may not be the same
        # -- as _hb_room, so always refer back to the space.host to be sure.
        heating_systems = space.host.properties.energy.hvac.properties.ph.heating_systems

        # -- Get or Build the PHX Heating systems
        # -- If the system already exists, just use that one.
        for hbph_sys in heating_systems:
            phx_subsystem = _variant.mech_systems.get_mech_subsystem_by_key(
                hbph_sys.key)
            if not phx_subsystem:
                # -- otherwise, build a new PHX-Heating-Sys from the HB-hvac
                phx_subsystem = create_hvac.build_phx_heating_sys(hbph_sys)
                _variant.mech_systems.add_new_mech_subsystem(
                    hbph_sys.key, phx_subsystem)

            hbph_sys.id_num = phx_subsystem.id_num

    return None


def add_cooling_systems_from_hb_rooms(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Add new PHX-Cooling SubSystem to the Variant based on the HB-Rooms.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX-Variant to add the new hvac systems to.
        * _hb_room (room.Room): The Honeybee-Room to use as the source.

    Returns:
    --------
        * None
    """

    for space in _hb_room.properties._ph.spaces:
        # -- Get the HBPH-Cooling-Systems from the space's host room
        # -- Note: in the case of a merged room, the space host may not be the same
        # -- as _hb_room, so always refer back to the space.host to be sure.
        cooling_systems = space.host.properties.energy.hvac.properties.ph.cooling_systems

        # -- Get or Build the PHX-Cooling systems
        # -- If the system already exists, just use that one.
        for hbph_sys in cooling_systems:
            phx_subsystem = _variant.mech_systems.get_mech_subsystem_by_key(
                hbph_sys.key)
            if not phx_subsystem:
                # -- otherwise, build a new PHX-Cooling-Sys from the HB-hvac
                phx_subsystem = create_hvac.build_phx_cooling_sys(hbph_sys)
                _variant.mech_systems.add_new_mech_subsystem(
                    hbph_sys.key, phx_subsystem)

            hbph_sys.id_num = phx_subsystem.id_num

    return None


def add_dhw_storage_from_hb_rooms(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Add new Service Hot Water Equipment to the Variant based on the HB-Rooms.

    Arguments:
    ----------
        * _variant (project.Variant): The PHX Variant to add the PHX DHW System to.
        * _hb_room (room.Room): The Honeybee room to get the DHW System data from.

    Returns:
    --------
        * None
    """

    for space in _hb_room.properties._ph.spaces:
        # -- Guard Clause
        if not space.host.properties.energy.shw:
            continue

        if not space.host.properties.energy.service_hot_water:
            continue

        # -- Build the HW-Tank
        for hw_tank in space.host.properties.energy.shw.properties.ph.tanks:
            if not hw_tank:
                continue

            equip_key = str(id(hw_tank))
            if _variant.mech_systems.subsystem_in_collection(equip_key):
                continue

            # -- Build a new PHS-HW-Tank from the HB-hvac
            phx_subsystem = create_shw.build_phx_hw_storage_subsystem(hw_tank)
            _variant.mech_systems.add_new_mech_subsystem(
                equip_key, phx_subsystem)

    return None


def add_dhw_heaters_from_hb_rooms(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    for space in _hb_room.properties.ph.spaces:
        """TODO: Two options:
            1) Its a Honeybee-SHW System only with 'efficiency', 'condition' and 'loss' data
            2) Its a detailed HB-PH-SHW System with full PH-Style data
        """

        if not space.host.properties.energy.shw:
            continue

        for heater in space.host.properties.energy.shw.properties.ph.heaters:
            equip_key = str(id(heater))

            if _variant.mech_systems.subsystem_in_collection(equip_key):
                continue

            # -- Build a new PHX-HW-Heater from the HBPH-HW-Heater
            phx_subsystem = create_shw.build_phx_hw_heating_subsystem(heater)
            _variant.mech_systems.add_new_mech_subsystem(
                equip_key, phx_subsystem)

    return None


def add_elec_equip_from_hb_room(_variant: project.PhxVariant, _hb_room: room.Room) -> None:
    """Creates new PHX-Elec-Equipment (Appliances) and adds them to each of the Variant.building.zones

    Arguments:
    ----------
        * _variant (project.Variant): The Variant to add the new elec-equipment to.
        # _hb_room (room.Room): The Honeybee Room to get the elec-equipment from.

    Returns:
    --------
        * None
    """

    ee_properties_ph: equipment.ElectricEquipmentPhProperties = _hb_room.properties.energy.electric_equipment.properties.ph
    for equip_key, device in ee_properties_ph.equipment_collection.items():
        phx_elec_device = create_elec_equip.build_phx_elec_device(device)
        for zone in _variant.building.zones:
            zone.elec_equipment_collection.add_new_device(
                equip_key, phx_elec_device)

    return


def from_hb_room(_hb_room: room.Room,
                 _assembly_dict: Dict[str, constructions.PhxConstructionOpaque],
                 _window_type_dict: Dict[str, constructions.PhxConstructionWindow],
                 group_components: bool = False) -> project.PhxVariant:
    """Create a new PHX-Variant based on a single PH/Honeybee Room.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeybee room to base the Variant on.
        * _assembly_dict (Dict[str, constructions.PhxConstructionOpaque]): The Assembly Type dict.
        * _window_type_dict (Dict[str, constructions.PhxConstructionWindow]): The Window Type dict.
        * group_components (bool): default=False. Set to true to have the converter
            group the components by assembly-type.

    Returns:
    --------
        * A new Variant object.
    """

    new_variant = project.PhxVariant()

    # -- Keep all the ID numbers aligned
    new_variant.id_num = project.PhxVariant._count
    _hb_room.properties.ph.id_num = new_variant.id_num
    new_variant.name = _hb_room.display_name

    # -- Build the Variant Elements (Dev. note: order matters!)
    add_ventilation_systems_from_hb_rooms(new_variant, _hb_room)
    add_heating_systems_from_hb_rooms(new_variant, _hb_room)
    add_cooling_systems_from_hb_rooms(new_variant, _hb_room)
    add_dhw_heaters_from_hb_rooms(new_variant, _hb_room)
    add_dhw_storage_from_hb_rooms(new_variant, _hb_room)
    add_building_from_hb_room(new_variant, _hb_room, _assembly_dict,
                              _window_type_dict, group_components)
    add_phius_certification_from_hb_room(new_variant, _hb_room)
    add_PH_Building_from_hb_room(new_variant, _hb_room)
    add_climate_from_hb_room(new_variant, _hb_room)
    add_local_pe_conversion_factors(new_variant, _hb_room)
    add_local_co2_conversion_factors(new_variant, _hb_room)
    add_elec_equip_from_hb_room(new_variant, _hb_room)

    return new_variant
