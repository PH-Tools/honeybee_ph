# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Phius Certification Data Class"""

from honeybee_ph_utils import enumerables
from honeybee_ph import _base


class BuildingStatus(enumerables.CustomEnum):
    allowed = [
        "IN_PLANNING",
        "UNDER_CONSTRUCTION",
        "COMPLETE",
    ]

    def __init__(self, _value=1):
        super(BuildingStatus, self).__init__()
        self.value = _value


class BuildingType(enumerables.CustomEnum):
    allowed = [
        "NEW_CONSTRUCTION",
        "RETROFIT",
        "MIXED",
    ]

    def __init__(self, _value=1):
        super(BuildingType, self).__init__()
        self.value = _value


class PhiusCertification(_base._Base):
    def __init__(self):
        super(PhiusCertification, self).__init__()
        self.certification_criteria = 3
        self.localization_selection_type = 2

        self.PHIUS2021_heating_demand = 15.0
        self.PHIUS2021_cooling_demand = 15.0
        self.PHIUS2021_heating_load = 10.0
        self.PHIUS2021_cooling_load = 10.0

        self.building_status = BuildingStatus('IN_PLANNING')
        self.building_type = BuildingType('NEW_CONSTRUCTION')

        self.int_gains_evap_per_person = 15
        self.int_gains_flush_heat_loss = True
        self.int_gains_num_toilets = 1
        self.int_gains_toilet_room_util_pat = None
        self.int_gains_use_school_defaults = False
        self.int_gains_dhw_marginal_perf_ratio = None

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['certification_criteria'] = self.certification_criteria
        d['localization_selection_type'] = self.localization_selection_type

        d['PHIUS2021_heating_demand'] = self.PHIUS2021_heating_demand
        d['PHIUS2021_cooling_demand'] = self.PHIUS2021_cooling_demand
        d['PHIUS2021_heating_load'] = self.PHIUS2021_heating_load
        d['PHIUS2021_cooling_load'] = self.PHIUS2021_cooling_load

        d['building_status'] = self.building_status.to_dict()
        d['building_type'] = self.building_type.to_dict()

        d['int_gains_evap_per_person'] = self.int_gains_evap_per_person
        d['int_gains_flush_heat_loss'] = self.int_gains_flush_heat_loss
        d['int_gains_num_toilets'] = self.int_gains_num_toilets
        d['int_gains_toilet_room_util_pat'] = self.int_gains_toilet_room_util_pat
        d['int_gains_use_school_defaults'] = self.int_gains_use_school_defaults
        d['int_gains_dhw_marginal_perf_ratio'] = self.int_gains_dhw_marginal_perf_ratio

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> PhiusCertification
        obj = cls()

        obj.certification_criteria = _dict.get('certification_criteria')
        obj.localization_selection_type = _dict.get(
            'localization_selection_type')

        obj.PHIUS2021_heating_demand = _dict.get('PHIUS2021_heating_demand')
        obj.PHIUS2021_cooling_demand = _dict.get('PHIUS2021_cooling_demand')
        obj.PHIUS2021_heating_load = _dict.get('PHIUS2021_heating_load')
        obj.PHIUS2021_cooling_load = _dict.get('PHIUS2021_cooling_load')

        obj.building_status = BuildingStatus.from_dict(
            _dict.get('building_status', {}))
        obj.building_type = BuildingType.from_dict(
            _dict.get('building_type', {}))

        obj.int_gains_evap_per_person = _dict.get('int_gains_evap_per_person')
        obj.int_gains_flush_heat_loss = _dict.get('int_gains_flush_heat_loss')
        obj.int_gains_num_toilets = _dict.get('int_gains_num_toilets')
        obj.int_gains_toilet_room_util_pat = _dict.get(
            'int_gains_toilet_room_util_pat')
        obj.int_gains_use_school_defaults = _dict.get(
            'int_gains_use_school_defaults')
        obj.int_gains_dhw_marginal_perf_ratio = _dict.get(
            'int_gains_dhw_marginal_perf_ratio')

        return obj
