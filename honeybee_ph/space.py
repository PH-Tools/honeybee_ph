# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH 'Space' and Related Sub-object Classes (FloorSegments, etc)"""

try:
    from typing import Any
except:
    pass  # IronPython

from xml.sax.handler import property_interning_dict
from honeybee_ph import _base
from honeybee_ph.properties import space
from ladybug_geometry import geometry3d


class SpaceFloorSegment(_base._Base):
    def __init__(self):
        super(SpaceFloorSegment, self).__init__()
        self.geometry = None
        self.reference_point = None
        self.weighting_factor = 1.0

    @property
    def weighted_area(self):
        # type: () -> float
        return self.geometry.area * self.weighting_factor

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['weighting_factor'] = self.weighting_factor
        if self.geometry:
            d['geometry'] = self.geometry.to_dict()
        if self.reference_point:
            d['reference_point'] = self.reference_point.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> SpaceFloorSegment
        new_obj = cls()

        new_obj.weighting_factor = _input_dict.get('weighting_factor', 1.0)

        geom_dict = _input_dict.get('geometry', None)
        if geom_dict:
            new_obj.geometry = geometry3d.Face3D.from_dict(geom_dict)

        ref_pt_dict = _input_dict.get('reference_point', None)
        if ref_pt_dict:
            new_obj.reference_point = geometry3d.Point3D.from_dict(ref_pt_dict)

        return new_obj

    def __str__(self):
        return '{}(weighting_factor={!r}, geometry={!r})'.format(self.__class__.__name__,
                                                                 self.weighting_factor,
                                                                 self.geometry)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class SpaceFloor(_base._Base):
    def __init__(self):
        super(SpaceFloor, self).__init__()
        self._floor_segments = list()  # list[geometry3d.Face3D]
        self.geometry = None  # geometry3d.Face3D

    @property
    def reference_points(self):
        # type() -> list[geometry3d.Point3D]
        return [seg.reference_point for seg in self.floor_segments]

    @property
    def weighted_area(self):
        # type: () ->  float
        return sum((seg.weighted_area for seg in self.floor_segments))

    def add_floor_segment(self, _floor_seg):
        # type: (SpaceFloorSegment) -> None
        """Add a new SpaceFloorSegment to the SpaceFloor.

        Arguments:
        ----------
            * _floor_seg (SpaceFloorSegment): The SpaceFloorSegment to add to the SpaceFloor.

        Returns:
        --------
            * None
        """
        if not _floor_seg:
            return
        self._floor_segments.append(_floor_seg)

    @property
    def floor_segments(self):
        return self._floor_segments

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['floor_segments'] = [seg.to_dict() for seg in self.floor_segments]
        d['geometry'] = self.geometry.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> SpaceFloor
        new_obj = cls()

        geom_dict = _input_dict.get('geometry', None)
        if geom_dict:
            new_obj.geometry = geometry3d.Face3D.from_dict(geom_dict)

        flr_seg_dicts = _input_dict.get('floor_segments', [])
        for seg_dict in flr_seg_dicts:
            new_obj.add_floor_segment(SpaceFloorSegment.from_dict(seg_dict))

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class SpaceVolume(_base._Base):
    def __init__(self):
        super(SpaceVolume, self).__init__()
        self.avg_ceiling_height = 2.5  # m
        self.floor = SpaceFloor()
        self.geometry = list()

    @property
    def weighted_floor_area(self):
        # type: () -> float
        return self.floor.weighted_area

    @property
    def reference_points(self):
        # type() -> list[geometry3d.Point3D]
        return self.floor.reference_points

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['avg_ceiling_height'] = self.avg_ceiling_height
        d['floor'] = self.floor.to_dict()
        d['geometry'] = [geom.to_dict() for geom in self.geometry]

        return d

    @ classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.avg_ceiling_height = _input_dict.get("avg_ceiling_height")
        new_obj.floor = SpaceFloor.from_dict(_input_dict.get("floor", {}))

        geom_list = _input_dict.get("geometry", [])
        for geom_dict in geom_list:
            new_obj.geometry.append(geometry3d.Face3D.from_dict(geom_dict))

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class Space(_base._Base):

    def __init__(self, _host=None):
        super(Space, self).__init__()
        self.quantity = 1
        self.wufi_type = 99  # -- User-Defined
        self.name = ''
        self.number = ''
        self.host = _host

        self.volume = 0.0
        self._volumes = list()
        self.program = None
        self.properties = space.SpaceProperties(self)

    @property
    def avg_clear_height(self):
        # type: () -> float

        # -- Calc the floor-area-weighted height for each volume
        total_weighted_height = 0
        for vol in self.volumes:
            total_weighted_height += vol.weighted_floor_area * vol.avg_ceiling_height

        return total_weighted_height / self.weighted_floor_area

    @property
    def weighted_floor_area(self):
        # type: () -> float
        return sum((vol.weighted_floor_area for vol in self.volumes))

    @property
    def reference_points(self):
        # type: () -> list[geometry3d.Point3D]
        pts = []
        for vol in self.volumes:
            pts += vol.reference_points
        return pts

    @property
    def volumes(self):
        return self._volumes

    def add_new_volumes(self, _new_volumes):
        # type: (list[SpaceVolume]) -> None
        """Add a new SpaceVolume or list of SpaceVolunes to the Space.

        Arguments:
        ----------
            * _new_volumes (list[SpaceVolume]): A list of the SpaceVolumes to add.

        Returns:
        --------
            *  None
        """
        if not isinstance(_new_volumes, (set, tuple, list)):
            _new_volumes = [_new_volumes]

        for new_vol in _new_volumes:
            self._volumes.append(new_vol)

    @property
    def full_name(self):
        return "{}-{}".format(self.number, self.name)

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['quantity'] = self.quantity
        d['wufi_type'] = self.wufi_type
        d['name'] = self.name
        d['number'] = self.number
        d['volume'] = self.volume
        d['volumes'] = [vol.to_dict() for vol in self.volumes]
        d['program'] = self.program
        d['properties'] = self.properties.to_dict()

        return d

    @property
    def display_name(self):
        return "{}: {}-{}".format(self.__class__.__name__, self.number, self.name)

    @classmethod
    def from_dict(cls, _input_dict, _host):
        new_obj = cls(_host)

        new_obj.quantity = _input_dict.get("quantity")
        new_obj.wufi_type = _input_dict.get("wufi_type")
        new_obj.name = _input_dict.get("name")
        new_obj.number = _input_dict.get("number")
        new_obj.volume = _input_dict.get("volume")
        new_obj.add_new_volumes([SpaceVolume.from_dict(d)
                                for d in _input_dict.get("volumes", [])])
        new_obj.program = _input_dict.get("program")
        new_obj.properties = space.SpaceProperties.from_dict(
            _input_dict.get("properties", {}), _host=new_obj)

        return new_obj

    def __str__(self):
        return '{}(name={!r}, number={!r}, volumes={!r})'.format(self.__class__.__name__,
                                                                 self.name, self.number, self.volumes)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
