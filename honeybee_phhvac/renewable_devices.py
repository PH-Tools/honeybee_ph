# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Renewable Energy Devices."""

import sys

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_phhvac import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


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

    def move(self, moving_vec3D):
        """Move the device's elements along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        """
        pass

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        """Rotate the device's elements by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        """
        pass

    def rotate_xy(self, angle_degrees, origin_pt3D):
        """Rotate the device's elements counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        """
        pass

    def reflect(self, normal_vec3D, origin_pt3D):
        """Reflected the device's elements across a plane with the input normal vector and origin_pt3D.

        Args:
            normal_vec3D: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin_pt3D: A Point3D representing the origin_pt3D from which to reflect.
        """
        pass

    def scale(self, scale_factor, origin_pt3D=None):
        """Scale the device's elements by a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        """
        pass


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
