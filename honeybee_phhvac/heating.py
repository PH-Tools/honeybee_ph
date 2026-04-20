# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Heating Devices."""

import sys
from copy import copy

try:
    from typing import Any, Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_phhvac import _base, fuels
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class UnknownPhHeatingTypeError(Exception):
    """Raised when an unrecognized PH heating system type is encountered.

    Attributes:
        msg (str): Human-readable error message describing the invalid type.
    """

    def __init__(self, _heater_types, _received_type):
        # type: (list[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Heating-SubSystem type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhHeatingTypeError, self).__init__(self.msg)


class PhHeatingSystem(_base._PhHVACBase):
    """Base class for all PH-Heating Systems (elec, boiler, etc...).

    Attributes:
        heating_type (str): The class name of the heating system type.
        percent_coverage (float): Fraction of total heating load covered by this system (0.0-1.0).
    """

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
        """Check that the input dict type is correct for the Heating System being constructed.

        Arguments:
        ----------
            * _input_dict (dict): Serialized heating system dictionary with a 'heating_type' key.

        Returns:
        --------
            * None
        """
        heating_type = _input_dict["heating_type"]
        msg = "Error creating Heating System from dict. Expected '{}' but got '{}'".format(
            self.__class__.__name__, heating_type
        )
        assert heating_type == str(self.__class__.__name__), msg
        return None

    @classmethod
    def from_dict(cls, _input_dict):
        raise NotImplementedError("Error: from_dict() called on BaseClass.")

    def __lt__(self, other):
        # type: (PhHeatingSystem) -> bool
        return self.identifier < other.identifier

    def move(self, moving_vec3D):
        """Move the System's elements along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A Vector3D with the direction and distance to move the ray.

        Returns:
        --------
            * None
        """
        pass

    def rotate(self, axis_vec3D, angle_degree, origin_pt3D):
        """Rotate the System's elements by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_vec3D (Vector3D): A Vector3D axis representing the axis of rotation.
            * angle_degree (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): A Point3D for the origin around which the object will be rotated.

        Returns:
        --------
            * None
        """
        pass

    def rotate_xy(self, angle_degree, origin_pt3D):
        """Rotate the System's elements counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degree (float): An angle in degrees.
            * origin_pt3D (Point3D): A Point3D for the origin around which the object will be rotated.

        Returns:
        --------
            * None
        """
        pass

    def reflect(self, normal_vec3D, origin_pt3D):
        """Reflect the System's elements across a plane with the input normal vector and origin.

        Arguments:
        ----------
            * normal_vec3D (Vector3D): A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            * origin_pt3D (Point3D): A Point3D representing the origin from which to reflect.

        Returns:
        --------
            * None
        """
        pass

    def scale(self, scale_factor, origin=None):
        """Scale the System's elements by a factor from an origin point.

        Arguments:
        ----------
            * scale_factor (float): A number representing how much the line segment should be scaled.
            * origin (Optional[Point3D]): A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * None
        """
        pass

    def duplicate(self):
        # type: () -> PhHeatingSystem
        raise NotImplementedError("Error: duplicate() called on BaseClass.")

    def __copy__(self):
        raise NotImplementedError("Error: __copy__() called on BaseClass.")


# -----------------------------------------------------------------------------
# Heating Types


class PhHeatingDirectElectric(PhHeatingSystem):
    """Heating via direct-electric (resistance heating).

    Attributes:
        heating_type (str): The class name of the heating system type.
        percent_coverage (float): Fraction of total heating load covered by this system (0.0-1.0).
    """

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

    def __copy__(self):
        return self.duplicate()

    def duplicate(self):
        # type: () -> PhHeatingDirectElectric
        obj = PhHeatingDirectElectric()
        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.percent_coverage = self.percent_coverage
        obj.user_data = copy(self.user_data)
        return obj


class PhHeatingFossilBoiler(PhHeatingSystem):
    """Heating via boiler using fossil-fuel (gas, oil).

    Attributes:
        fuel (str): Fuel type constant from the fuels module.
        condensing (bool): True if the boiler is a condensing type.
        in_conditioned_space (bool): True if the boiler is located within conditioned space.
        effic_at_30_percent_load (float): Boiler efficiency at 30 percent part-load.
        effic_at_nominal_load (float): Boiler efficiency at nominal (full) load.
        avg_rtrn_temp_at_30_percent_load (float): Average return temperature at 30 percent load (deg C).
        avg_temp_at_70C_55C (float): Average boiler temperature at 70C/55C flow/return (deg C).
        avg_temp_at_55C_45C (float): Average boiler temperature at 55C/45C flow/return (deg C).
        avg_temp_at_32C_28C (float): Average boiler temperature at 32C/28C flow/return (deg C).
    """

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
        new_obj.avg_rtrn_temp_at_30_percent_load = _input_dict["avg_rtrn_temp_at_30_percent_load"]
        new_obj.avg_temp_at_70C_55C = _input_dict["avg_temp_at_70C_55C"]
        new_obj.avg_temp_at_55C_45C = _input_dict["avg_temp_at_55C_45C"]
        new_obj.avg_temp_at_32C_28C = _input_dict["avg_temp_at_32C_28C"]

        return new_obj

    def __copy__(self):
        return self.duplicate()

    def duplicate(self):
        # type: () -> PhHeatingFossilBoiler
        obj = PhHeatingFossilBoiler()
        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.percent_coverage = self.percent_coverage
        obj.user_data = copy(self.user_data)
        obj.fuel = self.fuel
        obj.condensing = self.condensing
        obj.in_conditioned_space = self.in_conditioned_space
        obj.effic_at_30_percent_load = self.effic_at_30_percent_load
        obj.effic_at_nominal_load = self.effic_at_nominal_load
        obj.avg_rtrn_temp_at_30_percent_load = self.avg_rtrn_temp_at_30_percent_load
        obj.avg_temp_at_70C_55C = self.avg_temp_at_70C_55C
        obj.avg_temp_at_55C_45C = self.avg_temp_at_55C_45C
        obj.avg_temp_at_32C_28C = self.avg_temp_at_32C_28C
        return obj


class PhHeatingWoodBoiler(PhHeatingSystem):
    """Heating via boiler using wood (log, pellet).

    Attributes:
        fuel (str): Fuel type constant from the fuels module.
        in_conditioned_space (bool): True if the boiler is located within conditioned space.
        effic_in_basic_cycle (float): Efficiency during the basic heating cycle.
        effic_in_const_operation (float): Efficiency during constant operation.
        avg_frac_heat_output (float): Average fraction of rated heat output.
        temp_diff_on_off (float): Temperature difference between on and off cycles (deg C).
        rated_capacity (float): Rated heating capacity in kW.
        demand_basic_cycle (float): Energy demand per basic cycle in kWh.
        power_stationary_run (float): Electrical power during stationary run in W.
        power_standard_run (Optional[float]): Electrical power during standard run in W.
        no_transport_pellets (Optional[bool]): True if no pellet transport mechanism is used.
        only_control (Optional[bool]): True if only control power is consumed.
        area_mech_room (Optional[float]): Mechanical room area in m2.
    """

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
        # type: () -> float
        """Useful heat output (90 percent of rated capacity) in kWh."""
        return 0.9 * self.rated_capacity  # kWH

    @property
    def avg_power_output(self):
        # type: () -> float
        """Average power output (50 percent of rated capacity) in kW."""
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

    def __copy__(self):
        return self.duplicate()

    def duplicate(self):
        # type: () -> PhHeatingWoodBoiler
        obj = PhHeatingWoodBoiler()
        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.percent_coverage = self.percent_coverage
        obj.user_data = copy(self.user_data)
        obj.fuel = self.fuel
        obj.in_conditioned_space = self.in_conditioned_space
        obj.effic_in_basic_cycle = self.effic_in_basic_cycle
        obj.effic_in_const_operation = self.effic_in_const_operation
        obj.avg_frac_heat_output = self.avg_frac_heat_output
        obj.temp_diff_on_off = self.temp_diff_on_off
        obj.rated_capacity = self.rated_capacity
        obj.demand_basic_cycle = self.demand_basic_cycle
        obj.power_stationary_run = self.power_stationary_run
        obj.power_standard_run = self.power_standard_run
        obj.no_transport_pellets = self.no_transport_pellets
        obj.only_control = self.only_control
        obj.area_mech_room = self.area_mech_room
        return obj


class PhHeatingDistrict(PhHeatingSystem):
    """Heating via district-heat.

    Attributes:
        fuel (str): District energy carrier constant from the fuels module.
        util_factor_of_heat_transfer_station (float): Utilization factor of the heat transfer station.
    """

    def __init__(self):
        super(PhHeatingDistrict, self).__init__()
        self.fuel = fuels.GAS_CGS_70_PHC
        self.util_factor_of_heat_transfer_station = 0.5

    def to_dict(self):
        # type: () -> dict
        d = super(PhHeatingDistrict, self).to_dict()
        d["fuel"] = self.fuel
        d["util_factor_of_heat_transfer_station"] = self.util_factor_of_heat_transfer_station
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHeatingDistrict
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)

        new_obj.fuel = _input_dict["fuel"]
        new_obj.util_factor_of_heat_transfer_station = _input_dict["util_factor_of_heat_transfer_station"]
        return new_obj

    def __copy__(self):
        return self.duplicate()

    def duplicate(self):
        # type: () -> PhHeatingDistrict
        obj = PhHeatingDistrict()
        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.percent_coverage = self.percent_coverage
        obj.user_data = copy(self.user_data)
        obj.fuel = self.fuel
        obj.util_factor_of_heat_transfer_station = self.util_factor_of_heat_transfer_station
        return obj


# -----------------------------------------------------------------------------


class PhHeatingSystemBuilder(object):
    """Constructor class for PH-HeatingSystems.

    Provides a factory method to instantiate the correct PhHeatingSystem subclass
    from a serialized dictionary.
    """

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhHeatingSystem
        """Find the right appliance constructor class from the module based on the 'type' name."""
        valid_class_types = [nm for nm in dir(sys.modules[__name__]) if nm.startswith("Ph")]

        heating_type = _input_dict["heating_type"]
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
