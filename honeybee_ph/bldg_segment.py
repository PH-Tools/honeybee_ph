# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Building 'Segment' Level Data Attributes"""

try:
    from typing import Any
except ImportError:
    pass  # Python2.7

from honeybee_ph import _base, location, phius, phi
from honeybee_ph_standards.sourcefactors import factors
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
        self.climate = location.Climate()
        self.source_energy_factors = factors.FactorCollection('Source_Energy')
        self.co2e_factors = factors.FactorCollection('CO2')
        self.phius_certification = phius.PhiusCertification()
        self.phi_certification = phi.PhiCertification()
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
        d['source_energy_factors'] = self.source_energy_factors.to_dict()
        d['co2e_factors'] = self.co2e_factors.to_dict()
        d['phius_certification'] = self.phius_certification.to_dict()
        d['phi_certification'] = self.phi_certification.to_dict()
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
        obj.climate = location.Climate.from_dict(_dict.get('climate', {}))
        obj.source_energy_factors = factors.FactorCollection.from_dict(
            _dict.get('source_energy_factors', {}))
        obj.co2e_factors = factors.FactorCollection.from_dict(
            _dict.get('co2e_factors', {}))
        obj.phius_certification = phius.PhiusCertification.from_dict(
            _dict.get('phius_certification', {}))
        obj.phi_certification = phi.PhiCertification.from_dict(
            _dict.get('phi_certification', {}))
        obj.set_points = SetPoints.from_dict(_dict.get('set_points', {}))
        return obj
