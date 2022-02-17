# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Construction, Materials Classes"""

from __future__ import annotations
from typing import ClassVar
from dataclasses import dataclass, field


@dataclass
class Material:
    name: str = ""
    conductivity: float = 0.0
    density: float = 0.0
    porosity: float = 0.0
    heat_capacity: float = 0.0
    water_vapor_resistance: float = 0.0
    reference_water: float = 0.0


@dataclass
class Layer:
    thickness: float = 0.0
    material: Material = field(default_factory=Material)


@dataclass
class Assembly:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    layer_order: int = 2  # Outside to Inside
    grid_kind: int = 2  # Medium
    layers: list[Layer] = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Assembly, cls).__new__(cls, *args, **kwargs)


@dataclass
class WindowType:
    _count = 0
    id_num: int = 0
    name: str = ""

    use_detailed_uw: bool = True
    use_detailed_frame: bool = False

    u_value_window: float = 1.0
    u_value_glass: float = 1.0
    u_value_frame: float = 1.0

    frame_width_left: float = 0.1
    frame_psi_g_left: float = 0.1
    frame_psi_inst_left: float = 0.1
    frame_u_value_left: float = 1.0
    frame_factor: float = 0.75

    glass_mean_emissivity: float = 0.1
    glass_g_value: float = 0.4

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(WindowType, cls).__new__(cls, *args, **kwargs)
