# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Mechanical Ventilation Devices"""

from __future__ import annotations
from dataclasses import dataclass, field

from PHX.model.hvac.enums import DeviceType
from PHX.model.hvac import _base


@dataclass
class PhxDeviceVentilation(_base.PhxMechanicalEquipment):
    def __post_init__(self):
        super().__post_init__()
        self.usage_profile.ventilation = True


# -- HRV / ERV Air Cooling --------------------------------------------------


@dataclass
class PhxDeviceVentilatorParams(_base.PhxMechanicalEquipmentParams):
    sensible_heat_recovery: float = 0.0
    latent_heat_recovery: float = 0.0
    quantity: int = 1
    electric_efficiency: float = 0.55
    frost_protection_reqd: bool = True
    temperature_below_defrost_used: float = -5.0

    def __add__(self, other: PhxDeviceVentilatorParams) -> PhxDeviceVentilatorParams:
        base = super().__add__(other)
        new_obj = self.__class__(**vars(base))
        new_obj.sensible_heat_recovery = (
            self.sensible_heat_recovery + other.sensible_heat_recovery) / 2
        new_obj.latent_heat_recovery = (
            self.latent_heat_recovery + other.latent_heat_recovery) / 2
        new_obj.quantity = self.quantity + other.quantity
        new_obj.electric_efficiency = (
            self.electric_efficiency + other.electric_efficiency) / 2
        new_obj.frost_protection_reqd = any(
            [self.frost_protection_reqd, other.frost_protection_reqd])
        new_obj.temperature_below_defrost_used = (
            self.temperature_below_defrost_used + other.temperature_below_defrost_used) / 2
        return new_obj


@dataclass
class PhxDeviceVentilator(PhxDeviceVentilation):
    device_type: DeviceType = field(init=False, default=DeviceType.VENTILATION)
    params: PhxDeviceVentilatorParams = field(
        default_factory=PhxDeviceVentilatorParams)

    def __add__(self, other: PhxDeviceVentilator) -> PhxDeviceVentilator:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        return new_obj
