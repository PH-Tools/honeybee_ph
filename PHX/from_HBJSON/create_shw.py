# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create PHX-Service Hot Water objects from Honeybee-Energy-PH SHW"""

from PHX.model import mech_equip
from honeybee_energy_ph.hvac import hot_water


def build_phx_hw_tank(_tank: hot_water.PhSHWTank) -> mech_equip.PhxHotWaterTank:
    """Returns a new PHX Hot-Water Tank based on the HBPH Hot Water Tank input.

    Arguments:
    ----------
        * _hbph_heater (hot_water.PhSHWTank): The HBPH Hot-Water tank
            to use as the source.

    Returns:
    --------
        * mech_equip.PhxHotWaterTank: The new PHX-Hot-Water-Tank.
    """

    phx_tank = mech_equip.PhxHotWaterTank()

    phx_tank.name = _tank.name
    phx_tank.quantity = _tank.quantity

    phx_tank.storage_capacity = _tank.volume
    phx_tank.storage_loss_rate = _tank.heat_loss_rate
    phx_tank.solar_losses = _tank.heat_loss_rate
    phx_tank.standby_losses = _tank.heat_loss_rate

    phx_tank.in_conditioned_space = _tank.in_conditioned_space
    phx_tank.tank_room_temp = _tank.location_temp
    phx_tank.tank_water_temp = _tank.water_temp

    return phx_tank


def build_phx_hw_heater(_hbph_heater: hot_water.PhSHWHeaterElectric) -> mech_equip.PhxHotWaterHeater:
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
        'PhSHWHeaterElectric': mech_equip.PhxHotWaterHeaterElectric,
        'PhSHWHeaterBoiler': mech_equip.PhxHotWaterHeaterBoilerGas,
        'PhSHWHeaterBoilerWood': mech_equip.PhxHotWaterHeaterBoilerWood,
        'PhSHWHeaterDistrict': mech_equip.PhxHotWaterHeaterDistrictHeat,
        'PhSHWHeaterHeatPump': mech_equip.PhxHotWaterHeaterHeatPump,
    }

    # -- Build the basic heater and set basic data
    heater_class = heaters[_hbph_heater.__class__.__name__]
    phx_hw_heater = heater_class()

    phx_hw_heater.name = _hbph_heater.display_name
    phx_hw_heater.percent_coverage = _hbph_heater.percent_coverage
    phx_hw_heater.in_conditioned_space = _hbph_heater.in_conditioned_space

    # -- Pull out all the detailed data which varies depending on the 'type'
    for attr_name in vars(_hbph_heater).keys():
        try:
            if attr_name.startswith('_'):
                attr_name = attr_name[1:]
            setattr(phx_hw_heater, attr_name, getattr(_hbph_heater, attr_name))
        except KeyError:
            pass
    return phx_hw_heater
