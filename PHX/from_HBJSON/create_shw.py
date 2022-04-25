# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create PHX-Service Hot Water objects from Honeybee-Energy-PH SHW"""

from PHX.model import hvac
from honeybee_energy_ph.hvac import hot_water


def build_phx_hw_tank(_hbph_tank: hot_water.PhSHWTank) -> hvac.PhxHotWaterTank:
    """Returns a new PHX Hot-Water Tank based on the HBPH Hot Water Tank input.

    Arguments:
    ----------
        * _hbph_heater (hot_water.PhSHWTank): The HBPH Hot-Water tank
            to use as the source.

    Returns:
    --------
        * mech_equip.PhxHotWaterTank: The new PHX-Hot-Water-Tank.
    """

    phx_tank = hvac.PhxHotWaterTank()

    phx_tank.display_name = _hbph_tank.name
    phx_tank.params.quantity = _hbph_tank.quantity

    phx_tank.params.storage_capacity = _hbph_tank.volume
    phx_tank.params.storage_loss_rate = _hbph_tank.heat_loss_rate
    phx_tank.params.solar_losses = _hbph_tank.heat_loss_rate
    phx_tank.params.standby_losses = _hbph_tank.heat_loss_rate

    phx_tank.params.in_conditioned_space = _hbph_tank.in_conditioned_space
    phx_tank.params.tank_room_temp = _hbph_tank.location_temp
    phx_tank.params.tank_water_temp = _hbph_tank.water_temp

    return phx_tank


def build_phx_hw_storage_subsystem(_hbph_tank: hot_water.PhSHWTank) -> hvac.PhxMechanicalSubSystem:
    """

    Arguments:
    ----------
        * _hbph_heater (hot_water.PhSHWTank): The HBPH Hot-Water tank
            to use as the source.

    Returns:
    --------
        * (mech.PhxMechanicalSubSystem): The new Water Storage SubSystem.
    """

    phx_strg_subsystem = hvac.PhxMechanicalSubSystem()
    phx_strg_subsystem.device = build_phx_hw_tank(_hbph_tank)

    # TODO: Distribution...

    return phx_strg_subsystem


def build_phx_hw_heater(_hbph_heater: hot_water.PhSHWHeaterElectric) -> hvac.PhxHeatingDevice:
    """Returns a new PHX Hot-Water Heater based on the HBPH Hot Water Heater input.

    Arguments:
    ----------
        * _hbph_heater (hot_water.PhSHWHeaterElectric): The HBPH Hot-Water heater
            to use as the source for the PHX Heater.

    Returns:
    --------
        * mech_equip.PhxHotWaterHeater: The new PHX-Hot-Water-Heater.
    """

    # -- Get the right constructor based on the type of heater
    heaters = {
        'PhSHWHeaterElectric': hvac.PhxHeaterElectric,
        'PhSHWHeaterBoiler': hvac.PhxHeaterBoilerFossil,
        'PhSHWHeaterBoilerWood': hvac.PhxHeaterBoilerWood,
        'PhSHWHeaterDistrict': hvac.PhxHeaterDistrictHeat,
        'PhSHWHeaterHeatPump': hvac.PhxHeaterHeatPumpHotWater,
    }

    # -- Build the basic heater and set basic data
    heater_class = heaters[_hbph_heater.__class__.__name__]
    phx_hw_heater = heater_class()
    phx_hw_heater.display_name = _hbph_heater.display_name

    # -- Pull out all the detailed data which varies depending on the 'type'
    for attr_name in vars(phx_hw_heater).keys():
        try:
            if attr_name.startswith('_'):
                attr_name = attr_name[1:]
            setattr(phx_hw_heater, attr_name, getattr(_hbph_heater, attr_name))
        except AttributeError:
            pass

    for attr_name in vars(phx_hw_heater.params).keys():
        try:
            if attr_name.startswith('_'):
                attr_name = attr_name[1:]
            setattr(phx_hw_heater.params, attr_name, getattr(_hbph_heater, attr_name))
        except AttributeError:
            pass

    phx_hw_heater.usage_profile.dhw_heating = True

    return phx_hw_heater


def build_phx_hw_heating_subsystem(_hbph_heater: hot_water.PhSHWHeaterElectric) -> hvac.PhxMechanicalSubSystem:
    """

    Arguments:
    ----------
        * _hbph_heater (hot_water.PhSHWHeaterElectric): The HBPH Hot-Water heater
            to use as the source for the PHX Heater.

    Returns:
    --------
        * (mech.PhxMechanicalSubSystem): The new Water-Heating SubSystem.
    """

    phx_strg_subsystem = hvac.PhxMechanicalSubSystem()
    phx_strg_subsystem.device = build_phx_hw_heater(_hbph_heater)

    # TODO: Distribution...

    return phx_strg_subsystem
