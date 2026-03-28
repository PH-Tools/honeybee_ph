# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""HB-PH Electric Equipment and Appliances."""

import sys

try:
    from typing import Any, ItemsView, Iterator, KeysView, Type, ValuesView
except ImportError:
    pass  # IronPython

try:
    from honeybee import room
except ImportError as e:
    raise ImportError("Failed to import room: {}".format(e))

try:
    from honeybee_energy.schedule.ruleset import ScheduleRuleset
except ImportError as e:
    raise ImportError("Failed to import RoomEnergyProperties: {}".format(e))

try:
    from honeybee_energy_ph.load import _base
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy_ph: {}".format(e))

try:
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from honeybee_energy_ph.properties.load.equipment import ElectricEquipmentPhProperties
        from honeybee_energy_ph.properties.load.lighting import LightingPhProperties
        from honeybee_energy_ph.properties.load.process import ProcessPhProperties
except ImportError:
    pass  # IronPython

try:
    from honeybee_ph_utils.input_tools import input_to_int
except ImportError as e:
    raise ImportError("Failed to import honeybee_ph_utils: {}".format(e))

try:
    from honeybee_ph_standards.programtypes.default_elec_equip import ph_default_equip
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_standards:\n\t{}".format(e))

try:
    from honeybee_energy_ph.load import phius_residential
    from honeybee_energy_ph.load._ph_equip_types import (
        PhClothesDryerType,
        PhClothesWasherType,
        PhCookingType,
        PhDishwasherType,
    )
except ImportError as e:
    raise ImportError("Failed to import PhEquipment types: {}".format(e))


# -----------------------------------------------------------------------------
# - Appliance Base


class PhEquipment(_base._Base):
    """Base for PH Equipment / Appliances with the common attributes."""

    _phi_default = None
    _phius_default = None

    def __init__(self, _host=None, _defaults={}):
        # type: (ProcessPhProperties | None, dict) -> None
        super(PhEquipment, self).__init__()
        self.host = _host
        self.equipment_type = self.__class__.__name__
        self.display_name = "_unnamed_equipment_"
        self.comment = ""
        self.reference_quantity = 2  # Zone Occupants
        self.quantity = 0
        self.in_conditioned_space = True
        self.reference_energy_norm = 2  # Year
        self.energy_demand = 0.0  # kwh
        self.energy_demand_per_use = 0.0  # kwh/use
        self.combined_energy_factor = 0.0  # CEF

    def apply_default_attr_values(self, _defaults={}):
        # type: (dict[str, Any]) -> None
        """Sets all the object attributes to default values, as specified in a "defaults" dict."""

        if not _defaults:
            return

        for k, v in _defaults.items():
            setattr(self, k, v)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}

        d["display_name"] = self.display_name
        d["identifier"] = self.identifier
        d["user_data"] = self.user_data

        d["equipment_type"] = self.__class__.__name__
        d["comment"] = self.comment
        d["reference_quantity"] = self.reference_quantity
        d["quantity"] = self.quantity  # = 0
        d["in_conditioned_space"] = self.in_conditioned_space
        d["reference_energy_norm"] = self.reference_energy_norm
        d["energy_demand"] = self.energy_demand
        d["energy_demand_per_use"] = self.energy_demand_per_use
        d["combined_energy_factor"] = self.combined_energy_factor

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhEquipment
        """Set the object attributes from a dictionary"""

        # -- To be implemented by the equipment, as appropriate.

        raise NotImplementedError(cls)

    def base_attrs_from_dict(self, _obj, _input_dict):
        # type: (PhEquipment, dict[str, Any]) -> None
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
                if attr_name.startswith("_"):
                    attr_name = attr_name[1:]
                setattr(_obj, attr_name, _input_dict[attr_name])
            except KeyError:
                pass
        return None

    def merge(self, other, weighting_1=1.0, weighting_2=1.0):
        # type: (PhEquipment, float, float) -> PhEquipment
        """ "Merge together two pieces of PhEquipment.

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
                self.equipment_type, other.equipment_type
            )
            raise Exception(msg)

        self.quantity += other.quantity

        # ------------
        # TODO: Should there be some sort of area-weighted averaging as well?
        # ------------

        return self

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, *Any) -> float
        """Returns the annual energy use (kWh) of the equipment."""

        # -- To be implemented by the equipment, as appropriate.

        raise NotImplementedError(self)

    def annual_avg_wattage(self, _schedule=None, *args, **kwargs):
        # type: ( ScheduleRuleset | None, *Any, **Any) -> float
        """Returns the annual average wattage of the equipment."""

        if _schedule is not None:
            # -- Consider the host schedule....
            sched_factor_sum = sum(_schedule.values())
        else:
            sched_factor_sum = 8760

        annual_energy_Wh = self.annual_energy_kWh(*args, **kwargs) * 1000
        return annual_energy_Wh / sched_factor_sum

    def __str__(self):
        # type: () -> str
        return "{}(display_name={}, {})".format(
            self.__class__.__name__,
            self.display_name,
            ", ".join(["{}={}".format(str(k), str(v)) for k, v, in vars(self).items()]),
        )

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return str(self)

    @classmethod
    def phius_default(cls):
        # type: () -> 'PhEquipment'
        """Return the default instance of the object."""
        if not cls._phius_default:
            cls._phius_default = cls(_defaults=ph_default_equip[cls.__name__]["PHIUS"])
        return cls._phius_default

    @classmethod
    def phi_default(cls):
        # type: () -> 'PhEquipment'
        """Return the default instance of the object."""
        if not cls._phi_default:
            cls._phi_default = cls(_defaults=ph_default_equip[cls.__name__]["PHI"])
        return cls._phi_default


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
        # type: (str | int | None) -> None
        if _input:
            _input = input_to_int(_input)
            if not _input:
                raise ValueError("Invalid input for water_connection: {}".format(_input))
            self._water_connection = PhDishwasherType(_input)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhDishwasher, self).to_dict())
        d["capacity_type"] = self.capacity_type
        d["capacity"] = self.capacity
        d["_water_connection"] = self._water_connection.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhDishwasher
        new_obj = cls()
        super(PhDishwasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity_type = _input_dict["capacity_type"]
        new_obj.capacity = _input_dict["capacity"]
        new_obj._water_connection = PhDishwasherType.from_dict(_input_dict["_water_connection"])
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
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
        # type: (str | int | None) -> None
        if _input:
            _input = input_to_int(_input)
            if not _input:
                raise ValueError("Invalid input for water_connection: {}".format(_input))
            self._water_connection = PhClothesWasherType(_input)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhClothesWasher, self).to_dict())
        d["capacity"] = self.capacity
        d["modified_energy_factor"] = self.modified_energy_factor
        d["_water_connection"] = self._water_connection.to_dict()
        d["utilization_factor"] = self.utilization_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhClothesWasher
        new_obj = cls()
        super(PhClothesWasher, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.capacity = _input_dict["capacity"]
        new_obj.modified_energy_factor = _input_dict["modified_energy_factor"]
        new_obj._water_connection = PhClothesWasherType.from_dict(_input_dict["_water_connection"])
        new_obj.utilization_factor = _input_dict["utilization_factor"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
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
        # type: (str | int | None) -> None
        if _input:
            _input = input_to_int(_input)
            if not _input:
                raise ValueError("Invalid input for dryer_type: {}".format(_input))
            self._dryer_type = PhClothesDryerType(_input)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhClothesDryer, self).to_dict())
        d["_dryer_type"] = self._dryer_type.to_dict()
        d["gas_consumption"] = self.gas_consumption
        d["gas_efficiency_factor"] = self.gas_efficiency_factor
        d["field_utilization_factor_type"] = self.field_utilization_factor_type
        d["field_utilization_factor"] = self.field_utilization_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhClothesDryer
        new_obj = cls()
        super(PhClothesDryer, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj._dryer_type = PhClothesDryerType.from_dict(_input_dict["_dryer_type"])
        new_obj.gas_consumption = _input_dict["gas_consumption"]
        new_obj.gas_efficiency_factor = _input_dict["gas_efficiency_factor"]
        new_obj.field_utilization_factor_type = _input_dict["field_utilization_factor_type"]
        new_obj.field_utilization_factor = _input_dict["field_utilization_factor"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Returns the annual energy use (kWh) of the equipment."""
        # -- Appendix N - Normative | Phius 2024 Certification Guidebook v24.1.1
        # -- Table 11.6.4.0 prescriptive Path Appliance, Lighting and DHW REference Efficiencies

        _num_occupants = kwargs.get("_num_occupants", None)
        if _num_occupants is None:
            raise ValueError(
                "'_num_occupants' input is required for the annual_energy_kWh method. Got only: {}".format(kwargs)
            )
        try:
            return _num_occupants * (283 / 4.5) / self.combined_energy_factor * 8.45
        except ZeroDivisionError:
            return 0


class PhRefrigerator(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhRefrigerator, self).__init__()
        self.display_name = "Kitchen refrigerator"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhRefrigerator, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhRefrigerator
        new_obj = cls()
        super(PhRefrigerator, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        return self.energy_demand * 365


class PhFreezer(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhFreezer, self).__init__()
        self.display_name = "Kitchen freezer"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhFreezer, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhFreezer
        new_obj = cls()
        super(PhFreezer, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        return self.energy_demand * 365


class PhFridgeFreezer(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhFridgeFreezer, self).__init__()
        self.display_name = "Kitchen fridge/freeze combo"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhFridgeFreezer, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhFridgeFreezer
        new_obj = cls()
        super(PhFridgeFreezer, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
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
        # type: (str | int | None) -> None
        if _input:
            _input = input_to_int(_input)
            if not _input:
                raise ValueError("Invalid input for cooktop_type: {}".format(_input))
            self._cooktop_type = PhCookingType(_input)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhCooktop, self).to_dict())
        d["_cooktop_type"] = self._cooktop_type.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCooktop
        new_obj = cls()
        super(PhCooktop, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj._cooktop_type = PhCookingType.from_dict(_input_dict["_cooktop_type"])
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Return annual energy consumption [kWh] for a single dwelling."""

        _num_occupants = kwargs.get("_num_occupants", None)
        if _num_occupants is None:
            raise ValueError("'_num_occupants' input is required for the annual_energy_kWh method.")

        return phius_residential.cooktop(_num_occupants, self.energy_demand)


class PhPhiusMEL(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhPhiusMEL, self).__init__()
        self.display_name = "PHIUS+ MELS"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhPhiusMEL, self).to_dict())

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPhiusMEL
        new_obj = cls()
        super(PhPhiusMEL, new_obj).base_attrs_from_dict(new_obj, _input_dict)

        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Return annual energy consumption [kWh] for a single dwelling."""

        _num_bedrooms = kwargs.get("_num_bedrooms", None)
        if _num_bedrooms is None:
            raise ValueError("'_num_bedrooms' input is required for the annual_energy_kWh method.")

        _floor_area_ft2 = kwargs.get("_floor_area_ft2", None)
        if _floor_area_ft2 is None:
            raise ValueError("'_floor_area_ft2' input is required for the annual_energy_kWh method.")

        return phius_residential.misc_electrical(_num_bedrooms, _floor_area_ft2)


class PhPhiusLightingInterior(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhPhiusLightingInterior, self).__init__()
        self.display_name = "PHIUS+ Interior Lighting"
        self.frac_high_efficiency = 1  # CEF
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhPhiusLightingInterior, self).to_dict())
        d["frac_high_efficiency"] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPhiusLightingInterior
        new_obj = cls()
        super(PhPhiusLightingInterior, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict["frac_high_efficiency"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Return the annual energy consumption [kWh] for a single dwelling."""

        _floor_area_ft2 = kwargs.get("_floor_area_ft2", None)
        if _floor_area_ft2 is None:
            raise ValueError("'_floor_area_ft2' input is required for the annual_energy_kWh method.")

        return phius_residential.lighting_interior(_floor_area_ft2, self.frac_high_efficiency)


class PhPhiusLightingExterior(PhEquipment):
    def __init__(self, _defaults={}):
        # type: (dict[str, Any]) -> None
        super(PhPhiusLightingExterior, self).__init__()
        self.display_name = "PHIUS+ Exterior Lighting"
        self.frac_high_efficiency = 1  # CEF
        self.in_conditioned_space = False
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhPhiusLightingExterior, self).to_dict())
        d["frac_high_efficiency"] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhPhiusLightingExterior
        new_obj = cls()
        super(PhPhiusLightingExterior, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict["frac_high_efficiency"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Return the annual energy consumption [kWh] for a single dwelling."""

        _num_bedrooms = kwargs.get("_num_bedrooms", None)
        if _num_bedrooms is None:
            raise ValueError("'_num_bedrooms' input is required for the annual_energy_kWh method.")

        _floor_area_ft2 = kwargs.get("_floor_area_ft2", None)
        if _floor_area_ft2 is None:
            raise ValueError("'_floor_area_ft2' input is required for the annual_energy_kWh method.")

        return phius_residential.lighting_exterior(_floor_area_ft2, self.frac_high_efficiency)


class PhPhiusLightingGarage(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhPhiusLightingGarage, self).__init__()
        self.display_name = "PHIUS+ Garage Lighting"
        self.frac_high_efficiency = 1  # CEF
        self.in_conditioned_space = False
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhPhiusLightingGarage, self).to_dict())
        d["frac_high_efficiency"] = self.frac_high_efficiency
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhPhiusLightingGarage
        new_obj = cls()
        super(PhPhiusLightingGarage, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.frac_high_efficiency = _input_dict["frac_high_efficiency"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Return the annual energy consumption [kWh] for a single dwelling."""

        return phius_residential.lighting_garage(self.frac_high_efficiency)


class PhCustomAnnualElectric(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhCustomAnnualElectric, self).__init__()
        self.display_name = "User defined"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhCustomAnnualElectric, self).to_dict())
        d["energy_demand"] = self.energy_demand
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCustomAnnualElectric
        new_obj = cls()
        super(PhCustomAnnualElectric, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.energy_demand = _input_dict["energy_demand"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        return self.energy_demand


class PhCustomAnnualLighting(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhCustomAnnualLighting, self).__init__()
        self.display_name = "User defined - lighting"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhCustomAnnualLighting, self).to_dict())
        d["energy_demand"] = self.energy_demand
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCustomAnnualLighting
        new_obj = cls()
        super(PhCustomAnnualLighting, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.energy_demand = _input_dict["energy_demand"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        return self.energy_demand


class PhCustomAnnualMEL(PhEquipment):
    def __init__(self, _defaults={}):
        super(PhCustomAnnualMEL, self).__init__()
        self.display_name = "User defined - Misc electric loads"
        self.apply_default_attr_values(_defaults)

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhCustomAnnualMEL, self).to_dict())
        d["energy_demand"] = self.energy_demand
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhCustomAnnualMEL
        new_obj = cls()
        super(PhCustomAnnualMEL, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.energy_demand = _input_dict["energy_demand"]
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
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

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhElevatorHydraulic, self).to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhElevatorHydraulic
        new_obj = cls()
        super(PhElevatorHydraulic, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Returns the annual energy use (kWh) of the equipment."""
        return self.energy_demand


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

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhElevatorGearedTraction, self).to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhElevatorGearedTraction
        new_obj = cls()
        super(PhElevatorGearedTraction, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Returns the annual energy use (kWh) of the equipment."""
        return self.energy_demand


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

    def to_dict(self, _abridged=False):
        # type: (bool) -> dict
        d = {}
        d.update(super(PhElevatorGearlessTraction, self).to_dict())
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhElevatorGearlessTraction
        new_obj = cls()
        super(PhElevatorGearlessTraction, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        return new_obj

    def annual_energy_kWh(self, *args, **kwargs):
        # type: (*Any, **Any) -> float
        """Returns the annual energy use (kWh) of the equipment."""
        return self.energy_demand


def phius_elevator_by_stories(_num_of_stories):
    # type: (int) -> Type[PhElevatorHydraulic | PhElevatorGearedTraction | PhElevatorGearlessTraction]
    """Return the Elevator class, based on the number of stories."""
    if _num_of_stories <= 6:
        return PhElevatorHydraulic
    elif _num_of_stories <= 20:
        return PhElevatorGearedTraction
    else:
        return PhElevatorGearlessTraction


# -----------------------------------------------------------------------------
# Collections

# TODO: Deprecate these classes in favor of new the "Process Load" method.
# See: honeybee_energy_ph.load.process.py


class PhEquipmentBuilder(object):
    """Constructor class for PH Equipment objects"""

    @classmethod
    def from_dict(cls, _input_dict, _host=None):
        # type: (dict, ProcessPhProperties | LightingPhProperties | None) -> PhEquipment
        """Find the right appliance constructor class from the module based on the 'type' name."""

        equipment_type = _input_dict["equipment_type"]
        valid_class_types = [nm for nm in dir(sys.modules[__name__]) if nm.startswith("Ph")]
        if equipment_type not in valid_class_types:
            msg = 'Error: Unknown PH Equipment type? Got: "{}" but only types: {} are allowed?'.format(
                valid_class_types, equipment_type
            )
            raise Exception(msg)

        equipment_class = getattr(sys.modules[__name__], equipment_type)  # type: Type[PhEquipment]
        new_equipment = equipment_class.from_dict(_input_dict)

        return new_equipment

    def __str__(self):
        # type: () -> str
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return str(self)


class PhEquipmentCollection(object):
    """A Collection of PH-Equipment / Appliances.

    This is stored on the Honeybee-Room's properties.energy.electric_equipment.properties.ph
    """

    def __init__(self, _host=None):
        # type: (ElectricEquipmentPhProperties | None) -> None
        self._equipment_set = {}  # type: dict[str, PhEquipment]
        self._host = _host

    @property
    def host(self):
        # type: () -> ElectricEquipmentPhProperties | None
        return self._host

    def items(self):
        # type: () -> ItemsView[str, PhEquipment]
        return self._equipment_set.items()

    def keys(self):
        # type: () -> KeysView[str]
        return self._equipment_set.keys()

    def values(self):
        # type: () -> ValuesView[PhEquipment]
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
        # type: () -> None
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
        return sum(equip.annual_avg_wattage(_hb_room) for equip in self.values())  # type: ignore

    def to_dict(self):
        # type: () -> dict
        d = {}

        d["equipment_set"] = {}
        for key, device in self._equipment_set.items():
            d["equipment_set"][key] = device.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> PhEquipmentCollection
        new_obj = cls(_host)

        for k, device in _input_dict["equipment_set"].items():
            if k not in new_obj._equipment_set.keys():
                new_obj.add_equipment(PhEquipmentBuilder.from_dict(device), k)

        return new_obj

    def __iter__(self):
        # type: () -> Iterator[tuple[str, PhEquipment]]
        for _ in self._equipment_set.items():
            yield _

    def __setitem__(self, key, attr):
        # type: (str, PhEquipment) -> None
        self._equipment_set[key] = attr

    def __getitem__(self, key):
        # type: (str) -> PhEquipment
        return self._equipment_set[key]

    def __copy__(self, new_host=None):
        # type: (Any) -> PhEquipmentCollection
        host = new_host or self._host

        new_obj = self.__class__(host)
        for k, v in self._equipment_set.items():
            new_obj.add_equipment(v, k)

        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}({} pieces of equipment)".format(self.__class__.__name__, len(self._equipment_set.keys()))

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return str(self)
