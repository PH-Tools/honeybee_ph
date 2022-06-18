# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PHI Certification Settings Class"""

try:
    from typing import Optional
except ImportError:
    pass  # IronPython 2.7

from honeybee_ph_utils import enumerables
from honeybee_ph import _base


# -----------------------------------------------------------------------------


class PhiBuildingCategoryType(enumerables.CustomEnum):
    allowed = [
        "1-RESIDENTIAL BUILDING",
        "2-NON-RESIDENTIAL BUILDING",
    ]

    def __init__(self, _value=1):
        super(PhiBuildingCategoryType, self).__init__(_value)


class PhiBuildingUseType(enumerables.CustomEnum):
    allowed = [
        "",  # PHPP is so stupid. Who did the numbering?... sheesh...
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "10-DWELLING",
        "11-NURSING HOME / STUDENTS",
        "12-OTHER",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "20-OFFICE / ADMIN. BUILDING",
        "21-SCHOOL",
        "22-OTHER",
    ]

    def __init__(self, _value=1):
        super(PhiBuildingUseType, self).__init__(_value)

        # Quick double check cus' the numbering here is so stupid
        if self.value == "":
            raise Exception(
                "Error: PHPP's '_building_use_type' numbering is weird. Check the inputs is valid."
            )


class PhiIHGType(enumerables.CustomEnum):
    allowed = [
        "",
        "2-STANDARD",
        "3-PHPP CALCULATION ('IHG' WORKSHEET)",
        "4-PHPP CALCULATION ('IHG NON-RES' WORKSHEET)",
    ]

    def __init__(self, _value=1):
        super(PhiIHGType, self).__init__(_value)

        # Quick double check cus' the numbering here is so stupid
        if self.value == "":
            raise Exception(
                "Error: PHPP's '_building_use_type' numbering is weird. Check the inputs is valid."
            )


class PhiOccupancyType(enumerables.CustomEnum):
    allowed = [
        "1-STANDARD (ONLY FOR RESIDENTIAL BUILDINGS)",
        "2-USER DETERMINED",
    ]

    def __init__(self, _value=1):
        super(PhiOccupancyType, self).__init__(_value)


class PhiCertificationType(enumerables.CustomEnum):
    allowed = [
        "1-PASSIVE HOUSE",
        "2-ENERPHIT",
        "3-PHI LOW ENERGY BUILDING",
        "4-OTHER",
    ]

    def __init__(self, _value=1):
        super(PhiCertificationType, self).__init__(_value)


class PhiCertificationClass(enumerables.CustomEnum):
    allowed = [
        "1-CLASSIC",
        "2-PLUS",
        "3-PREMIUM",
    ]

    def __init__(self, _value=1):
        super(PhiCertificationClass, self).__init__(_value)


class PhiPrimaryEnergyType(enumerables.CustomEnum):
    allowed = [
        "1-PE (NON-RENEWABLE)",
        "2-PER (RENEWABLE)",
    ]

    def __init__(self, _value=1):
        super(PhiPrimaryEnergyType, self).__init__(_value)


class PhiEnerPHitType(enumerables.CustomEnum):
    allowed = [
        "1-COMPONENT METHOD",
        "2-ENERGY DEMAND METHOD",
    ]

    def __init__(self, _value=1):
        super(PhiEnerPHitType, self).__init__(_value)


class PhiRetrofitType(enumerables.CustomEnum):
    allowed = [
        "1-NEW BUILDING",
        "2-RETROFIT",
        "3-STEP-BY-STEP RETROFIT",
    ]

    def __init__(self, _value=1):
        super(PhiRetrofitType, self).__init__(_value)


# -----------------------------------------------------------------------------


class PhiCertification(_base._Base):

    def __init__(self):
        super(PhiCertification, self).__init__()
        self._building_category_type = PhiBuildingCategoryType("1-RESIDENTIAL BUILDING")
        self._building_use_type = PhiBuildingUseType("10-DWELLING")
        self._ihg_type = PhiIHGType("2-Standard")
        self._occupancy_type = PhiOccupancyType(
            "1-STANDARD (ONLY FOR RESIDENTIAL BUILDINGS)")

        self._certification_type = PhiCertificationType("1-PASSIVE HOUSE")
        self._certification_class = PhiCertificationClass("1-CLASSIC")
        self._primary_energy_type = PhiPrimaryEnergyType("2-PER (RENEWABLE)")
        self._enerphit_type = PhiEnerPHitType("2-ENERGY DEMAND METHOD")
        self._retrofit_type = PhiRetrofitType("1-NEW BUILDING")

    @property
    def building_category_type(self):
        return self._building_category_type

    @building_category_type.setter
    def building_category_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._building_category_type = PhiBuildingCategoryType(_input)

    @property
    def building_use_type(self):
        return self._building_use_type

    @building_use_type.setter
    def building_use_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._building_use_type = PhiBuildingUseType(_input)

    @property
    def occupancy_type(self):
        return self._occupancy_type

    @occupancy_type.setter
    def occupancy_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._occupancy_type = PhiOccupancyType(_input)

    @property
    def ihg_type(self):
        return self._ihg_type

    @ihg_type.setter
    def ihg_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._ihg_type = PhiIHGType(_input)

    @property
    def certification_type(self):
        return self._certification_type

    @certification_type.setter
    def certification_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._certification_type = PhiCertificationType(_input)

    @property
    def certification_class(self):
        return self._certification_class

    @certification_class.setter
    def certification_class(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._certification_class = PhiCertificationClass(_input)

    @property
    def primary_energy_type(self):
        return self._primary_energy_type

    @primary_energy_type.setter
    def primary_energy_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._primary_energy_type = PhiPrimaryEnergyType(_input)

    @property
    def enerphit_type(self):
        return self._enerphit_type

    @enerphit_type.setter
    def enerphit_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._enerphit_type = PhiEnerPHitType(_input)

    @property
    def retrofit_type(self):
        return self._retrofit_type

    @retrofit_type.setter
    def retrofit_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._retrofit_type = PhiRetrofitType(_input)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d['_building_category_type'] = self._building_category_type.to_dict()
        d['_building_use_type'] = self._building_use_type.to_dict()
        d['_ihg_type'] = self._ihg_type.to_dict()
        d['_occupancy_type'] = self._occupancy_type.to_dict()

        d['_certification_type'] = self._certification_type.to_dict()
        d['_certification_class'] = self._certification_class.to_dict()
        d['_primary_energy_type'] = self._primary_energy_type.to_dict()
        d['_enerphit_type'] = self._enerphit_type.to_dict()
        d['_retrofit_type'] = self._retrofit_type.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhiCertification
        new_obj = cls()

        new_obj._building_category_type = PhiBuildingCategoryType.from_dict(
            _input_dict['_building_category_type'])
        new_obj._building_use_type = PhiBuildingUseType.from_dict(
            _input_dict['_building_use_type'])
        new_obj._ihg_type = PhiIHGType.from_dict(
            _input_dict['_ihg_type'])
        new_obj._occupancy_type = PhiOccupancyType.from_dict(
            _input_dict['_occupancy_type'])

        new_obj._certification_type = PhiCertificationType.from_dict(
            _input_dict['_certification_type'])
        new_obj._certification_class = PhiCertificationClass.from_dict(
            _input_dict['_certification_class'])
        new_obj._primary_energy_type = PhiPrimaryEnergyType.from_dict(
            _input_dict['_primary_energy_type'])
        new_obj._enerphit_type = PhiEnerPHitType.from_dict(
            _input_dict['_enerphit_type'])
        new_obj._retrofit_type = PhiRetrofitType.from_dict(
            _input_dict['_retrofit_type'])
        return new_obj

    def __copy__(self):
        # type: () -> PhiCertification
        obj = PhiCertification()

        obj.set_base_attrs_from_source(self)
        obj._building_category_type = self._building_category_type
        obj._building_use_type = self._building_use_type
        obj._ihg_type = self._ihg_type
        obj._occupancy_type = self._occupancy_type
        obj._certification_type = self._certification_type
        obj._certification_class = self._certification_class
        obj._primary_energy_type = self._primary_energy_type
        obj._enerphit_type = self._enerphit_type
        obj._retrofit_type = self._retrofit_type

        return obj

    def duplicate(self):
        # type: () -> PhiCertification
        return self.__copy__()
