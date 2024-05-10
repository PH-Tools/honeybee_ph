# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH Foundation Objects."""

from copy import copy

try:
    from typing import Any, Dict, List, Union
except ImportError:
    pass  # Python2.7

try:
    from honeybee_ph import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph:\n\t{}".format(e))

try:
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_ph_utils:\n\t{}".format(e))


# -----------------------------------------------------------------------------


class PhFoundationType(enumerables.CustomEnum):
    allowed = [
        "1-HEATED_BASEMENT",
        "2-UNHEATED_BASEMENT",
        "3-SLAB_ON_GRADE",
        "4-VENTED_CRAWLSPACE",
        "5-NONE",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhFoundationType, self).__init__(_value)


class PhSlabEdgeInsulationPosition(enumerables.CustomEnum):
    allowed = [
        "1-UNDEFINED",
        "2-HORIZONTAL",
        "3-VERTICAL",
    ]

    def __init__(self, _value=1):
        # type: (Union[str, int]) -> None
        super(PhSlabEdgeInsulationPosition, self).__init__(_value)


# -----------------------------------------------------------------------------
# -- Base Class


class PhFoundation(_base._Base):
    def __init__(self):
        super(PhFoundation, self).__init__()
        self.foundation_type = PhFoundationType("5-NONE")

    def duplicate(self):
        # type: () -> PhFoundation
        return self.__copy__()

    def __copy__(self):
        new_obj = self.__class__()
        new_obj.display_name = self.display_name
        new_obj.identifier = self.identifier
        new_obj.user_data = self.user_data
        new_obj.foundation_type = PhFoundationType(self.foundation_type.value)
        new_obj.user_data = self.user_data
        return new_obj

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}

        d["identifier"] = str(self.identifier)
        d["display_name"] = self.display_name
        d["user_data"] = copy(self.user_data)
        d["foundation_type_value"] = self.foundation_type.value
        d["user_data"] = copy(self.user_data)

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhFoundation
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.foundation_type = PhFoundationType(_input_dict["foundation_type_value"])
        new_obj.user_data = _input_dict.get("user_data", {})

        return new_obj

    def base_attrs_from_dict(self, _obj, _input_dict):
        # type: (PhFoundation, dict) -> None
        """Set the base object attributes from a dictionary

        Arguments:
        ----------
            * _obj (PhFoundation): The PH Foundation object to set the attributes of.
            * _input_dict (dict): The dictionary to get the attribute values from.

        Returns:
        --------
            * None
        """
        for attr_name in vars(self).keys():
            try:
                # Strip off underscore so it uses the property setters
                if attr_name.startswith("_"):
                    attr_name = attr_name[1:]
                setattr(_obj, attr_name, _input_dict[attr_name])
            except KeyError:
                pass
        return None

    def __str__(self):
        return "{}(display_name: {}, type: {})".format(
            self.__class__.__name__, self.display_name, self.foundation_type.value
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


# -----------------------------------------------------------------------------
# -- Specific Foundation Types


class PhHeatedBasement(PhFoundation):
    def __init__(self):
        super(PhHeatedBasement, self).__init__()
        self.foundation_type = PhFoundationType("1-HEATED_BASEMENT")
        self.floor_slab_area_m2 = 0.0
        self.floor_slab_u_value = 1.0
        self.floor_slab_exposed_perimeter_m = 0.0
        self.slab_depth_below_grade_m = 2.5
        self.basement_wall_u_value = 1.0

    def __copy__(self):
        # type: () -> PhHeatedBasement
        obj = self.__class__()
        obj.display_name = self.display_name
        obj.identifier = self.identifier
        obj.user_data = self.user_data
        obj.foundation_type = self.foundation_type
        obj.floor_slab_area_m2 = self.floor_slab_area_m2
        obj.floor_slab_u_value = self.floor_slab_u_value
        obj.floor_slab_exposed_perimeter_m = self.floor_slab_exposed_perimeter_m
        obj.slab_depth_below_grade_m = self.slab_depth_below_grade_m
        obj.basement_wall_u_value = self.basement_wall_u_value
        return obj

    def duplicate(self):
        # type: () -> PhHeatedBasement
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhHeatedBasement, self).to_dict())
        d["floor_slab_area_m2"] = self.floor_slab_area_m2
        d["floor_slab_u_value"] = self.floor_slab_u_value
        d["floor_slab_exposed_perimeter_m"] = self.floor_slab_exposed_perimeter_m
        d["slab_depth_below_grade_m"] = self.slab_depth_below_grade_m
        d["basement_wall_u_value"] = self.basement_wall_u_value
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHeatedBasement
        new_obj = cls()
        super(PhHeatedBasement, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.floor_slab_area_m2 = _input_dict["floor_slab_area_m2"]
        new_obj.floor_slab_u_value = _input_dict["floor_slab_u_value"]
        new_obj.floor_slab_exposed_perimeter_m = _input_dict["floor_slab_exposed_perimeter_m"]
        new_obj.slab_depth_below_grade_m = _input_dict["slab_depth_below_grade_m"]
        new_obj.basement_wall_u_value = _input_dict["basement_wall_u_value"]
        return new_obj


class PhUnheatedBasement(PhFoundation):
    def __init__(self):
        super(PhUnheatedBasement, self).__init__()
        self.foundation_type = PhFoundationType("2-UNHEATED_BASEMENT")
        self.floor_ceiling_area_m2 = 0.0
        self.ceiling_u_value = 1.0
        self.floor_slab_exposed_perimeter_m = 0.0
        self.slab_depth_below_grade_m = 0.0
        self.basement_wall_height_above_grade_m = 0.0
        self.basement_wall_uValue_below_grade = 1.0
        self.basement_wall_uValue_above_grade = 1.0
        self.floor_slab_u_value = 1.0
        self.basement_volume_m3 = 0.0
        self.basement_ventilation_ach = 0.0

    def __copy__(self):
        # type: () -> PhUnheatedBasement
        obj = self.__class__()
        obj.display_name = self.display_name
        obj.identifier = self.identifier
        obj.user_data = self.user_data
        obj.foundation_type = self.foundation_type
        obj.floor_ceiling_area_m2 = self.floor_ceiling_area_m2
        obj.ceiling_u_value = self.ceiling_u_value
        obj.floor_slab_exposed_perimeter_m = self.floor_slab_exposed_perimeter_m
        obj.slab_depth_below_grade_m = self.slab_depth_below_grade_m
        obj.basement_wall_height_above_grade_m = self.basement_wall_height_above_grade_m
        obj.basement_wall_uValue_below_grade = self.basement_wall_uValue_below_grade
        obj.basement_wall_uValue_above_grade = self.basement_wall_uValue_above_grade
        obj.floor_slab_u_value = self.floor_slab_u_value
        obj.basement_volume_m3 = self.basement_volume_m3
        obj.basement_ventilation_ach = self.basement_ventilation_ach
        return obj

    def duplicate(self):
        # type: () -> PhUnheatedBasement
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhUnheatedBasement, self).to_dict())
        d["floor_ceiling_area_m2"] = self.floor_ceiling_area_m2
        d["ceiling_u_value"] = self.ceiling_u_value
        d["floor_slab_exposed_perimeter_m"] = self.floor_slab_exposed_perimeter_m
        d["slab_depth_below_grade_m"] = self.slab_depth_below_grade_m
        d["basement_wall_height_above_grade_m"] = self.basement_wall_height_above_grade_m
        d["basement_wall_uValue_below_grade"] = self.basement_wall_uValue_below_grade
        d["basement_wall_uValue_above_grade"] = self.basement_wall_uValue_above_grade
        d["floor_slab_u_value"] = self.floor_slab_u_value
        d["basement_volume_m3"] = self.basement_volume_m3
        d["basement_ventilation_ach"] = self.basement_ventilation_ach
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhUnheatedBasement
        new_obj = cls()
        super(PhUnheatedBasement, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.floor_ceiling_area_m2 = _input_dict["floor_ceiling_area_m2"]
        new_obj.ceiling_u_value = _input_dict["ceiling_u_value"]
        new_obj.floor_slab_exposed_perimeter_m = _input_dict["floor_slab_exposed_perimeter_m"]
        new_obj.slab_depth_below_grade_m = _input_dict["slab_depth_below_grade_m"]
        new_obj.basement_wall_height_above_grade_m = _input_dict["basement_wall_height_above_grade_m"]
        new_obj.basement_wall_uValue_below_grade = _input_dict["basement_wall_uValue_below_grade"]
        new_obj.basement_wall_uValue_above_grade = _input_dict["basement_wall_uValue_above_grade"]
        new_obj.floor_slab_u_value = _input_dict["floor_slab_u_value"]
        new_obj.basement_volume_m3 = _input_dict["basement_volume_m3"]
        new_obj.basement_ventilation_ach = _input_dict["basement_ventilation_ach"]
        return new_obj


class PhSlabOnGrade(PhFoundation):
    def __init__(self):
        super(PhSlabOnGrade, self).__init__()
        self.foundation_type = PhFoundationType("3-SLAB_ON_GRADE")
        self.floor_slab_area_m2 = 0.0
        self.floor_slab_u_value = 1.0
        self.floor_slab_exposed_perimeter_m = 0.0
        self._perim_insulation_position = PhSlabEdgeInsulationPosition("3-VERTICAL")
        self.perim_insulation_width_or_depth_m = 0.300
        self.perim_insulation_thickness_m = 0.050
        self.perim_insulation_conductivity = 0.04

    @property
    def perim_insulation_position(self):
        return self._perim_insulation_position

    @perim_insulation_position.setter
    def perim_insulation_position(self, _input):
        self._perim_insulation_position = PhSlabEdgeInsulationPosition(_input)

    def __copy__(self):
        # type: () -> PhSlabOnGrade
        obj = self.__class__()
        obj.display_name = self.display_name
        obj.identifier = self.identifier
        obj.user_data = self.user_data
        obj.foundation_type = self.foundation_type
        obj.floor_slab_area_m2 = self.floor_slab_area_m2
        obj.floor_slab_u_value = self.floor_slab_u_value
        obj.floor_slab_exposed_perimeter_m = self.floor_slab_exposed_perimeter_m
        obj._perim_insulation_position = self._perim_insulation_position
        obj.perim_insulation_width_or_depth_m = self.perim_insulation_width_or_depth_m
        obj.perim_insulation_thickness_m = self.perim_insulation_thickness_m
        obj.perim_insulation_conductivity = self.perim_insulation_conductivity
        return obj

    def duplicate(self):
        # type: () -> PhSlabOnGrad
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhSlabOnGrade, self).to_dict())
        d["floor_slab_area_m2"] = self.floor_slab_area_m2
        d["floor_slab_u_value"] = self.floor_slab_u_value
        d["floor_slab_exposed_perimeter_m"] = self.floor_slab_exposed_perimeter_m
        d["perim_insulation_position_value"] = self.perim_insulation_position.value
        d["perim_insulation_width_or_depth_m"] = self.perim_insulation_width_or_depth_m
        d["perim_insulation_thickness_m"] = self.perim_insulation_thickness_m
        d["perim_insulation_conductivity"] = self.perim_insulation_conductivity
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhSlabOnGrade
        new_obj = cls()
        super(PhSlabOnGrade, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.floor_slab_area_m2 = _input_dict["floor_slab_area_m2"]
        new_obj.floor_slab_u_value = _input_dict["floor_slab_u_value"]
        new_obj.floor_slab_exposed_perimeter_m = _input_dict["floor_slab_exposed_perimeter_m"]
        new_obj.perim_insulation_position = _input_dict["perim_insulation_position_value"]
        new_obj.perim_insulation_width_or_depth_m = _input_dict["perim_insulation_width_or_depth_m"]
        new_obj.perim_insulation_thickness_m = _input_dict["perim_insulation_thickness_m"]
        new_obj.perim_insulation_conductivity = _input_dict["perim_insulation_conductivity"]
        return new_obj


class PhVentedCrawlspace(PhFoundation):
    def __init__(self):
        super(PhVentedCrawlspace, self).__init__()
        self.foundation_type = PhFoundationType("4-VENTED_CRAWLSPACE")
        self.crawlspace_floor_slab_area_m2 = 0.0
        self.ceiling_above_crawlspace_u_value = 1.0
        self.crawlspace_floor_exposed_perimeter_m = 2.5
        self.crawlspace_wall_height_above_grade_m = 0.0
        self.crawlspace_floor_u_value = 1.0
        self.crawlspace_vent_opening_are_m2 = 0.0
        self.crawlspace_wall_u_value = 1.0

    def __copy__(self):
        # type: () -> PhVentedCrawlspace
        obj = self.__class__()
        obj.display_name = self.display_name
        obj.identifier = self.identifier
        obj.user_data = self.user_data
        obj.foundation_type = self.foundation_type
        obj.crawlspace_floor_slab_area_m2 = self.crawlspace_floor_slab_area_m2
        obj.ceiling_above_crawlspace_u_value = self.ceiling_above_crawlspace_u_value
        obj.crawlspace_floor_exposed_perimeter_m = self.crawlspace_floor_exposed_perimeter_m
        obj.crawlspace_wall_height_above_grade_m = self.crawlspace_wall_height_above_grade_m
        obj.crawlspace_floor_u_value = self.crawlspace_floor_u_value
        obj.crawlspace_vent_opening_are_m2 = self.crawlspace_vent_opening_are_m2
        obj.crawlspace_wall_u_value = self.crawlspace_wall_u_value
        return obj

    def duplicate(self):
        # type: () -> PhVentedCrawlspace
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = {}
        d.update(super(PhVentedCrawlspace, self).to_dict())
        d["crawlspace_floor_slab_area_m2"] = self.crawlspace_floor_slab_area_m2
        d["ceiling_above_crawlspace_u_value"] = self.ceiling_above_crawlspace_u_value
        d["crawlspace_floor_exposed_perimeter_m"] = self.crawlspace_floor_exposed_perimeter_m
        d["crawlspace_wall_height_above_grade_m"] = self.crawlspace_wall_height_above_grade_m
        d["crawlspace_floor_u_value"] = self.crawlspace_floor_u_value
        d["crawlspace_vent_opening_are_m2"] = self.crawlspace_vent_opening_are_m2
        d["crawlspace_wall_u_value"] = self.crawlspace_wall_u_value
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhVentedCrawlspace
        new_obj = cls()
        super(PhVentedCrawlspace, new_obj).base_attrs_from_dict(new_obj, _input_dict)
        new_obj.crawlspace_floor_slab_area_m2 = _input_dict["crawlspace_floor_slab_area_m2"]
        new_obj.ceiling_above_crawlspace_u_value = _input_dict["ceiling_above_crawlspace_u_value"]
        new_obj.crawlspace_floor_exposed_perimeter_m = _input_dict["crawlspace_floor_exposed_perimeter_m"]
        new_obj.crawlspace_wall_height_above_grade_m = _input_dict["crawlspace_wall_height_above_grade_m"]
        new_obj.crawlspace_floor_u_value = _input_dict["crawlspace_floor_u_value"]
        new_obj.crawlspace_vent_opening_are_m2 = _input_dict["crawlspace_vent_opening_are_m2"]
        new_obj.crawlspace_wall_u_value = _input_dict["crawlspace_wall_u_value"]
        return new_obj


# -----------------------------------------------------------------------------
# --- Factory


class PhFoundationFactory(object):
    """Factory class to build any PhFoundation from an input dictionary."""

    type_map = {
        # enum-value: foundation class,
        "1-HEATED_BASEMENT": PhHeatedBasement,
        "2-UNHEATED_BASEMENT": PhUnheatedBasement,
        "3-SLAB_ON_GRADE": PhSlabOnGrade,
        "4-VENTED_CRAWLSPACE": PhVentedCrawlspace,
        "5-NONE": PhFoundation,
    }

    @classmethod
    def _check_input_type_name(cls, _input_type_name):
        # type: (str) -> None
        valid_class_type_names = list(cls.type_map.keys())

        if _input_type_name not in valid_class_type_names:
            msg = 'Error: Unknown PH-Foundation type? Got type of: "{}" but only types: {} are allowed?'.format(
                _input_type_name, valid_class_type_names
            )
            raise Exception(msg)

    @classmethod
    def _get_input_type_name(cls, _input_dict):
        # type: (Dict[str, Any]) -> str
        input_type_enum = PhFoundationType(_input_dict["foundation_type_value"])
        cls._check_input_type_name(input_type_enum.value)
        return input_type_enum.value

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhFoundation

        input_type_name = cls._get_input_type_name(_input_dict)
        foundation_class = cls.type_map[input_type_name]
        new_foundation = foundation_class.from_dict(_input_dict)

        return new_foundation
