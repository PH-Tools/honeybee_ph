# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Building 'Segment' Level Data Attributes"""

try:
    from typing import Any
except ImportError:
    pass  # Python2.7

from honeybee_ph import _base, phius, climate
from honeybee_ph_utils import enumerables


class OccupancyType(enumerables.CustomEnum):
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


class UsageType(enumerables.CustomEnum):
    allowed = [
        "RESIDENTIAL",
        "NON-RESIDENTIAL",
    ]

    def __init__(self, _value=1):
        super(UsageType, self).__init__()
        self.value = _value


class SetPoints(_base._Base):
    def __init__(self):
        super(SetPoints, self).__init__()
        self.winter = 20.0
        self.summer = 25.0

    def to_dict(self):
        # type: () -> dict[str, float]
        d = {}

        d['winter'] = self.winter
        d['summer'] = self.summer

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, float]) -> SetPoints
        obj = cls()

        obj.winter = _dict.get('winter', 20.0)
        obj.summer = _dict.get('summer', 25.0)

        return obj


class BldgSegment(_base._Base):

    def __init__(self):
        super(BldgSegment, self).__init__()
        self.name = 'Unnamed_Bldg_Segment'
        self.occupancy_type = OccupancyType("RESIDENTIAL")
        self.usage_type = UsageType("RESIDENTIAL")
        self.num_floor_levels = 1
        self.num_dwelling_units = 1
        self.climate = climate.Climate()
        self.ph_certification = phius.PhiusCertifiction()
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
        obj.occupancy_type = OccupancyType.from_dict(
            _dict.get('occupancy_type', {}))
        obj.usage_type = UsageType.from_dict(_dict.get('usage_type', {}))
        obj.num_floor_levels = _dict.get('num_floor_levels')
        obj.num_dwelling_units = _dict.get('num_dwelling_units')
        obj.climate = climate.Climate.from_dict(_dict.get('climate', {}))
        obj.ph_certification = phius.PhiusCertifiction.from_dict(
            _dict.get('ph_certification', {}))
        obj.set_points = SetPoints.from_dict(_dict.get('set_points', {}))

        return obj
