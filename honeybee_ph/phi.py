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


class PhiCertificationType(enumerables.CustomEnum):
    allowed = [
        "1-Passive House",
        "2-EnerPHit",
        "3-PHI Low Energy Building",
        "4-Other",
    ]

    def __init__(self, _value=1):
        super(PhiCertificationType, self).__init__()
        self.value = _value


class PhiCertificationClass(enumerables.CustomEnum):
    allowed = [
        "1-Classic",
        "2-Plus",
        "3-Premium",
    ]

    def __init__(self, _value=1):
        super(PhiCertificationClass, self).__init__()
        self.value = _value


class PhiPrimaryEnergyType(enumerables.CustomEnum):
    allowed = [
        "1-PE (non-renewable)",
        "2-PER (renewable)",
    ]

    def __init__(self, _value=1):
        super(PhiPrimaryEnergyType, self).__init__()
        self.value = _value


class PhiEnerPHitType(enumerables.CustomEnum):
    allowed = [
        "1-Component method",
        "2-Energy demand method",
    ]

    def __init__(self, _value=1):
        super(PhiEnerPHitType, self).__init__()
        self.value = _value


class PhiRetrofitType(enumerables.CustomEnum):
    allowed = [
        "1-New building",
        "2-Retrofit",
        "3-Step-by-step retrofit",
    ]

    def __init__(self, _value=1):
        super(PhiRetrofitType, self).__init__()
        self.value = _value


# -----------------------------------------------------------------------------


class PhiCertification(_base._Base):

    def __init__(self):
        super(PhiCertification, self).__init__()
        self._certification_type = PhiCertificationType(1)
        self._certification_class = PhiCertificationClass(1)
        self._primary_energy_type = PhiPrimaryEnergyType(1)
        self._enerphit_type = PhiEnerPHitType(1)
        self._retrofit_type = PhiRetrofitType(1)

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
