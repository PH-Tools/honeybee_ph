# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Geometry Classes"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar, Collection, List, Union, Iterable


@dataclass
class PhxVertix:
    _count: ClassVar[int] = 0

    id_num: int = field(init=False, default=0)
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def __eq__(self, other: PhxVertix) -> bool:
        return (self.x == other.x) and \
            (self.y == other.y) and \
            (self.z == other.z) and \
            (self.id_num == other.id_num)

    def __post_init__(self):
        self.__class__._count += 1
        self.id_num = self.__class__._count

    @property
    def unique_key(self) -> str:
        """Return a unique key (str) for the Vertex. Used for dicts, welding, etc"""
        return f"{self.x :0.10f}_{self.y :0.10f}_{self.z :0.10f}"

    def __hash__(self) -> int:
        return hash(self.unique_key)


@dataclass
class PhxVector:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0


@dataclass
class PhxPolygon:
    _count: ClassVar[int] = 0

    id_num: int = field(init=False, default=0)
    _display_name: str = ''
    area: float = 0.0
    normal_vector: PhxVector = PhxVector()
    vertices: List[PhxVertix] = field(default_factory=list)
    child_polygon_ids: List[int] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        if not self._display_name:
            return str(self.id_num)
        else:
            return self._display_name

    @display_name.setter
    def display_name(self, _in: str):
        self._display_name = str(_in)

    def __post_init__(self):
        self.__class__._count += 1
        self.id_num = self.__class__._count

    @property
    def vertices_id_numbers(self) -> List[int]:
        return [v.id_num for v in self.vertices]

    def add_vertix(self, _phx_vertix: PhxVertix) -> None:
        self.vertices.append(_phx_vertix)

    def add_child_poly_id(self, _child_ids: Union[Collection[int], int]) -> None:
        if not isinstance(_child_ids, Collection):
            _child_ids = (_child_ids,)

        for child_id in _child_ids:
            self.child_polygon_ids.append(child_id)


@dataclass
class PhxGraphics3D:
    polygons: List[PhxPolygon] = field(default_factory=list)

    @property
    def vertices(self) -> List[PhxVertix]:
        """Returns a sorted list with all of the unique vertix objects of all the polygons in the collection."""
        return sorted(
            {vertix
             for polygon in self.polygons
             for vertix in polygon.vertices
             },
            key=lambda _: _.id_num)

    def add_polygons(self, _polygons: Union[Collection[PhxPolygon], PhxPolygon]) -> None:
        """Adds a new Polygon object to the collection"""

        if not isinstance(_polygons, Collection):
            _polygons = [_polygons]

        for polygon in _polygons:
            self.polygons.append(polygon)

    def get_polygons_by_id(self, _ids: Collection[int]) -> List[PhxPolygon]:
        """Returns a sorted list of polygons in the collection matching the IDs supplied.

        Arguments:
        ----------
            * _ids: (Collection[int]): A collection of one or more id_nums to look for.

        Returns:
        --------
            * List[PhxPolygon]: A sorted (by display_name) list of all the 
                polygons with matching id_nums.
        """

        if not isinstance(_ids, Collection):
            _ids = {_ids}

        return sorted(
            [p for p in self.polygons if p.id_num in _ids],
            key=lambda _: _.display_name
        )

    def __bool__(self) -> bool:
        return bool(self.polygons)
