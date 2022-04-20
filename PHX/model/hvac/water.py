# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from typing import Optional

from PHX.model.hvac.enums import DeviceType, PhxHotWaterInputOptions
from PHX.model.hvac import _base


class PhxHotWaterTankParams(_base.PhxMechanicalEquipmentParams):
    # -- Device Params
    quantity: Optional[int] = 0
    solar_losses: Optional[float] = 0.0  # W/K
    storage_loss_rate: Optional[float] = 0.0  # W
    standby_losses: Optional[float] = 0.0  # W/K

    input_option: PhxHotWaterInputOptions = PhxHotWaterInputOptions.SPEC_TOTAL_LOSSES
    storage_capacity: Optional[float] = 0.0  # Liter

    tank_room_temp: float = 20.0
    tank_water_temp: float = 55.0


class PhxHotWaterTank(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.WATER_STORAGE
        self.params: PhxHotWaterTankParams = PhxHotWaterTankParams()
