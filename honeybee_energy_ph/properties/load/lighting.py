# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties for Honeybee-Energy-PH | Load | Lighting"""

try:
    from typing import Any
except ImportError:
    pass  # Python 2.7

try:
    from honeybee_energy_ph.load.ph_equipment import PhEquipment, PhEquipmentBuilder
except ImportError as e:
    raise ImportError('Failed to import honeybee_energy_ph', e)


class LightingPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(LightingPhProperties_FromDictError, self).__init__(self.msg)


class LightingPhProperties(object):
    """Ph Properties for Honeybee-Energy Lighting"""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.target_lux = 300
        self.target_lux_height = 0.8  # m
        self._ph_equipment = None

    @property
    def ph_equipment(self):
        # type: () -> PhEquipment | None
        return self._ph_equipment
    
    @ph_equipment.setter
    def ph_equipment(self, _equipment):
        # type: (PhEquipment) -> None
        if not isinstance(_equipment, PhEquipment):
            raise ValueError("Input must be of type PhEquipment")
        self._ph_equipment = _equipment
    
    def duplicate(self, new_host=None):
        # type: (Any) -> LightingPhProperties
        return self.__copy__(new_host)
    
    def __copy__(self, new_host=None):
        # type: (Any) -> LightingPhProperties
        _host = new_host or self._host

        new_obj = self.__class__(_host)
        new_obj.id_num = self.id_num
        new_obj.target_lux = self.target_lux
        new_obj.target_lux_height = self.target_lux_height
        if self._ph_equipment:
            new_obj.ph_equipment = PhEquipmentBuilder.from_dict(self._ph_equipment.to_dict(), _host=new_obj)
        
        return new_obj

    @property
    def host(self):
        return self._host

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}

        if abridged:
            d["type"] = "LightingPhPropertiesAbridged"
        else:
            d["type"] = "LightingPhProperties"

        d["id_num"] = self.id_num
        d["target_lux"] = self.target_lux
        d["target_lux_height"] = self.target_lux_height
        if self._ph_equipment:
            d["equipment"] = self._ph_equipment.to_dict(_abridged=abridged)

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (dict, Any) -> LightingPhProperties
        valid_types = ("LightingPhProperties", "LightingPhPropertiesAbridged")
        if _input_dict["type"] not in valid_types:
            raise LightingPhProperties_FromDictError(valid_types, _input_dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _input_dict["id_num"]
        new_prop.target_lux = _input_dict["target_lux"]
        new_prop.target_lux_height = _input_dict["target_lux_height"]
        if "equipment" in _input_dict:
            new_prop.ph_equipment = PhEquipmentBuilder.from_dict(_input_dict["equipment"], _host=new_prop)

        return new_prop
