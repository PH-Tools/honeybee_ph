# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HB-PH Electric Equipment and Appliances."""

try:
    from typing import Any, Dict, Optional, Union
except ImportError:
    pass  # IronPython

import sys

from honeybee import room

from honeybee_energy_ph.load import _base
try:
    from honeybee_energy_ph.properties.load.equipment import ElectricEquipmentPhProperties
except ImportError:
    pass

from honeybee_ph_utils import enumerables
from honeybee_ph_utils.input_tools import input_to_int


# -----------------------------------------------------------------------------
# - Type Enums

class PhDishwasherType(enumerables.CustomEnum):
    allowed = [
        "1-DHW CONNECTION",
        "2-COLD WATER CONNECTION",
    ]

    def __init__(self, _value=1):
        # type: (Union[int, str]) -> None
        super(PhDishwasherType, self).__init__(_value)


class PhClothesWasherType(enumerables.CustomEnum):
    allowed = [
        "1-DHW CONNECTION",
        "2-COLD WATER CONNECTION",
    ]

    def __init__(self, _value=1):
        # type: (Union[int, str]) -> None
        super(PhClothesWasherType, self).__init__(_value)


class PhClothesDryerType(enumerables.CustomEnum):
    allowed = [
        "1-CLOTHES LINE",
        "2-DRYING CLOSET (COLD!)",
        "3-DRYING CLOSET (COLD!) IN EXTRACT AIR",
        "4-CONDENSATION DRYER",
        "5-ELECTRIC EXHAUST AIR DRYER",
        "6-GAS EXHAUST AIR DRYER",
    ]

    def __init__(self, _value=1):
        # type: (Union[int, str]) -> None
        super(PhClothesDryerType, self).__init__(_value)


class PhCookingType(enumerables.CustomEnum):
    allowed = [
        "1-ELECTRICITY",
        "2-NATURAL GAS",
        "3-LPG",
    ]

    def __init__(self, _value=1):
        # type: (Union[int, str]) -> None
        super(PhCookingType, self).__init__(_value)


# -----------------------------------------------------------------------------
# - Appliance Base

class PhEquipment(_base._Base):
    """Base for PH Equipment / Appliances with the common attributes."""

    def __init__(self):
        super(PhEquipment, self).__init__()
        self.equipment_type = self.__class__.__name__
        self.display_name = '_unnamed_equipment_'
        self.comment = ""
        self.reference_quantity = 2  # Zone Occupants
        self.quantity = 0
        self.in_conditioned_space = True
        self.reference_energy_norm = 2  # Year
        self.energy_demand = 0.0  # kwh
        self.energy_demand_per_use = 0.0  # kwh/use
        self.combined_energy_factor = 0.0  # CEF

    def apply_default_attr_values(self, _defaults={}):
        # type: (Dict[str, Any]) -> None
        """Sets all the object attributes to default values, as specified in a "defaults" dict."""

        if not _defaults:
            return

        for k, v in _defaults.items():
            setattr(self, k, v)

    def to_dict(self):
        # type: () -> Dict[str, Any]
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
        # type: (PhEquipment, Dict[str, Any]) -> None
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
                # Strip off underscore so it uses the property setters
                if attr_name.startswith('_'):
                    attr_name = attr_name[1:]
                setattr(_obj, attr_name, _input_dict[attr_name])
            except KeyError:
                pass
        return None

    def merge(self, other, weighting_1=1.0, weighting_2=1.0):
        # type: (PhEquipment, float, float) -> PhEquipment
        """"Merge together two pieces of PhEquipment.

        Arguments:
        ----------
            * other (PhEquipment): the PhEquipment to merge with.
            * weighting_1 (float): Optional weighting factor to apply to the 'self' equipment values.
            * weighting_2 (float): Optional weighting factor to apply to the 'other' equipment values.

        Returns:
        --------
            * (PhEquipment) The PhEquipment with updated attribute values.
        """

        if self.equipment_type != other.equipment_type:
            msg = 'Error: Cannot merge PhEquipment with type: "{}" to PhEquipment with type: "{}"'.format(
                self.equipment_type, other.equipment_type)
            raise Exception(msg)

        self.quantity += other.quantity

        # ------------
        # TODO: Should there be some sort of area-weighted averaging as well?
        # ------------

        return self

    def annual_energy_kWh(self, _ref_room=None):
        # type: (room.Room | None) -> float
        """Returns the annual energy use (kWh) of the equipment."""

        # -- To be implemented by the equipment, as appropriate.

        raise NotImplementedError(self)

    def annual_avg_wattage(self, _ref_room=None):
        # type: (room.Room | None) -> float
        """Returns the annual average wattage of the equipment."""
        return (self.annual_energy_kWh(_ref_room) * 1000) / 8760

    def __str__(self):
        return "{}(name={}, {})".format(self.__class__.__name__, self.display_name, ", ".join(["{}={}".format(str(k), str(v)) for k, v, in vars(self).items()]))

    def __repr__(self):
        return str(self)

# -----------------------------------------------------------------------------
# - Appliances


class PhDishwasher(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhDishwasher, self).__init__()
        self.display_name = "Kitchen dishwasher"
        self.capacity_type = 1
        self.capacity = 12
        self._water_connection = PhDishwasherType("1-DHW CONNECTION")
        self.apply_default_attr_values(_defaults)

    @property
    def water_connection(self):
        return self._water_connection

    @water_connection.setter
    def water_connection(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._water_connection = PhDishwasherType(input_to_int(_input))

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhDishwasher, self).to_dict())
        d['capacity_type'] = self.capacity_type
        d['capacity'] = self.capacity
        d['_water_connection'] = self._water_connection.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhDishwasher
        new_obj = cls()
        super(PhDishwasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity_type = _input_dict['capacity_type']
        new_obj.capacity = _input_dict['capacity']
        new_obj._water_connection = PhDishwasherType.from_dict(
            _input_dict['_water_connection'])
        return new_obj

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand


class PhClothesWasher(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhClothesWasher, self).__init__()
        self.display_name = "Laundry - washer"
        self.capacity = 0.1274
        self.modified_energy_factor = 2.7
        self._water_connection = PhClothesWasherType("1-DHW CONNECTION")
        self.utilization_factor = 1
        self.apply_default_attr_values(_defaults)

    @property
    def water_connection(self):
        return self._water_connection

    @water_connection.setter
    def water_connection(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._water_connection = PhClothesWasherType(input_to_int(_input))

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhClothesWasher, self).to_dict())
        d['capacity'] = self.capacity
        d['modified_energy_factor'] = self.modified_energy_factor
        d['_water_connection'] = self._water_connection.to_dict()
        d['utilization_factor'] = self.utilization_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhClothesWasher
        new_obj = cls()
        super(PhClothesWasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity = _input_dict['capacity']
        new_obj.modified_energy_factor = _input_dict['modified_energy_factor']
        new_obj._water_connection = PhClothesWasherType.from_dict(
            _input_dict['_water_connection'])
        new_obj.utilization_factor = _input_dict['utilization_factor']
        return new_obj

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand


class PhClothesDryer(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhClothesDryer, self).__init__()
        self.display_name = "Laundry - dryer"
        self._dryer_type = PhClothesDryerType("5-ELECTRIC EXHAUST AIR DRYER")
        self.gas_consumption = 0
        self.gas_efficiency_factor = 2.67
        self.field_utilization_factor_type = 1
        self.field_utilization_factor = 1.18
        self.apply_default_attr_values(_defaults)

    @property
    def dryer_type(self):
        return self._dryer_type

    @dryer_type.setter
    def dryer_type(self, _input):
        # type: (Optional[Union[int, str]]) -> None
        if _input:
            self._dryer_type = PhClothesDryerType(input_to_int(_input))

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhClothesDryer, self).to_dict())
        d['_dryer_type'] = self._dryer_type.to_dict()
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
        new_obj._dryer_type = PhClothesDryerType.from_dict(_input_dict['_dryer_type'])
        new_obj.gas_consumption = _input_dict['gas_consumption']
        new_obj.gas_efficiency_factor = _input_dict['gas_efficiency_factor']
        new_obj.field_utilization_factor_type = _input_dict['field_utilization_factor_type']
        new_obj.field_utilization_factor = _input_dict['field_utilization_factor']
        return new_obj

    def annual_energy_kWh(self, _ref_room=None):

        # TODO: Figure out how they calculate dryer energy? ANSI/Resnet?

        return 0.0


class PhRefrigerator(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhRefrigerator, self).__init__()
        self.display_name = "Kitchen refrigerator"
        self.apply_default_attr_values(_defaults)

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

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand * 365


class PhFreezer(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhFreezer, self).__init__()
        self.display_name = "Kitchen freezer"
        self.apply_default_attr_values(_defaults)

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

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand * 365


class PhFridgeFreezer(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhFridgeFreezer, self).__init__()
        self.display_name = "Kitchen fridge/freeze combo"
        self.apply_default_attr_values(_defaults)

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

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand * 365


class PhCooktop(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhCooktop, self).__init__()
        self.display_name = "Kitchen cooking"
        self._cooktop_type = PhCookingType("1-ELECTRICITY")
        self.apply_default_attr_values(_defaults)

    @property
    def cooktop_type(self):
        return self._cooktop_type

    @cooktop_type.setter
    def cooktop_type(self, _input):
        # type: (Optional[str]) -> None
        if _input:
            self._cooktop_type = PhCookingType(input_to_int(_input))

    def to_dict(self):
        # type: () -> dict
        d = {}
        d.update(super(PhCooktop, self).to_dict())
        d['_cooktop_type'] = self._cooktop_type.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCooktop
        new_obj = cls()
        super(PhCooktop, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj._cooktop_type = PhCookingType.from_dict(_input_dict['_cooktop_type'])
        return new_obj

    def annual_energy_kWh(self, _ref_room=None):
        # Num. Meals as per Phius Guidebook V3.02, pg 73 footnote #31
        annual_meals_per_occupant = 500
        num_meals = _ref_room.properties.energy.people.properties.ph.number_people * \
            annual_meals_per_occupant
        return self.energy_demand * num_meals


class PhPhiusMEL(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhPhiusMEL, self).__init__()
        self.display_name = "PHIUS+ MELS"
        self.apply_default_attr_values(_defaults)

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
    # TODO: annual_avg_wattage


class PhPhiusLightingInterior(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhPhiusLightingInterior, self).__init__()
        self.display_name = "PHIUS+ Interior Lighting"
        self.frac_high_efficiency = 1  # CEF
        self.apply_default_attr_values(_defaults)

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
    # TODO: annual_avg_wattage


class PhPhiusLightingExterior(PhEquipment):

    def __init__(self, _defaults={}):
        # type: (Dict[str, Any]) -> None
        super(PhPhiusLightingExterior, self).__init__()
        self.display_name = "PHIUS+ Exterior Lighting"
        self.frac_high_efficiency = 1  # CEF
        self.in_conditioned_space = False
        self.apply_default_attr_values(_defaults)

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhPhiusLightingExterior, self).to_dict())
        d['frac_high_efficiency'] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhPhiusLightingExterior
        new_obj = cls()
        super(PhPhiusLightingExterior, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict['frac_high_efficiency']
        return new_obj
    # TODO: annual_avg_wattage


class PhPhiusLightingGarage(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhPhiusLightingGarage, self).__init__()
        self.display_name = "PHIUS+ Garage Lighting"
        self.frac_high_efficiency = 1  # CEF
        self.in_conditioned_space = False
        self.apply_default_attr_values(_defaults)

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhPhiusLightingGarage, self).to_dict())
        d['frac_high_efficiency'] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhPhiusLightingGarage
        new_obj = cls()
        super(PhPhiusLightingGarage, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict['frac_high_efficiency']
        return new_obj
    # TODO:  annual_avg_wattage


class PhCustomAnnualElectric(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhCustomAnnualElectric, self).__init__()
        self.display_name = "User defined"
        self.apply_default_attr_values(_defaults)

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

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand


class PhCustomAnnualLighting(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhCustomAnnualLighting, self).__init__()
        self.display_name = "User defined - lighting"
        self.apply_default_attr_values(_defaults)

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

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand


class PhCustomAnnualMEL(PhEquipment):

    def __init__(self, _defaults={}):
        super(PhCustomAnnualMEL, self).__init__()
        self.display_name = "User defined - Misc electric loads"
        self.apply_default_attr_values(_defaults)

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

    def annual_energy_kWh(self, _ref_room=None):
        return self.energy_demand

# -- Elevator classes

class PhElevatorHydraulic(PhEquipment):
    
    def __init__(self, _num_dwellings=1):
        super(PhElevatorHydraulic, self).__init__()
        self.display_name = "User defined - Misc electric loads"
        self.comment = "Elevator - Hydraulic"
        self.set_energy_demand(_num_dwellings)
        self.quantity = 1
    
    def set_energy_demand(self, _num_dwellings):
        """Set the annual energy demand (kWh) based on the number of dwelling units"""
        if _num_dwellings <= 6:
            self.energy_demand = 1910.0
        elif _num_dwellings <= 20:
            self.energy_demand = 2150.0
        elif _num_dwellings <= 50:
            self.energy_demand = 2940.0
        else:
            self.energy_demand = 4120.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhElevatorHydraulic, self).to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhElevatorHydraulic
        new_obj = cls()
        super(PhElevatorHydraulic, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        return new_obj


class PhElevatorGearedTraction(PhEquipment):
    
    def __init__(self, _num_dwellings=1):
        super(PhElevatorGearedTraction, self).__init__()
        self.display_name = "User defined - Misc electric loads"
        self.comment = "Elevator - Geared Traction"
        self.set_energy_demand(_num_dwellings)
        self.quantity = 1

    def set_energy_demand(self, _num_dwellings):
        """Set the annual energy demand (kWh) based on the number of dwelling units"""
        if _num_dwellings <= 6:
            self.energy_demand = 3150.0
        elif _num_dwellings <= 20:
            self.energy_demand = 3150.0
        elif _num_dwellings <= 50:
            self.energy_demand = 3150.0
        else:
            self.energy_demand = 4550.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhElevatorGearedTraction, self).to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhElevatorGearedTraction
        new_obj = cls()
        super(PhElevatorGearedTraction, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        return new_obj


class PhElevatorGearlessTraction(PhEquipment):
    
    def __init__(self, _num_dwellings=1):
        super(PhElevatorGearlessTraction, self).__init__()
        self.display_name = "User defined - Misc electric loads"
        self.comment = "Elevator - Gearless Traction"
        self.set_energy_demand(_num_dwellings)
        self.quantity = 1

    def set_energy_demand(self, _num_dwellings):
        """Set the annual energy demand (kWh) based on the number of dwelling units"""
        if _num_dwellings <= 6:
            self.energy_demand = 7570.0
        elif _num_dwellings <= 20:
            self.energy_demand = 7570.0
        elif _num_dwellings <= 50:
            self.energy_demand = 7570.0
        else:
            self.energy_demand = 7570.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhElevatorGearlessTraction, self).to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhElevatorGearlessTraction
        new_obj = cls()
        super(PhElevatorGearlessTraction, new_obj).base_attrs_from_dict(new_obj, _input_dict)
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
            msg = 'Error: Unknown PH Equipment type? Got: "{}" but only types: {} are allowed?'.format(
                valid_class_types, equipment_type)
            raise Exception(msg)

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
    """A Collection of PH-Equipment / Appliances.

    This is stored on the Honeybee-Room's properties.energy.electric_equipment.properties.ph
    """

    def __init__(self, _host):
        self._equipment_set = {}
        self._host = _host

    @property
    def host(self):
        # type: () -> ElectricEquipmentPhProperties
        return self._host

    def items(self):
        return self._equipment_set.items()

    def keys(self):
        return self._equipment_set.keys()

    def values(self):
        return self._equipment_set.values()

    def duplicate(self, new_host=None):
        # type: (Any) -> PhEquipmentCollection
        return self.__copy__(new_host)

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

    def remove_all_equipment(self):
        """Reset the Collection to an empty set."""
        self._equipment_set = {}

    def total_collection_wattage(self, _hb_room):
        # type: (room.Room) -> float
        """Returns the total annual-average-wattage of the appliances.

        This value assumes constant 24/7 operation (PH-Style modeling).

        Arguments:
        ----------
            * _hb_room (room.Room): The reference Honeybee-Room to get occupancy from.

        Returns:
        --------
            * (float): total Wattage of all installed PH-Equipment in the collection.
        """
        return sum(equip.annual_avg_wattage(_hb_room) for equip in self.values())

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

    def __iter__(self):
        for _ in self._equipment_set.items():
            yield _

    def __setitem__(self, key, attr):
        self._equipment_set[key] = attr

    def __getitem__(self, key):
        return self._equipment_set[key]

    def __copy__(self, new_host=None):
        # type: (Any) -> PhEquipmentCollection
        host = new_host or self._host

        new_obj = self.__class__(host)
        for k, v in self._equipment_set.items():
            new_obj.add_equipment(v, k)

        return new_obj

    def __str__(self):
        return '{}({} pieces of equipment)'.format(self.__class__.__name__, len(self._equipment_set.keys()))

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
