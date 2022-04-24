# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Fresh-Air Ventilation Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field


@dataclass
class PhxVentilationFlowrates:
    flow_supply: float = 0.0
    flow_extract: float = 0.0
    flow_transfer: float = 0.0


@dataclass
class PhxRoomVentilation:
    _count: ClassVar[int] = 0
    id_num: int = field(init=False, default=0)
    name: str = 'Unnamed_Space'
    wufi_type: int = 99  # User Determined
    quantity: int = 1
    floor_area: float = 0.0
    weighted_floor_area: float = 0.0
    net_volume: float = 0.0
    clear_height: float = 2.5

    # -- Ventilation related items
    vent_unit_id_num: int = 0
    vent_pattern_id_num: int = 0
    flow_rates: PhxVentilationFlowrates = field(default_factory=PhxVentilationFlowrates)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count
