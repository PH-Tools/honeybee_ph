# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Construction, Materials Classes"""

from __future__ import annotations
from typing import ClassVar, Union
from dataclasses import dataclass, field
import uuid


@dataclass
class PhxMaterial:
    display_name: str = ""
    conductivity: float = 0.0
    density: float = 0.0
    porosity: float = 0.0
    heat_capacity: float = 0.0
    water_vapor_resistance: float = 0.0
    reference_water: float = 0.0


@dataclass
class PhxLayer:
    thickness: float = 0.0
    material: PhxMaterial = field(default_factory=PhxMaterial)


@dataclass
class PhxConstructionOpaque:
    _count: ClassVar[int] = 0

    _identifier: Union[uuid.UUID, str] = field(
        init=False, default_factory=uuid.uuid4)
    id_num: int = field(init=False, default=0)
    display_name: str = ""
    layer_order: int = 2  # Outside to Inside
    grid_kind: int = 2  # Medium
    layers: list[PhxLayer] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    @property
    def identifier(self):
        return str(self._identifier)

    @identifier.setter
    def identifier(self, _in: str):
        if not _in:
            return
        self._identifier = str(_in)

    def __hash__(self):
        return hash(self.identifier)

# ------------------------------------------------------------
# Windows


@dataclass
class PhxWindowFrameElement:
    width: float = 0.1  # m
    u_value: float = 1.0  # W/m2k
    psi_glazing: float = 0.00  # W/mk
    psi_install: float = 0.00  # W/mk


@dataclass
class PhxConstructionWindow:
    _count: ClassVar[int] = 0
    id_num: int = field(init=False, default=0)
    display_name: str = ""

    use_detailed_uw: bool = True
    use_detailed_frame: bool = True

    u_value_window: float = 1.0
    u_value_glass: float = 1.0
    u_value_frame: float = 1.0

    frame_top: PhxWindowFrameElement = field(
        default_factory=PhxWindowFrameElement)
    frame_right: PhxWindowFrameElement = field(
        default_factory=PhxWindowFrameElement)
    frame_bottom: PhxWindowFrameElement = field(
        default_factory=PhxWindowFrameElement)
    frame_left: PhxWindowFrameElement = field(
        default_factory=PhxWindowFrameElement)
    frame_factor: float = 0.75

    glass_mean_emissivity: float = 0.1
    glass_g_value: float = 0.4

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count
