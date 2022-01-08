# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Building 'Segment' Level Data Attributes"""

try:
    from typing import Any
except ImportError:
    pass  # Python2.7

from honeybee_ph._base import _Base
from honeybee_ph.phius import PhiusCertifiction
from honeybee_ph.climate import Climate
from honeybee_ph_utils.enumerables import CustomEnum


class OccupancyType(CustomEnum):
    allowed = [
        "RESIDENTIAL",
        "",
        "",
        "OFFICE/ADMINISTRATIVE BUILDING",
        "SCHOOL",
        "OTHER",
        "UNDEFINED/UNFINISHED",
    ]

    def __init__(self, _value=1):
        super(OccupancyType, self).__init__()
        self.value = _value


class UsageType(CustomEnum):
    allowed = [
        "RESIDENTIAL",
        "NON-RESIDENTIAL",
    ]

    def __init__(self, _value=1):
        super(UsageType, self).__init__()
        self.value = _value


class SetPoints:
    def __init__(self):
        self.winter = 20
        self.summer = 25

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['winter'] = self.winter
        d['summer'] = self.summer

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> SetPoints
        obj = cls()

        obj.winter = _dict.get('winter')
        obj.summer = _dict.get('summer')

        return obj


class BldgSegment(_Base):

    def __init__(self):
        super(BldgSegment, self).__init__()
        self.name = 'Unnamed_Bldg_Segment'
        self.occupancy_type = OccupancyType("RESIDENTIAL")
        self.usage_type = UsageType("RESIDENTIAL")
        self.num_floor_levels = 1
        self.num_dwelling_units = 1
        self.climate = Climate()
        self.ph_certification = PhiusCertifiction()
        self.set_points = SetPoints()

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['identifier'] = self.identifier
        d['name'] = self.name
        d['occupancy_type'] = self.occupancy_type.to_dict()
        d['usage_type'] = self.usage_type.to_dict()
        d['num_floor_levels'] = self.num_floor_levels
        d['num_dwelling_units'] = self.num_dwelling_units
        d['climate'] = self.climate.to_dict()
        d['ph_certification'] = self.ph_certification.to_dict()
        d['set_points'] = self.set_points.to_dict()

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, Any]) -> BldgSegment
        obj = cls()

        obj.identifier = _dict.get('identifier')
        obj.name = _dict.get('name')
        obj.occupancy_type = OccupancyType.from_dict(_dict.get('occupancy_type', {}))
        obj.usage_type = UsageType.from_dict(_dict.get('usage_type', {}))
        obj.num_floor_levels = _dict.get('num_floor_levels')
        obj.num_dwelling_units = _dict.get('num_dwelling_units')
        obj.climate = Climate.from_dict(_dict.get('climate', {}))
        obj.ph_certification = PhiusCertifiction.from_dict(
            _dict.get('ph_certification', {}))
        obj.set_points = SetPoints.from_dict(_dict.get('set_points', {}))

        return obj

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
