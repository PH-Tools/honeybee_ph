# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBPH Renewable Energy Objects"""

import sys

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_energy_ph.hvac import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph:\n\t{}".format(e))


class UnknownPhRenewableEnergyTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        # type: (list[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Heating-SubSystem type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhRenewableEnergyTypeError, self).__init__(self.msg)


class PhRenewableEnergyDevice(_base._PhHVACBase):
    """Base class for all HBPH Renewable Energy Systems (PV, etc)."""

    def __init__(self):
        super(PhRenewableEnergyDevice, self).__init__()
        self.device_typename = self.__class__.__name__
        self.percent_coverage = 1.0

    def to_dict(self):
        # type: () -> dict
        d = super(PhRenewableEnergyDevice, self).to_dict()
        d["device_typename"] = self.device_typename
        d["percent_coverage"] = self.percent_coverage
        return d

    def base_attrs_from_dict(self, _input_dict):
        # type: (PhRenewableEnergyDevice, dict) -> PhRenewableEnergyDevice
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.user_data = _input_dict["user_data"]
        self.device_typename = _input_dict["device_typename"]
        self.percent_coverage = _input_dict["percent_coverage"]
        return self

    def check_dict_type(self, _input_dict):
        # type: (dict) -> None
        """Check that the input dict type is correct for the Heating System being constructed."""
        device_type = _input_dict["device_typename"]
        msg = "Error creating Heating System from dict. Expected '{}' but got '{}'".format(
            self.__class__.__name__, device_type
        )
        assert device_type == str(self.__class__.__name__), msg
        return None

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhRenewableEnergyDevice
        raise NotImplementedError("Error: from_dict() called on BaseClass.")

    def __lt__(self, other):
        # type: (PhRenewableEnergyDevice) -> bool
        return self.identifier < other.identifier


# -----------------------------------------------------------------------------
# Renewable Energy Device Types


class PhPhotovoltaicDevice(PhRenewableEnergyDevice):
    """PV System."""

    def __init__(self):
        super(PhPhotovoltaicDevice, self).__init__()
        self.photovoltaic_renewable_energy = 0.0
        self.array_size = 0.0
        self.utilization_factor = 1.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhPhotovoltaicDevice, self).to_dict()
        d["photovoltaic_renewable_energy"] = self.photovoltaic_renewable_energy
        d["array_size"] = self.array_size
        d["utilization_factor"] = self.utilization_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhPhotovoltaicDevice
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.photovoltaic_renewable_energy = _input_dict["photovoltaic_renewable_energy"]
        new_obj.array_size = _input_dict["array_size"]
        new_obj.utilization_factor = _input_dict["utilization_factor"]

        return new_obj


# -----------------------------------------------------------------------------


class PhRenewableEnergyDeviceBuilder(object):
    """Constructor class for PH-Renewable-Energy-System objects."""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhRenewableEnergyDevice
        """Find the right device constructor class from the module based on the device_typename."""
        valid_device_typenames = [nm for nm in dir(sys.modules[__name__]) if nm.startswith("Ph")]

        device_typename = _input_dict["device_typename"]
        if device_typename not in valid_device_typenames:
            raise UnknownPhRenewableEnergyTypeError(valid_device_typenames, device_typename)
        device_class = getattr(sys.modules[__name__], device_typename)  # type: PhRenewableEnergyDevice
        new_device = device_class.from_dict(_input_dict)
        return new_device

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
