# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Component (Face, Aperture) Classes"""

from __future__ import annotations
from typing import ClassVar, Collection, List, Set, Union, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from functools import reduce

from PHX.model import loads, elec_equip, geometry, constructions
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceType, ComponentFaceOpacity, ComponentColor


class PhxComponentBase:
    _count: ClassVar[int] = 0

    def __init__(self):
        PhxComponentBase._count += 1
        self._id_num: int = self.__class__._count

    @property
    def id_num(self) -> int:
        return self._id_num


class PhxComponentOpaque(PhxComponentBase):

    def __init__(self):
        super().__init__()

        self.display_name: str = ""
        self.face_type: ComponentFaceType = ComponentFaceType.WALL
        self.face_opacity: ComponentFaceOpacity = ComponentFaceOpacity.OPAQUE
        self.color_interior: ComponentColor = ComponentColor.EXT_WALL_INNER
        self.color_exterior: ComponentColor = ComponentColor.EXT_WALL_INNER
        self.exposure_exterior: ComponentExposureExterior = ComponentExposureExterior.EXTERIOR
        self.exposure_interior: int = 1
        self.interior_attachment_id: int = -1

        self.assembly: constructions.PhxConstructionOpaque = constructions.PhxConstructionOpaque()
        self.assembly_type_id_num: int = -1

        self.apertures: List[PhxComponentAperture] = []
        self.polygons: List[geometry.PhxPolygon] = []

    @property
    def polygon_ids(self) -> Set[int]:
        return {polygon.id_num for polygon in self.polygons}

    @property
    def unique_key(self) -> str:
        return f'{self.face_type}-{self.face_opacity}-{self.exposure_interior}-{self.interior_attachment_id}-'\
            f'{self.exposure_exterior}-{self.assembly_type_id_num}'

    def add_polygons(self,
                     _input: Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]) -> None:
        if not isinstance(_input, Collection):
            _input = (_input,)

        for polygon in _input:
            self.polygons.append(polygon)

    def __add__(self, other: PhxComponentOpaque) -> PhxComponentOpaque:
        new_compo = self.__class__()
        for attr_name, attr_val in vars(self).items():
            if attr_name.startswith('_'):
                continue
            setattr(new_compo, attr_name, attr_val)

        new_compo.display_name = 'Merged_Component'
        new_compo.polygons = self.polygons + other.polygons
        for phx_aperture in new_compo.apertures:
            phx_aperture.host = new_compo
        for phx_aperture in other.apertures:
            new_compo.add_aperture(phx_aperture)

        return new_compo

    def add_aperture(self, _aperture: PhxComponentAperture) -> None:
        _aperture.host = self
        self.apertures.append(_aperture)


class PhxComponentAperture(PhxComponentBase):

    def __init__(self, _host: PhxComponentOpaque):
        super().__init__()

        self.host = _host

        self.display_name: str = ""
        self.face_type: ComponentFaceType = ComponentFaceType.WINDOW
        self.face_opacity: ComponentFaceOpacity = ComponentFaceOpacity.TRANSPARENT
        self.color_interior: ComponentColor = ComponentColor.WINDOW
        self.color_exterior: ComponentColor = ComponentColor.WINDOW
        self.exposure_exterior: ComponentExposureExterior = ComponentExposureExterior.EXTERIOR
        self.exposure_interior: int = 1
        self.interior_attachment_id: int = -1

        self.window_type: constructions.PhxConstructionWindow = constructions.PhxConstructionWindow()
        self.window_type_id_num: int = -1

        self.polygons: List[geometry.PhxPolygon] = []

    @property
    def polygon_ids(self) -> Set[int]:
        return {polygon.id_num for polygon in self.polygons}

    @property
    def unique_key(self) -> str:
        return f'{self.face_type}-{self.face_opacity}-{self.exposure_interior}-{self.interior_attachment_id}-'\
            f'{self.exposure_exterior}-{self.window_type_id_num}'

    def add_polygons(self,
                     _input: Union[Collection[geometry.PhxPolygon], geometry.PhxPolygon]) -> None:
        if not isinstance(_input, Collection):
            _input = (_input,)

        for polygon in _input:
            self.polygons.append(polygon)

    def __add__(self, other) -> PhxComponentAperture:
        new_compo = self.__class__(_host=self.host)
        for attr_name, attr_val in vars(self).items():
            if attr_name.startswith('_'):
                continue
            setattr(new_compo, attr_name, attr_val)

        new_compo.display_name = 'Merged_Component'
        new_compo.polygons = self.polygons + other.polygons

        return new_compo
