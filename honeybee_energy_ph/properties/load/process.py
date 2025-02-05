# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Process Equipment PH-Properties"""

try:
    from typing import Any
except:
    pass  # IronPython


try:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from honeybee_energy.properties.extension import ProcessProperties
except ImportError as e:
    pass  # IronPython


try:
    from honeybee_energy_ph.load.ph_equipment import PhEquipment, PhEquipmentBuilder
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy_ph", e)


class ProcessPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(ProcessPhProperties_FromDictError, self).__init__(self.msg)


class ProcessPhProperties(object):
    def __init__(self, _host):
        # type: (ProcessProperties) -> None
        self._host = _host
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

    @property
    def host(self):
        # type: () -> ProcessProperties
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict
        d = {}

        if abridged:
            d["type"] = "ProcessPhPropertiesAbridged"
        else:
            d["type"] = "ProcessPhProperties"

        if self._ph_equipment:
            d["equipment"] = self._ph_equipment.to_dict(_abridged=abridged)

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> ProcessPhProperties
        valid_types = (
            "ProcessPhProperties",
            "ProcessPhPropertiesAbridged",
        )
        if _input_dict["type"] not in valid_types:
            raise ProcessPhProperties_FromDictError(valid_types, _input_dict["type"])

        new_prop = cls(_host)

        if "equipment" in _input_dict:
            new_prop.ph_equipment = PhEquipmentBuilder.from_dict(_input_dict["equipment"], _host=new_prop)

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        # type: (dict) -> None
        return None

    def __copy__(self, new_host=None):
        # type: (ProcessProperties | None) -> ProcessPhProperties
        host = new_host or self._host
        new_obj = self.__class__(host)
        if self._ph_equipment:
            new_obj.ph_equipment = PhEquipmentBuilder.from_dict(self._ph_equipment.to_dict(), _host=new_obj)
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> ProcessPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
