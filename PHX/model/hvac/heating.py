# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Mechanical Heating Devices"""

from __future__ import annotations
from typing import Optional, Union
from dataclasses import dataclass, field

from PHX.model.enums.hvac import DeviceType, HeatPumpType, FuelType
from PHX.model.hvac import _base


@dataclass
class PhxHeatingDevice(_base.PhxMechanicalEquipment):
    def __post_init__(self):
        super().__post_init__()


# -----------------------------------------------------------------------------
# Electric

@dataclass
class PhxHeaterElectricParams(_base.PhxMechanicalEquipmentParams):
    pass


@dataclass
class PhxHeaterElectric(PhxHeatingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.ELECTRIC)
    params: PhxHeaterElectricParams = field(
        default_factory=PhxHeaterElectricParams)


# -----------------------------------------------------------------------------
# Boilers


@dataclass
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


@dataclass
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


@dataclass
class PhxHeaterBoilerFossil(PhxHeatingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.BOILER)
    params: PhxHeaterBoilerFossilParams = field(
        default_factory=PhxHeaterBoilerFossilParams)


@dataclass
class PhxHeaterBoilerWood(PhxHeatingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.BOILER)
    params: PhxHeaterBoilerWoodParams = field(
        default_factory=PhxHeaterBoilerWoodParams)


PhxHeaterBoiler = Union[PhxHeaterBoilerFossil, PhxHeaterBoilerWood]


# -----------------------------------------------------------------------------
# District Heat


@dataclass
class PhxHeaterDistrictHeatParams(_base.PhxMechanicalEquipmentParams):
    pass


@dataclass
class PhxHeaterDistrictHeat(PhxHeatingDevice):
    device_type: DeviceType = field(init=False, default=DeviceType.DISTRICT_HEAT)
    params: PhxHeaterDistrictHeatParams = field(
        default_factory=PhxHeaterDistrictHeatParams)


# -----------------------------------------------------------------------------
# Heat Pumps


@dataclass
class PhxHeaterHeatPumpAnnualParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.ANNUAL)
    annual_COP: Optional[float] = None
    total_system_perf_ratio: Optional[float] = None


@dataclass
class PhxHeaterHeatPumpMonthlyParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.RATED_MONTHLY)
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


@dataclass
class PhxHeaterHeatPumpHotWaterParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.HOT_WATER)
    annual_COP: Optional[float] = None
    annual_system_perf_ratio: Optional[float] = None
    annual_energy_factor: Optional[float] = None


@dataclass
class PhxHeaterHeatPumpCombinedParams(_base.PhxMechanicalEquipmentParams):
    hp_type: HeatPumpType = field(init=False, default=HeatPumpType.COMBINED)


@dataclass
class PhxHeaterHeatPumpAnnual(PhxHeatingDevice):
    device_type: DeviceType = DeviceType.HEAT_PUMP
    params: PhxHeaterHeatPumpAnnualParams = field(
        default_factory=PhxHeaterHeatPumpAnnualParams)


@dataclass
class PhxHeaterHeatPumpMonthly(PhxHeatingDevice):
    device_type: DeviceType = DeviceType.HEAT_PUMP
    params: PhxHeaterHeatPumpMonthlyParams = field(
        default_factory=PhxHeaterHeatPumpMonthlyParams)


@dataclass
class PhxHeaterHeatPumpHotWater(PhxHeatingDevice):
    device_type: DeviceType = DeviceType.HEAT_PUMP
    params: PhxHeaterHeatPumpHotWaterParams = field(
        default_factory=PhxHeaterHeatPumpHotWaterParams)


@dataclass
class PhxHeaterHeatPumpCombined(PhxHeatingDevice):
    device_type: DeviceType = DeviceType.HEAT_PUMP
    params: PhxHeaterHeatPumpCombinedParams = field(
        default_factory=PhxHeaterHeatPumpCombinedParams)


PhxHeaterHeatPump = Union[PhxHeaterHeatPumpAnnual, PhxHeaterHeatPumpMonthly,
                          PhxHeaterHeatPumpHotWater, PhxHeaterHeatPumpCombined]
