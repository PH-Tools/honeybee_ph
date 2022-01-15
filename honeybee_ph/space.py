# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH 'Space' and Related Sub-object Classes (FloorSegments, etc)"""

try:
    from typing import Any
except:
    pass  # IronPython

from honeybee_ph import _base
from honeybee_ph.properties import space
from ladybug_geometry import geometry3d


class SpaceFloorSegment(_base._Base):
    def __init__(self):
        super(SpaceFloorSegment, self).__init__()
        self.geometry = None
        self.reference_point = None
        self.weighting_factor = 1.0

    def to_dict(self):
        # type: () -> dict
        d = {}

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

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
        self._floor_segments = []
        self.geometry = None

    @property
    def reference_points(self):
        # type() -> list[geometry3d.Point3D]
        return [seg.reference_point for seg in self.floor_segments]

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
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> SpaceFloor
        new_obj = cls()
        for seg_dict in _input_dict.get('floor_segments', []):
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
        self.floor = SpaceFloor()
        self.geometry = None
        self.avg_ceiling_height = 2.5  # m

    @property
    def reference_points(self):
        # type() -> list[geometry3d.Point3D]
        return self.floor.reference_points

    def to_dict(self):
        # type: () -> dict
        d = {}

        return d

    @ classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

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
        self.type = 99  # -- User-Defined
        self.name = ''
        self.number = ''
        self.host = _host

        self.volume = 0.0
        self._volumes = []
        self.program = None
        self.properties = space.SpaceProperties(self)

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

    @ property
    def full_name(self):
        return "{}-{}".format(self.number, self.name)

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['host'] = self.host

        return d

    @ property
    def display_name(self):
        return "{}: {}-{}".format(self.__class__.__name__, self.number, self.name)

    @ classmethod
    def from_dict(cls, _input_dict, _host):
        new_obj = cls(_host)

        return new_obj

    def __str__(self):
        return '{}(name={!r}, number={!r}, volumes={!r})'.format(self.__class__.__name__,
                                                                 self.name, self.number, self.volumes)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
