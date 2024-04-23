# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Aux. Energy Supportive Devices."""

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_phhvac import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class PhSupportiveDevice(_base._PhHVACBase):
    def __init__(self):
        # type: () -> None
        super(PhSupportiveDevice, self).__init__()
        self.display_name = "__unnamed_device__"
        self.device_type = 10
        self.quantity = 1
        self.in_conditioned_space = True
        self.norm_energy_demand_W = 1.0
        self.annual_period_operation_khrs = 8.760  # 100% of the year

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhSupportiveDevice, self).to_dict()
        d["device_class_name"] = self.__class__.__name__
        d["display_name"] = self.display_name
        d["device_type"] = self.device_type
        d["quantity"] = self.quantity
        d["in_conditioned_space"] = self.in_conditioned_space
        d["norm_energy_demand_W"] = self.norm_energy_demand_W
        d["annual_period_operation_khrs"] = self.annual_period_operation_khrs
        return d

    def base_attrs_from_dict(self, _input_dict):
        # type: (Dict[str, Any]) -> PhSupportiveDevice
        self.identifier = _input_dict["identifier"]
        self.display_name = _input_dict["display_name"]
        self.user_data = _input_dict.get("user_data", {})
        self.device_type = _input_dict["device_type"]
        self.quantity = _input_dict["quantity"]
        self.in_conditioned_space = _input_dict["in_conditioned_space"]
        self.norm_energy_demand_W = _input_dict["norm_energy_demand_W"]
        self.annual_period_operation_khrs = _input_dict["annual_period_operation_khrs"]
        return self

    def check_dict_type(self, _input_dict):
        # type: (Dict[str, Any]) -> None
        """Check that the input dict type is correct for the Supportive Device being constructed."""
        device_class_name = _input_dict["device_class_name"]
        msg = "Error creating Supportive Device from dict. Expected '{}' but got '{}'".format(
            self.__class__.__name__, device_class_name
        )
        assert device_class_name == str(self.__class__.__name__), msg
        return None

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhSupportiveDevice
        new_obj = cls()
        new_obj.check_dict_type(_input_dict)
        new_obj.base_attrs_from_dict(_input_dict)
        return new_obj

    def __lt__(self, other):
        # type: (PhSupportiveDevice) -> bool
        return self.identifier < other.identifier

    def __str__(self):
        return "{}(display_name={!r}, device_type={!r}, quantity={!r})".format(
            self.__class__.__name__, self.display_name, self.device_type, self.quantity
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

    def move(self, moving_vec):
        """Move the device along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        pass

    def rotate(self, axis, angle, origin):
        """Rotate the device by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        pass

    def rotate_xy(self, angle, origin):
        """Rotate the device counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        pass

    def reflect(self, normal, origin):
        """Reflected the device across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        pass

    def scale(self, factor, origin=None):
        """Scale the device by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        pass
