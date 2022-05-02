# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Building Classes"""

from __future__ import annotations
from typing import ClassVar, Collection, List, Set, Union
from dataclasses import dataclass, field
from collections import defaultdict
from functools import reduce
import operator

from PHX.model import loads, elec_equip, geometry
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceType, ComponentColor


@dataclass
class PhxZone:
    _count: ClassVar[int] = 0
    id_num: int = field(init=False, default=0)
    name: str = ""
    volume_gross: float = 0.0
    volume_net: float = 0.0
    weighted_net_floor_area: float = 0.0
    clearance_height: float = 2.5
    specific_heat_capacity: float = 132
    wufi_rooms: List[loads.PhxRoomVentilation] = field(default_factory=list)
    elec_equipment_collection: elec_equip.PhxElectricDeviceCollection = field(
        default_factory=elec_equip.PhxElectricDeviceCollection)
    res_occupant_quantity: int = 0
    res_number_bedrooms: int = 0

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count


@dataclass
class PhxComponent:
    _count: ClassVar[int] = 0
    id_num: int = field(init=False, default=0)
    display_name: str = ""
    face_type: ComponentFaceType = ComponentFaceType.OPAQUE
    color_interior: ComponentColor = ComponentColor.EXT_WALL_INNER
    color_exterior: ComponentColor = ComponentColor.EXT_WALL_INNER
    exposure_exterior: ComponentExposureExterior = ComponentExposureExterior.EXTERIOR
    exposure_interior: int = 1
    interior_attachment_id: int = -1
    assembly_type_id_num: int = -1
    window_type_id_num: int = -1
    polygons: List[geometry.PhxPolygon] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    @property
    def polygon_ids(self) -> Set[int]:
        return {polygon.id_num for polygon in self.polygons}

    @property
    def unique_key(self) -> str:
        return f'{self.face_type}-{self.exposure_interior}-{self.interior_attachment_id}-'\
            f'{self.exposure_exterior}-{self.assembly_type_id_num}-{self.window_type_id_num}'

    def add_polygons(self,
                     _input: Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]) -> None:
        if not isinstance(_input, Collection):
            _input = (_input,)

        for polygon in _input:
            self.polygons.append(polygon)

    def __add__(self, other: PhxComponent) -> PhxComponent:
        new_obj = self.__class__()
        for attr_name, attr_val in vars(self).items():
            setattr(new_obj, attr_name, attr_val)

        new_obj.display_name = 'Merged_Component'
        new_obj.polygons = self.polygons + other.polygons
        return new_obj


@dataclass
class PhxBuilding:
    components: List[PhxComponent] = field(default_factory=list)
    zones: List[PhxZone] = field(default_factory=list)

    def add_components(self, _components: Union[PhxComponent, Collection[PhxComponent]]) -> None:
        """Add a new PHX-Component to the PHX-Building"""
        if not isinstance(_components, Collection):
            _components = (_components,)

        for compo in _components:
            self.components.append(compo)

    def add_zones(self, _zones: Union[PhxZone, Collection[PhxZone]]) -> None:
        """Add a new PHX-Zone to the PHX-Building"""
        if not isinstance(_zones, Collection):
            _zones = (_zones,)

        for zone in _zones:
            self.zones.append(zone)

    def merge_components_by_assembly(self) -> None:
        """Merge together the Components in the Building if they gave the same Attributes."""
        # -- Group the components by their unique key / type
        new_component_groups = defaultdict(list)
        for c in self.components:
            new_component_groups[c.unique_key].append(c)

        # -- Create new components from the group
        grouped_components = []
        for component_group in new_component_groups.values():
            grouped_components.append(reduce(operator.add, component_group))

        # -- Reset the Building's Components
        self.components = grouped_components

    @property
    def opaque_components(self) -> List[PhxComponent]:
        return sorted(
            [c for c in self.components if c.face_type == ComponentFaceType.OPAQUE],
            key=lambda _: _.display_name
        )

    @property
    def transparent_components(self) -> List[PhxComponent]:
        return sorted(
            [c for c in self.components if c.face_type == ComponentFaceType.TRANSPARENT],
            key=lambda _: _.display_name
        )

    @property
    def polygon_ids(self) -> set[int]:
        """Return a set of all the Polygon IDs of of all the Components in the building."""
        p_ids = set()
        for compo in self.components:
            p_ids.update(compo.polygon_ids)
        return p_ids

    def __bool__(self) -> bool:
        return bool(self.components) or bool(self.zones)
