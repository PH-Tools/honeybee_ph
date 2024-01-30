# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Electric Equipment"""

try:
    from typing import Any
except:
    pass  # IronPython

from honeybee_energy_ph.load import ph_equipment


class ElectricEquipmentPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(ElectricEquipmentPhProperties_FromDictError, self).__init__(self.msg)


class ElectricEquipmentPhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.equipment_collection = ph_equipment.PhEquipmentCollection(self)

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict
        d = {}

        if abridged:
            d["type"] = "ElectricEquipmentPhPropertiesAbridged"
        else:
            d["type"] = "ElectricEquipmentPhProperties"

        d["equipment_collection"] = self.equipment_collection.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> ElectricEquipmentPhProperties
        valid_types = (
            "ElectricEquipmentPhProperties",
            "ElectricEquipmentPhPropertiesAbridged",
        )
        if _input_dict["type"] not in valid_types:
            raise ElectricEquipmentPhProperties_FromDictError(
                valid_types, _input_dict["type"]
            )

        new_prop = cls(_host)

        new_prop.equipment_collection = ph_equipment.PhEquipmentCollection.from_dict(
            _input_dict["equipment_collection"], _host=new_prop
        )

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> ElectricEquipmentPhProperties
        host = new_host or self._host
        new_obj = self.__class__(host)
        new_obj.equipment_collection = self.equipment_collection.duplicate(host)
        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> ElectricEquipmentPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return "{}(equipment_collection={})".format(
            self.__class__.__name__, self.equipment_collection
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
