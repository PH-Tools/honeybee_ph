# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Phius Certification Data Class"""

from copy import copy

try:
    from typing import Optional, Union
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph import _base
from honeybee_ph_utils import enumerables

# -----------------------------------------------------------------------------


class PhiusBuildingCertificationProgram(enumerables.CustomEnum):
    allowed = [
        "1-Default",
        "2-PHIUS 2015",
        "3-PHIUS 2018",
        "4-Italian",
        "5-PHIUS 2018 CORE",
        "6-PHIUS 2018 ZERO",
        "7-PHIUS 2021 CORE",
        "8-PHIUS 2021 ZERO",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingCertificationProgram, self).__init__(_value)


class PhiusBuildingCategoryType(enumerables.CustomEnum):
    allowed = [
        "1-RESIDENTIAL BUILDING",
        "2-NON-RESIDENTIAL BUILDING",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingCategoryType, self).__init__(_value)


class PhiusBuildingUseType(enumerables.CustomEnum):
    allowed = [
        "1-RESIDENTIAL",
        "",
        "",
        "4-OFFICE/ADMINISTRATIVE BUILDING",
        "5-SCHOOL",
        "6-OTHER",
        "7-UNDEFINED/UNFINISHED",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingUseType, self).__init__(_value)

        # Quick double check cus' the numbering here is so stupid
        if self.value == "":
            raise Exception("Error: WUFI's '_building_use_type' numbering is weird. Check the 'inputs' value is valid?")


class PhiusBuildingStatus(enumerables.CustomEnum):
    allowed = [
        "1-IN_PLANNING",
        "2-UNDER_CONSTRUCTION",
        "3-COMPLETE",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingStatus, self).__init__(_value)


class PhiusBuildingType(enumerables.CustomEnum):
    allowed = [
        "1-NEW_CONSTRUCTION",
        "2-RETROFIT",
        "3-MIXED",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingType, self).__init__(_value)


# -----------------------------------------------------------------------------


class PhiusCertification(_base._Base):
    def __init__(self):
        super(PhiusCertification, self).__init__()
        self.localization_selection_type = 2

        self._certification_program = PhiusBuildingCertificationProgram("7-PHIUS 2021 CORE")
        self._building_category_type = PhiusBuildingCategoryType("1-RESIDENTIAL BUILDING")
        self._building_use_type = PhiusBuildingUseType("1-RESIDENTIAL")
        self._building_status = PhiusBuildingStatus("1-IN_PLANNING")
        self._building_type = PhiusBuildingType("1-NEW_CONSTRUCTION")

        self.PHIUS2021_heating_demand = 15.0
        self.PHIUS2021_cooling_demand = 15.0
        self.PHIUS2021_heating_load = 10.0
        self.PHIUS2021_cooling_load = 10.0

        self.int_gains_evap_per_person = 15
        self.int_gains_flush_heat_loss = True
        self.int_gains_num_toilets = 1
        self.int_gains_toilet_room_util_pat = None
        self.int_gains_use_school_defaults = False
        self.int_gains_dhw_marginal_perf_ratio = None

        self.icfa_override = None  # type: Optional[float]

    @property
    def certification_program(self):
        # type: () -> PhiusBuildingCertificationProgram
        return self._certification_program

    @certification_program.setter
    def certification_program(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._certification_program = PhiusBuildingCertificationProgram(_input)

    @property
    def building_category_type(self):
        # type: () -> PhiusBuildingCategoryType
        return self._building_category_type

    @building_category_type.setter
    def building_category_type(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_category_type = PhiusBuildingCategoryType(_input)

    @property
    def building_use_type(self):
        # type: () -> PhiusBuildingUseType
        return self._building_use_type

    @building_use_type.setter
    def building_use_type(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_use_type = PhiusBuildingUseType(_input)

    @property
    def building_status(self):
        # type: () -> PhiusBuildingStatus
        return self._building_status

    @building_status.setter
    def building_status(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_status = PhiusBuildingStatus(_input)

    @property
    def building_type(self):
        # type: () -> PhiusBuildingType
        return self._building_type

    @building_type.setter
    def building_type(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_type = PhiusBuildingType(_input)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict
        d = {}

        d["localization_selection_type"] = self.localization_selection_type

        d["certification_program"] = self.certification_program.to_dict()
        d["building_category_type"] = self.building_category_type.to_dict()
        d["building_use_type"] = self.building_use_type.to_dict()
        d["building_status"] = self.building_status.to_dict()
        d["building_type"] = self.building_type.to_dict()

        d["PHIUS2021_heating_demand"] = self.PHIUS2021_heating_demand
        d["PHIUS2021_cooling_demand"] = self.PHIUS2021_cooling_demand
        d["PHIUS2021_heating_load"] = self.PHIUS2021_heating_load
        d["PHIUS2021_cooling_load"] = self.PHIUS2021_cooling_load

        d["int_gains_evap_per_person"] = self.int_gains_evap_per_person
        d["int_gains_flush_heat_loss"] = self.int_gains_flush_heat_loss
        d["int_gains_num_toilets"] = self.int_gains_num_toilets
        d["int_gains_toilet_room_util_pat"] = self.int_gains_toilet_room_util_pat
        d["int_gains_use_school_defaults"] = self.int_gains_use_school_defaults
        d["int_gains_dhw_marginal_perf_ratio"] = self.int_gains_dhw_marginal_perf_ratio

        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)
        d["display_name"] = self.display_name

        d["icfa_override"] = self.icfa_override

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> PhiusCertification
        obj = cls()

        obj.localization_selection_type = _dict.get("localization_selection_type")

        obj._certification_program = PhiusBuildingCertificationProgram.from_dict(_dict.get("certification_program", {}))
        obj._building_category_type = PhiusBuildingCategoryType.from_dict(_dict.get("building_category_type", {}))
        obj._building_use_type = PhiusBuildingUseType.from_dict(_dict.get("building_use_type", {}))
        obj._building_status = PhiusBuildingStatus.from_dict(_dict.get("building_status", {}))
        obj._building_type = PhiusBuildingType.from_dict(_dict.get("building_type", {}))

        obj.PHIUS2021_heating_demand = _dict.get("PHIUS2021_heating_demand")
        obj.PHIUS2021_cooling_demand = _dict.get("PHIUS2021_cooling_demand")
        obj.PHIUS2021_heating_load = _dict.get("PHIUS2021_heating_load")
        obj.PHIUS2021_cooling_load = _dict.get("PHIUS2021_cooling_load")

        obj.int_gains_evap_per_person = _dict.get("int_gains_evap_per_person")
        obj.int_gains_flush_heat_loss = _dict.get("int_gains_flush_heat_loss")
        obj.int_gains_num_toilets = _dict.get("int_gains_num_toilets")
        obj.int_gains_toilet_room_util_pat = _dict.get("int_gains_toilet_room_util_pat")
        obj.int_gains_use_school_defaults = _dict.get("int_gains_use_school_defaults")
        obj.int_gains_dhw_marginal_perf_ratio = _dict.get("int_gains_dhw_marginal_perf_ratio")

        obj.identifier = _dict.get("identifier")
        obj.user_data = _dict.get("user_data", {})
        obj.display_name = _dict.get("display_name")

        obj.icfa_override = _dict.get("icfa_override")

        return obj

    def __copy__(self):
        # type: () -> PhiusCertification
        obj = PhiusCertification()

        obj.set_base_attrs_from_source(self)
        obj.localization_selection_type = self.localization_selection_type

        obj._certification_program = self._certification_program
        obj._building_category_type = self._building_category_type
        obj._building_use_type = self._building_use_type
        obj._building_status = self._building_status
        obj._building_type = self._building_type

        obj.PHIUS2021_heating_demand = self.PHIUS2021_heating_demand
        obj.PHIUS2021_cooling_demand = self.PHIUS2021_cooling_demand
        obj.PHIUS2021_heating_load = self.PHIUS2021_heating_load
        obj.PHIUS2021_cooling_load = self.PHIUS2021_cooling_load

        obj.int_gains_evap_per_person = self.int_gains_evap_per_person
        obj.int_gains_flush_heat_loss = self.int_gains_flush_heat_loss
        obj.int_gains_num_toilets = self.int_gains_num_toilets
        obj.int_gains_toilet_room_util_pat = self.int_gains_toilet_room_util_pat
        obj.int_gains_use_school_defaults = self.int_gains_use_school_defaults
        obj.int_gains_dhw_marginal_perf_ratio = self.int_gains_dhw_marginal_perf_ratio

        obj.icfa_override = self.icfa_override

        return obj

    def duplicate(self):
        # type: () -> PhiusCertification
        return self.__copy__()
