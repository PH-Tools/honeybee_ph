# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Aux. Energy Supportive Devices."""

from copy import copy

try:
    from typing import Any, Dict
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee_phhvac import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


# -- IHG usage-profile int codes. Shared contract across honeybee-ph / PHX /
# -- OpenPH: which PHPP 'Aux Electricity' block (and therefore which season and
# -- utilization period) a device's internal heat gain lands in.
IHG_USAGE_PROFILE_ALL_YEAR = 1  # Other block (rows 71-79): both seasons, / 8.76 kh
IHG_USAGE_PROFILE_WINTER = 2  # Heating/ventilation winter block (rows 15-31)
IHG_USAGE_PROFILE_SUMMER = 3  # Cooling/ventilation summer + dehumidification (rows 35-57)
IHG_USAGE_PROFILE_NONE = 4  # DHW block (rows 59-69): 0 IHG (already booked in DHW distribution)

# -- Default IHG usage-profile keyed off device_type, so a DHW pump never
# -- defaults into the cooling balance (the over-count OpenPH corrected).
# -- Unlisted/custom device types fall back to ALL_YEAR.
_DEFAULT_IHG_USAGE_PROFILE_BY_DEVICE_TYPE = {
    4: IHG_USAGE_PROFILE_WINTER,  # Heat Circulation Pump
    6: IHG_USAGE_PROFILE_NONE,  # DHW Circulation Pump
    7: IHG_USAGE_PROFILE_NONE,  # DHW Storage Load Pump
    10: IHG_USAGE_PROFILE_ALL_YEAR,  # Other / Custom
}


def default_ihg_usage_profile(device_type):
    # type: (int) -> int
    """Return the default IHG usage-profile int code for a supportive-device type."""
    return _DEFAULT_IHG_USAGE_PROFILE_BY_DEVICE_TYPE.get(device_type, IHG_USAGE_PROFILE_ALL_YEAR)


class PhSupportiveDevice(_base._PhHVACBase):
    """Auxiliary energy supportive device for Passive House HVAC systems.

    Attributes:
        display_name (str): Human-readable name for the device.
        device_type (int): Numeric code identifying the device type.
        quantity (int): Number of identical devices.
        in_conditioned_space (bool): Whether the device is located inside the thermal envelope.
        norm_energy_demand_W (float): Normalized energy demand in Watts.
        annual_period_operation_khrs (float): Annual operating period in thousands of hours.
        ihg_utilization_factor (float): Fraction of energy that becomes internal heat gain inside the envelope (0.0-1.0).
        ihg_usage_profile (int): PHPP season/block the device's IHG lands in (1=all-year, 2=winter, 3=summer, 4=none/DHW).
    """

    def __init__(self):
        # type: () -> None
        super(PhSupportiveDevice, self).__init__()
        self.display_name = "__unnamed_device__"
        self.device_type = 10  # setter seeds ihg_usage_profile off this type
        self.quantity = 1
        self.in_conditioned_space = True
        self.norm_energy_demand_W = 1.0
        self.annual_period_operation_khrs = 8.760  # 100% of the year
        self.ihg_utilization_factor = 1.0  # Fraction of energy that becomes IHG inside envelope [0.0-1.0]

    @property
    def device_type(self):
        # type: () -> int
        return self._device_type

    @device_type.setter
    def device_type(self, value):
        # type: (int) -> None
        self._device_type = value
        # Re-seed the IHG season/block default for the new type, so a DHW pump
        # can never carry the all-year default into the cooling balance. Explicit
        # ihg_usage_profile assignments must therefore follow device_type -- as
        # __init__, base_attrs_from_dict, duplicate, and the GH factory all do.
        self.ihg_usage_profile = default_ihg_usage_profile(value)

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
        d["ihg_utilization_factor"] = self.ihg_utilization_factor
        d["ihg_usage_profile"] = self.ihg_usage_profile
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
        self.ihg_utilization_factor = _input_dict.get("ihg_utilization_factor", 1.0)
        # -- Legacy dicts (pre-seasonal-IHG) have no profile; derive it from device_type
        # -- so an old DHW pump stays NONE rather than defaulting into the cooling balance.
        self.ihg_usage_profile = _input_dict.get("ihg_usage_profile", default_ihg_usage_profile(self.device_type))
        return self

    def check_dict_type(self, _input_dict):
        # type: (Dict[str, Any]) -> None
        """Check that the input dict type is correct for the Supportive Device being constructed.

        Arguments:
        ----------
            * _input_dict (Dict[str, Any]): The dictionary to validate.

        Returns:
        --------
            * None
        """
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
        # type: () -> PhSupportiveDevice
        return self.duplicate()

    def duplicate(self):
        # type: () -> PhSupportiveDevice
        obj = PhSupportiveDevice()
        obj.identifier = self.identifier
        obj.display_name = self.display_name
        obj.user_data = copy(self.user_data)
        obj.device_type = self.device_type
        obj.quantity = self.quantity
        obj.in_conditioned_space = self.in_conditioned_space
        obj.norm_energy_demand_W = self.norm_energy_demand_W
        obj.annual_period_operation_khrs = self.annual_period_operation_khrs
        obj.ihg_utilization_factor = self.ihg_utilization_factor
        obj.ihg_usage_profile = self.ihg_usage_profile
        return obj
