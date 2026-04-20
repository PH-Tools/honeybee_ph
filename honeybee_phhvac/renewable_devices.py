# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Renewable Energy Devices."""

import sys
from copy import copy

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_phhvac import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class UnknownPhRenewableEnergyTypeError(Exception):
    """Raised when an unrecognized renewable energy device type is encountered.

    Attributes:
        msg (str): Formatted error message describing the unknown type and valid options.
    """

    def __init__(self, _heater_types, _received_type):
        # type: (list[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Heating-SubSystem type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhRenewableEnergyTypeError, self).__init__(self.msg)


class PhRenewableEnergyDevice(_base._PhHVACBase):
    """Base class for all HBPH Renewable Energy Systems (PV, etc).

    Attributes:
        device_typename (str): Class name string identifying the device type for serialization.
        percent_coverage (float): Fraction of energy demand covered by this device (0.0-1.0).
    """

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
        """Check that the input dict type is correct for the Heating System being constructed.

        Arguments:
        ----------
            * _input_dict (dict): The dictionary to validate.

        Returns:
        --------
            * None
        """
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

    def move(self, moving_vec3D):
        """Move the device's elements along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A Vector3D with the direction and distance to move the ray.

        Returns:
        --------
            * None
        """
        pass

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        """Rotate the device's elements by a certain angle around an axis and origin point.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_vec3D (Vector3D): A Vector3D representing the axis of rotation.
            * angle_degrees (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): A Point3D for the origin around which the object will be rotated.

        Returns:
        --------
            * None
        """
        pass

    def rotate_xy(self, angle_degrees, origin_pt3D):
        """Rotate the device's elements counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degrees (float): An angle in degrees.
            * origin_pt3D (Point3D): A Point3D for the origin around which the object will be rotated.

        Returns:
        --------
            * None
        """
        pass

    def reflect(self, normal_vec3D, origin_pt3D):
        """Reflect the device's elements across a plane with the input normal vector and origin.

        Arguments:
        ----------
            * normal_vec3D (Vector3D): A normalized Vector3D representing the normal vector for the
                plane across which the element will be reflected.
            * origin_pt3D (Point3D): A Point3D representing the origin from which to reflect.

        Returns:
        --------
            * None
        """
        pass

    def scale(self, scale_factor, origin_pt3D=None):
        """Scale the device's elements by a factor from an origin point.

        Arguments:
        ----------
            * scale_factor (float): A number representing how much the element should be scaled.
            * origin_pt3D (Optional[Point3D]): A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * None
        """
        pass

    def __copy__(self):
        # type: () -> PhPhotovoltaicDevice
        raise NotImplementedError("Error: __copy__() called on BaseClass.")

    def duplicate(self):
        # type: () -> PhPhotovoltaicDevice
        raise NotImplementedError("Error: duplicate() called on BaseClass.")


# -----------------------------------------------------------------------------
# Renewable Energy Device Types


class PhPhotovoltaicDevice(PhRenewableEnergyDevice):
    """Photovoltaic (PV) renewable energy device.

    Attributes:
        photovoltaic_renewable_energy (float): Annual PV renewable energy production (kWh/yr).
        array_size (float): Total PV array area (m2).
        utilization_factor (float): Fraction of generated energy that is utilized (0.0-1.0).
    """

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

    def __copy__(self):
        # type: () -> PhPhotovoltaicDevice
        return self.duplicate()

    def duplicate(self):
        # type: () -> PhPhotovoltaicDevice
        """Duplicate the device."""
        obj = PhPhotovoltaicDevice()
        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.user_data = copy(self.user_data)
        obj.photovoltaic_renewable_energy = self.photovoltaic_renewable_energy
        obj.array_size = self.array_size
        obj.utilization_factor = self.utilization_factor
        obj.percent_coverage = self.percent_coverage
        return obj


# -----------------------------------------------------------------------------


class PhRenewableEnergyDeviceBuilder(object):
    """Constructor class for PH-Renewable-Energy-System objects."""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhRenewableEnergyDevice
        """Find the right device constructor class from the module based on the device_typename."""
        valid_device_type_names = [nm for nm in dir(sys.modules[__name__]) if nm.startswith("Ph")]

        device_typename = _input_dict["device_typename"]
        if device_typename not in valid_device_type_names:
            raise UnknownPhRenewableEnergyTypeError(valid_device_type_names, device_typename)
        device_class = getattr(sys.modules[__name__], device_typename)  # type: PhRenewableEnergyDevice
        new_device = device_class.from_dict(_input_dict)
        return new_device

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
