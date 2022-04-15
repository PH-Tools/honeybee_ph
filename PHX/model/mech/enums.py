# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Valid 'types' for Mech Equipment Options."""

from enum import Enum


class FuelType(Enum):
    GAS = 1
    OIL = 2
    WOOD_LOG = 3
    WOOD_PELLET = 4
    # HARD_COAL_CGS_70_PHC = 'HARD_COAL_CGS_70_PHC'
    # HARD_COAL_CGS_35_PHC = 'HARD_COAL_CGS_35_PHC'
    # HARD_COAL_HS_0_PHC = 'HARD_COAL_HS_0_PHC'
    # GAS_CGS_70_PHC = 'GAS_CGS_70_PHC'
    # GAS_CGS_35_PHC = 'GAS_CGS_35_PHC'
    # GAS_HS_0_PHC = 'GAS_HS_0_PHC'
    # OIL_CGS_70_PHC = 'OIL_CGS_70_PHC'
    # OIL_CGS_35_PHC = 'OIL_CGS_35_PHC'
    # OIL_HS_0_PHC = 'OIL_HS_0_PHC'


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
