# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Ventilation (ERV) Devices."""

import sys
from copy import copy

try:
    from typing import Any, Dict, List, Optional
except ImportError:
    pass  # IronPython

try:
    from ladybug_geometry.geometry3d.pointvector import Point3D
except ImportError as e:
    raise ImportError("Failed to import ladybug_geometry", e)

try:
    from honeybee_phhvac import _base, ducting
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


# -----------------------------------------------------------------------------


class UnknownPhExhaustVentTypeError(Exception):
    def __init__(self, _device_types, _received_type):
        # type: (list[str], str) -> None
        self.msg = 'Error: Unknown HBPH-Exhaust Ventilation type? Got: "{}"\
            "but only types: {} are allowed?'.format(
            _received_type, _device_types
        )
        super(UnknownPhExhaustVentTypeError, self).__init__(self.msg)


# -----------------------------------------------------------------------------
# -- ERV units


class Ventilator(_base._PhHVACBase):
    def __init__(self):
        super(Ventilator, self).__init__()
        self.display_name = "_unnamed_ventilator_"  # type: str
        self.id_num = 0  # type: int
        self.quantity = 1  # type: int
        self.sensible_heat_recovery = 0.0  # type:float
        self.latent_heat_recovery = 0.0  # type float
        self.electric_efficiency = 0.55  # type: float
        self.frost_protection_reqd = True  # type: bool
        self.temperature_below_defrost_used = -5  # type: float
        self.in_conditioned_space = True  # type: bool

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(Ventilator, self).to_dict()
        d["quantity"] = self.quantity
        d["sensible_heat_recovery"] = self.sensible_heat_recovery
        d["latent_heat_recovery"] = self.latent_heat_recovery
        d["electric_efficiency"] = self.electric_efficiency
        d["frost_protection_reqd"] = self.frost_protection_reqd
        d["temperature_below_defrost_used"] = self.temperature_below_defrost_used
        d["in_conditioned_space"] = self.in_conditioned_space
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> Ventilator
        obj = cls()
        obj.display_name = _input_dict["display_name"]
        obj.identifier = _input_dict["identifier"]
        obj.user_data = _input_dict.get("user_data", {})
        obj.quantity = _input_dict["quantity"]
        obj.sensible_heat_recovery = _input_dict["sensible_heat_recovery"]
        obj.latent_heat_recovery = _input_dict["latent_heat_recovery"]
        obj.electric_efficiency = _input_dict["electric_efficiency"]
        obj.frost_protection_reqd = _input_dict["frost_protection_reqd"]
        obj.temperature_below_defrost_used = _input_dict["temperature_below_defrost_used"]
        obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        return obj

    def duplicate(self):
        # type: () -> Ventilator
        new_obj = Ventilator()
        new_obj.display_name = self.display_name
        new_obj.identifier = self.identifier
        new_obj.user_data = copy(self.user_data)
        new_obj.id_num = self.id_num
        new_obj.quantity = self.quantity
        new_obj.sensible_heat_recovery = self.sensible_heat_recovery
        new_obj.latent_heat_recovery = self.latent_heat_recovery
        new_obj.electric_efficiency = self.electric_efficiency
        new_obj.frost_protection_reqd = self.frost_protection_reqd
        new_obj.temperature_below_defrost_used = self.temperature_below_defrost_used
        new_obj.in_conditioned_space = self.in_conditioned_space
        return new_obj

    def __lt__(self, other):
        # type: (PhVentilationSystem) -> bool
        return self.identifier < other.identifier

    def __copy__(self):
        # type: () -> Ventilator
        return self.duplicate()

    def __repr__(self):
        return "{}(display_name={!r}, sensible_heat_recovery={:0.2f})".format(
            self.__class__.__name__, self.display_name, self.sensible_heat_recovery
        )

    def ToString(self):
        return self.__repr__()


class PhVentilationSystem(_base._PhHVACBase):
    """Passive House Fresh-Air Ventilation System."""

    def __init__(self):
        # type: () -> None
        super(PhVentilationSystem, self).__init__()
        self.display_name = "_unnamed_ph_vent_system_"
        self.sys_type = 1  # '1-Balanced PH ventilation with HR'
        self.supply_ducting = []  # type: List[ducting.PhDuctElement]
        self.exhaust_ducting = []  # type: List[ducting.PhDuctElement]
        self._ventilation_unit = None  # type: Optional[Ventilator]
        self.id_num = 0

    @property
    def ventilation_unit(self):
        # type: () -> Optional[Ventilator]
        return self._ventilation_unit

    @ventilation_unit.setter
    def ventilation_unit(self, _in):
        # type: (Optional[Ventilator]) -> None
        self._ventilation_unit = _in

        if not self._ventilation_unit:
            return None

        if self._ventilation_unit.display_name == "_unnamed_ventilator_":
            self._ventilation_unit.display_name = self.display_name
        return None

    def add_supply_duct_element(self, _duct_element):
        # type: (ducting.PhDuctElement) -> None
        """Add a supply-air duct element to the ventilation system."""
        self.supply_ducting.append(_duct_element)

    def add_exhaust_duct_element(self, _duct_element):
        # type: (ducting.PhDuctElement) -> None
        """Add an exhaust-air duct element to the ventilation system."""
        self.exhaust_ducting.append(_duct_element)

    @property
    def supply_ducting_total_length(self):
        # type: () -> float
        """Return the total length of all supply-air ducting in model-units."""
        return sum(duct.length for duct in self.supply_ducting)

    @property
    def exhaust_ducting_total_length(self):
        # type: () -> float
        """Return the total length of all exhaust-air ducting in model-units."""
        return sum(duct.length for duct in self.exhaust_ducting)

    @property
    def supply_ducting_size_description(self):
        # type: () -> Optional[str]
        """Return the size of the supply-air ducting."""
        descriptions = {s.shape_type_description for s in self.supply_ducting}
        if len(descriptions) == 0:
            return None
        elif len(descriptions) == 1:
            return descriptions.pop()
        else:
            raise ValueError("Mixed shape-types in supply-air duct segments.")

    @property
    def exhaust_ducting_size_description(self):
        # type: () -> Optional[str]
        """Return the size of the exhaust-air ducting."""
        descriptions = {s.shape_type_description for s in self.exhaust_ducting}
        if len(descriptions) == 0:
            return None
        elif len(descriptions) == 1:
            return descriptions.pop()
        else:
            raise ValueError("Mixed shape-types in exhaust-air duct segments.")

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhVentilationSystem, self).to_dict()
        d["sys_type"] = self.sys_type
        d["exhaust_ducting"] = [e_duct.to_dict() for e_duct in self.exhaust_ducting]
        d["supply_ducting"] = [s_duct.to_dict() for s_duct in self.supply_ducting]
        d["id_num"] = self.id_num
        if self.ventilation_unit:
            d["ventilation_unit"] = self.ventilation_unit.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhVentilationSystem
        obj = cls()

        obj.identifier = _input_dict["identifier"]
        obj.display_name = _input_dict["display_name"]
        obj.user_data = _input_dict.get("user_data", {})
        obj.sys_type = _input_dict["sys_type"]
        obj.supply_ducting = [ducting.PhDuctElement.from_dict(s_duct) for s_duct in _input_dict["supply_ducting"]]
        obj.exhaust_ducting = [ducting.PhDuctElement.from_dict(e_duct) for e_duct in _input_dict["exhaust_ducting"]]
        obj.id_num = _input_dict.get("id_num", 0)

        vent_unit_dict = _input_dict.get("ventilation_unit", None)
        if vent_unit_dict:
            obj.ventilation_unit = Ventilator.from_dict(vent_unit_dict)

        return obj

    def duplicate(self):
        # type: () -> PhVentilationSystem
        new_obj = self.__class__()
        new_obj.display_name = self.display_name
        new_obj.identifier = self.identifier
        new_obj.user_data = copy(self.user_data)
        new_obj.sys_type = self.sys_type
        new_obj.supply_ducting = [s_duct.duplicate() for s_duct in self.supply_ducting]
        new_obj.exhaust_ducting = [e_duct.duplicate() for e_duct in self.exhaust_ducting]
        new_obj.id_num = self.id_num

        if self.ventilation_unit:
            new_obj._ventilation_unit = self.ventilation_unit.duplicate()

        return new_obj

    def __copy__(self):
        # type: () -> PhVentilationSystem
        return self.duplicate()

    def __lt__(self, other):
        # type: (PhVentilationSystem) -> bool
        return self.identifier < other.identifier

    def __repr__(self):
        return "{}(display_name={!r}, sys_type={!r})".format(self.__class__.__name__, self.display_name, self.sys_type)

    def ToString(self):
        return self.__repr__()

    def move(self, moving_vec3D):
        """Move the System's ducts along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        """
        new_system = self.duplicate()
        new_system.identifier = self.identifier
        new_system.supply_ducting = [duct_element.move(moving_vec3D) for duct_element in self.supply_ducting]
        new_system.exhaust_ducting = [duct_element.move(moving_vec3D) for duct_element in self.exhaust_ducting]
        return new_system

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        """Rotate the System's ducts by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis representing the axis of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin around which the object will be rotated.
        """
        print("  - PhVentilationSystem<id={}>.rotate(angle_degrees={})".format(id(self), angle_degrees))

        new_system = self.duplicate()
        new_system.identifier = self.identifier
        new_system.supply_ducting = [
            duct_element.rotate(axis_vec3D, angle_degrees, origin_pt3D) for duct_element in self.supply_ducting
        ]
        new_system.exhaust_ducting = [
            duct_element.rotate(axis_vec3D, angle_degrees, origin_pt3D) for duct_element in self.exhaust_ducting
        ]
        return new_system

    def rotate_xy(self, angle_degrees, origin_pt3D):
        """Rotate the System's ducts counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin around which the object will be rotated.
        """
        print("  - PhVentilationSystem<id={}>.rotate_xy(angle_degrees={})".format(id(self), angle_degrees))

        new_system = self.duplicate()
        new_system.identifier = self.identifier
        new_system.supply_ducting = [
            duct_element.rotate_xy(angle_degrees, origin_pt3D) for duct_element in self.supply_ducting
        ]
        new_system.exhaust_ducting = [
            duct_element.rotate_xy(angle_degrees, origin_pt3D) for duct_element in self.exhaust_ducting
        ]
        return new_system

    def reflect(self, normal_vec3D, origin_pt3D):
        """Reflected the System's ducts across a plane with the input normal vector and origin.

        Args:
            normal_vec3D: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin_pt3D: A Point3D representing the origin from which to reflect.
        """
        new_system = self.duplicate()
        new_system.identifier = self.identifier
        new_system.supply_ducting = [
            duct_element.reflect(normal_vec3D, origin_pt3D) for duct_element in self.supply_ducting
        ]
        new_system.exhaust_ducting = [
            duct_element.reflect(normal_vec3D, origin_pt3D) for duct_element in self.exhaust_ducting
        ]
        return new_system

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> PhVentilationSystem
        """Scale the System's ducts by a factor from an origin point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_system = self.duplicate()
        new_system.identifier = self.identifier
        new_system.supply_ducting = [
            duct_element.scale(scale_factor, origin_pt3D) for duct_element in self.supply_ducting
        ]
        new_system.exhaust_ducting = [
            duct_element.scale(scale_factor, origin_pt3D) for duct_element in self.exhaust_ducting
        ]
        return new_system


# -----------------------------------------------------------------------------
# -- Exhaust Ventilators are not part of the Ventilation System,
# -- but instead are treated more like appliances which get added to the Room.


class _ExhaustVentilatorBase(_base._PhHVACBase):
    def __init__(self):
        super(_ExhaustVentilatorBase, self).__init__()
        self.device_class_name = self.__class__.__name__
        self.display_name = "_unnamed_exhaust_ventilator_"
        self.quantity = 1
        self.annual_runtime_minutes = 0.0
        self.exhaust_flow_rate_m3s = 0.0

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(_ExhaustVentilatorBase, self).to_dict()
        d["device_class_name"] = self.device_class_name
        d["quantity"] = self.quantity
        d["annual_runtime_minutes"] = self.annual_runtime_minutes
        d["exhaust_flow_rate_m3s"] = self.exhaust_flow_rate_m3s
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> _ExhaustVentilatorBase
        new_obj = cls()
        new_obj.display_name = _input_dict["display_name"]
        new_obj.identifier = _input_dict["identifier"]
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.device_class_name = _input_dict["device_class_name"]
        new_obj.quantity = _input_dict["quantity"]
        new_obj.annual_runtime_minutes = _input_dict["annual_runtime_minutes"]
        new_obj.exhaust_flow_rate_m3s = _input_dict["exhaust_flow_rate_m3s"]
        return new_obj

    def __lt__(self, other):
        # type: (_ExhaustVentilatorBase) -> bool
        return self.identifier < other.identifier

    def __str__(self):
        return "{}(display_name={!r}, exhaust_flow_rate_m3s={:0.02f})".format(
            self.__class__.__name__, self.display_name, self.exhaust_flow_rate_m3s
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

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

    def __copy__(self):
        # type: () -> ExhaustVentDryer
        raise NotImplementedError("This method must be implemented by the subclass.")

    def duplicate(self):
        # type: () -> ExhaustVentDryer
        raise NotImplementedError("This method must be implemented by the subclass.")


class ExhaustVentDryer(_ExhaustVentilatorBase):
    def __init__(self):
        super(ExhaustVentDryer, self).__init__()
        self.display_name = "_unnamed_dryer_exh_"

    def __copy__(self):
        # type: () -> ExhaustVentDryer
        return self.duplicate()

    def duplicate(self):
        # type: () -> ExhaustVentDryer
        new_obj = self.__class__()
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = copy(self.user_data)
        new_obj.quantity = self.quantity
        new_obj.annual_runtime_minutes = self.annual_runtime_minutes
        new_obj.device_class_name = self.device_class_name
        new_obj.exhaust_flow_rate_m3s = self.exhaust_flow_rate_m3s
        return new_obj


class ExhaustVentKitchenHood(_ExhaustVentilatorBase):
    def __init__(self):
        super(ExhaustVentKitchenHood, self).__init__()
        self.display_name = "_unnamed_kitchen_hood_exh_"

    def __copy__(self):
        # type: () -> ExhaustVentKitchenHood
        return self.duplicate()

    def duplicate(self):
        # type: () -> ExhaustVentKitchenHood
        new_obj = self.__class__()
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = copy(self.user_data)
        new_obj.quantity = self.quantity
        new_obj.annual_runtime_minutes = self.annual_runtime_minutes
        new_obj.device_class_name = self.device_class_name
        new_obj.exhaust_flow_rate_m3s = self.exhaust_flow_rate_m3s
        return new_obj


class ExhaustVentUserDefined(_ExhaustVentilatorBase):
    def __init__(self):
        super(ExhaustVentUserDefined, self).__init__()
        self.display_name = "_unnamed_user_defined_exh_"

    def __copy__(self):
        # type: () -> ExhaustVentUserDefined
        return self.duplicate()

    def duplicate(self):
        # type: () -> ExhaustVentUserDefined
        new_obj = self.__class__()
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = copy(self.user_data)
        new_obj.quantity = self.quantity
        new_obj.annual_runtime_minutes = self.annual_runtime_minutes
        new_obj.device_class_name = self.device_class_name
        new_obj.exhaust_flow_rate_m3s = self.exhaust_flow_rate_m3s
        return new_obj


class PhExhaustDeviceBuilder(object):
    """Constructor class for HBPH-Exhaust Ventilation Devices"""

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> _ExhaustVentilatorBase
        """Find the right device constructor class from the module based on the 'type' name."""
        device_class_name = _input_dict["device_class_name"]  # type: str

        valid_class_types = [nm for nm in dir(sys.modules[__name__]) if nm.startswith("ExhaustVent")]

        if device_class_name not in valid_class_types:
            raise UnknownPhExhaustVentTypeError(valid_class_types, device_class_name)
        device_class = getattr(sys.modules[__name__], device_class_name)  # type: _ExhaustVentilatorBase
        new_equipment = device_class.from_dict(_input_dict)
        return new_equipment

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        """Overwrite .NET ToString."""
        return repr(self)
