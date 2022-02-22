# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Building Classes"""

from __future__ import annotations
from typing import ClassVar, Collection
from dataclasses import dataclass, field
from collections import defaultdict
from functools import reduce
import operator

from PHX.model import ventilation
from PHX.model import elec_equip


@dataclass
class Zone:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    volume_gross: float = 0.0
    volume_net: float = 0.0
    weighted_net_floor_area: float = 0.0
    clearance_height: float = 2.5
    specific_heat_capacity: float = 132
    wufi_rooms: list[ventilation.RoomVentilation] = field(default_factory=list)
    elec_equipment_collection: elec_equip.PhxElectricEquipmentCollection = field(
        default_factory=elec_equip.PhxElectricEquipmentCollection)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Zone, cls).__new__(cls, *args, **kwargs)


@dataclass
class Component:
    _count: ClassVar[int] = 0
    id_num: int = 0
    name: str = ""
    type: int = 1
    color_interior: int = 1
    color_exterior: int = 1
    exposure_exterior: int = -1
    exposure_interior: int = 1
    interior_attachment_id: int = -1
    assembly_type_id_num: int = -1
    window_type_id_num: int = -1
    polygon_ids: list[int] = field(default_factory=list)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Component, cls).__new__(cls, *args, **kwargs)

    def __add__(self, other):
        self.name = 'Merged_Component'
        self.polygon_ids += other.polygon_ids
        return self


@dataclass
class Building:
    components: list[Component] = field(default_factory=list)
    zones: list[Zone] = field(default_factory=list)

    def add_components(self, _components: Component | list[Component]) -> None:
        """Add a new PHX-Component to the PHX-Building"""
        if not isinstance(_components, Collection):
            _components = [_components]

        for compo in _components:
            self.components.append(compo)

    def add_zones(self, _zones: Zone | list[Zone]) -> None:
        """Add a new PHX-Zone to the PHX-Building"""
        if not isinstance(_zones, Collection):
            _zones = [_zones]

        for zone in _zones:
            self.zones.append(zone)

    def group_components_by_assembly(self):
        # -- Group the components by their unique key / type
        new_component_groups = defaultdict(list)
        for c in self.components:
            type_key = f'{c.type}-{c.exposure_interior}-{c.interior_attachment_id}-'\
                f'{c.exposure_exterior}-{c.assembly_type_id_num}-{c.window_type_id_num}'
            new_component_groups[type_key].append(c)

        # -- Create new components from the group
        grouped_components = []
        for component_group in new_component_groups.values():
            grouped_components.append(reduce(operator.add, component_group))

        # -- Reset the Building's Components
        self.components = grouped_components
