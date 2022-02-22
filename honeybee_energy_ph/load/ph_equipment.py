# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House Equipments (Electric Equipment)"""


try:
    from typing import Any
except ImportError:
    pass  # IronPython

from honeybee_energy_ph.load import _base


class UnknownPhEquipmentTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        self.msg = 'Error: Unknown PH Equipment type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types)
        super(UnknownPhEquipmentTypeError, self).__init__(self.msg)


class PhEquipment(_base._Base):
    """Base for PH Equipments with common attributes."""

    def __init__(self):
        super(PhEquipment, self).__init__()
        self.equipment_type = 1
        self.display_name = ""
        self.comment = None
        self.reference_quantity = 2  # Zone Occupants
        self.quantity = 0
        self.in_conditioned_space = True
        self.reference_energy_norm = 2  # Year
        self.energy_demand = 100  # kwh
        self.energy_demand_per_use = 100  # kwh/use
        self.combined_energy_factor = 0  # CEF

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['equipment_type'] = self.equipment_type
        d['display_name'] = self.display_name
        d['comment'] = self.comment
        d['reference_quantity'] = self.reference_quantity
        d['quantity'] = self.quantity  # = 0
        d['in_conditioned_space'] = self.in_conditioned_space
        d['reference_energy_norm'] = self.reference_energy_norm
        d['energy_demand'] = self.energy_demand
        d['energy_demand_per_use'] = self.energy_demand_per_use
        d['combined_energy_factor'] = self.combined_energy_factor

        return d

    def base_attrs_from_dict(self, _obj, _input_dict):
        # type: (PhEquipment, dict) -> Any
        """Set the base object attributes from a dictionary

        Arguments:
        ----------
            * _obj (PhEquipment): The PH Equipment to set the attributes of.
            * _input_dict (dict): The dictionary to get the attribute values from.

        Returns:
        --------
            * (PhEquipment): The input PhEquipment object, with its attribute values set.
        """
        for var in vars(self):
            if str(var).startswith('_'):
                continue
            try:
                setattr(_obj, var, _input_dict[var])
            except KeyError:
                pass

        return _obj


class PhDishwasher(PhEquipment):
    def __init__(self):
        super(PhDishwasher, self).__init__()
        self.capacity_type = 1  # standard
        self.capacity = 12
        self.water_connection = 1  # DHW Connection

    def to_dict(self):
        # type: () -> dict
        d = {}

        d.update(super(PhDishwasher, self).to_dict())
        d['capacity_type'] = self.capacity_type
        d['capacity'] = self.capacity
        d['water_connection'] = self.water_connection

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhDishwasher
        new_obj = cls()

        new_obj = super(PhDishwasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity_type = _input_dict['capacity_type']
        new_obj.capacity = _input_dict['capacity']
        new_obj.water_connection = _input_dict['water_connection']

        return new_obj


# ---

class PhEquipmentBuilder(object):
    """Constructor class for PH Equipment objects"""

    equipment = {
        'PhDishwasher': PhDishwasher,
    }

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhEquipment

        equipment_type = _input_dict.get('equipment_type')
        if equipment_type is None:
            raise UnknownPhEquipmentTypeError(cls.equipment.keys(), equipment_type)

        equipment_class = cls.equipment[equipment_type]
        new_equipment = equipment_class.from_dict(_input_dict)

        return new_equipment

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhEquipmentCollection(object):
    """Singleton"""

    def __init__(self, _host):
        self._equipment_set = {}
        self._host = _host

    @property
    def equipment(self):
        # type: () -> list[PhEquipment]
        return list(self._equipment_set.values())

    @property
    def host(self):
        return self._host

    def duplicate(self, new_host=None):
        # type: (Any) -> PhEquipmentCollection
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Any) -> PhEquipmentCollection
        host = new_host or self._host

        new_obj = self.__class__(host)
        for k, v in self._equipment_set.items():
            new_obj.add_equipment(v, k)

        return new_obj

    def add_equipment(self, _new_equipment, _key=None):
        # type: (PhEquipment, Any) -> None
        key = _key or _new_equipment.identifier

        if key in self._equipment_set.keys():
            return

        self._equipment_set[key] = _new_equipment

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['equipment_set'] = {}
        for key, device in self._equipment_set.items():
            d['equipment_set'][key] = device.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> PhEquipmentCollection
        new_obj = cls(_host)

        for k, d in _input_dict['equipment_set'].items():
            new_obj.add_equipment(PhEquipmentBuilder.from_dict(d), k)

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
