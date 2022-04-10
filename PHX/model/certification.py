# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Certification Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field


@dataclass
class PH_Building:
    _count: ClassVar[int] = 0
    building_category: int = 1
    occupancy_type: int = 1
    building_status: int = 1
    building_type: int = 1
    num_of_units: int = 1
    num_of_floors: int = 1
    occupancy_setting_method: int = 2  # Design

    airtightness_q50: float = 1.0  # m3/hr-m2-envelope
    foundations: list = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(PH_Building, cls).__new__(cls, *args, **kwargs)


@dataclass
class PassivehouseData:
    ph_certificate_criteria: int = 3
    ph_selection_target_data: int = 2
    annual_heating_demand: float = 15.0
    annual_cooling_demand: float = 15.0
    peak_heating_load: float = 10.0
    peak_cooling_load: float = 10.0
    ph_buildings: list[PH_Building] = field(default_factory=list)
