from enum import Enum


class SystemType(Enum):
    VENTILATION = 1
    ELECTRIC = 2
    BOILER = 3
    DISTRICT_HEAT = 4
    HEAT_PUMP = 5
    WATER_STORAGE = 8


class DeviceType(Enum):
    VENTILATION = 1
    ELECTRIC = 2
    BOILER = 3
    DISTRICT_HEAT = 4
    HEAT_PUMP = 5
    WATER_STORAGE = 8


class HeatPumpType(Enum):
    COMBINED = 2
    ANNUAL = 3
    RATED_MONTHLY = 4
    HOT_WATER = 5
