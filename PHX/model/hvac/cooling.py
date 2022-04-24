# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Cooling Equipment Classes"""

from __future__ import annotations
from dataclasses import dataclass, field

from PHX.model.hvac.enums import CoolingType, DeviceType, HeatPumpType
from PHX.model.hvac import _base

@dataclass
class PhxCoolingDevice(_base.PhxMechanicalEquipment):
    def __post_init__(self):
        super().__post_init__()
        self.usage_profile.cooling = True

# -- Ventilation Air Cooling --------------------------------------------------

@dataclass
class PhxCoolingVentilationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    single_speed: bool = False
    min_coil_temp: float = 12  # C
    capacity: float = 10  # kW
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingVentilationParams) -> PhxCoolingVentilationParams:
        base = super().__add__(other)
        print(vars(base))
        new_obj = self.__class__(**vars(base))
        new_obj.hp_type = self.hp_type
        new_obj.single_speed = any([self.single_speed, other.single_speed])
        new_obj.min_coil_temp = (self.min_coil_temp + other.min_coil_temp) / 2
        new_obj.capacity = (self.capacity + other.capacity) / 2
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj

@dataclass
class PhxCoolingVentilation(PhxCoolingDevice):
    device_type: DeviceType = DeviceType.HEAT_PUMP
    cooling_type: CoolingType = CoolingType.VENTILATION
    params: PhxCoolingVentilationParams = field(default_factory=PhxCoolingVentilationParams)
    
    def __add__(self, other: PhxCoolingVentilation) -> PhxCoolingVentilation:
        base = super().__add__(other)
        new_obj = self.__class__.from_kwargs(**vars(base))
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj


# -- Recirculation Cooling ----------------------------------------------------


class PhxCoolingRecirculationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    single_speed: bool = False
    min_coil_temp: float = 12  # C
    flow_rate_m3_hr: float = 100
    flow_rate_variable: bool = True
    capacity: float = 10  # kW
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingRecirculationParams) -> PhxCoolingRecirculationParams:
        new_obj = self.__class__()
        new_obj.hp_type = self.hp_type
        new_obj.single_speed = any([self.single_speed, other.single_speed])
        new_obj.min_coil_temp = (self.min_coil_temp + other.min_coil_temp) / 2
        new_obj.flow_rate_m3_hr = (self.flow_rate_m3_hr + other.flow_rate_m3_hr) / 2
        new_obj.capacity = (self.capacity + other.capacity) / 2
        new_obj.flow_rate_variable = any(
            [self.flow_rate_variable, other.flow_rate_variable])
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


class PhxCoolingRecirculation(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.RECIRCULATION
        self.params: PhxCoolingRecirculationParams = PhxCoolingRecirculationParams()

    def __add__(self, other: PhxCoolingRecirculation) -> PhxCoolingRecirculation:
        new_obj = self.__class__()
        new_obj.cooling_type = self.cooling_type
        new_obj.device_type = self.device_type
        new_obj.params = self.params + other.params
        return new_obj

# -- Dehumidification ---------------------------------------------------------


class PhxCoolingDehumidificationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    useful_heat_loss: bool = False
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingDehumidificationParams) -> PhxCoolingDehumidificationParams:
        new_obj = self.__class__()
        new_obj.hp_type = self.hp_type
        new_obj.useful_heat_loss = any([self.useful_heat_loss, other.useful_heat_loss])
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


class PhxCoolingDehumidification(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.DEHUMIDIFICATION
        self.params: PhxCoolingDehumidificationParams = PhxCoolingDehumidificationParams()

    def __add__(self, other: PhxCoolingDehumidification) -> PhxCoolingDehumidification:
        new_obj = self.__class__()
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj


# -- Panel Cooling ------------------------------------------------------------


class PhxCoolingPanelParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: PhxCoolingPanelParams) -> PhxCoolingPanelParams:
        new_obj = self.__class__()
        new_obj.hp_type = self.hp_type
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj


class PhxCoolingPanel(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.PANEL
        self.params: PhxCoolingPanelParams = PhxCoolingPanelParams()

    def __add__(self, other: PhxCoolingPanel) -> PhxCoolingPanel:
        new_obj = self.__class__()
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj
