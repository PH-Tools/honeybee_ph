# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Ducts."""

try:
    from typing import Any, Dict, List, Optional, Union
except ImportError:
    pass  # IronPython

try:
    from ladybug_geometry.geometry3d.pointvector import Point3D
    from ladybug_geometry.geometry3d.polyline import LineSegment3D
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee_phhvac import _base
except ImportError as e:
    raise ImportError("\nFailed to import honeybee_phhvac:\n\t{}".format(e))


class PhDuctSegment(_base._PhHVACBase):
    """A single duct segment (linear) with geometry and a attributes.

    Note: All geometric information is in the model's unit-type (meters by default).
    """

    def __init__(
        self,
        _geom,
        _insul_thickness=0.0254,
        _insul_conductivity=0.04,
        _insul_refl=True,
        _diameter=0.160,
        _height=None,
        _width=None,
    ):
        # type: (LineSegment3D, float, float, bool, float, Optional[float], Optional[float]) -> None
        super(PhDuctSegment, self).__init__()
        self.geometry = _geom
        self.insulation_thickness = _insul_thickness
        self.insulation_conductivity = _insul_conductivity
        self.insulation_reflective = _insul_refl
        self.diameter = _diameter
        self.height = _height
        self.width = _width

    @property
    def length(self):
        # type: () -> float
        """Return the length of the duct segment in model-units."""
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
            return "{:.3f} Θ".format(float(self.diameter))
        else:
            return "{:.3f} x {:.3f}".format(self.width or 0.0, self.height or 0.0)

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
        return "{}: diam={}, length={:.3f}".format(self.__class__.__name__, self.diameter, self.length)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

    def move(self, moving_vec):
        # type: (Point3D) -> PhDuctSegment
        """Move the duct segment along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        new_segment = self.duplicate()
        new_segment.geometry = self.geometry.move(moving_vec)
        return new_segment

    def rotate(self, axis, angle, origin):
        # type: (Point3D, float, Point3D) -> PhDuctSegment
        """Rotate the duct segment by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_segment = self.duplicate()
        new_segment.geometry = self.geometry.rotate(axis, angle, origin)
        return new_segment

    def rotate_xy(self, angle, origin):
        # type: (float, Point3D) -> PhDuctSegment
        """Rotate the duct segment counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_segment = self.duplicate()
        new_segment.geometry = self.geometry.rotate_xy(angle, origin)
        return new_segment

    def reflect(self, normal, origin):
        # type: (Point3D, Point3D) -> PhDuctSegment
        """Reflected the duct segment across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        new_segment = self.duplicate()
        new_segment.geometry = self.geometry.reflect(normal, origin)
        return new_segment

    def scale(self, factor, origin=None):
        # type: (float, Optional[Point3D]) -> PhDuctSegment
        """Scale the duct segment by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_segment = self.duplicate()
        new_segment.geometry = self.geometry.scale(factor, origin)
        new_segment.insulation_thickness = self.insulation_thickness * factor
        new_segment.diameter = self.diameter * factor
        new_segment.height = factor * self.height if self.height else None
        new_segment.width = factor * self.width if self.width else None
        return new_segment


class PhDuctElement(_base._PhHVACBase):
    """A Duct Element made up of one or more individual Duct Segments.

    Note: All geometric information is in the model's unit-type (meters by default).
    """

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
        """Return the total duct length of all the PhDuctSegments in model-units."""
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

    def clear_segments(self):
        # type: () -> None
        """Clear all the segments from the duct element."""
        self._segments = {}

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

    def move(self, moving_vec):
        """Move the duct element's segment along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        new_element = self.duplicate()
        new_element.clear_segments()
        for segment in self.segments:
            new_element.add_segment(segment.move(moving_vec))
        return new_element

    def rotate(self, axis, angle, origin):
        """Rotate the duct element's segment by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_element = self.duplicate()
        new_element.clear_segments()
        for segment in self.segments:
            new_element.add_segment(segment.rotate(axis, angle, origin))
        return new_element

    def rotate_xy(self, angle, origin):
        """Rotate the duct element's segment counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_element = self.duplicate()
        new_element.clear_segments()
        for segment in self.segments:
            new_element.add_segment(segment.rotate_xy(angle, origin))
        return new_element

    def reflect(self, normal, origin):
        """Reflected the duct element's segment across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        new_element = self.duplicate()
        new_element.clear_segments()
        for segment in self.segments:
            new_element.add_segment(segment.reflect(normal, origin))
        return new_element

    def scale(self, factor, origin=None):
        # type: (float, Optional[Point3D]) -> PhDuctElement
        """Scale the duct element's segments by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_element = self.duplicate()
        new_element.clear_segments()
        for segment in self.segments:
            new_element.add_segment(segment.scale(factor, origin))
        return new_element
