# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Cooling Equipment Classes"""

from PHX.model.mech.enums import CoolingType, DeviceType, HeatPumpType
from PHX.model.mech import _base


class PhxCoolingDevice(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.usage_profile.cooling = True

    def __add__(self, other: 'PhxCoolingDevice') -> 'PhxCoolingDevice':
        return self.__class__()

    def __radd__(self, other):
        if isinstance(other, int):
            return self + self
        else:
            return self + other


# -- Ventilation Air Cooling --------------------------------------------------


class PhxCoolingVentilationParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    single_speed: bool = False
    min_coil_temp: float = 12  # C
    capacity: float = 10  # kW
    annual_COP: float = 4  # W/W

    @property
    def total_system_perf_ratio(self):
        return 1 / self.annual_COP

    def __add__(self, other: 'PhxCoolingVentilationParams') -> 'PhxCoolingVentilationParams':
        new_obj = self.__class__()
        new_obj.hp_type = self.hp_type
        new_obj.single_speed = any([self.single_speed, other.single_speed])
        new_obj.min_coil_temp = (self.min_coil_temp + other.min_coil_temp) / 2
        new_obj.capacity = (self.capacity + other.capacity) / 2
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj

    def __radd__(self, other):
        if isinstance(other, int):
            return self + self
        else:
            return self + other


class PhxCoolingVentilation(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.VENTILATION
        self.params: PhxCoolingVentilationParams = PhxCoolingVentilationParams()

    def __add__(self, other: 'PhxCoolingVentilation') -> 'PhxCoolingVentilation':
        new_obj = self.__class__()
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

    def __add__(self, other: 'PhxCoolingRecirculationParams') -> 'PhxCoolingRecirculationParams':
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

    def __radd__(self, other):
        if isinstance(other, int):
            return self + self
        else:
            return self + other


class PhxCoolingRecirculation(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.RECIRCULATION
        self.params: PhxCoolingRecirculationParams = PhxCoolingRecirculationParams()

    def __add__(self, other: 'PhxCoolingRecirculation') -> 'PhxCoolingRecirculation':
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

    def __add__(self, other: 'PhxCoolingDehumidificationParams') -> 'PhxCoolingDehumidificationParams':
        new_obj = self.__class__()
        new_obj.hp_type = self.hp_type
        new_obj.useful_heat_loss = any([self.useful_heat_loss, other.useful_heat_loss])
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj

    def __radd__(self, other):
        if isinstance(other, int):
            return self + self
        else:
            return self + other


class PhxCoolingDehumidification(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.DEHUMIDIFICATION
        self.params: PhxCoolingDehumidificationParams = PhxCoolingDehumidificationParams()

    def __add__(self, other: 'PhxCoolingDehumidification') -> 'PhxCoolingDehumidification':
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

    def __add__(self, other: 'PhxCoolingPanelParams') -> 'PhxCoolingPanelParams':
        new_obj = self.__class__()
        new_obj.hp_type = self.hp_type
        new_obj.annual_COP = (self.annual_COP + other.annual_COP) / 2
        return new_obj

    def __radd__(self, other):
        if isinstance(other, int):
            return self + self
        else:
            return self + other


class PhxCoolingPanel(PhxCoolingDevice):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP
        self.cooling_type: CoolingType = CoolingType.PANEL
        self.params: PhxCoolingPanelParams = PhxCoolingPanelParams()

    def __add__(self, other: 'PhxCoolingPanel') -> 'PhxCoolingPanel':
        new_obj = self.__class__()
        new_obj.device_type = self.device_type
        new_obj.cooling_type = self.cooling_type
        new_obj.params = self.params + other.params
        return new_obj
