# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Fresh-Air Ventilation Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field

from honeybee_ph import space
from honeybee_ph_utils import ventilation


@dataclass
class VentilationLoad:
    flow_supply: float = 0.0
    flow_extract: float = 0.0
    flow_trasfer: float = 0.0


@dataclass
class RoomVentilation:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = 'Unnamed_Space'
    wufi_type: int = 99  # User Determined
    quantity: int = 1
    weighted_floor_area: float = 0.0
    net_volume: float = 0.0
    clear_height: float = 2.5
    ventilation_load: VentilationLoad = field(default_factory=VentilationLoad)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(RoomVentilation, cls).__new__(cls, *args, **kwargs)

    @classmethod
    def from_space(cls, _space: space.Space) -> RoomVentilation:
        obj = cls()

        obj.name = _space.full_name
        obj.wufi_type = _space.wufi_type
        obj.quantity = _space.quantity
        obj.weighted_floor_area = _space.weighted_floor_area
        obj.clear_height = _space.avg_clear_height
        obj.net_volume = _space.net_volume

        peak_airflow_rate = ventilation.hb_room_peak_ventilation_airflow_total(
            _space.host) * 3600  # m3/s --> m3/h
        obj.ventilation_load.flow_supply = peak_airflow_rate
        obj.ventilation_load.flow_extract = peak_airflow_rate

        return obj
