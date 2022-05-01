# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Mechanical Cooling Devices"""

from __future__ import annotations
from dataclasses import dataclass, field

from PHX.model.enums.hvac import CoolingType, DeviceType, HeatPumpType
from PHX.model.hvac import _base


@dataclass
class PhxCoolingDevice(_base.PhxMechanicalEquipment):
    def __post_init__(self):
        super().__post_init__()
        self.usage_profile.cooling = True


# -- Ventilation Air Cooling --------------------------------------------------


@dataclass
class PhxCoolingVentilationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.ANNUAL)
    single_speed: bool = False
    min_coil_temp: float = 12  # C
    capacity: float = 10  # kW
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingVentilationParams) -> PhxCoolingVentilationParams:
        base = super().__add__(other)
        new_obj = self.__class__(**vars(base))
        new_obj.hp_type = self.hp_type
        new_obj.single_speed = any([self.single_speed, other.single_speed])
        new_obj.min_coil_temp = (self.min_coil_temp + other.min_coil_temp) / 2
        new_obj.capacity = (self.capacity + other.capacity) / 2
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


@dataclass
class PhxCoolingVentilation(PhxCoolingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.HEAT_PUMP)
    cooling_type: CoolingType = field(init=False, default=CoolingType.VENTILATION)
    params: PhxCoolingVentilationParams = field(
        default_factory=PhxCoolingVentilationParams)

    def __add__(self, other: PhxCoolingVentilation) -> PhxCoolingVentilation:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj


# -- Recirculation Cooling ----------------------------------------------------


@dataclass
class PhxCoolingRecirculationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.ANNUAL)
    single_speed: bool = False
    min_coil_temp: float = 12  # C
    capacity: float = 10  # kW
    annual_COP: float = 4  # W/W
    flow_rate_m3_hr: float = 100
    flow_rate_variable: bool = True

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingRecirculationParams) -> PhxCoolingRecirculationParams:
        base = super().__add__(other)
        new_obj = self.__class__(**vars(base))
        new_obj.hp_type = self.hp_type
        new_obj.single_speed = any([self.single_speed, other.single_speed])
        new_obj.min_coil_temp = (self.min_coil_temp + other.min_coil_temp) / 2
        new_obj.flow_rate_m3_hr = (self.flow_rate_m3_hr + other.flow_rate_m3_hr) / 2
        new_obj.capacity = (self.capacity + other.capacity) / 2
        new_obj.flow_rate_variable = any(
            [self.flow_rate_variable, other.flow_rate_variable])
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


@dataclass
class PhxCoolingRecirculation(PhxCoolingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.HEAT_PUMP)
    cooling_type: CoolingType = field(init=False, default=CoolingType.RECIRCULATION)
    params: PhxCoolingRecirculationParams = field(
        default_factory=PhxCoolingRecirculationParams)

    def __add__(self, other: PhxCoolingRecirculation) -> PhxCoolingRecirculation:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        new_obj.cooling_type = self.cooling_type
        new_obj.device_type = self.device_type
        new_obj.params = self.params + other.params
        return new_obj


# -- Dehumidification ---------------------------------------------------------


@dataclass
class PhxCoolingDehumidificationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.ANNUAL)
    annual_COP: float = 4  # W/W
    useful_heat_loss: bool = False

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingDehumidificationParams) -> PhxCoolingDehumidificationParams:
        base = super().__add__(other)
        new_obj = self.__class__(**vars(base))
        new_obj.hp_type = self.hp_type
        new_obj.useful_heat_loss = any([self.useful_heat_loss, other.useful_heat_loss])
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


@dataclass
class PhxCoolingDehumidification(PhxCoolingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.HEAT_PUMP)
    cooling_type: CoolingType = field(init=False, default=CoolingType.DEHUMIDIFICATION)
    params: PhxCoolingDehumidificationParams = field(
        default_factory=PhxCoolingDehumidificationParams)

    def __add__(self, other: PhxCoolingDehumidification) -> PhxCoolingDehumidification:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj


# -- Panel Cooling ------------------------------------------------------------


@dataclass
class PhxCoolingPanelParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingPanelParams) -> PhxCoolingPanelParams:
        base = super().__add__(other)
        new_obj = self.__class__(**vars(base))
        new_obj.hp_type = self.hp_type
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


@dataclass
class PhxCoolingPanel(PhxCoolingDevice):
    device_type: DeviceType = DeviceType.HEAT_PUMP
    cooling_type: CoolingType = CoolingType.PANEL
    params: PhxCoolingPanelParams = field(
        default_factory=PhxCoolingPanelParams)

    def __add__(self, other: PhxCoolingPanel) -> PhxCoolingPanel:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj
