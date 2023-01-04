# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBPH Cooling Objects"""

try:
    from typing import Any, List, Dict
except ImportError:
    pass  # IronPython 2.7

import sys

from honeybee_energy_ph.hvac import _base

# -----------------------------------------------------------------------------
# Cooling Base


class UnknownPhCoolingTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        # type: (List[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Cooling-SubSystem type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhCoolingTypeError, self).__init__(self.msg)


class PhCoolingSystem(_base._PhHVACBase):
    """Base class for all HBPH-Cooling-Systems."""

    def __init__(self):
        super(PhCoolingSystem, self).__init__()
        self.cooling_class_name = self.__class__.__name__
        self.percent_coverage = 1.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        d["cooling_class_name"] = self.cooling_class_name
        d["percent_coverage"] = self.percent_coverage
        return d

    def base_attrs_from_dict(self, _input_dict):
        # type: (PhCoolingSystem, Dict[str, Any]) -> PhCoolingSystem
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.cooling_class_name = _input_dict["cooling_class_name"]
        self.percent_coverage = _input_dict["percent_coverage"]
        return self

    def check_dict_type(self, _input_dict):
        # type: (Dict[str, Any]) -> None
        """Check that the input dict type is correct for the Cooling System being constructed."""
        cooling_class_name = _input_dict["cooling_class_name"]
        msg = (
            "Error creating Cooling System from dict. Expected '{}' but got '{}'".format(
                self.__class__.__name__, cooling_class_name
            )
        )
        assert cooling_class_name == str(self.__class__.__name__), msg
        return None

    @classmethod
    def from_dict(cls, input_dict):
        raise NotImplementedError("Error: from_dict() called from BaseClass")

    def __lt__(self, other):
        # type: (PhCoolingSystem) -> bool
        return self.identifier < other.identifier


# -----------------------------------------------------------------------------
# Cooling Types


class PhCoolingVentilation(PhCoolingSystem):
    """Cooling via the Fresh-Air Ventilation System (ERV)."""

    def __init__(self):
        super(PhCoolingVentilation, self).__init__()
        self.single_speed = False
        self.min_coil_temp = 12
        self.capacity = 10
        self.annual_COP = 4

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhCoolingVentilation, self).to_dict()
        d["single_speed"] = self.single_speed
        d["min_coil_temp"] = self.min_coil_temp
        d["capacity"] = self.capacity
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhCoolingVentilation
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.single_speed = _input_dict["single_speed"]
        new_obj.min_coil_temp = _input_dict["min_coil_temp"]
        new_obj.capacity = _input_dict["capacity"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhCoolingRecirculation(PhCoolingSystem):
    """Cooling via a 'recirculation' system (typical AC)."""

    def __init__(self):
        super(PhCoolingRecirculation, self).__init__()
        self.single_speed = False
        self.min_coil_temp = 12
        self.flow_rate_m3_hr = 100
        self.flow_rate_variable = True
        self.capacity = 10
        self.annual_COP = 4

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhCoolingRecirculation, self).to_dict()
        d["single_speed"] = self.single_speed
        d["min_coil_temp"] = self.min_coil_temp
        d["flow_rate_m3_hr"] = self.flow_rate_m3_hr
        d["flow_rate_variable"] = self.flow_rate_variable
        d["capacity"] = self.capacity
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhCoolingRecirculation
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.single_speed = _input_dict["single_speed"]
        new_obj.min_coil_temp = _input_dict["min_coil_temp"]
        new_obj.flow_rate_m3_hr = _input_dict["flow_rate_m3_hr"]
        new_obj.flow_rate_variable = _input_dict["flow_rate_variable"]
        new_obj.capacity = _input_dict["capacity"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhCoolingDehumidification(PhCoolingSystem):
    """Cooling via dedicated dehumidification system."""

    def __init__(self):
        super(PhCoolingDehumidification, self).__init__()
        self.useful_heat_loss = False
        self.annual_COP = 4

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhCoolingDehumidification, self).to_dict()
        d["useful_heat_loss"] = self.useful_heat_loss
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhCoolingDehumidification
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.useful_heat_loss = _input_dict["useful_heat_loss"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhCoolingPanel(PhCoolingSystem):
    """Cooling via radiant panels."""

    def __init__(self):
        super(PhCoolingPanel, self).__init__()
        self.annual_COP = 4

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhCoolingPanel, self).to_dict()
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhCoolingPanel
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


# -----------------------------------------------------------------------------


class PhCoolingSystemBuilder(object):
    """Constructor class for HBPH-CoolingSystems"""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhCoolingSystem
        """Find the right cooling constructor class from the module based on the 'type' name."""
        cooling_class_name = _input_dict["cooling_class_name"]  # type: str

        valid_class_types = [
            nm for nm in dir(sys.modules[__name__]) if nm.startswith("Ph")
        ]

        if cooling_class_name not in valid_class_types:
            raise UnknownPhCoolingTypeError(valid_class_types, cooling_class_name)
        cooling_class = getattr(sys.modules[__name__], cooling_class_name)
        new_equipment = cooling_class.from_dict(_input_dict)
        return new_equipment

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
