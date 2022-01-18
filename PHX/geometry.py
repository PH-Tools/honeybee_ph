# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Geometry Classes"""

from dataclasses import dataclass, field
from typing import Any, ClassVar
from ladybug_geometry_ph.geometry3d_ph.pointvector import PH_Point3D
from honeybee.face import Face as HB_Face
from honeybee.aperture import Aperture as HB_Aperture


@dataclass
class Vertix:
    _count: ClassVar[int] = 0
    id_num: int = 0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @classmethod
    def from_LBT_P3D(cls, _lbt_Point3D: PH_Point3D):
        obj = cls()

        obj.id_num = cls._count
        _lbt_Point3D.properties._ph.id_num = obj.id_num

        obj.x = _lbt_Point3D.x
        obj.y = _lbt_Point3D.y
        obj.z = _lbt_Point3D.z

        return obj

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

    @classmethod
    def from_HB_Face(cls, _hb_face: HB_Face):
        obj = cls()

        obj.id_num = cls._count
        _hb_face.properties._ph.id_num = obj.id_num
        obj.normal_vector = _hb_face.normal
        obj.vertices = [Vertix.from_LBT_P3D(v) for v in _hb_face.vertices]
        obj.child_polygon_ids = [
            aperture.properties._ph.id_num for aperture in _hb_face.apertures]

        return obj

    @classmethod
    def from_HB_Aperture(cls, _hb_aperture: HB_Aperture):
        obj = cls()

        obj.id_num = cls._count
        _hb_aperture.properties._ph.id_num = obj.id_num
        obj.normal_vector = _hb_aperture.normal
        obj.vertices = [Vertix.from_LBT_P3D(v) for v in _hb_aperture.vertices]

        return obj

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(Polygon, cls).__new__(cls, *args, **kwargs)


@dataclass
class Graphics3D:
    polygons: list[Polygon] = field(default_factory=list)

    @property
    def vertices(self):
        return [vertix for polygon in self.polygons for vertix in polygon.vertices]
