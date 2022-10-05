# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.material.opaque.EnergyMaterial Objects"""

try:
    from typing import Any, List
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_energy.material import opaque
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy:\n\t{}'.format(e))


class EnergyMaterialPhProperties:
    def __init__(self, _host=None):
        self._host = _host
        self.id_num = 0
        self.percentage_of_assembly = 1.0
        self.base_materials = [] # type: List[opaque.EnergyMaterial]

    def add_base_material(self, _hb_material):
        # type: (opaque.EnergyMaterial) -> None
        """For heterogeneous materials, keep track of the various sub-materials"""
        self.base_materials.append(_hb_material)

    def clear_base_materials(self):
        """Remove any existing base-materials."""
        self.base_materials = []

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d['id_num'] = self.id_num
        d['percentage_of_assembly'] = self.percentage_of_assembly
        base_mat_dict = {}
        for mat in self.base_materials:
            base_mat_dict[mat.display_name] = mat.to_dict()
        d['base_material_dict'] = base_mat_dict
        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict['id_num']
        new_prop.percentage_of_assembly = _input_dict['percentage_of_assembly']
        new_prop.clear_base_materials()
        base_mat_dict = _input_dict['base_material_dict']
        for mat_dict in base_mat_dict.values():
            new_prop.add_base_material(
                opaque.EnergyMaterial.from_dict(mat_dict)
            )
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> EnergyMaterialPhProperties
        _host = new_host or self._host
        new_obj = EnergyMaterialPhProperties(_host)
        new_obj.id_num = self.id_num
        new_obj.percentage_of_assembly = self.percentage_of_assembly
        new_obj.clear_base_materials()
        for mat in self.base_materials:
            new_obj.add_base_material(mat)
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, percentage_of_assembly={})".format(self.__class__.__name__, self.id_num, self.percentage_of_assembly)

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
