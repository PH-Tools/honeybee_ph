# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Mechanical Equipment Classes"""

from typing import Optional, Union
from PHX.model.mech.enums import DeviceType, HeatPumpType, FuelType
from PHX.model.mech import _base


# -----------------------------------------------------------------------------
# Electric


class PhxHeaterElectric(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.ELECTRIC


# -----------------------------------------------------------------------------
# Boilers


class PhxHeaterBoilerFossilParams(_base.PhxMechanicalEquipmentParams):
    _fuel: FuelType = FuelType.GAS
    condensing: bool = True
    in_conditioned_space: bool = True
    effic_at_30_percent_load: float = 0.98
    effic_at_nominal_load: float = 0.94
    avg_rtrn_temp_at_30_percent_load: float = 30
    avg_temp_at_70C_55C: float = 41
    avg_temp_at_55C_45C: float = 35
    avg_temp_at_32C_28C: float = 24
    standby_loss_at_70C: Optional[float] = None
    rated_capacity: float = 10.0  # kW

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, _in):
        self._fuel = FuelType(_in)


class PhxHeaterBoilerWoodParams(_base.PhxMechanicalEquipmentParams):
    _fuel: FuelType = FuelType.WOOD_LOG
    effic_in_basic_cycle: float = 0.6
    effic_in_const_operation: float = 0.7
    avg_frac_heat_output: float = 0.4
    temp_diff_on_off: float = 30.0
    rated_capacity: float = 15.0  # kW
    demand_basic_cycle: float = 1.0  # kWh
    power_stationary_run: float = 1.0  # W
    power_standard_run: Optional[float] = None
    no_transport_pellets: Optional[bool] = None
    only_control: Optional[bool] = None
    area_mech_room: Optional[float] = None

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, _in):
        self._fuel = FuelType(_in)


class PhxHeaterBoiler(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.BOILER

    @classmethod
    def fossil(cls) -> 'PhxHeaterBoiler':
        obj = cls()
        obj.params = PhxHeaterBoilerFossilParams()
        return obj

    @classmethod
    def wood(cls) -> 'PhxHeaterBoiler':
        obj = cls()
        obj.params = PhxHeaterBoilerWoodParams()
        return obj


# -----------------------------------------------------------------------------
# District Heat


class PhxHeaterDistrictHeat(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.DISTRICT_HEAT


# -----------------------------------------------------------------------------
# Heat Pumps


class PhxHeaterHeatPumpParamsAnnual(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.ANNUAL
    annual_COP: Optional[float] = None
    total_system_perf_ratio: Optional[float] = None


class PhxHeaterHeatPumpParamsMonthly(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.RATED_MONTHLY
    COP_1: Optional[float] = None
    COP_2: Optional[float] = None
    ambient_temp_1: Optional[float] = None
    ambient_temp_2: Optional[float] = None

    @property
    def monthly_COPS(self):
        return None

    @monthly_COPS.setter
    def monthly_COPS(self, _in):
        if not _in:
            return

        self.COP_1 = _in[0]
        try:
            self.COP_2 = _in[1]
        except IndexError:
            self.COP_2 = _in[0]

    @property
    def monthly_temps(self):
        return None

    @monthly_temps.setter
    def monthly_temps(self, _in):
        if not _in:
            return

        self.ambient_temp_1 = _in[0]
        try:
            self.ambient_temp_2 = _in[1]
        except IndexError:
            self.ambient_temp_2 = _in[0]


class PhxHeaterHeatPumpParamsHotWater(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.HOT_WATER
    annual_COP: Optional[float] = None
    annual_system_perf_ratio: Optional[float] = None
    annual_energy_factor: Optional[float] = None


class PhxHeaterHeatPumpParamsCombined(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = HeatPumpType.COMBINED


class PhxHeaterHeatPump(_base.PhxMechanicalEquipment):
    def __init__(self):
        super().__init__()
        self.device_type: DeviceType = DeviceType.HEAT_PUMP

    @classmethod
    def annual(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsAnnual()
        return new_obj

    @classmethod
    def monthly(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsMonthly()
        return new_obj

    @classmethod
    def hot_water(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsHotWater()
        return new_obj

    @classmethod
    def combined(cls) -> 'PhxHeaterHeatPump':
        new_obj = cls()
        new_obj.params = PhxHeaterHeatPumpParamsCombined()
        return new_obj


PhxHeater = Union[PhxHeaterElectric,
                  PhxHeaterBoiler,
                  PhxHeaterDistrictHeat,
                  PhxHeaterHeatPump,
                  ]
