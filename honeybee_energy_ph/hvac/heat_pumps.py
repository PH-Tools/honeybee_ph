# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBPH Cooling Objects"""

try:
    from typing import Any, Dict, List, Sequence
except ImportError:
    pass  # IronPython 2.7

import sys

from honeybee_energy_ph.hvac import _base

# -----------------------------------------------------------------------------
# Heat Pump Base


class UnknownPhHeatPumpTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        # type: (List[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Heat-pump system type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhHeatPumpTypeError, self).__init__(self.msg)


class PhHeatPumpSystem(_base._PhHVACBase):
    """Base class for all HBPH-Cooling-Systems."""

    def __init__(self):
        super(PhHeatPumpSystem, self).__init__()
        self.heat_pump_class_name = self.__class__.__name__
        self.percent_coverage = 1.0
        self.cooling_params = PhHeatPumpCoolingParams()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpSystem, self).to_dict()
        d["heat_pump_class_name"] = self.heat_pump_class_name
        d["percent_coverage"] = self.percent_coverage
        return d

    def base_attrs_from_dict(self, _input_dict):
        # type: (PhHeatPumpSystem, Dict[str, Any]) -> PhHeatPumpSystem
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.user_data = _input_dict.get("user_data", {})
        self.heat_pump_class_name = _input_dict["heat_pump_class_name"]
        self.percent_coverage = _input_dict["percent_coverage"]
        return self

    def check_dict_type(self, _input_dict):
        # type: (Dict[str, Any]) -> None
        """Check that the input dict type is correct for the Heat Pump System being constructed."""
        heat_pump_class_name = _input_dict["heat_pump_class_name"]
        msg = "Error creating Heat Pump System from dict. Expected '{}' but got '{}'".format(
            self.__class__.__name__, heat_pump_class_name
        )
        assert heat_pump_class_name == str(self.__class__.__name__), msg
        return None

    @classmethod
    def from_dict(cls, input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpSystem
        raise NotImplementedError("Error: from_dict() called from BaseClass")

    def __lt__(self, other):
        # type: (PhHeatPumpSystem) -> bool
        return self.identifier < other.identifier


# -----------------------------------------------------------------------------
# Heat-Pump Cooling Parameters


class PhHeatPumpCoolingParams_Base(_base._PhHVACBase):
    """Base class for all HBPH-Cooling-Parameters."""

    def __init__(self):
        super(PhHeatPumpCoolingParams_Base, self).__init__()
        self.used = False

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpCoolingParams_Base, self).to_dict()
        d["used"] = self.used
        return d

    def base_attrs_from_dict(self, _input_dict):
        # type: (PhHeatPumpCoolingParams_Base, Dict[str, Any]) -> PhHeatPumpCoolingParams_Base
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.user_data = _input_dict.get("user_data", {})
        self.used = _input_dict["used"]
        return self

    @classmethod
    def from_dict(cls, input_dict):
        raise NotImplementedError(
            "Error: from_dict() called from PhHeatPumpCoolingParams_Base?"
        )

    def __str__(self):
        # type: () -> str
        return "{}(used={})".format(self.__class__.__name__, self.used)


class PhHeatPumpCoolingParams_Ventilation(PhHeatPumpCoolingParams_Base):
    """Cooling via the Fresh-Air Ventilation System (ERV)."""

    def __init__(self):
        super(PhHeatPumpCoolingParams_Ventilation, self).__init__()
        self.single_speed = False
        self.min_coil_temp = 12.0
        self.capacity = 10.0
        self.annual_COP = 4.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpCoolingParams_Ventilation, self).to_dict()
        d["single_speed"] = self.single_speed
        d["min_coil_temp"] = self.min_coil_temp
        d["capacity"] = self.capacity
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpCoolingParams_Ventilation
        new_obj = cls()
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.single_speed = _input_dict["single_speed"]
        new_obj.min_coil_temp = _input_dict["min_coil_temp"]
        new_obj.capacity = _input_dict["capacity"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhHeatPumpCoolingParams_Recirculation(PhHeatPumpCoolingParams_Base):
    """Cooling via a 'recirculation' system (typical AC)."""

    def __init__(self):
        super(PhHeatPumpCoolingParams_Recirculation, self).__init__()
        self.single_speed = False
        self.min_coil_temp = 12.0
        self.flow_rate_m3_hr = 100.0
        self.flow_rate_variable = True
        self.capacity = 10.0
        self.annual_COP = 4.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpCoolingParams_Recirculation, self).to_dict()
        d["single_speed"] = self.single_speed
        d["min_coil_temp"] = self.min_coil_temp
        d["flow_rate_m3_hr"] = self.flow_rate_m3_hr
        d["flow_rate_variable"] = self.flow_rate_variable
        d["capacity"] = self.capacity
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpCoolingParams_Recirculation
        new_obj = cls()
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.single_speed = _input_dict["single_speed"]
        new_obj.min_coil_temp = _input_dict["min_coil_temp"]
        new_obj.flow_rate_m3_hr = _input_dict["flow_rate_m3_hr"]
        new_obj.flow_rate_variable = _input_dict["flow_rate_variable"]
        new_obj.capacity = _input_dict["capacity"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhHeatPumpCoolingParams_Dehumidification(PhHeatPumpCoolingParams_Base):
    """Cooling via dedicated dehumidification system."""

    def __init__(self):
        super(PhHeatPumpCoolingParams_Dehumidification, self).__init__()
        self.useful_heat_loss = False
        self.annual_COP = 4.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpCoolingParams_Dehumidification, self).to_dict()
        d["useful_heat_loss"] = self.useful_heat_loss
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpCoolingParams_Dehumidification
        new_obj = cls()
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.useful_heat_loss = _input_dict["useful_heat_loss"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhHeatPumpCoolingParams_Panel(PhHeatPumpCoolingParams_Base):
    """Cooling via radiant panels."""

    def __init__(self):
        super(PhHeatPumpCoolingParams_Panel, self).__init__()
        self.annual_COP = 4.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpCoolingParams_Panel, self).to_dict()
        d["annual_COP"] = self.annual_COP
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpCoolingParams_Panel
        new_obj = cls()
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.annual_COP = _input_dict["annual_COP"]
        return new_obj


class PhHeatPumpCoolingParams:
    """A Collection of Cooling Parameters for various types of systems."""

    def __init__(self):
        self.percent_coverage = 1.0
        self.ventilation = PhHeatPumpCoolingParams_Ventilation()
        self.recirculation = PhHeatPumpCoolingParams_Recirculation()
        self.dehumidification = PhHeatPumpCoolingParams_Dehumidification()
        self.panel = PhHeatPumpCoolingParams_Panel()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d["percent_coverage"] = self.percent_coverage
        d["ventilation"] = self.ventilation.to_dict()
        d["recirculation"] = self.recirculation.to_dict()
        d["dehumidification"] = self.dehumidification.to_dict()
        d["panel"] = self.panel.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpCoolingParams
        new_obj = cls()
        new_obj.percent_coverage = _input_dict["percent_coverage"]
        new_obj.ventilation = PhHeatPumpCoolingParams_Ventilation.from_dict(
            _input_dict["ventilation"]
        )
        new_obj.recirculation = PhHeatPumpCoolingParams_Recirculation.from_dict(
            _input_dict["recirculation"]
        )
        new_obj.dehumidification = PhHeatPumpCoolingParams_Dehumidification.from_dict(
            _input_dict["dehumidification"]
        )
        new_obj.panel = PhHeatPumpCoolingParams_Panel.from_dict(_input_dict["panel"])
        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}(percent_coverage={}, ventilation={}, recirculation={}, dehumidification={}, panel={})".format(
            self.__class__.__name__,
            self.percent_coverage,
            self.ventilation.used,
            self.recirculation.used,
            self.dehumidification.used,
            self.panel.used,
        )

    def ToString(self):
        # type: () -> str
        return str(self)


# -----------------------------------------------------------------------------
# -- Heat Pumps Types


class PhHeatPumpAnnual(PhHeatPumpSystem):
    """Electric heat-pump with only Annual performance values."""

    def __init__(self):
        super(PhHeatPumpAnnual, self).__init__()
        self.annual_COP = 2.5
        self.total_system_perf_ratio = 0.4

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpAnnual, self).to_dict()
        d["annual_COP"] = self.annual_COP
        d["total_system_perf_ratio"] = self.total_system_perf_ratio
        d["cooling_params"] = self.cooling_params.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpAnnual
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.annual_COP = _input_dict["annual_COP"]
        new_obj.total_system_perf_ratio = _input_dict["total_system_perf_ratio"]
        new_obj.cooling_params = PhHeatPumpCoolingParams.from_dict(
            _input_dict["cooling_params"]
        )
        return new_obj


class PhHeatPumpRatedMonthly(PhHeatPumpSystem):
    """Electric heat-pump with 2 separate monthly performance values."""

    def __init__(self):
        super(PhHeatPumpRatedMonthly, self).__init__()
        self.COP_1 = 2.5
        self.ambient_temp_1 = -8.333  # =17F
        self.COP_2 = 2.5
        self.ambient_temp_2 = 8.333  # =47F

    @property
    def monthly_COPS(self):
        return [self.COP_1, self.COP_2]

    @monthly_COPS.setter
    def monthly_COPS(self, _cops):
        # type: (Sequence[float]) -> None
        self.COP_1 = _cops[0]
        try:
            self.COP_2 = _cops[1]
        except IndexError:
            self.COP_2 = _cops[0]
        return

    @property
    def monthly_temps(self):
        return [self.ambient_temp_1, self.ambient_temp_2]

    @monthly_temps.setter
    def monthly_temps(self, _cops):
        # type: (Sequence[float]) -> None
        self.ambient_temp_1 = _cops[0]
        try:
            self.ambient_temp_2 = _cops[1]
        except IndexError:
            self.ambient_temp_2 = _cops[0]
        return

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhHeatPumpRatedMonthly, self).to_dict()
        d["COP_1"] = self.COP_1
        d["ambient_temp_1"] = self.ambient_temp_1
        d["COP_2"] = self.COP_2
        d["ambient_temp_2"] = self.ambient_temp_2
        d["cooling_params"] = self.cooling_params.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpRatedMonthly
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        new_obj.COP_1 = _input_dict["COP_1"]
        new_obj.ambient_temp_1 = _input_dict["ambient_temp_1"]
        new_obj.COP_2 = _input_dict["COP_2"]
        new_obj.ambient_temp_2 = _input_dict["ambient_temp_2"]
        new_obj.cooling_params = PhHeatPumpCoolingParams.from_dict(
            _input_dict["cooling_params"]
        )
        return new_obj


class PhHeatPumpCombined(PhHeatPumpSystem):
    def __init__(self):
        msg = "Sorry, Combined Heat Pumps are not yet supported in HBPH."
        raise NotImplementedError(msg)


# -----------------------------------------------------------------------------


class PhHeatPumpSystemBuilder(object):
    """Constructor class for HBPH-CoolingSystems"""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatPumpSystem
        """Find the right heat-pump constructor class from the module based on the 'type' name."""

        valid_class_type_names = [
            nm for nm in dir(sys.modules[__name__]) if nm.startswith("PhHeatPump")
        ]

        heat_pump_class_name = _input_dict["heat_pump_class_name"]
        if heat_pump_class_name not in valid_class_type_names:
            raise UnknownPhHeatPumpTypeError(valid_class_type_names, heat_pump_class_name)
        heat_pump_class = getattr(sys.modules[__name__], heat_pump_class_name)
        new_equipment = heat_pump_class.from_dict(_input_dict)
        return new_equipment

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
