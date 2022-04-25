# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Passive House Certification Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field

from PHX.model import ground


@dataclass
class PhxPHBuilding:
    _count: ClassVar[int] = 0

    id_num: int = field(init=False, default=0)
    building_category: int = 1
    occupancy_type: int = 1
    building_status: int = 1
    building_type: int = 1
    num_of_units: int = 1
    num_of_floors: int = 1
    occupancy_setting_method: int = 2  # Design

    airtightness_q50: float = 1.0  # m3/hr-m2-envelope
    foundations: list[ground.Foundation] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    def add_foundation(self, _input: ground.Foundation) -> None:
        self.foundations.append(_input)


@dataclass
class PhxPHCertificationCriteria:
    ph_certificate_criteria: int = 3
    ph_selection_target_data: int = 2
    annual_heating_demand: float = 15.0
    annual_cooling_demand: float = 15.0
    peak_heating_load: float = 10.0
    peak_cooling_load: float = 10.0


@dataclass
class PhxPHCertification:
    certification_criteria: PhxPHCertificationCriteria = field(
        default_factory=PhxPHCertificationCriteria)
    building_data: list[PhxPHBuilding] = field(default_factory=list)

    def add_ph_building(self, _input: PhxPHBuilding) -> None:
        self.building_data.append(_input)
