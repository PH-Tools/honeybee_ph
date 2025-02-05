# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Building 'Segment' Level Data Attributes"""

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


class PhVentilationSummerBypassMode(enumerables.CustomEnum):
    allowed = ["1-None", "2-Temperature Controlled", "3-Enthalpy Controlled", "4-Always"]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhVentilationSummerBypassMode, self).__init__(_value)


class PhWindExposureType(enumerables.CustomEnum):
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


class SetPoints(_base._Base):
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


class BldgSegment(_base._Base):
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
        self.summer_hrv_bypass_mode = PhVentilationSummerBypassMode("4-Always")

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
        d["summer_hrv_bypass_mode"] = self.summer_hrv_bypass_mode.to_dict()
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
        obj.summer_hrv_bypass_mode = PhVentilationSummerBypassMode.from_dict(_dict.get("summer_hrv_bypass_mode", {}))
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
        new_obj.summer_hrv_bypass_mode = PhVentilationSummerBypassMode(self.summer_hrv_bypass_mode.value)
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
