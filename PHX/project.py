# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Project Classes"""

from __future__ import annotations
from typing import Any, ClassVar
from dataclasses import dataclass, field

from PHX import mech_equip, building, geometry, climate, certification, constructions, schedules


@dataclass
class Variant:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = "unnamed_variant"
    remarks: str = ""
    plugin: str = ""
    graphics3D: geometry.Graphics3D = field(default_factory=geometry.Graphics3D)
    building: building.Building = field(default_factory=building.Building)
    ph_data: certification.PassivehouseData = field(
        default_factory=certification.PassivehouseData)
    climate: climate.ClimateLocation = field(default_factory=climate.ClimateLocation)
    mech_systems: mech_equip.PhxMechanicalEquipmentCollection = field(
        default_factory=mech_equip.PhxMechanicalEquipmentCollection)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Variant, cls).__new__(cls, *args, **kwargs)


@dataclass
class ProjectData_Agent:
    name: str = ""
    street: str = ""
    city: str = ""
    post_code: str = ""
    telephone: str = ""
    email: str = ""
    license_number: str = ""


@dataclass
class ProjectData:
    customer: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    building: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    owner: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    responsible: ProjectData_Agent = field(default_factory=ProjectData_Agent)

    project_date: str = ""
    owner_is_client: bool = False
    year_constructed: int = 0
    image: None = None


@dataclass
class Project:
    name: str = "unnamed_project"

    _assembly_types: dict[str, constructions.Assembly] = field(default_factory=dict)
    _window_types: dict[str, Any] = field(default_factory=dict)
    utilisation_patterns_ventilation: schedules.UtilPat_Vent_Collection = field(
        default_factory=schedules.UtilPat_Vent_Collection)
    utilisation_patterns_ph: list = field(default_factory=list)
    variants: list = field(default_factory=list)

    project_data: ProjectData = field(default_factory=ProjectData)

    data_version: int = 48
    unit_system: int = 1
    program_version: str = "3.2.0.1"
    scope: int = 3
    visualized_geometry: int = 2

    @property
    def assembly_types(self):
        return self._assembly_types.values()

    @property
    def window_types(self):
        return self._window_types.values()

    def add_new_variant(self, _variant: Variant) -> None:
        """Adds a new PHX Variant to the Project."""
        self.variants.append(_variant)

    def add_new_assembly(self, _key, _assembly: constructions.Assembly) -> None:
        self._assembly_types[_key] = _assembly

    def assembly_in_project(self, _key) -> bool:
        return _key in self._assembly_types.keys()
