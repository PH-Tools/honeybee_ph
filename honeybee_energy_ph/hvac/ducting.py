# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House HVAC Ducting Segment and Element Classes"""
try:
    from typing import Any, Dict, List, Optional, Union
except ImportError:
    pass  # IronPython

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_energy_ph.hvac import _base


class PhDuctSegment(_base._PhHVACBase):
    """A single duct segment (linear) with geometry and a attributes."""

    def __init__(
        self,
        _geom,
        _insul_thickness=25.4,
        _insul_conductivity=0.04,
        _insul_refl=True,
        _diameter=160,
        _height=None,
        _width=None,
    ):
        # type: (LineSegment3D, float, float, bool, float, Optional[float], Optional[float]) -> None
        super(PhDuctSegment, self).__init__()
        self.geometry = _geom
        self.insulation_thickness = _insul_thickness  # MM
        self.insulation_conductivity = _insul_conductivity
        self.insulation_reflective = _insul_refl
        self.diameter = _diameter  # MM
        self.height = _height  # MM
        self.width = _width  # MM

    @property
    def length(self):
        # type: () -> float
        """Return the length of the duct segment (M)."""
        return self.geometry.length

    @property
    def shape_type(self):
        # type: () -> int
        if (self.height is not None) and (self.width is not None):
            return 2  # Rectangular Duct
        else:
            return 1  # Round Duct

    @property
    def is_round_duct(self):
        # type: () -> bool
        return self.shape_type == 1

    @property
    def shape_type_description(self):
        # type: () -> str
        """Return a string description of the shape of the duct segment."""
        if self.is_round_duct:
            return "{:.2f}mm Θ".format(float(self.diameter))
        else:
            return "{:.0f}mm x {:.0f}mm".format(self.width or 0.0, self.height or 0.0)

    @classmethod
    def default(cls):
        # type: () -> PhDuctSegment
        """Return a default Duct segment with a length of 1.0"""

        pt1 = Point3D(0, 0, 0)
        pt2 = Point3D(1, 0, 0)
        geom = LineSegment3D.from_end_points(pt1, pt2)

        return cls(geom)

    def __copy__(self):
        # type: () -> PhDuctSegment
        new_obj = PhDuctSegment(self.geometry)

        new_obj.geometry = self.geometry
        new_obj.insulation_thickness = self.insulation_thickness
        new_obj.insulation_conductivity = self.insulation_conductivity
        new_obj.insulation_reflective = self.insulation_reflective
        new_obj.diameter = self.diameter
        new_obj.height = self.height
        new_obj.width = self.width
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data

        return self

    def duplicate(self):
        # type: () -> PhDuctSegment
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, dict]]
        d = super(PhDuctSegment, self).to_dict()

        d["geometry"] = self.geometry.to_dict()
        d["insulation_thickness"] = self.insulation_thickness
        d["insulation_conductivity"] = self.insulation_conductivity
        d["insulation_reflective"] = self.insulation_reflective
        d["diameter"] = self.diameter
        d["height"] = self.height
        d["width"] = self.width

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhDuctSegment
        new_obj = cls(_geom=LineSegment3D.from_dict(_input_dict["geometry"]))
        new_obj.insulation_thickness = _input_dict["insulation_thickness"]
        new_obj.insulation_conductivity = _input_dict["insulation_conductivity"]
        new_obj.insulation_reflective = _input_dict["insulation_reflective"]
        new_obj.diameter = _input_dict["diameter"]
        new_obj.height = _input_dict["height"]
        new_obj.width = _input_dict["width"]
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        return new_obj

    def __str__(self):
        return "{}: diam={}, length={:.3f}".format(
            self.__class__.__name__, self.diameter, self.length
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()


class PhDuctElement(_base._PhHVACBase):
    """A Duct Element made up of one or more individual Duct Segments."""

    def __init__(self, _display_name=None, _duct_type=1, *args, **kwargs):
        # type: (Optional[str], int, *Any, **Any) -> None
        super(PhDuctElement, self).__init__()
        self.display_name = _display_name or self.identifier_short
        self.duct_type = _duct_type
        self._segments = {}  # type: Dict[str, PhDuctSegment]

    @property
    def segments(self):
        # type: () -> List[PhDuctSegment]
        """Return a list of all the PhDuctSegments that make up the PhDuctElement."""
        return list(self._segments.values())

    @property
    def length(self):
        # type: () -> float
        """Return the total duct length of all the PhDuctSegments (M)."""
        return sum(s.length for s in self.segments)

    @property
    def is_round_duct(self):
        # type: () -> bool
        return self.shape_type == 1

    @property
    def shape_type(self):
        # type: () -> Optional[int]
        segment_types = {s.shape_type for s in self.segments}
        if len(segment_types) == 0:
            return None
        elif len(segment_types) == 1:
            return segment_types.pop()
        else:
            raise ValueError("Mixed shape-types in duct segments.")

    @property
    def shape_type_description(self):
        # type: () -> Optional[str]
        descriptions = {s.shape_type_description for s in self.segments}
        if len(descriptions) == 0:
            return None
        elif len(descriptions) == 1:
            return descriptions.pop()
        else:
            raise ValueError("Mixed shapes/sizes in duct segments.")

    @classmethod
    def default_supply_duct(cls, *args, **kwargs):
        # type: (*Any, **Any) -> PhDuctElement
        """Returns a default PhDuctElement with a single segment and a length of 1.0"""

        duct_element = cls(*args, **kwargs)
        duct_element.duct_type = 1
        duct_element.add_segment(PhDuctSegment.default())
        return duct_element

    @classmethod
    def default_exhaust_duct(cls, *args, **kwargs):
        # type: (*Any, **Any) -> PhDuctElement
        """Returns a default PhDuctElement with a single segment and a length of 1.0"""

        duct_element = cls(*args, **kwargs)
        duct_element.duct_type = 2
        duct_element.add_segment(PhDuctSegment.default())
        return duct_element

    def add_segment(self, _segment):
        # type: (PhDuctSegment) -> None
        """Add a new PhDuctSegment to the Duct Element."""
        # -- Check that the new segment is the right shape type
        if len(self.segments) > 0:
            if not _segment.shape_type == self.shape_type:
                msg = "Error: Cannot join round and rectangular duct segments."
                raise Exception(msg)

        self._segments[_segment.identifier] = _segment

    def __copy__(self):
        # type: () -> PhDuctElement
        new_obj = PhDuctElement()

        for segment in self.segments:
            new_obj.add_segment(segment.duplicate())

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.duct_type = self.duct_type
        new_obj.user_data = self.user_data

        return new_obj

    def duplicate(self):
        # type: () -> PhDuctElement
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, dict]]
        d = super(PhDuctElement, self).to_dict()

        d["segments"] = {}
        for segment in self.segments:
            d["segments"][segment.identifier] = segment.to_dict()
        d["duct_type"] = self.duct_type

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhDuctElement
        new_obj = cls()

        for seg_dict in _input_dict["segments"].values():
            new_obj._segments[seg_dict["identifier"]] = PhDuctSegment.from_dict(seg_dict)
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.duct_type = _input_dict["duct_type"]
        new_obj.user_data = _input_dict["user_data"]

        return new_obj

    def __str__(self):
        return "{}: (display_name={}, identifier={} ) [{} segments, len={:.3f}]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier,
            len(self.segments),
            self.length,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()
