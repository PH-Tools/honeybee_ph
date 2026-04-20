# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Building 'Segment' Level Data Attributes"""

import warnings
from copy import copy

try:
    from typing import Any, Dict, Union
except ImportError:
    pass  # Python2.7

try:
    from ladybug_geometry.geometry3d.plane import Plane
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee_energy_ph.construction.thermal_bridge import PhThermalBridge
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_energy_ph.construction:\n\t{}".format(e))

try:
    from honeybee_ph import _base, phi, phius, site
    from honeybee_ph_standards.sourcefactors import factors
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


## --------------------------------------------------------------------------------------
## -- Enums


class PhVentilationSummerBypassMode(enumerables.CustomEnum):
    """Summer bypass control mode for the ventilation system heat exchanger.

    Values:
        1-None: No bypass.
        2-Temperature Controlled: Bypass activated by temperature difference.
        3-Enthalpy Controlled: Bypass activated by enthalpy difference.
        4-Always: Bypass always active in summer.
    """

    allowed = ["1-None", "2-Temperature Controlled", "3-Enthalpy Controlled", "4-Always"]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhVentilationSummerBypassMode, self).__init__(_value)


class PhWindExposureType(enumerables.CustomEnum):
    """Wind exposure classification for infiltration calculations.

    Values:
        1-SEVERAL_SIDES_EXPOSED_NO_SCREENING: Multiple exposed sides, no screening.
        2-SEVERAL_SIDES_EXPOSED_MODERATE_SCREENING: Multiple exposed sides, moderate screening.
        3-SEVERAL_SIDES_EXPOSED_HIGH_SCREENING: Multiple exposed sides, high screening.
        4-ONE_SIDE_EXPOSED_NO_SCREENING: One exposed side, no screening.
        5-ONE_SIDE_EXPOSED_MODERATE_SCREENING: One exposed side, moderate screening.
        6-USER_DEFINED: User-defined wind exposure coefficient.
        7-ONE_SIDE_EXPOSED_HIGH_SCREENING: One exposed side, high screening.
    """

    allowed = [
        "1-SEVERAL_SIDES_EXPOSED_NO_SCREENING",
        "2-SEVERAL_SIDES_EXPOSED_MODERATE_SCREENING",
        "3-SEVERAL_SIDES_EXPOSED_HIGH_SCREENING",
        "4-ONE_SIDE_EXPOSED_NO_SCREENING",
        "5-ONE_SIDE_EXPOSED_MODERATE_SCREENING",
        "6-USER_DEFINED",
        "7-ONE_SIDE_EXPOSED_HIGH_SCREENING",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhWindExposureType, self).__init__(_value)


class PhSummerVentilationExtractSystemControl(enumerables.CustomEnum):
    """Control mode for summer nighttime extract ventilation system.

    Values:
        1-TEMPERATURE_CONTROLLED: Controlled by temperature setpoint.
        2-HUMIDITY_CONTROLLED: Controlled by humidity setpoint.
    """

    allowed = [
        "1-TEMPERATURE_CONTROLLED",
        "2-HUMIDITY_CONTROLLED",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhSummerVentilationExtractSystemControl, self).__init__(_value)


## --------------------------------------------------------------------------------------
## -- Data Classes


class SummerVentilation(_base._Base):
    """Summer ventilation settings for a building segment.

    Controls bypass mode, daytime/nighttime extract ventilation, and
    window ventilation parameters used in overheating calculations.

    Attributes:
        ventilation_system_ach (Optional[float]): Ventilation system air change rate.
        summer_bypass_mode (PhVentilationSummerBypassMode): HRV bypass control mode.
            Default: "4-Always".
        daytime_extract_system_ach (float): Daytime extract system ACH.
        daytime_extract_system_fan_power_wh_m3 (float): Daytime extract fan specific
            power in Wh/m3.
        daytime_window_ach (float): Daytime window ventilation ACH.
        nighttime_extract_system_ach (float): Nighttime extract system ACH.
        nighttime_extract_system_fan_power_wh_m3 (float): Nighttime extract fan
            specific power in Wh/m3.
        nighttime_extract_system_heat_fraction (float): Nighttime extract heat
            recovery fraction.
        nighttime_extract_system_control (PhSummerVentilationExtractSystemControl):
            Nighttime extract system control mode. Default: "1-TEMPERATURE_CONTROLLED".
        nighttime_window_ach (float): Nighttime window ventilation ACH.
        nighttime_minimum_indoor_temp_C (float): Minimum indoor temperature for
            nighttime ventilation in degrees Celsius.
    """

    def __init__(
        self,
        _ventilation_system_ach=None,
        _ventilation_system_summer_bypass_mode="4-Always",
        _daytime_extract_system_ach=0.0,
        _daytime_extract_system_fan_power_wh_m3=0.0,
        _daytime_window_ach=0.0,
        _nighttime_extract_system_ach=0.0,
        _nighttime_extract_system_fan_power_wh_m3=0.0,
        _nighttime_extract_system_heat_fraction=0.0,
        _nighttime_extract_system_control="1-TEMPERATURE_CONTROLLED",
        _nighttime_window_ach=0.0,
        _nighttime_minimum_indoor_temp_C=0.0,
    ):
        # type: (float | None, int | str, float, float, float, float, float, float, int | str, float, float) -> None
        super(SummerVentilation, self).__init__()
        self.ventilation_system_ach = _ventilation_system_ach
        self.summer_bypass_mode = PhVentilationSummerBypassMode(_ventilation_system_summer_bypass_mode)
        self.daytime_extract_system_ach = _daytime_extract_system_ach
        self.daytime_extract_system_fan_power_wh_m3 = _daytime_extract_system_fan_power_wh_m3
        self.daytime_window_ach = _daytime_window_ach
        self.nighttime_extract_system_ach = _nighttime_extract_system_ach
        self.nighttime_extract_system_fan_power_wh_m3 = _nighttime_extract_system_fan_power_wh_m3
        self.nighttime_extract_system_heat_fraction = _nighttime_extract_system_heat_fraction
        self.nighttime_extract_system_control = PhSummerVentilationExtractSystemControl(
            _nighttime_extract_system_control
        )
        self.nighttime_window_ach = _nighttime_window_ach
        self.nighttime_minimum_indoor_temp_C = _nighttime_minimum_indoor_temp_C

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)
        d["display_name"] = self.display_name
        d["summer_bypass_mode"] = self.summer_bypass_mode.to_dict()
        d["ventilation_system_ach"] = self.ventilation_system_ach
        d["daytime_extract_system_ach"] = self.daytime_extract_system_ach
        d["daytime_extract_system_fan_power_wh_m3"] = self.daytime_extract_system_fan_power_wh_m3
        d["daytime_window_ach"] = self.daytime_window_ach
        d["nighttime_extract_system_ach"] = self.nighttime_extract_system_ach
        d["nighttime_extract_system_fan_power_wh_m3"] = self.nighttime_extract_system_fan_power_wh_m3
        d["nighttime_extract_system_heat_fraction"] = self.nighttime_extract_system_heat_fraction
        d["nighttime_extract_system_control"] = self.nighttime_extract_system_control.to_dict()
        d["nighttime_window_ach"] = self.nighttime_window_ach
        d["nighttime_minimum_indoor_temp_C"] = self.nighttime_minimum_indoor_temp_C

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (Dict[str, Any]) -> SummerVentilation
        obj = cls()

        obj.identifier = _dict.get("identifier")
        obj.user_data = _dict.get("user_data", {})
        obj.display_name = _dict.get("display_name")
        obj.ventilation_system_ach = _dict.get("ventilation_system_ach")
        obj.summer_bypass_mode = PhVentilationSummerBypassMode.from_dict(_dict.get("summer_bypass_mode", "4-Always"))
        obj.daytime_extract_system_ach = _dict.get("daytime_extract_system_ach")
        obj.daytime_extract_system_fan_power_wh_m3 = _dict.get("daytime_extract_system_fan_power_wh_m3")
        obj.daytime_window_ach = _dict.get("daytime_window_ach")
        obj.nighttime_extract_system_ach = _dict.get("nighttime_extract_system_ach")
        obj.nighttime_extract_system_fan_power_wh_m3 = _dict.get("nighttime_extract_system_fan_power_wh_m3")
        obj.nighttime_extract_system_heat_fraction = _dict.get("nighttime_extract_system_heat_fraction")
        obj.nighttime_extract_system_control = PhSummerVentilationExtractSystemControl.from_dict(
            _dict.get("nighttime_extract_system_control", {"value": "1-TEMPERATURE_CONTROLLED"})
        )
        obj.nighttime_window_ach = _dict.get("nighttime_window_ach")
        obj.nighttime_minimum_indoor_temp_C = _dict.get("nighttime_minimum_indoor_temp_C")

        return obj

    def __copy__(self):
        # type: () -> SummerVentilation
        obj = SummerVentilation()
        obj.set_base_attrs_from_source(self)
        obj.user_data = self.user_data
        obj.summer_bypass_mode = PhVentilationSummerBypassMode(self.summer_bypass_mode.value)
        obj.ventilation_system_ach = self.ventilation_system_ach
        obj.daytime_extract_system_ach = self.daytime_extract_system_ach
        obj.daytime_extract_system_fan_power_wh_m3 = self.daytime_extract_system_fan_power_wh_m3
        obj.daytime_window_ach = self.daytime_window_ach
        obj.nighttime_extract_system_ach = self.nighttime_extract_system_ach
        obj.nighttime_extract_system_fan_power_wh_m3 = self.nighttime_extract_system_fan_power_wh_m3
        obj.nighttime_extract_system_heat_fraction = self.nighttime_extract_system_heat_fraction
        obj.nighttime_extract_system_control = PhSummerVentilationExtractSystemControl(
            self.nighttime_extract_system_control.value
        )
        obj.nighttime_window_ach = self.nighttime_window_ach
        obj.nighttime_minimum_indoor_temp_C = self.nighttime_minimum_indoor_temp_C

        return obj

    def duplicate(self):
        # type: () -> SummerVentilation
        return self.__copy__()


class SetPoints(_base._Base):
    """Heating and cooling temperature setpoints for a building segment.

    Attributes:
        winter (float): Winter heating setpoint in degrees Celsius. Default: 20.0.
        summer (float): Summer cooling setpoint in degrees Celsius. Default: 25.0.
    """

    def __init__(self):
        super(SetPoints, self).__init__()
        self.winter = 20.0
        self.summer = 25.0

    def to_dict(self):
        # type: () -> Dict[str, float]
        d = {}

        d["winter"] = self.winter
        d["summer"] = self.summer
        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)
        d["display_name"] = self.display_name

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (Dict[str, Any]) -> SetPoints
        obj = cls()

        obj.winter = _dict.get("winter", 20.0)
        obj.summer = _dict.get("summer", 25.0)
        obj.identifier = _dict.get("identifier")
        obj.user_data = _dict.get("user_data", {})
        obj.display_name = _dict.get("display_name")

        return obj

    def __copy__(self):
        # type: () -> SetPoints
        obj = SetPoints()
        obj.set_base_attrs_from_source(self)
        obj.winter = self.winter
        obj.summer = self.summer
        obj.user_data = self.user_data

        return obj

    def duplicate(self):
        # type: () -> SetPoints
        return self.__copy__()


## --------------------------------------------------------------------------------------
## -- Building Segment Class


class BldgSegment(_base._Base):
    """A building segment representing one thermally distinct zone for PH certification.

    Contains site/climate data, certification settings, setpoints, thermal bridges,
    and summer ventilation parameters. Typically one per building, but multi-zone
    models may have several.

    Attributes:
        num_floor_levels (int): Number of above-grade floor levels. Default: 1.
        num_dwelling_units (int): Number of dwelling units. Default: 1.
        site (Site): Climate and location data for this segment.
        source_energy_factors (FactorCollection): Source energy conversion factors.
        co2e_factors (FactorCollection): CO2-equivalent emission factors.
        phius_certification (PhiusCertification): Phius certification settings.
        phi_certification (PhiCertification): PHI certification settings.
        set_points (SetPoints): Heating/cooling temperature setpoints.
        mech_room_temp (float): Mechanical room temperature in degrees Celsius.
            Default: 20.0.
        non_combustible_materials (bool): True if non-combustible construction.
            Default: False.
        thermal_bridges (Dict[str, PhThermalBridge]): Thermal bridges keyed by
            identifier.
        wind_exposure_type (PhWindExposureType): Wind exposure classification.
        summer_ventilation (SummerVentilation): Summer ventilation parameters.
    """

    def __init__(self):
        super(BldgSegment, self).__init__()
        self.display_name = "Unnamed_Bldg_Segment"
        self.num_floor_levels = 1
        self.num_dwelling_units = 1
        self.site = site.Site()
        self.source_energy_factors = factors.FactorCollection("Source_Energy")
        self.co2e_factors = factors.FactorCollection("CO2")
        self.phius_certification = phius.PhiusCertification()
        self.phi_certification = phi.PhiCertification()
        self.set_points = SetPoints()
        self.mech_room_temp = 20.0
        self.non_combustible_materials = False
        self.thermal_bridges = {}  # type: Dict[str, PhThermalBridge]
        self.wind_exposure_type = PhWindExposureType("1-SEVERAL_SIDES_EXPOSED_NO_SCREENING")
        self.summer_ventilation = SummerVentilation()

    @property
    def summer_hrv_bypass_mode(self):
        ## Provide user-warning to use the new `summer_ventilation` attribute instead of the old `summer_hrv_bypass_mode` attribute"""
        warnings.warn(
            "The summer_hrv_bypass_mode attribute is now part of the summer_ventilation attribute. Please use the summer_ventilation attribute instead.",
            DeprecationWarning,
        )
        return self.summer_ventilation.summer_bypass_mode

    @summer_hrv_bypass_mode.setter
    def summer_hrv_bypass_mode(self, value):
        # type: (Union[str, int, PhVentilationSummerBypassMode]) -> None
        ## Provide user-warning to use the new `summer_ventilation` attribute instead of the old `summer_hrv_bypass_mode` attribute
        warnings.warn(
            "The summer_hrv_bypass_mode attribute is now part of the summer_ventilation attribute. Please use the summer_ventilation attribute instead.",
            DeprecationWarning,
        )
        if isinstance(value, PhVentilationSummerBypassMode):
            self.summer_ventilation.summer_bypass_mode = value
        else:
            self.summer_ventilation.summer_bypass_mode = PhVentilationSummerBypassMode(value)

    def add_new_thermal_bridge(self, tb):
        # type: (PhThermalBridge) -> None
        self.thermal_bridges[tb.identifier] = tb

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)
        d["display_name"] = self.display_name
        d["name"] = self.display_name
        d["num_floor_levels"] = self.num_floor_levels
        d["num_dwelling_units"] = self.num_dwelling_units
        d["site"] = self.site.to_dict()
        d["source_energy_factors"] = self.source_energy_factors.to_dict()
        d["co2e_factors"] = self.co2e_factors.to_dict()
        d["phius_certification"] = self.phius_certification.to_dict()
        d["phi_certification"] = self.phi_certification.to_dict()
        d["set_points"] = self.set_points.to_dict()
        d["mech_room_temp"] = self.mech_room_temp
        d["non_combustible_materials"] = self.non_combustible_materials
        d["thermal_bridges"] = {}
        for tb in self.thermal_bridges.values():
            d["thermal_bridges"][str(tb.identifier)] = tb.to_dict()
        d["summer_ventilation"] = self.summer_ventilation.to_dict()
        d["wind_exposure_type"] = self.wind_exposure_type.to_dict()
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (Dict[str, Any]) -> BldgSegment
        obj = cls()

        obj.identifier = _dict.get("identifier", "")
        obj.user_data = _dict.get("user_data", {})
        obj.display_name = _dict.get("name", "")
        obj.num_floor_levels = _dict.get("num_floor_levels")
        obj.num_dwelling_units = _dict.get("num_dwelling_units")
        obj.site = site.Site.from_dict(_dict.get("site", {}))
        obj.source_energy_factors = factors.FactorCollection.from_dict(_dict.get("source_energy_factors", {}))
        obj.co2e_factors = factors.FactorCollection.from_dict(_dict.get("co2e_factors", {}))
        obj.phius_certification = phius.PhiusCertification.from_dict(_dict.get("phius_certification", {}))
        obj.phi_certification = phi.PhiCertification.from_dict(_dict.get("phi_certification", {}))
        obj.set_points = SetPoints.from_dict(_dict.get("set_points", {}))
        obj.mech_room_temp = _dict["mech_room_temp"]
        obj.non_combustible_materials = _dict.get("non_combustible_materials", False)
        for tb_dict in _dict.get("thermal_bridges", {}).values():
            tb_obj = PhThermalBridge.from_dict(tb_dict)
            obj.thermal_bridges[tb_obj.identifier] = tb_obj
        # Support both new and old serialization formats
        if "summer_ventilation" in _dict:
            obj.summer_ventilation = SummerVentilation.from_dict(_dict["summer_ventilation"])
        elif "summer_hrv_bypass_mode" in _dict:
            obj.summer_ventilation.summer_bypass_mode = PhVentilationSummerBypassMode.from_dict(_dict["summer_hrv_bypass_mode"])  # type: ignore
        obj.wind_exposure_type = PhWindExposureType.from_dict(_dict.get("wind_exposure_type", {}))

        return obj

    def __copy__(self):
        # type () -> BldgSegment
        new_obj = BldgSegment()
        new_obj.set_base_attrs_from_source(self)
        new_obj.num_floor_levels = self.num_floor_levels
        new_obj.num_dwelling_units = self.num_dwelling_units
        new_obj.site = self.site.duplicate()
        new_obj.source_energy_factors = self.source_energy_factors.duplicate()
        new_obj.co2e_factors = self.co2e_factors.duplicate()
        new_obj.phius_certification = self.phius_certification.duplicate()
        new_obj.phi_certification = self.phi_certification.duplicate()
        new_obj.set_points = self.set_points.duplicate()
        new_obj.mech_room_temp = self.mech_room_temp
        new_obj.non_combustible_materials = self.non_combustible_materials
        new_obj.thermal_bridges = {}
        for tb_k, tb_v in self.thermal_bridges.items():
            new_obj.thermal_bridges[tb_k] = tb_v.duplicate()
        new_obj.summer_ventilation = self.summer_ventilation.duplicate()
        new_obj.wind_exposure_type = PhWindExposureType(self.wind_exposure_type.value)
        return new_obj

    def duplicate(self):
        # type () -> BldgSegment
        return self.__copy__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> BldgSegment
        """Move the BldgSegment along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        """
        new_seg = self.duplicate()
        for k, tb in new_seg.thermal_bridges.items():
            new_seg.thermal_bridges[k] = tb.move(moving_vec3D)
        new_seg.phius_certification = new_seg.phius_certification.move(moving_vec3D)
        new_seg.phi_certification = new_seg.phi_certification.move(moving_vec3D)
        return new_seg

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> BldgSegment
        """Rotate the BldgSegment by a certain angle around an axis_vec3D and origin_pt3D.

        Right hand rule applies:
        If axis_vec3D has a positive orientation, rotation will be clockwise.
        If axis_vec3D has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis_vec3D representing the axis_vec3D of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        """
        new_seg = self.duplicate()
        for k, tb in new_seg.thermal_bridges.items():
            new_seg.thermal_bridges[k] = tb.rotate(axis_vec3D, angle_degrees, origin_pt3D)
        new_seg.phius_certification = new_seg.phius_certification.rotate(axis_vec3D, angle_degrees, origin_pt3D)
        new_seg.phi_certification = new_seg.phi_certification.rotate(axis_vec3D, angle_degrees, origin_pt3D)
        return new_seg

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> BldgSegment
        """Rotate the BldgSegment counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin_pt3D around which the object will be rotated.
        """
        new_seg = self.duplicate()
        for k, tb in new_seg.thermal_bridges.items():
            new_seg.thermal_bridges[k] = tb.rotate_xy(angle_degrees, origin_pt3D)
        new_seg.phius_certification = new_seg.phius_certification.rotate_xy(angle_degrees, origin_pt3D)
        new_seg.phi_certification = new_seg.phi_certification.rotate_xy(angle_degrees, origin_pt3D)
        return new_seg

    def reflect(self, plane):
        # type: (Plane) -> BldgSegment
        """Reflected the BldgSegment across a plane with the input normal vector and origin_pt3D.

        Args:
            plane: A Plane representing the plane across which the object will be reflected.
        """
        new_seg = self.duplicate()
        for k, tb in new_seg.thermal_bridges.items():
            new_seg.thermal_bridges[k] = tb.reflect(plane)
        new_seg.phius_certification = new_seg.phius_certification.reflect(plane)
        new_seg.phi_certification = new_seg.phi_certification.reflect(plane)
        return new_seg

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Point3D | None) -> BldgSegment
        """Scale the BldgSegment a factor from an origin_pt3D point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin_pt3D from which to scale.
                If None, it will be scaled from the World origin_pt3D (0, 0, 0).
        """
        new_seg = self.duplicate()
        for k, tb in new_seg.thermal_bridges.items():
            new_seg.thermal_bridges[k] = tb.scale(scale_factor, origin_pt3D)
        new_seg.phius_certification = new_seg.phius_certification.scale(scale_factor, origin_pt3D)
        new_seg.phi_certification = new_seg.phi_certification.scale(scale_factor, origin_pt3D)

        return new_seg
