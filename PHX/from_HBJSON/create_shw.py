# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create PHX-Service Hot Water objects from Honeybee-Energy SHW"""

from PHX.model import mech_equip
from honeybee_energy_ph.hvac import hot_water


def build_phx_hw_tank(_tank: hot_water.PhSHWTank) -> mech_equip.PhxHotWaterTank:
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


def build_phx_hw_heater() -> mech_equip.PhxHotWaterHeater:
    phx_hw_heater = mech_equip.PhxHotWaterHeater()

    return phx_hw_heater
