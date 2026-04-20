# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Phius Certification Data Class"""

from copy import copy

try:
    from typing import Optional, Union
except ImportError:
    pass  # IronPython 2.7

try:
    from ladybug_geometry.geometry3d.plane import Plane
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee_ph import _base
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))


# -----------------------------------------------------------------------------


class PhiusBuildingCertificationProgram(enumerables.CustomEnum):
    """Phius building certification program type enumeration.

    Values:
        1-Default: Default (unspecified) certification program.
        2-PHIUS 2015: PHIUS 2015 standard.
        3-PHIUS 2018: PHIUS 2018 standard.
        4-Italian: Italian certification standard.
        5-PHIUS 2018 CORE: PHIUS 2018 CORE standard.
        6-PHIUS 2018 ZERO: PHIUS 2018 ZERO standard.
        7-PHIUS 2021 CORE: PHIUS 2021 CORE standard.
        8-PHIUS 2021 ZERO: PHIUS 2021 ZERO standard.
    """

    allowed = [
        "1-Default",
        "2-PHIUS 2015",
        "3-PHIUS 2018",
        "4-Italian",
        "5-PHIUS 2018 CORE",
        "6-PHIUS 2018 ZERO",
        "7-PHIUS 2021 CORE",
        "8-PHIUS 2021 ZERO",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingCertificationProgram, self).__init__(_value)


class PhiusBuildingCategoryType(enumerables.CustomEnum):
    """Phius building category type enumeration.

    Values:
        1-RESIDENTIAL BUILDING: Residential building category.
        2-NON-RESIDENTIAL BUILDING: Non-residential building category.
    """

    allowed = [
        "1-RESIDENTIAL BUILDING",
        "2-NON-RESIDENTIAL BUILDING",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingCategoryType, self).__init__(_value)


class PhiusBuildingUseType(enumerables.CustomEnum):
    """Phius building use type enumeration.

    Values:
        1-RESIDENTIAL: Residential use.
        4-OFFICE/ADMINISTRATIVE BUILDING: Office or administrative building use.
        5-SCHOOL: School use.
        6-OTHER: Other use type.
        7-UNDEFINED/UNFINISHED: Undefined or unfinished use type.
    """

    allowed = [
        "1-RESIDENTIAL",
        "",
        "",
        "4-OFFICE/ADMINISTRATIVE BUILDING",
        "5-SCHOOL",
        "6-OTHER",
        "7-UNDEFINED/UNFINISHED",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingUseType, self).__init__(_value)

        # Quick double check cus' the numbering here is so stupid
        if self.value == "":
            raise Exception("Error: WUFI's '_building_use_type' numbering is weird. Check the 'inputs' value is valid?")


class PhiusBuildingStatus(enumerables.CustomEnum):
    """Phius building status enumeration.

    Values:
        1-IN_PLANNING: Building is in the planning phase.
        2-UNDER_CONSTRUCTION: Building is under construction.
        3-COMPLETE: Building is complete.
    """

    allowed = [
        "1-IN_PLANNING",
        "2-UNDER_CONSTRUCTION",
        "3-COMPLETE",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingStatus, self).__init__(_value)


class PhiusBuildingType(enumerables.CustomEnum):
    """Phius building type enumeration.

    Values:
        1-NEW_CONSTRUCTION: New construction project.
        2-RETROFIT: Retrofit of an existing building.
        3-MIXED: Mixed new construction and retrofit.
    """

    allowed = [
        "1-NEW_CONSTRUCTION",
        "2-RETROFIT",
        "3-MIXED",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhiusBuildingType, self).__init__(_value)


# -----------------------------------------------------------------------------


class PhiusCertification(_base._Base):
    """Phius certification configuration and performance targets for a building.

    Attributes:
        localization_selection_type (int): Localization selection type identifier.
        PHIUS2021_heating_demand (float): PHIUS 2021 heating demand target (kBtu/ft2/yr).
        PHIUS2021_cooling_demand (float): PHIUS 2021 cooling demand target (kBtu/ft2/yr).
        PHIUS2021_heating_load (float): PHIUS 2021 heating load target (Btu/h/ft2).
        PHIUS2021_cooling_load (float): PHIUS 2021 cooling load target (Btu/h/ft2).
        int_gains_evap_per_person (int): Evaporative internal gains per person (W/person).
        int_gains_flush_heat_loss (bool): Whether to account for flush heat loss.
        int_gains_num_toilets (int): Number of toilets in the building.
        int_gains_toilet_room_util_pat (Optional[str]): Toilet room utilization pattern name.
        int_gains_use_school_defaults (bool): Whether to use school default internal gains.
        int_gains_dhw_marginal_perf_ratio (Optional[float]): DHW marginal performance ratio.
        icfa_override (Optional[float]): Manual override for interior conditioned floor area.
    """

    def __init__(self):
        super(PhiusCertification, self).__init__()
        self.localization_selection_type = 2

        self._certification_program = PhiusBuildingCertificationProgram("7-PHIUS 2021 CORE")
        self._building_category_type = PhiusBuildingCategoryType("1-RESIDENTIAL BUILDING")
        self._building_use_type = PhiusBuildingUseType("1-RESIDENTIAL")
        self._building_status = PhiusBuildingStatus("1-IN_PLANNING")
        self._building_type = PhiusBuildingType("1-NEW_CONSTRUCTION")

        self.PHIUS2021_heating_demand = 15.0
        self.PHIUS2021_cooling_demand = 15.0
        self.PHIUS2021_heating_load = 10.0
        self.PHIUS2021_cooling_load = 10.0

        self.int_gains_evap_per_person = 15
        self.int_gains_flush_heat_loss = True
        self.int_gains_num_toilets = 1
        self.int_gains_toilet_room_util_pat = None
        self.int_gains_use_school_defaults = False
        self.int_gains_dhw_marginal_perf_ratio = None

        self.icfa_override = None  # type: float | None

    @property
    def certification_program(self):
        # type: () -> PhiusBuildingCertificationProgram
        """The Phius certification program for this building."""
        return self._certification_program

    @certification_program.setter
    def certification_program(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._certification_program = PhiusBuildingCertificationProgram(_input)

    @property
    def building_category_type(self):
        # type: () -> PhiusBuildingCategoryType
        """The Phius building category type (residential or non-residential)."""
        return self._building_category_type

    @building_category_type.setter
    def building_category_type(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_category_type = PhiusBuildingCategoryType(_input)

    @property
    def building_use_type(self):
        # type: () -> PhiusBuildingUseType
        """The Phius building use type (residential, school, office, etc.)."""
        return self._building_use_type

    @building_use_type.setter
    def building_use_type(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_use_type = PhiusBuildingUseType(_input)

    @property
    def building_status(self):
        # type: () -> PhiusBuildingStatus
        """The Phius building status (planning, construction, or complete)."""
        return self._building_status

    @building_status.setter
    def building_status(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_status = PhiusBuildingStatus(_input)

    @property
    def building_type(self):
        # type: () -> PhiusBuildingType
        """The Phius building type (new construction, retrofit, or mixed)."""
        return self._building_type

    @building_type.setter
    def building_type(self, _input):
        # type: (Optional[Union[str, int]]) -> None
        if _input:
            self._building_type = PhiusBuildingType(_input)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> dict
        d = {}

        d["localization_selection_type"] = self.localization_selection_type

        d["certification_program"] = self.certification_program.to_dict()
        d["building_category_type"] = self.building_category_type.to_dict()
        d["building_use_type"] = self.building_use_type.to_dict()
        d["building_status"] = self.building_status.to_dict()
        d["building_type"] = self.building_type.to_dict()

        d["PHIUS2021_heating_demand"] = self.PHIUS2021_heating_demand
        d["PHIUS2021_cooling_demand"] = self.PHIUS2021_cooling_demand
        d["PHIUS2021_heating_load"] = self.PHIUS2021_heating_load
        d["PHIUS2021_cooling_load"] = self.PHIUS2021_cooling_load

        d["int_gains_evap_per_person"] = self.int_gains_evap_per_person
        d["int_gains_flush_heat_loss"] = self.int_gains_flush_heat_loss
        d["int_gains_num_toilets"] = self.int_gains_num_toilets
        d["int_gains_toilet_room_util_pat"] = self.int_gains_toilet_room_util_pat
        d["int_gains_use_school_defaults"] = self.int_gains_use_school_defaults
        d["int_gains_dhw_marginal_perf_ratio"] = self.int_gains_dhw_marginal_perf_ratio

        d["identifier"] = self.identifier
        d["user_data"] = copy(self.user_data)
        d["display_name"] = self.display_name

        d["icfa_override"] = self.icfa_override

        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict) -> PhiusCertification
        obj = cls()

        obj.localization_selection_type = _dict.get("localization_selection_type")

        obj._certification_program = PhiusBuildingCertificationProgram.from_dict(_dict.get("certification_program", {}))
        obj._building_category_type = PhiusBuildingCategoryType.from_dict(_dict.get("building_category_type", {}))
        obj._building_use_type = PhiusBuildingUseType.from_dict(_dict.get("building_use_type", {}))
        obj._building_status = PhiusBuildingStatus.from_dict(_dict.get("building_status", {}))
        obj._building_type = PhiusBuildingType.from_dict(_dict.get("building_type", {}))

        obj.PHIUS2021_heating_demand = _dict.get("PHIUS2021_heating_demand")
        obj.PHIUS2021_cooling_demand = _dict.get("PHIUS2021_cooling_demand")
        obj.PHIUS2021_heating_load = _dict.get("PHIUS2021_heating_load")
        obj.PHIUS2021_cooling_load = _dict.get("PHIUS2021_cooling_load")

        obj.int_gains_evap_per_person = _dict.get("int_gains_evap_per_person")
        obj.int_gains_flush_heat_loss = _dict.get("int_gains_flush_heat_loss")
        obj.int_gains_num_toilets = _dict.get("int_gains_num_toilets")
        obj.int_gains_toilet_room_util_pat = _dict.get("int_gains_toilet_room_util_pat")
        obj.int_gains_use_school_defaults = _dict.get("int_gains_use_school_defaults")
        obj.int_gains_dhw_marginal_perf_ratio = _dict.get("int_gains_dhw_marginal_perf_ratio")

        obj.identifier = _dict.get("identifier")
        obj.user_data = _dict.get("user_data", {})
        obj.display_name = _dict.get("display_name")

        obj.icfa_override = _dict.get("icfa_override")

        return obj

    def __copy__(self):
        # type: () -> PhiusCertification
        obj = PhiusCertification()

        obj.set_base_attrs_from_source(self)
        obj.localization_selection_type = self.localization_selection_type

        obj._certification_program = self._certification_program
        obj._building_category_type = self._building_category_type
        obj._building_use_type = self._building_use_type
        obj._building_status = self._building_status
        obj._building_type = self._building_type

        obj.PHIUS2021_heating_demand = self.PHIUS2021_heating_demand
        obj.PHIUS2021_cooling_demand = self.PHIUS2021_cooling_demand
        obj.PHIUS2021_heating_load = self.PHIUS2021_heating_load
        obj.PHIUS2021_cooling_load = self.PHIUS2021_cooling_load

        obj.int_gains_evap_per_person = self.int_gains_evap_per_person
        obj.int_gains_flush_heat_loss = self.int_gains_flush_heat_loss
        obj.int_gains_num_toilets = self.int_gains_num_toilets
        obj.int_gains_toilet_room_util_pat = self.int_gains_toilet_room_util_pat
        obj.int_gains_use_school_defaults = self.int_gains_use_school_defaults
        obj.int_gains_dhw_marginal_perf_ratio = self.int_gains_dhw_marginal_perf_ratio

        obj.icfa_override = self.icfa_override

        return obj

    def duplicate(self):
        # type: () -> PhiusCertification
        return self.__copy__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhiusCertification
        """Move the Phius Certification Object along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A Vector3D with the direction and distance to move the ray.

        Returns:
        --------
            * PhiusCertification: A new duplicated PhiusCertification object.
        """
        new_obj = self.duplicate()
        return new_obj

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhiusCertification
        """Rotate the Phius Certification Object by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_vec3D (Vector3D): A Vector3D axis representing the axis of rotation.
            * angle_degrees (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): A Point3D for the origin around which the object will be rotated.

        Returns:
        --------
            * PhiusCertification: A new duplicated PhiusCertification object.
        """
        new_obj = self.duplicate()
        return new_obj

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhiusCertification
        """Rotate the Phius Certification Object counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degrees (float): An angle in degrees.
            * origin_pt3D (Point3D): A Point3D for the origin around which the object will be rotated.

        Returns:
        --------
            * PhiusCertification: A new duplicated PhiusCertification object.
        """
        new_obj = self.duplicate()
        return new_obj

    def reflect(self, plane):
        # type: (Plane) -> PhiusCertification
        """Reflect the Phius Certification Object across a plane.

        Arguments:
        ----------
            * plane (Plane): A Plane representing the plane across which to reflect.

        Returns:
        --------
            * PhiusCertification: A new duplicated PhiusCertification object.
        """
        new_obj = self.duplicate()
        return new_obj

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> PhiusCertification
        """Scale the Phius Certification Object by a factor from an origin point.

        Arguments:
        ----------
            * scale_factor (float): A number representing how much the object should be scaled.
            * origin_pt3D (Optional[Point3D]): A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * PhiusCertification: A new duplicated PhiusCertification object with scaled icfa_override.
        """
        new_obj = self.duplicate()
        if new_obj.icfa_override is not None:
            new_obj.icfa_override = new_obj.icfa_override * scale_factor
        return new_obj
