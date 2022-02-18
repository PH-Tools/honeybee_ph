# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to create PHX-Service Hot Water objects from Honeybee-Energy SHW"""

from PHX.model import mech_equip
from honeybee_energy_ph.hvac import hot_water


def build_phx_hw_tank(_tank: hot_water.PhSHWTank) -> mech_equip.PhxHotWaterTank:
    tank = mech_equip.PhxHotWaterTank()

    tank.name = _tank.name
    tank.quantity = _tank.quantity

    tank.storage_capacity = _tank.volume
    tank.storage_loss_rate = _tank.heat_loss_rate
    tank.solar_losses = _tank.heat_loss_rate
    tank.standby_losses = _tank.heat_loss_rate

    tank.in_conditioned_space = _tank.in_conditioned_space
    tank.tank_room_temp = _tank.location_temp
    tank.tank_water_temp = _tank.water_temp

    return tank
