# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHC Climate Classes"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Ground:
    ground_thermal_conductivity: float = 2
    ground_heat_capacitiy: float = 1000
    ground_density: float = 2000
    depth_groundwater: float = 3
    flow_rate_groundwater: float = 0.05


@dataclass
class Location:
    latitude: float = 40.6
    longitude: float = -73.8
    weather_station_elevation: float = 3.0
    climate_zone: int = 1
    hours_from_UTC: int = -4


@dataclass
class PeakLoad:
    temp: float = 0
    rad_north: float = 0
    rad_east: float = 0
    rad_south: float = 0
    rad_west: float = 0
    rad_global: float = 0


@dataclass
class PH_ClimateLocation:
    selection: int = 6
    selection_pe_co2_factor: int = 1
    daily_temp_swing: float = 8.0
    avg_wind_speed: float = 4.0
    location: Location = field(default_factory=Location)
    ground: Ground = field(default_factory=Ground)

    monthly_temperature_air: list[float] = field(default_factory=list)
    monthly_temperature_dewpoint: list[float] = field(default_factory=list)
    monthly_temperature_sky: list[float] = field(default_factory=list)

    monthly_radiation_north: list[float] = field(default_factory=list)
    monthly_radiation_east: list[float] = field(default_factory=list)
    monthly_radiation_south: list[float] = field(default_factory=list)
    monthly_radiation_west: list[float] = field(default_factory=list)
    monthly_radiation_global: list[float] = field(default_factory=list)

    peak_heating_1: PeakLoad = field(default_factory=PeakLoad)
    peak_heating_2: PeakLoad = field(default_factory=PeakLoad)
    peak_cooling_1: PeakLoad = field(default_factory=PeakLoad)
    peak_cooling_2: PeakLoad = field(default_factory=PeakLoad)


@dataclass
class ClimateLocation:
    selection: int = 1
    ph_climate_location: PH_ClimateLocation = field(default_factory=PH_ClimateLocation)
