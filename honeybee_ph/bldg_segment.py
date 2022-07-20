# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Building 'Segment' Level Data Attributes"""

try:
    from typing import Any, Dict
except ImportError:
    pass  # Python2.7

from honeybee_ph import _base, phius, phi, site
from honeybee_ph_standards.sourcefactors import factors
from honeybee_ph_utils import enumerables
from honeybee_energy_ph.construction import thermal_bridge


class BuildingCategoryType(enumerables.CustomEnum):
    allowed = [
        "RESIDENTIAL",
        "NON-RESIDENTIAL"
    ]

    def __init__(self, _value=1):
        super(BuildingCategoryType, self).__init__()
        self.value = _value


class OccupancyType(enumerables.CustomEnum):
    allowed = [
        "RESIDENTIAL",  # 1
        "",  # 2
        "",  # 3
        "OFFICE/ADMINISTRATIVE BUILDING",  # 4
        "SCHOOL",  # 5
        "OTHER",  # 6
        "UNDEFINED/UNFINISHED",  # 7
    ]

    def __init__(self, _value=1):
        super(OccupancyType, self).__init__()
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

    def __copy__(self):
        # type: () -> SetPoints
        obj = SetPoints()
        obj.set_base_attrs_from_source(self)
        obj.winter = self.winter
        obj.summer = self.summer
        return obj

    def duplicate(self):
        # type: () -> SetPoints
        return self.__copy__()


class BldgSegment(_base._Base):

    def __init__(self):
        super(BldgSegment, self).__init__()
        self.display_name = 'Unnamed_Bldg_Segment'
        self.num_floor_levels = 1
        self.num_dwelling_units = 1
        self.site = site.Site()
        self.source_energy_factors = factors.FactorCollection('Source_Energy')
        self.co2e_factors = factors.FactorCollection('CO2')
        self.phius_certification = phius.PhiusCertification()
        self.phi_certification = phi.PhiCertification()
        self.set_points = SetPoints()
        self.thermal_bridges = {}

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['identifier'] = self.identifier
        d['name'] = self.display_name
        d['num_floor_levels'] = self.num_floor_levels
        d['num_dwelling_units'] = self.num_dwelling_units
        d['site'] = self.site.to_dict()
        d['source_energy_factors'] = self.source_energy_factors.to_dict()
        d['co2e_factors'] = self.co2e_factors.to_dict()
        d['phius_certification'] = self.phius_certification.to_dict()
        d['phi_certification'] = self.phi_certification.to_dict()
        d['set_points'] = self.set_points.to_dict()
        d['thermal_bridges'] = {}
        for tb in self.thermal_bridges.values():
            d['thermal_bridges'][str(tb.identifier)] = tb.to_dict()
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, Any]) -> BldgSegment
        obj = cls()

        obj.identifier = _dict.get('identifier')
        obj.display_name = _dict.get('name')
        obj.num_floor_levels = _dict.get('num_floor_levels')
        obj.num_dwelling_units = _dict.get('num_dwelling_units')
        obj.site = site.Site.from_dict(_dict.get('site', {}))
        obj.source_energy_factors = factors.FactorCollection.from_dict(
            _dict.get('source_energy_factors', {}))
        obj.co2e_factors = factors.FactorCollection.from_dict(
            _dict.get('co2e_factors', {}))
        obj.phius_certification = phius.PhiusCertification.from_dict(
            _dict.get('phius_certification', {}))
        obj.phi_certification = phi.PhiCertification.from_dict(
            _dict.get('phi_certification', {}))
        obj.set_points = SetPoints.from_dict(_dict.get('set_points', {}))
        for tb_dict in _dict['thermal_bridges'].values():
            tb_obj = thermal_bridge.PhThermalBridge.from_dict(tb_dict)
            obj.thermal_bridges[tb_obj.identifier] = tb_obj
        return obj

    def __copy__(self):
        # type () -> BldgSegment
        new_obj = BldgSegment()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.num_floor_levels = self.num_floor_levels
        new_obj.num_dwelling_units = self.num_dwelling_units
        new_obj.site = self.site.duplicate()
        new_obj.source_energy_factors = self.source_energy_factors.duplicate()
        new_obj.co2e_factors = self.co2e_factors.duplicate()
        new_obj.phius_certification = self.phius_certification.duplicate()
        new_obj.phi_certification = self.phi_certification.duplicate()
        new_obj.set_points = self.set_points.duplicate()
        new_obj.thermal_bridges = {}
        for tb_k, tb_v in self.thermal_bridges.items():
            new_obj.thermal_bridges[tb_k] = tb_v

        return new_obj

    def duplicate(self):
        # type () -> BldgSegment
        return self.__copy__()
