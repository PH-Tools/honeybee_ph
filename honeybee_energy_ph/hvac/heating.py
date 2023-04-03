# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBPH Heating Objects"""

import sys

try:
    from typing import Any, Optional, Sequence
except ImportError:
    pass  # IronPython 2.7

from honeybee_energy_ph.hvac import _base, fuels


class UnknownPhHeatingTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        # type: (list[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Heating-SubSystem type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhHeatingTypeError, self).__init__(self.msg)


class PhHeatingSystem(_base._PhHVACBase):
    """Base class for all PH-Heating Systems (elec, boiler, etc...)"""

    def __init__(self):
        super(PhHeatingSystem, self).__init__()
        self.heating_type = self.__class__.__name__
        self.percent_coverage = 1.0

    def to_dict(self):
        # type: () -> dict
        d = super(PhHeatingSystem, self).to_dict()
        d["heating_type"] = self.heating_type
        d["percent_coverage"] = self.percent_coverage
        return d

    def base_attrs_from_dict(self, _input_dict):
        # type: (PhHeatingSystem, dict) -> PhHeatingSystem
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.user_data = _input_dict["user_data"]
        self.heating_type = _input_dict["heating_type"]
        self.percent_coverage = _input_dict["percent_coverage"]
        return self

    def check_dict_type(self, _input_dict):
        # type: (dict) -> None
        """Check that the input dict type is correct for the Heating System being constructed."""
        heating_type = _input_dict["heating_type"]
        msg = (
            "Error creating Heating System from dict. Expected '{}' but got '{}'".format(
                self.__class__.__name__, heating_type
            )
        )
        assert heating_type == str(self.__class__.__name__), msg
        return None

    @classmethod
    def from_dict(cls, _input_dict):
        raise NotImplementedError("Error: from_dict() called on BaseClass.")

    def __lt__(self, other):
        # type: (PhHeatingSystem) -> bool
        return self.identifier < other.identifier


# -----------------------------------------------------------------------------
# Heating Types


class PhHeatingDirectElectric(PhHeatingSystem):
    """Heating via direct-electric (resistance heating)."""

    def __init__(self):
        super(PhHeatingDirectElectric, self).__init__()

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhHeatingDirectElectric, self).to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhHeatingDirectElectric
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        return new_obj


class PhHeatingFossilBoiler(PhHeatingSystem):
    """Heating via boiler using fossil-fuel (gas, oil)"""

    def __init__(self):
        super(PhHeatingFossilBoiler, self).__init__()
        self.fuel = fuels.NATURAL_GAS
        self.condensing = True
        self.in_conditioned_space = True
        self.effic_at_30_percent_load = 0.98
        self.effic_at_nominal_load = 0.94
        self.avg_rtrn_temp_at_30_percent_load = 30
        self.avg_temp_at_70C_55C = 41
        self.avg_temp_at_55C_45C = 35
        self.avg_temp_at_32C_28C = 24

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhHeatingFossilBoiler, self).to_dict()

        d["fuel"] = self.fuel
        d["condensing"] = self.condensing
        d["in_conditioned_space"] = self.in_conditioned_space
        d["effic_at_30_percent_load"] = self.effic_at_30_percent_load
        d["effic_at_nominal_load"] = self.effic_at_nominal_load
        d["avg_rtrn_temp_at_30_percent_load"] = self.avg_rtrn_temp_at_30_percent_load
        d["avg_temp_at_70C_55C"] = self.avg_temp_at_70C_55C
        d["avg_temp_at_55C_45C"] = self.avg_temp_at_55C_45C
        d["avg_temp_at_32C_28C"] = self.avg_temp_at_32C_28C

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhHeatingFossilBoiler
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.fuel = _input_dict["fuel"]
        new_obj.condensing = _input_dict["condensing"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        new_obj.effic_at_30_percent_load = _input_dict["effic_at_30_percent_load"]
        new_obj.effic_at_nominal_load = _input_dict["effic_at_nominal_load"]
        new_obj.avg_rtrn_temp_at_30_percent_load = _input_dict[
            "avg_rtrn_temp_at_30_percent_load"
        ]
        new_obj.avg_temp_at_70C_55C = _input_dict["avg_temp_at_70C_55C"]
        new_obj.avg_temp_at_55C_45C = _input_dict["avg_temp_at_55C_45C"]
        new_obj.avg_temp_at_32C_28C = _input_dict["avg_temp_at_32C_28C"]

        return new_obj


class PhHeatingWoodBoiler(PhHeatingSystem):
    """Heating via boiler using wood (log, pellet)."""

    def __init__(self):
        super(PhHeatingWoodBoiler, self).__init__()
        self.fuel = fuels.WOOD_LOG
        self.in_conditioned_space = True
        self.effic_in_basic_cycle = 0.6
        self.effic_in_const_operation = 0.7
        self.avg_frac_heat_output = 0.4
        self.temp_diff_on_off = 30
        self.rated_capacity = 15  # kW
        self.demand_basic_cycle = 1  # kWh
        self.power_stationary_run = 1  # W
        self.power_standard_run = None  # type: Optional[float]
        self.no_transport_pellets = None  # type: Optional[bool]
        self.only_control = None  # type: Optional[bool]
        self.area_mech_room = None  # type: Optional[float]

    @property
    def useful_heat_output(self):
        return 0.9 * self.rated_capacity  # kWH

    @property
    def avg_power_output(self):
        return 0.5 * self.rated_capacity  # kW

    def to_dict(self):
        # type: () -> dict
        d = super(PhHeatingWoodBoiler, self).to_dict()

        d["fuel"] = self.fuel
        d["in_conditioned_space"] = self.in_conditioned_space
        d["effic_in_basic_cycle"] = self.effic_in_basic_cycle
        d["effic_in_const_operation"] = self.effic_in_const_operation
        d["avg_frac_heat_output"] = self.avg_frac_heat_output
        d["temp_diff_on_off"] = self.temp_diff_on_off
        d["rated_capacity"] = self.rated_capacity
        d["demand_basic_cycle"] = self.demand_basic_cycle
        d["power_stationary_run"] = self.power_stationary_run
        d["power_standard_run"] = self.power_standard_run
        d["no_transport_pellets"] = self.no_transport_pellets
        d["only_control"] = self.only_control
        d["area_mech_room"] = self.area_mech_room

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHeatingWoodBoiler

        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.fuel = _input_dict["fuel"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        new_obj.effic_in_basic_cycle = _input_dict["effic_in_basic_cycle"]
        new_obj.effic_in_const_operation = _input_dict["effic_in_const_operation"]
        new_obj.avg_frac_heat_output = _input_dict["avg_frac_heat_output"]
        new_obj.temp_diff_on_off = _input_dict["temp_diff_on_off"]
        new_obj.rated_capacity = _input_dict["rated_capacity"]
        new_obj.demand_basic_cycle = _input_dict["demand_basic_cycle"]
        new_obj.power_stationary_run = _input_dict["power_stationary_run"]
        new_obj.no_transport_pellets = _input_dict["no_transport_pellets"]
        new_obj.only_control = _input_dict["only_control"]
        new_obj.area_mech_room = _input_dict["area_mech_room"]

        return new_obj


class PhHeatingDistrict(PhHeatingSystem):
    """Heating via district-heat."""

    def __init__(self):
        super(PhHeatingDistrict, self).__init__()
        self.fuel = fuels.GAS_CGS_70_PHC
        self.util_factor_of_heat_transfer_station = 0.5

    def to_dict(self):
        # type: () -> dict
        d = super(PhHeatingDistrict, self).to_dict()
        d["fuel"] = self.fuel
        d[
            "util_factor_of_heat_transfer_station"
        ] = self.util_factor_of_heat_transfer_station
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHeatingDistrict
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.fuel = _input_dict["fuel"]
        new_obj.util_factor_of_heat_transfer_station = _input_dict[
            "util_factor_of_heat_transfer_station"
        ]
        return new_obj


class PhHeatingHeatPumpAnnual(PhHeatingSystem):
    def __init__(self):
        super(PhHeatingHeatPumpAnnual, self).__init__()
        self.annual_COP = 2.5
        self.total_system_perf_ratio = 0.4

    def to_dict(self):
        # type: () -> dict
        d = super(PhHeatingHeatPumpAnnual, self).to_dict()
        d["annual_COP"] = self.annual_COP
        d["total_system_perf_ratio"] = self.total_system_perf_ratio
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHeatingHeatPumpAnnual
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.annual_COP = _input_dict["annual_COP"]
        new_obj.total_system_perf_ratio = _input_dict["total_system_perf_ratio"]
        return new_obj


class PhHeatingHeatPumpRatedMonthly(PhHeatingSystem):
    """Heating via electric heat-pump."""

    def __init__(self):
        super(PhHeatingHeatPumpRatedMonthly, self).__init__()
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
        # type: () -> dict[str, Any]
        d = super(PhHeatingHeatPumpRatedMonthly, self).to_dict()
        d["COP_1"] = self.COP_1
        d["ambient_temp_1"] = self.ambient_temp_1
        d["COP_2"] = self.COP_2
        d["ambient_temp_2"] = self.ambient_temp_2
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhHeatingHeatPumpRatedMonthly
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.COP_1 = _input_dict["COP_1"]
        new_obj.ambient_temp_1 = _input_dict["ambient_temp_1"]
        new_obj.COP_2 = _input_dict["COP_2"]
        new_obj.ambient_temp_2 = _input_dict["ambient_temp_2"]
        return new_obj


class PhHeatingHeatPumpCombined(PhHeatingSystem):
    def __init__(self):
        raise NotImplementedError()


# -----------------------------------------------------------------------------


class PhHeatingSystemBuilder(object):
    """Constructor class for PH-HeatingSystems"""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhHeatingSystem
        """Find the right appliance constructor class from the module based on the 'type' name."""
        heating_type = _input_dict.get("heating_type")

        valid_class_types = [
            nm for nm in dir(sys.modules[__name__]) if nm.startswith("Ph")
        ]

        if heating_type not in valid_class_types:
            raise UnknownPhHeatingTypeError(valid_class_types, heating_type)
        heating_class = getattr(sys.modules[__name__], heating_type)
        new_equipment = heating_class.from_dict(_input_dict)
        return new_equipment

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
