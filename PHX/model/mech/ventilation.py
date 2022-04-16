# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from typing import Optional

from PHX.model.mech.enums import DeviceType
from PHX.model.mech import _base


class PhxVentilatorParams(_base.PhxMechanicalEquipmentParams):
    sensible_heat_recovery: float = 0.0
    latent_heat_recovery: float = 0.0
    quantity: Optional[int] = 0
    electric_efficiency: float = 0.55
    frost_protection_reqd: bool = True
    temperature_below_defrost_used: float = -5.0


class PhxVentilator(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.VENTILATION
        self.usage_profile.ventilation = True
        self.params: PhxVentilatorParams = PhxVentilatorParams()
