# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Fresh-Air Ventilation Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field


@dataclass
class VentilationLoad:
    flow_supply: float = 0.0
    flow_extract: float = 0.0
    flow_trasfer: float = 0.0


@dataclass
class RoomVentilation:
    _count: ClassVar[int] = 0
    vent_pattern_id_num: int = 0
    name: str = 'Unnamed_Space'
    wufi_type: int = 99  # User Determined
    quantity: int = 1
    floor_area: float = 0.0
    weighted_floor_area: float = 0.0
    net_volume: float = 0.0
    clear_height: float = 2.5
    ventilation_load: VentilationLoad = field(default_factory=VentilationLoad)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(RoomVentilation, cls).__new__(cls, *args, **kwargs)
