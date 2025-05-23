# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PHI Certification Settings Class."""

from copy import copy

try:
    from typing import Any, Dict, Optional, Type, Union
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


class EnumProperty(object):
    """Descriptor for creating and managing the PHI-Cert Enum items.

    This Descriptor will create a new Enum type when it is called using the
    attribute name and the phpp_version #, This new enum will be used to manage
    the allowable values and clean / filter the user inputs.
    """

    allowed_inputs = {  # type: Dict[str, Dict[int, List]]
        "building_category_type": {
            9: [
                "1-RESIDENTIAL BUILDING",
                "2-NON-RESIDENTIAL BUILDING",
            ],
            10: [],
        },
        "building_use_type": {
            9: [
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "10-DWELLING",
                "11-NURSING HOME / STUDENTS",
                "12-OTHER",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "20-OFFICE / ADMIN. BUILDING",
                "21-SCHOOL",
                "22-OTHER",
            ],
            10: [
                "_",  # PHPP is so stupid. Who did the numbering?... sheesh...
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "10-RESIDENTIAL BUILDING: RESIDENTIAL (DEFAULT)",
                "_",
                "12-RESIDENTIAL BUILDING: OTHER",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "20-NON-RES BUILDING: OFFICE/ADMINISTRATION",
                "21-NON-RES BUILDING: SCHOOL HALF-DAYS (< 7 H)",
                "22-NON-RES BUILDING: SCHOOL FULL-TIME (≥ 7 H)",
                "23-NON-RES.: OTHER",
            ],
        },
        "ihg_type": {
            9: [
                "_",
                "2-STANDARD",
                "3-PHPP CALCULATION ('IHG' WORKSHEET)",
                "4-PHPP CALCULATION ('IHG NON-RES' WORKSHEET)",
            ],
            10: [
                "_",
                "2-STANDARD",
                "3-PHPP-CALCULATION ('IHG' WORKSHEET)",
                "4-PHPP-CALCULATION ('IHG NON-RES' WORKSHEET)",
            ],
        },
        "occupancy_type": {
            9: [
                "1-STANDARD (ONLY FOR RESIDENTIAL BUILDINGS)",
                "2-USER DETERMINED",
            ],
            10: [],
        },
        "certification_type": {
            9: [
                "1-PASSIVE HOUSE",
                "2-ENERPHIT",
                "3-PHI LOW ENERGY BUILDING",
                "4-OTHER",
            ],
            10: [
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "10-PASSIVE HOUSE",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "21-ENERPHIT (COMPONENT METHOD)",
                "22-ENERPHIT (ENERGY DEMAND METHOD)",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "30-PHI LOW ENERGY BUILDING",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "40-OTHER",
            ],
        },
        "certification_class": {
            9: [
                "1-CLASSIC",
                "2-PLUS",
                "3-PREMIUM",
            ],
            10: [
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "10-CLASSIC | PER (RENEWABLE)",
                "11-CLASSIC | PE (NON-RENEWABLE)",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "20-PLUS | PER (RENEWABLE)",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "_",
                "30-PREMIUM | PER (RENEWABLE)",
            ],
        },
        "primary_energy_type": {
            9: [
                "1-PE (NON-RENEWABLE)",
                "2-PER (RENEWABLE)",
            ],
            10: [
                "1-STANDARD",
                "2-PROJECT-SPECIFIC",
            ],
        },
        "enerphit_type": {
            9: [
                "1-COMPONENT METHOD",
                "2-ENERGY DEMAND METHOD",
            ],
            10: [],
        },
        "retrofit_type": {
            9: [
                "1-NEW BUILDING",
                "2-RETROFIT",
                "3-STEP-BY-STEP RETROFIT",
            ],
            10: [
                "1-NEW BUILDING",
                "2-RETROFIT",
                "3-STAGED RETROFIT",
            ],
        },
    }

    def __init__(self, attribute_name, _phpp_version=9):
        # type: (str, int) -> None
        self.attribute_name = attribute_name  # normally the same as the Class Attribute
        self.phpp_version = _phpp_version
        self.enum = self._create_enum_class()
        self.enum.allowed = self.allowed_inputs[self.attribute_name][self.phpp_version]

    def _create_enum_class(self):
        # type: () -> Type[enumerables.CustomEnum]
        """Create a new Enum based on the type of value."""
        return type("{}_phpp_v{}".format(self.attribute_name, self.phpp_version), (enumerables.CustomEnum,), {})

    def __set__(self, instance, value):
        # type: (Any, Optional[Union[str, int]]) -> None
        """Set the enum with the input value on the instance __dict__

        Arguments:
        ----------
            * instance: The descriptor class variable.
            * value: The value to validate and set.
        """

        if value:
            instance.__dict__[self.attribute_name] = self.enum(value)

        if instance.__dict__[self.attribute_name].value == "_":
            msg = "Error: Input value: '{}' for '{}' is not allowed. Check inputs.".format(value, self.attribute_name)
            raise Exception(msg)

    def __get__(self, instance, owner):
        # type: (Any, Any) -> enumerables.CustomEnum
        """
        Arguments:
        ---------
            * instance: The descriptor class variable.
            * owner: The Class which has the descriptor as a class variable.
        Returns:
        --------
            * (enumerables.CustomEnum): The Enum Instance object.
        """
        return instance.__dict__[self.attribute_name]

    def __str__(self):
        return "Validated[{}](storage_name={})".format(self.__class__.__name__, self.attribute_name)


# -----------------------------------------------------------------------------


class _PHPPSettingsBase(object):
    """Base class with methods for use by PHPP-Settings objects."""

    phpp_version = 9  # default
    tfa_override = None  # type: float | None

    def to_dict(self):
        # type: () -> Dict[str, int | str]
        d = {}
        d["phpp_version"] = self.phpp_version
        for k in vars(self).keys():
            attribute = getattr(self, k)
            try:
                d[k] = attribute.value  # -- Try and set the 'value' first
            except AttributeError:
                d[k] = attribute  # -- fallback if that fails for some reason
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, int | str]) -> _PHPPSettingsBase
        new_obj = cls()
        for k in vars(new_obj).keys():
            setattr(new_obj, k, _input_dict[k])
        return new_obj

    def __copy__(self):
        # type: () -> _PHPPSettingsBase
        new_obj = self.__class__()
        for k in vars(new_obj).keys():
            attribute = getattr(self, k)
            try:
                setattr(new_obj, k, attribute.value)  # -- Try and set the 'value' first
            except AttributeError:
                setattr(new_obj, k, attribute)  # -- fallback if that fails for some reason
        return new_obj

    def duplicate(self):
        # type: () -> _PHPPSettingsBase
        return self.__copy__()


class PHPPSettings10(_PHPPSettingsBase):
    """Settings for PHPP v10"""

    phpp_version = 10
    building_use_type = EnumProperty("building_use_type", phpp_version)
    ihg_type = EnumProperty("ihg_type", phpp_version)
    certification_class = EnumProperty("certification_class", phpp_version)
    certification_type = EnumProperty("certification_type", phpp_version)
    primary_energy_type = EnumProperty("primary_energy_type", phpp_version)
    retrofit_type = EnumProperty("retrofit_type", phpp_version)

    def __init__(self):
        # -- Setup the enum defaults
        super(PHPPSettings10, self).__init__()
        self.building_use_type = "10-RESIDENTIAL BUILDING: RESIDENTIAL (DEFAULT)"  # type: EnumProperty
        self.ihg_type = "2-STANDARD"  # type: EnumProperty
        self.certification_class = "10-CLASSIC | PER (RENEWABLE)"  # type: EnumProperty
        self.certification_type = "10-PASSIVE HOUSE"  # type: EnumProperty
        self.primary_energy_type = "1-STANDARD"  # type: EnumProperty
        self.retrofit_type = "1-NEW BUILDING"  # type: EnumProperty
        self.tfa_override = None


class PHPPSettings9(_PHPPSettingsBase):
    """Settings for PHPP v9"""

    phpp_version = 9
    building_category_type = EnumProperty("building_category_type", phpp_version)
    building_use_type = EnumProperty("building_use_type", phpp_version)
    ihg_type = EnumProperty("ihg_type", phpp_version)
    occupancy_type = EnumProperty("occupancy_type", phpp_version)
    certification_type = EnumProperty("certification_type", phpp_version)
    certification_class = EnumProperty("certification_class", phpp_version)
    primary_energy_type = EnumProperty("primary_energy_type", phpp_version)
    enerphit_type = EnumProperty("enerphit_type", phpp_version)
    retrofit_type = EnumProperty("retrofit_type", phpp_version)

    def __init__(self):
        # -- Setup the enum defaults
        super(PHPPSettings9, self).__init__()
        self.building_category_type = "1-RESIDENTIAL BUILDING"  # type: EnumProperty
        self.building_use_type = "10-DWELLING"  # type: EnumProperty
        self.ihg_type = "2-Standard"  # type: EnumProperty
        self.occupancy_type = "1-STANDARD (ONLY FOR RESIDENTIAL BUILDINGS)"  # type: EnumProperty
        self.certification_type = "1-PASSIVE HOUSE"  # type: EnumProperty
        self.certification_class = "1-CLASSIC"  # type: EnumProperty
        self.primary_energy_type = "2-PER (RENEWABLE)"  # type: EnumProperty
        self.enerphit_type = "2-ENERGY DEMAND METHOD"  # type: EnumProperty
        self.retrofit_type = "1-NEW BUILDING"  # type: EnumProperty
        self.tfa_override = None


class PhiCertification(_base._Base):
    """PHI PHPP Certification object with Attributes that vary by version (9 | 10)"""

    def __init__(self, phpp_version=9):
        # type: (int) -> None
        super(PhiCertification, self).__init__()
        self.phpp_version = phpp_version
        if phpp_version == 10:
            self.attributes = PHPPSettings10()
        elif self.phpp_version == 9:
            self.attributes = PHPPSettings9()
        else:
            msg = "Error: Unknown PHPP Version? Got: '{}'".format(self.phpp_version)
            raise Exception(msg)

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)

    def to_dict(self):
        # type: () -> Dict
        d = {}
        d["phpp_version"] = self.phpp_version
        d["attributes"] = self.attributes.to_dict()
        d["identifier"] = self.identifier
        d["user_data"] = self.user_data
        d["display_name"] = self.display_name
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhiCertification
        new_obj = cls()
        attr_dict = _input_dict["attributes"]
        if attr_dict["phpp_version"] == 10:
            new_obj.attributes = PHPPSettings10.from_dict(attr_dict)
        else:
            new_obj.attributes = PHPPSettings9.from_dict(attr_dict)

        new_obj.identifier = _input_dict.get("identifier", "")
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.display_name = _input_dict.get("display_name", "")

        return new_obj

    def __copy__(self):
        # type: () -> PhiCertification
        obj = PhiCertification()
        obj.phpp_version = self.phpp_version
        obj.set_base_attrs_from_source(self)
        obj.attributes = self.attributes.duplicate()
        obj.user_data = copy(self.user_data)

        return obj

    def duplicate(self):
        # type: () -> PhiCertification
        return self.__copy__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhiCertification
        """Move the Phius Certification Object along a vector.

        Args:
            moving_vec3D: A Vector3D with the direction and distance to move the ray.
        """
        new_obj = self.duplicate()
        return new_obj

    def rotate(self, axis_vec3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhiCertification
        """Rotate the Phius Certification Object by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis_vec3D: A Vector3D axis representing the axis of rotation.
            angle_degrees: An angle for rotation in degrees.
            origin_pt3D: A Point3D for the origin around which the object will be rotated.
        """
        new_obj = self.duplicate()
        return new_obj

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhiCertification
        """Rotate the Phius Certification Object counterclockwise in the XY plane by a certain angle.

        Args:
            angle_degrees: An angle in degrees.
            origin_pt3D: A Point3D for the origin around which the object will be rotated.
        """
        new_obj = self.duplicate()
        return new_obj

    def reflect(self, plane):
        # type: (Plane) -> PhiCertification
        """Reflected the Phius Certification Object across a plane.

        Args:
            normal_vec3D: A Plane representing the plane across which to reflect.
        """
        new_obj = self.duplicate()
        return new_obj

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Point3D | None) -> PhiCertification
        """Scale the Phius Certification Object by a factor from an origin point.

        Args:
            scale_factor: A number representing how much the line segment should be scaled.
            origin_pt3D: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_obj = self.duplicate()
        if new_obj.attributes.tfa_override is not None:
            new_obj.attributes.tfa_override = new_obj.attributes.tfa_override * scale_factor
        return new_obj
