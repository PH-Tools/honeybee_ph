# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Project Classes"""

from __future__ import annotations
from typing import Any, ClassVar, List, Dict
from dataclasses import dataclass, field

from PHX.model import schedules
from PHX.model import building, certification, climate, constructions, geometry
from PHX.model.hvac import collection


@dataclass
class PhxVariant:
    _count: ClassVar[int] = 0
    id_num: int = field(init=False, default=0)
    name: str = "unnamed_variant"
    remarks: str = ""
    plugin: str = ""
    building: building.PhxBuilding = field(
        default_factory=building.PhxBuilding)
    ph_certification: certification.PhxPHCertification = field(
        default_factory=certification.PhxPHCertification)
    location: climate.PhxLocation = field(default_factory=climate.PhxLocation)
    mech_systems: collection.PhxMechanicalEquipmentCollection = field(
        default_factory=collection.PhxMechanicalEquipmentCollection)

    @property
    def graphics3D(self):
        """Collects all of the geometry (Polygons, Vertices) in the Project."""
        phx_graphics3D = geometry.PhxGraphics3D()
        for phx_component in self.building.components:
            phx_graphics3D.add_polygons(phx_component.polygons)
        return phx_graphics3D

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count


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
class PhxProjectData:
    customer: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    building: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    owner: ProjectData_Agent = field(default_factory=ProjectData_Agent)
    responsible: ProjectData_Agent = field(default_factory=ProjectData_Agent)

    project_date: str = ""
    owner_is_client: bool = False
    year_constructed: int = 0
    image: None = None


@dataclass
class PhxProject:
    name: str = "unnamed_project"

    _assembly_types: Dict[str, constructions.PhxConstructionOpaque] = field(
        default_factory=dict)
    _window_types: Dict[str, constructions.PhxConstructionWindow] = field(
        default_factory=dict)
    utilization_patterns_ventilation: schedules.UtilPat_Vent_Collection = field(
        default_factory=schedules.UtilPat_Vent_Collection)
    utilization_patterns_ph: List = field(default_factory=list)
    variants: List[PhxVariant] = field(default_factory=list)

    project_data: PhxProjectData = field(default_factory=PhxProjectData)

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

    def add_new_variant(self, _variant: PhxVariant) -> None:
        """Adds a new PHX Variant to the Project."""
        self.variants.append(_variant)

    def add_new_assembly(self, _key, _assembly: constructions.PhxConstructionOpaque) -> None:
        self._assembly_types[_key] = _assembly

    def assembly_in_project(self, _key) -> bool:
        return _key in self._assembly_types.keys()

    def __str__(self):
        return f"{self.__class__.__name__}"
