# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH 'Space' and Related Sub-object Classes (FloorSegments, etc)"""

from honeybee_ph import _base
from honeybee_ph.properties import space


class SpaceFloorSegment(_base._Base):
    def __init__(self):
        self.geometry = None
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
        self.floor_segments = []

    def to_dict(self):
        # type: () -> dict
        d = {}

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class SpaceVolume(_base._Base):
    def __init__(self):
        self.floor = SpaceFloor()
        self._geometry = None
        self.avg_ceiling_height = 2.5  # m

    def to_dict(self):
        # type: () -> dict
        d = {}

        return d

    @classmethod
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
        self._host = _host

        self.volume = 0.0
        self.volumes = []
        self.program = None
        self.properties = space.SpaceProperties(self)

    @property
    def full_name(self):
        return "{}-{}".format(self.number, self.name)

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['_host'] = self._host

        return d

    @property
    def display_name(self):
        return "{}: {}-{}".format(self.__class__.__name__, self.number, self.name)

    @classmethod
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
