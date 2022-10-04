# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.material.opaque.EnergyMaterial Objects"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython 2.7


class EnergyMaterialPhProperties:
    def __init__(self, _host=None):
        self._host = _host
        self.id_num = 0

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d['id_num'] = self.id_num
        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict['id_num']
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> EnergyMaterialPhProperties
        _host = new_host or self._host
        new_obj = EnergyMaterialPhProperties(_host)
        new_obj.id_num = self.id_num
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialNoMassPhProperties:
    def __init__(self, _host=None):
        self.host = _host
        self.id_num = 0

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d['id_num'] = self.id_num
        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialNoMassPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict['id_num']
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> EnergyMaterialNoMassPhProperties
        _host = new_host or self._host
        new_obj = EnergyMaterialNoMassPhProperties(_host)
        new_obj.id_num = self.id_num
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialNoMassPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialVegetationPhProperties:
    def __init__(self, _host=None):
        self.host = _host
        self.id_num = 0

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d['id_num'] = self.id_num
        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialVegetationPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict['id_num']
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> EnergyMaterialVegetationPhProperties
        _host = new_host or self._host
        new_obj = EnergyMaterialVegetationPhProperties(_host)
        new_obj.id_num = self.id_num
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialVegetationPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
