# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHC Climate Classes"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Union


@dataclass
class PhxGround:
    ground_thermal_conductivity: float = 2
    ground_heat_capacity: float = 1000
    ground_density: float = 2000
    depth_groundwater: float = 3
    flow_rate_groundwater: float = 0.05


@dataclass
class PhxPEFactor:
    """Conversion Factors for Site-Energy->Primary-Energy"""
    value: float = 0.0
    unit: str = ''
    fuel_name: str = ''


@dataclass
class PhxCO2Factor:
    """Conversion Factors for Site->CO2"""
    value: float = 0.0
    unit: str = ''
    fuel_name: str = ''


PhxEnergyFactor = Union[PhxPEFactor, PhxCO2Factor]


@dataclass
class PhxSiteEnergyFactors:
    selection_pe_co2_factor: int = 6
    pe_factors: dict[str, PhxEnergyFactor] = field(default_factory=dict)
    co2_factors: dict[str, PhxEnergyFactor] = field(default_factory=dict)

    def __post_init__(self):
        self.pe_factors = {
            "OIL": PhxPEFactor(1.1, "kWh/kWh", "OIL"),
            "NATURAL_GAS": PhxPEFactor(1.1, "kWh/kWh", "NATURAL_GAS"),
            "LPG": PhxPEFactor(1.1, "kWh/kWh", "LPG"),
            "HARD_COAL": PhxPEFactor(1.1, "kWh/kWh", "HARD_COAL"),
            "WOOD": PhxPEFactor(0.2, "kWh/kWh", "WOOD"),
            "ELECTRICITY_MIX": PhxPEFactor(1.8, "kWh/kWh", "ELECTRICITY_MIX"),
            "ELECTRICITY_PV": PhxPEFactor(1.7, "kWh/kWh", "ELECTRICITY_PV"),
            "HARD_COAL_CGS_70_CHP": PhxPEFactor(0.8, "kWh/kWh", "HARD_COAL_CGS_70_CHP"),
            "HARD_COAL_CGS_35_CHP": PhxPEFactor(1.1, "kWh/kWh", "HARD_COAL_CGS_35_CHP"),
            "HARD_COAL_CGS_0_CHP": PhxPEFactor(1.5, "kWh/kWh", "HARD_COAL_CGS_0_CHP"),
            "GAS_CGS_70_CHP": PhxPEFactor(0.7, "kWh/kWh", "GAS_CGS_70_CHP"),
            "GAS_CGS_35_CHP": PhxPEFactor(1.1, "kWh/kWh", "GAS_CGS_35_CHP"),
            "GAS_CGS_0_CHP": PhxPEFactor(1.5, "kWh/kWh", "GAS_CGS_0_CHP"),
            "OIL_CGS_70_CHP": PhxPEFactor(0.8, "kWh/kWh", "OIL_CGS_70_CHP"),
            "OIL_CGS_35_CHP": PhxPEFactor(1.1, "kWh/kWh", "OIL_CGS_35_CHP"),
            "OIL_CGS_0_CHP": PhxPEFactor(1.5, "kWh/kWh", "OIL_CGS_0_CHP"),
        }
        self.co2_factors: dict[str, PhxEnergyFactor] = {
            "OIL": PhxCO2Factor(309.9966, "g/kWh", "OIL"),
            "NATURAL_GAS": PhxCO2Factor(250.0171, "g/kWh", "NATURAL_GAS"),
            "LPG": PhxCO2Factor(270.0102, "g/kWh", "LPG"),
            "HARD_COAL": PhxCO2Factor(439.9864, "g/kWh", "HARD_COAL"),
            "WOOD": PhxCO2Factor(53.4289, "g/kWh", "WOOD"),
            "ELECTRICITY_MIX": PhxCO2Factor(680.0068, "g/kWh", "ELECTRICITY_MIX"),
            "ELECTRICITY_PV": PhxCO2Factor(250.0171, "g/kWh", "ELECTRICITY_PV"),
            "HARD_COAL_CGS_70_CHP": PhxCO2Factor(239.9864, "g/kWh", "HARD_COAL_CGS_70_CHP"),
            "HARD_COAL_CGS_35_CHP": PhxCO2Factor(319.9932, "g/kWh", "HARD_COAL_CGS_35_CHP"),
            "HARD_COAL_CGS_0_CHP": PhxCO2Factor(409.9966, "g/kWh", "HARD_COAL_CGS_0_CHP"),
            "GAS_CGS_70_CHP": PhxCO2Factor(-70.0102, "g/kWh", "GAS_CGS_70_CHP"),
            "GAS_CGS_35_CHP": PhxCO2Factor(129.9898, "g/kWh", "GAS_CGS_35_CHP"),
            "GAS_CGS_0_CHP": PhxCO2Factor(319.9932, "g/kWh", "GAS_CGS_0_CHP"),
            "OIL_CGS_70_CHP": PhxCO2Factor(100, "g/kWh", "OIL_CGS_70_CHP"),
            "OIL_CGS_35_CHP": PhxCO2Factor(250.0171, "g/kWh", "OIL_CGS_35_CHP"),
            "OIL_CGS_0_CHP": PhxCO2Factor(409.9966, "g/kWh", "OIL_CGS_0_CHP"),
        }


@dataclass
class PhxSite:
    latitude: float = 40.6
    longitude: float = -73.8
    elevation: float = 3.0
    climate_zone: int = 1
    hours_from_UTC: int = -4


@dataclass
class PhxClimatePeakLoad:
    temp: float = 0
    rad_north: float = 0
    rad_east: float = 0
    rad_south: float = 0
    rad_west: float = 0
    rad_global: float = 0


@dataclass
class PhxClimate:
    weather_station_elevation: float = 3.0
    selection: int = 6
    daily_temp_swing: float = 8.0
    avg_wind_speed: float = 4.0

    monthly_temperature_air: list[float] = field(default_factory=list)
    monthly_temperature_dewpoint: list[float] = field(default_factory=list)
    monthly_temperature_sky: list[float] = field(default_factory=list)

    monthly_radiation_north: list[float] = field(default_factory=list)
    monthly_radiation_east: list[float] = field(default_factory=list)
    monthly_radiation_south: list[float] = field(default_factory=list)
    monthly_radiation_west: list[float] = field(default_factory=list)
    monthly_radiation_global: list[float] = field(default_factory=list)

    peak_heating_1: PhxClimatePeakLoad = field(default_factory=PhxClimatePeakLoad)
    peak_heating_2: PhxClimatePeakLoad = field(default_factory=PhxClimatePeakLoad)
    peak_cooling_1: PhxClimatePeakLoad = field(default_factory=PhxClimatePeakLoad)
    peak_cooling_2: PhxClimatePeakLoad = field(default_factory=PhxClimatePeakLoad)


@dataclass
class PhxLocation:
    display_name: str = "__unnamed_location__"
    source: str = "__unknown__"
    selection: int = 1
    site: PhxSite = field(default_factory=PhxSite)
    climate: PhxClimate = field(default_factory=PhxClimate)
    ground: PhxGround = field(default_factory=PhxGround)
    energy_factors: PhxSiteEnergyFactors = field(default_factory=PhxSiteEnergyFactors)
