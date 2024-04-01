# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House properties for honeybee_energy.material.opaque.EnergyMaterial Objects"""

try:
    from typing import Any, List, Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_energy.material import opaque
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy:\n\t{}".format(e))

try:
    from honeybee_ph_utils.color import PhColor
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_utils:\n\t{}".format(e))


class EnergyMaterialPhProperties(object):
    def __init__(self, _host=None):
        self._host = _host
        self.id_num = 0
        self.percentage_of_assembly = 1.0
        self.base_materials = []  # type: List[opaque.EnergyMaterial]
        self._ph_color = None  # type: Optional[PhColor]

    @property
    def ph_color(self):
        # type: () -> Optional[PhColor]
        return self._ph_color

    @ph_color.setter
    def ph_color(self, _input_color):
        # type: (Optional[PhColor]) -> None
        self._ph_color = _input_color

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
        d["id_num"] = self.id_num
        d["percentage_of_assembly"] = self.percentage_of_assembly
        base_mat_dict = {}
        for mat in self.base_materials:
            base_mat_dict[mat.display_name] = mat.to_dict()
        d["base_material_dict"] = base_mat_dict

        if self.ph_color:
            d["ph_color"] = self.ph_color.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop.percentage_of_assembly = _input_dict["percentage_of_assembly"]
        new_prop.clear_base_materials()
        base_mat_dict = _input_dict["base_material_dict"]
        for mat_dict in base_mat_dict.values():
            new_prop.add_base_material(opaque.EnergyMaterial.from_dict(mat_dict))

        new_prop._ph_color = PhColor.from_dict(_input_dict.get("ph_color", None))

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
        if self.ph_color:
            new_obj.ph_color = self.ph_color.duplicate()
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, percentage_of_assembly={}, ph_color={!r})".format(
            self.__class__.__name__,
            self.id_num,
            self.percentage_of_assembly,
            self.ph_color,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialNoMassPhProperties(object):
    def __init__(self, _host=None):
        self.host = _host
        self.id_num = 0
        self._ph_color = None  # type: Optional[PhColor]

    @property
    def ph_color(self):
        # type: () -> Optional[PhColor]
        return self._ph_color

    @ph_color.setter
    def ph_color(self, _input_color):
        # type: (Optional[PhColor]) -> None
        self._ph_color = _input_color

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d["id_num"] = self.id_num

        if self.ph_color:
            d["ph_color"] = self.ph_color.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialNoMassPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop._ph_color = PhColor.from_dict(_input_dict.get("ph_color", None))
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> EnergyMaterialNoMassPhProperties
        _host = new_host or self.host
        new_obj = EnergyMaterialNoMassPhProperties(_host)
        new_obj.id_num = self.id_num
        if self.ph_color:
            new_obj.ph_color = self.ph_color.duplicate()
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialNoMassPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, ph_color={!r})".format(
            self.__class__.__name__, self.id_num, self.ph_color
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class EnergyMaterialVegetationPhProperties(object):
    def __init__(self, _host=None):
        self.host = _host
        self.id_num = 0
        self._ph_color = None  # type: Optional[PhColor]

    @property
    def ph_color(self):
        # type: () -> Optional[PhColor]
        return self._ph_color

    @ph_color.setter
    def ph_color(self, _input_color):
        # type: (Optional[PhColor]) -> None
        self._ph_color = _input_color

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        d["id_num"] = self.id_num

        if self.ph_color:
            d["ph_color"] = self.ph_color.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> EnergyMaterialVegetationPhProperties
        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop._ph_color = PhColor.from_dict(_input_dict.get("ph_color", None))
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> EnergyMaterialVegetationPhProperties
        _host = new_host or self.host
        new_obj = EnergyMaterialVegetationPhProperties(_host)
        new_obj.id_num = self.id_num
        if self.ph_color:
            new_obj.ph_color = self.ph_color.duplicate()
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> EnergyMaterialVegetationPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(id_num={!r}, ph_color={!r})".format(
            self.__class__.__name__, self.id_num, self.ph_color
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
