# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Water Devices"""

from __future__ import annotations
from dataclasses import dataclass, field

from PHX.model.hvac.enums import DeviceType, PhxHotWaterInputOptions
from PHX.model.hvac import _base


@dataclass
class PhxHotWaterDevice(_base.PhxMechanicalEquipment):
    def __post_init__(self):
        super().__post_init__()
        self.usage_profile.ventilation = True


# -- Hot Water Tank -----------------------------------------------------------


@dataclass
class PhxHotWaterTankParams(_base.PhxMechanicalEquipmentParams):
    # -- Device Params
    quantity: int = 0
    solar_losses: float = 0.0  # W/K
    storage_loss_rate: float = 0.0  # W
    standby_losses: float = 0.0  # W/K

    input_option: PhxHotWaterInputOptions = PhxHotWaterInputOptions.SPEC_TOTAL_LOSSES
    storage_capacity: float = 0.0  # Liter

    tank_room_temp: float = 20.0
    tank_water_temp: float = 55.0

    def __add__(self, other: PhxHotWaterTankParams) -> PhxHotWaterTankParams:
        base = super().__add__(other)
        new_obj = self.__class__(**vars(base))
        new_obj.quantity = self.quantity + other.quantity
        new_obj.solar_losses = (
            self.solar_losses + other.solar_losses) / 2
        new_obj.storage_loss_rate = (
            self.storage_loss_rate + other.storage_loss_rate) / 2
        new_obj.standby_losses = (
            self.standby_losses + other.standby_losses) / 2
        new_obj.input_option = self.input_option
        new_obj.storage_capacity = (
            self.storage_capacity + other.storage_capacity) / 2
        new_obj.tank_room_temp = (
            self.tank_room_temp + other.tank_room_temp) / 2
        new_obj.tank_water_temp = (
            self.tank_water_temp + other.tank_water_temp) / 2
        return new_obj


@dataclass
class PhxHotWaterTank(PhxHotWaterDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.WATER_STORAGE)
    params: PhxHotWaterTankParams = field(default_factory=PhxHotWaterTankParams)

    def __add__(self, other: PhxHotWaterTank) -> PhxHotWaterTank:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        return new_obj
