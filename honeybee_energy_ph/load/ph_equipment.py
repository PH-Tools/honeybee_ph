# -*- Python Version: 2.7 -*-

# -*- coding: utf-8 -*-
"""Passive House Equipments (Electric Equipment)"""


try:
    from typing import Any, TypeVar
except ImportError:
    pass  # IronPython

import sys
from honeybee_energy_ph.load import _base


class UnknownPhEquipmentTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        self.msg = 'Error: Unknown PH Equipment type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types)
        super(UnknownPhEquipmentTypeError, self).__init__(self.msg)


class PhEquipment(_base._Base):
    """Base for PH Equipment / Appliances with the common attributes."""

    defaults = {}  # Implemented by subclasses

    def __init__(self, _defaults=False):
        super(PhEquipment, self).__init__()
        self.equipment_type = self.__class__.__name__
        self.comment = None
        self.reference_quantity = 2  # Zone Occupants
        self.quantity = 0
        self.in_conditioned_space = True
        self.reference_energy_norm = 2  # Year
        self.energy_demand = 100  # kwh
        self.energy_demand_per_use = 100  # kwh/use
        self.combined_energy_factor = 0  # CEF

        self.apply_default_attr_values(_defaults)

    def apply_default_attr_values(self, _defaults):
        # type: (bool) -> None
        """Sets all the object attributes to default values, as specified in the class's "defaults" dict."""

        if not _defaults:
            return

        for k, v in self.defaults.items():
            setattr(self, k, v)

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['display_name'] = self.display_name
        d['identifier'] = self.identifier
        d['user_data'] = self.user_data

        d['equipment_type'] = self.__class__.__name__
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
        # type: (PhEquipment, dict) -> None
        """Set the base object attributes from a dictionary

        Arguments:
        ----------
            * _obj (PhEquipment): The PH Equipment to set the attributes of.
            * _input_dict (dict): The dictionary to get the attribute values from.

        Returns:
        --------
            * None
        """
        for attr_name in vars(self).keys():
            try:
                # Strip off underscore so it uses the propertry setters
                if attr_name.startswith('_'):
                    attr_name = attr_name[1:]
                setattr(_obj, attr_name, _input_dict[attr_name])
            except KeyError:
                pass
        return None


# -----------------------------------------------------------------------------
# - Appliances

class PhDishwasher(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 1,  # PH case occupants
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,  # Year
        'energy_demand': 269,  # kWh
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
        'capacity_type': 1,  # Standard
        'capacity': 12,
        'water_connection': 1,  # DHW connection
    }

    def __init__(self, _defaults=False):
        super(PhDishwasher, self).__init__(_defaults)
        self.capacity_type = 1
        self.capacity = 12
        self.water_connection = 1

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
        super(PhDishwasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity_type = _input_dict['capacity_type']
        new_obj.capacity = _input_dict['capacity']
        new_obj.water_connection = _input_dict['water_connection']
        return new_obj


class PhClothesWasher(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 1,  # PH case occupants
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,  # Year
        'energy_demand': 120,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
        'capacity': 0.1274,
        'modified_energy_factor': 2.7,
        'connection': 1,  # DHW connection
        'utilization_factor': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhClothesWasher, self).__init__(_defaults)
        self.capacity = 0.1274
        self.modified_energy_factor = 2.7
        self.connection = 1
        self.utilization_factor = 1

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhClothesWasher, self).to_dict())
        d['capacity'] = self.capacity
        d['modified_energy_factor'] = self.modified_energy_factor
        d['connection'] = self.connection
        d['utilization_factor'] = self.utilization_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhClothesWasher
        new_obj = cls()
        super(PhClothesWasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity = _input_dict['capacity']
        new_obj.modified_energy_factor = _input_dict['modified_energy_factor']
        new_obj.connection = _input_dict['connection']
        new_obj.utilization_factor = _input_dict['utilization_factor']
        return new_obj


class PhClothesDryer(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 1,  # PH case occupants
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,  # CEF - Combined Energy Factor
        'energy_demand': None,
        'energy_demand_per_use': None,
        'combined_energy_factor': 3.93,
        'dryer_type': 4,  # Condensation dryer
        'gas_consumption': None,
        'gas_efficiency_factor': 2.67,
        'field_utilization_factor_type': 1,  # Timer controls
        'field_utilization_factor': 1.18,
    }

    def __init__(self, _defaults=False):
        super(PhClothesDryer, self).__init__(_defaults)
        self.dryer_type = 4
        self.gas_consumption = 0
        self.gas_efficiency_factor = 2.67
        self.field_utilization_factor_type = 1
        self.field_utilization_factor = 1.18

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhClothesDryer, self).to_dict())
        d['dryer_type'] = self.dryer_type
        d['gas_consumption'] = self.gas_consumption
        d['gas_efficiency_factor'] = self.gas_efficiency_factor
        d['field_utilization_factor_type'] = self.field_utilization_factor_type
        d['field_utilization_factor'] = self.field_utilization_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhClothesDryer
        new_obj = cls()
        super(PhClothesDryer, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.dryer_type = _input_dict['dryer_type']
        new_obj.gas_consumption = _input_dict['gas_consumption']
        new_obj.gas_efficiency_factor = _input_dict['gas_efficiency_factor']
        new_obj.field_utilization_factor_type = _input_dict['field_utilization_factor_type']
        new_obj.field_utilization_factor = _input_dict['field_utilization_factor']
        return new_obj


class PhRefrigerator(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 4,  # PH case Units
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Day
        'energy_demand': 1.0,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
    }

    def __init__(self, _defaults=False):
        super(PhRefrigerator, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhRefrigerator, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhRefrigerator
        new_obj = cls()
        super(PhRefrigerator, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj


class PhFreezer(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 4,  # PH case Units
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Day
        'energy_demand': 2.07,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
    }

    def __init__(self, _defaults=False):
        super(PhFreezer, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhFreezer, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhFreezer
        new_obj = cls()
        super(PhFreezer, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj


class PhFridgeFreezer(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 4,  # PH case Units
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Day
        'energy_demand': 1.22,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
    }

    def __init__(self, _defaults=False):
        super(PhFridgeFreezer, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhFridgeFreezer, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhFridgeFreezer
        new_obj = cls()
        super(PhFridgeFreezer, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj


class PhCooktop(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 1,  # PH case occupants
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Use
        'energy_demand': 0.2,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
        'cooktop_type': 1,  # Cooking with electricity
    }

    def __init__(self, _defaults=False):
        super(PhCooktop, self).__init__(_defaults)
        self.cooktop_type = 1  # Electric

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhCooktop, self).to_dict())
        d['cooktop_type'] = self.cooktop_type
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCooktop
        new_obj = cls()
        super(PhCooktop, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.cooktop_type = _input_dict['cooktop_type']
        return new_obj


class PhPhiusMEL(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 3,  # Bedroooms
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Use
        'energy_demand': None,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
    }

    def __init__(self, _defaults=False):
        super(PhPhiusMEL, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhPhiusMEL, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPhiusMEL
        new_obj = cls()
        super(PhPhiusMEL, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj


class PhPhiusLightingInterior(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 6,  # PH case floor area
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Use
        'energy_demand': None,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
        'frac_high_efficiency': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhPhiusLightingInterior, self).__init__(_defaults)
        self.frac_high_efficiency = 1  # CEF

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhPhiusLightingInterior, self).to_dict())
        d['frac_high_efficiency'] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPhiusLightingInterior
        new_obj = cls()
        super(PhPhiusLightingInterior, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict['frac_high_efficiency']
        return new_obj


class PhPhiusLightingExterior(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 6,  # PH case floor area
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 1,  # Use
        'energy_demand': None,
        'energy_demand_per_use': None,
        'combined_energy_factor': None,
        'frac_high_efficiency': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhPhiusLightingExterior, self).__init__(_defaults)
        self.frac_high_efficiency = 1  # CEF

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhPhiusLightingExterior, self).to_dict())
        d['frac_high_efficiency'] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPhiusLightingExterior
        new_obj = cls()
        super(PhPhiusLightingExterior, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict['frac_high_efficiency']
        return new_obj


class PhPhiusLightingGarage(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 2,
        'quantity': 0,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,
        'energy_demand': 100,
        'energy_demand_per_use': 100,
        'combined_energy_factor': 0,
        'frac_high_efficiency': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhPhiusLightingGarage, self).__init__(_defaults)
        self.frac_high_efficiency = 1  # CEF

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhPhiusLightingGarage, self).to_dict())
        d['frac_high_efficiency'] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPhiusLightingGarage
        new_obj = cls()
        super(PhPhiusLightingGarage, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict['frac_high_efficiency']
        return new_obj


class PhCustomAnnualElectric(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 5,
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,
        'energy_demand': 0,
        'energy_demand_per_use': 0,
        'combined_energy_factor': 0,
        'frac_high_efficiency': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhCustomAnnualElectric, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhCustomAnnualElectric, self).to_dict())
        d['energy_demand'] = self.energy_demand
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCustomAnnualElectric
        new_obj = cls()
        super(PhCustomAnnualElectric, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.energy_demand = _input_dict['energy_demand']
        return new_obj


class PhCustomAnnualLighting(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 5,
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,
        'energy_demand': 0,
        'energy_demand_per_use': 0,
        'combined_energy_factor': 0,
        'frac_high_efficiency': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhCustomAnnualLighting, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhCustomAnnualLighting, self).to_dict())
        d['energy_demand'] = self.energy_demand
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCustomAnnualLighting
        new_obj = cls()
        super(PhCustomAnnualLighting, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.energy_demand = _input_dict['energy_demand']
        return new_obj


class PhCustomAnnualMEL(PhEquipment):

    defaults = {
        'comment': 'default',
        'reference_quantity': 5,
        'quantity': 1,
        'in_conditioned_space': True,
        'reference_energy_norm': 2,
        'energy_demand': 0,
        'energy_demand_per_use': 0,
        'combined_energy_factor': 0,
        'frac_high_efficiency': 1.0,
    }

    def __init__(self, _defaults=False):
        super(PhCustomAnnualMEL, self).__init__(_defaults)

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhCustomAnnualMEL, self).to_dict())
        d['energy_demand'] = self.energy_demand
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCustomAnnualMEL
        new_obj = cls()
        super(PhCustomAnnualMEL, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.energy_demand = _input_dict['energy_demand']
        return new_obj

# -----------------------------------------------------------------------------
# Collections


class PhEquipmentBuilder(object):
    """Constructor class for PH Equipment objects"""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhEquipment
        """Find the right appliance constructor class from the module based on the 'type' name."""

        equipment_type = _input_dict.get('equipment_type')
        valid_class_types = [nm for nm in dir(
            sys.modules[__name__]) if nm.startswith('Ph')]
        if equipment_type not in valid_class_types:
            raise UnknownPhEquipmentTypeError(valid_class_types, equipment_type)

        equipment_class = getattr(sys.modules[__name__], equipment_type)
        new_equipment = equipment_class.from_dict(_input_dict)

        return new_equipment

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhEquipmentCollection(object):

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
        """Adds a new piece of Ph-Equipment to the collection.

        Arguments:
        ----------
            * _new_equipment (PhEquipment): The new Ph Equipment to add to the set.
            * _key (Any): Optional key to use for storing the equipment. If None, the
                equipment's "identifier" will be used as the key.

        Returns:
        --------
            * None
        """

        key = _key or _new_equipment.identifier

        if key in self._equipment_set.keys():
            _new_equipment = self._equipment_set[key]
            return

        self._equipment_set[key] = _new_equipment
        return None

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

        for k, device in _input_dict['equipment_set'].items():
            if k not in new_obj._equipment_set.keys():
                new_obj.add_equipment(PhEquipmentBuilder.from_dict(device), k)

        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
