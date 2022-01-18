# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Geometry Classes"""

from dataclasses import dataclass, field
from typing import Any, ClassVar, Collection


@dataclass
class Vertix:
    _count: ClassVar[int] = 0
    id_num: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Vertix, cls).__new__(cls, *args, **kwargs)


@dataclass
class Polygon:
    _count: ClassVar[int] = 0
    id_num: int = 0
    normal_vector: Any = None
    vertices: list[Vertix] = field(default_factory=list)
    child_polygon_ids: list[int] = field(default_factory=list)

    @property
    def vertices_id_numbers(self) -> list[int]:
        return [v.id_num for v in self.vertices]

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Polygon, cls).__new__(cls, *args, **kwargs)


@dataclass
class Graphics3D:
    polygons: list[Polygon] = field(default_factory=list)

    @property
    def vertices(self):
        return [vertix for polygon in self.polygons for vertix in polygon.vertices]

    def add_polygons(self, _polygons: list[Polygon] | Polygon) -> None:
        if not isinstance(_polygons, Collection):
            _polygons = [_polygons]

        for polygon in _polygons:
            self.polygons.append(polygon)
