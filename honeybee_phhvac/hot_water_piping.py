# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC: Hot Water Piping."""

from copy import copy
from math import radians

try:
    from typing import Any, Dict, List, Optional, Union
except ImportError:
    pass  # IronPython

try:
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
    from ladybug_geometry.geometry3d.polyline import LineSegment3D
except ImportError as e:
    raise ImportError("Failed to import ladybug_geometry", e)

try:
    from honeybee_phhvac import _base
except ImportError as e:
    raise ImportError("Failed to import honeybee_phhvac", e)

try:
    from honeybee_ph_utils import enumerables
except ImportError as e:
    raise ImportError("Failed to import honeybee_ph_utils", e)


# -- Piping  Enums ------------------------------------------------------------


class PhHvacPipeMaterial(enumerables.CustomEnum):
    """Enumeration of allowable pipe material types.

    Values:
        1-COPPER_M: Copper type M.
        2-COPPER_L: Copper type L (default).
        3-COPPER_K: Copper type K.
        4-CPVC_CTS_SDR: CPVC CTS SDR.
        5-CPVC_SCH_40: CPVC Schedule 40.
        6-PEX: PEX tubing.
        7-PE: Polyethylene tubing.
        8-PEX_CTS_SDR: PEX CTS SDR.
    """

    allowed = [
        "1-COPPER_M",
        "2-COPPER_L",
        "3-COPPER_K",
        "4-CPVC_CTS_SDR",
        "5-CPVC_SCH_40",
        "6-PEX",
        "7-PE",
        "8-PEX_CTS_SDR",
    ]

    def __init__(self, _value=2):
        # type: (Union[str, int]) -> None
        super(PhHvacPipeMaterial, self).__init__(_value)

    def __eq__(self, other):
        # type: (PhHvacPipeMaterial) -> bool
        return self.value == other.value

    def __ne__(self, other):
        # type: (PhHvacPipeMaterial) -> bool
        return self.value != other.value

    def __hash__(self):
        # type: () -> int
        return hash(self.value)


# -- Piping -------------------------------------------------------------------


class PhHvacPipeSegment(_base._PhHVACBase):
    """A single pipe segment (linear) with geometry and a diameter.

    Note: Following the LBT convention, while the geometry can be in a variety of
    units, thicknesses are all required to be in meters. This means that while the geometry
    will scale, the thickness and diameter will not.

    Attributes:
        geometry (LineSegment3D): The 3D line segment geometry of the pipe.
        diameter_mm (float): The pipe diameter in millimeters.
        insulation_thickness_mm (float): The insulation thickness in millimeters.
        insulation_conductivity (float): The insulation thermal conductivity (W/m-K).
        insulation_reflective (bool): True if the insulation has a reflective surface.
        insulation_quality (None): Reserved for future use.
        daily_period (float): Hours per day the pipe is in use.
        water_temp_c (float): The water temperature in degrees Celsius.
        material (PhHvacPipeMaterial): The pipe material type.
    """

    # fmt: off
    def __init__(
        self,
        _geom,
        _diameter_mm=12.7,
        _insul_thickness_mm=12.7,
        _insul_conductivity=0.04,
        _insul_refl=True,
        _insul_quality=None,
        _daily_period=24,
        _water_temp_c=60.0,
        _material=2,
        *args,
        **kwargs
    ):  # fmt: on
        # type: (LineSegment3D, float, float, float, bool, None, float, float, int, *Any, **Any) -> None
        super(PhHvacPipeSegment, self).__init__()
        self.geometry = _geom
        self.diameter_mm = _diameter_mm
        self.insulation_thickness_mm = _insul_thickness_mm
        self.insulation_conductivity = _insul_conductivity
        self.insulation_reflective = _insul_refl
        self.insulation_quality = _insul_quality
        self.daily_period = _daily_period
        self.water_temp_c = _water_temp_c
        self.material = PhHvacPipeMaterial(_material)

    @property
    def length(self):
        # type: () -> float
        """Return the length of the pipe segment in model-units."""
        return self.geometry.length

    @property
    def diameter_m(self):
        # type: () -> float
        """Return the diameter of the pipe segment in meters."""
        return self.diameter_mm * 0.001

    @property
    def insulation_thickness_m(self):
        # type: () -> float
        """Return the insulation thickness of the pipe segment in meters."""
        return self.insulation_thickness_mm * 0.001

    def __copy__(self):
        # type: () -> PhHvacPipeSegment
        new_obj = PhHvacPipeSegment(self.geometry.duplicate())

        new_obj.diameter_mm = self.diameter_mm
        new_obj.material = PhHvacPipeMaterial(self.material.value)
        new_obj.insulation_thickness_mm = self.insulation_thickness_mm
        new_obj.insulation_conductivity = self.insulation_conductivity
        new_obj.insulation_reflective = self.insulation_reflective
        new_obj.insulation_quality = self.insulation_quality
        new_obj.daily_period = self.daily_period
        new_obj.water_temp_c = self.water_temp_c
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = copy(self.user_data)

        return new_obj

    def duplicate(self):
        # type: () -> PhHvacPipeSegment
        return self.__copy__()

    def to_dict(self, _include_properties=False):
        # type: (bool) -> Dict[str, Union[str, Dict]]
        d = super(PhHvacPipeSegment, self).to_dict()
        d["geometry"] = self.geometry.to_dict()
        d["diameter_mm"] = self.diameter_mm
        d["material_value"] = self.material.value
        d["insulation_thickness_mm"] = self.insulation_thickness_mm
        d["insulation_conductivity"] = self.insulation_conductivity
        d["insulation_reflective"] = self.insulation_reflective
        d["insulation_quality"] = self.insulation_quality
        d["daily_period"] = self.daily_period
        d["water_temp_c"] = self.water_temp_c

        if _include_properties:
            d["length"] = self.length

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhHvacPipeSegment
        new_obj = cls(_geom=LineSegment3D.from_dict(_input_dict["geometry"]))
        new_obj.diameter_mm = _input_dict["diameter_mm"]
        new_obj.material = PhHvacPipeMaterial(_input_dict["material_value"])
        new_obj.insulation_thickness_mm = _input_dict["insulation_thickness_mm"]
        new_obj.insulation_conductivity = _input_dict["insulation_conductivity"]
        new_obj.insulation_reflective = _input_dict["insulation_reflective"]
        new_obj.insulation_quality = _input_dict["insulation_quality"]
        new_obj.daily_period = _input_dict["daily_period"]
        new_obj.water_temp_c = _input_dict["water_temp_c"]
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        return new_obj

    def __str__(self):
        return "{}: diam={:.3f} (MM), length={:.3f} (Model-Unit)".format(
            self.__class__.__name__, self.diameter_mm, self.length
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhHvacPipeSegment
        """Move the pipe's geometry along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A vector with the direction and distance to move.

        Returns:
        --------
            * PhHvacPipeSegment: A new PhHvacPipeSegment with the moved geometry.
        """
        dup = self.duplicate()
        dup.geometry = self.geometry.move(moving_vec3D)
        return dup

    def rotate(self, axis_3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeSegment
        """Rotate the pipe's geometry by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis_3D has a positive orientation, rotation will be clockwise.
        If axis_3D has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_3D (Vector3D): A vector representing the axis of rotation.
            * angle_degrees (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeSegment: A new PhHvacPipeSegment with the rotated geometry.
        """
        dup = self.duplicate()
        dup.geometry = self.geometry.rotate(axis_3D, radians(angle_degrees), origin_pt3D)
        return dup

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhHvacPipeSegment
        """Rotate the pipe's geometry counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degrees (float): An angle in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeSegment: A new PhHvacPipeSegment with the rotated geometry.
        """
        dup = self.duplicate()
        dup.geometry = self.geometry.rotate_xy(radians(angle_degrees), origin_pt3D)
        return dup

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> PhHvacPipeSegment
        """Reflect the pipe's geometry across a plane with the input normal vector and origin.

        Arguments:
        ----------
            * normal_vec3D (Vector3D): The normal vector for the reflection plane. THIS VECTOR MUST BE NORMALIZED.
            * origin_pt3D (Point3D): The origin from which to reflect.

        Returns:
        --------
            * PhHvacPipeSegment: A new PhHvacPipeSegment with the reflected geometry.
        """
        dup = self.duplicate()
        dup.geometry = self.geometry.reflect(normal_vec3D, origin_pt3D)
        return dup

    def scale(self, scale_factor, origin_pt3D=None):
        # type: (float, Union[None, Point3D]) -> PhHvacPipeSegment
        """Scale the pipe's geometry by a factor from an origin point.

        Note that following the LBT convention, while the geometry can be in a variety of
        units, thicknesses are all required to be in meters. This means that while the geometry
        will scale, the thickness and diameter will not.

        Arguments:
        ----------
            * scale_factor (float): How much the line segment should be scaled.
            * origin_pt3D (Optional[Point3D]): The origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * PhHvacPipeSegment: A new PhHvacPipeSegment with the scaled geometry.
        """
        new_pipe_segment = self.duplicate()
        new_pipe_segment.geometry = self.geometry.scale(scale_factor, origin_pt3D)
        return new_pipe_segment


class PhHvacPipeElement(_base._PhHVACBase):
    """A Pipe Element (Fixture) made up of one or more individual Pipe Segments.

    Attributes:
        identifier (str): Unique identifier for the pipe element.
        display_name (str): User-facing display name for the pipe element.
        user_data (dict): User-defined metadata.
    """

    def __init__(self):
        super(PhHvacPipeElement, self).__init__()
        self._segments = {}  # type: Dict[str, PhHvacPipeSegment]

    @property
    def segments(self):
        # type: () -> List[PhHvacPipeSegment]
        """Return a list of all the Pipe-Segments in the Pipe-Element."""
        return list(self._segments.values())

    @property
    def length(self):
        # type: () -> float
        """Return the total length of the pipe element in model-units."""
        return sum(s.length for s in self.segments)

    @property
    def diameter_mm(self):
        # type: () -> float
        """Return the length-weighted average diameter of all the pipe segments"""
        try:
            return sum(s.length * s.diameter_mm for s in self.segments) / self.length
        except ZeroDivisionError:
            return 0

    @property
    def water_temp_c(self):
        # type: () -> float
        """Return the length-weighted average water temperature of all the pipe segments"""
        try:
            return sum(s.length * s.water_temp_c for s in self.segments) / self.length
        except ZeroDivisionError:
            return 60.0

    @property
    def daily_period(self):
        # type: () -> float
        """Return the length-weighted average daily period of all the pipe segments"""
        try:
            return sum(s.length * s.daily_period for s in self.segments) / self.length
        except ZeroDivisionError:
            return 24.0

    @property
    def segment_names(self):
        # type: () -> List[str]
        """Return a list of the names of all the PipeSegments in the PipeElement."""
        return [s.display_name for s in self.segments]

    @property
    def material_name(self):
        # type: () -> str
        """Return the material name of the pipe element."""
        materials = {s.material for s in self.segments}
        if len(materials) == 0:
            return PhHvacPipeMaterial.allowed[0]
        elif len(materials) == 1:
            mat = materials.pop()
            return mat.value
        else:
            raise ValueError("Pipe segments: {} have different materials.".format(self.segment_names))

    def add_segment(self, _segment):
        # type: (PhHvacPipeSegment) -> None
        """Add a new Pipe Segment to the Pipe Element.

        Arguments:
        ----------
            * _segment (PhHvacPipeSegment): The pipe segment to add.
        """
        self._segments[_segment.identifier] = _segment

    def clear_segments(self):
        # type: () -> None
        """Clear all the segments from the pipe element."""
        self._segments = {}

    def __copy__(self):
        # type: () -> PhHvacPipeElement
        """Duplicate the pipe element."""
        new_obj = PhHvacPipeElement()

        for segment in self.segments:
            new_obj.add_segment(segment.duplicate())

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data

        return new_obj

    def duplicate(self):
        # type: () -> PhHvacPipeElement
        return self.__copy__()

    def to_dict(self, _include_properties=False):
        # type: (bool) -> dict[str, Union[str, dict]]
        d = super(PhHvacPipeElement, self).to_dict()
        d["segments"] = {}
        for segment in self.segments:
            d["segments"][segment.identifier] = segment.to_dict(_include_properties)

        if _include_properties:
            d["length"] = self.length
            d["water_temp"] = self.water_temp_c
            d["daily_period"] = self.daily_period
            d["material_name"] = self.material_name
            d["diameter"] = self.diameter_mm

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHvacPipeElement
        new_obj = cls()

        for seg_dict in _input_dict["segments"].values():
            new_obj._segments[seg_dict["identifier"]] = PhHvacPipeSegment.from_dict(seg_dict)
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        return new_obj

    def __str__(self):
        return "{}: (display_name={}, identifier={} ) [{} segments, len={:.3f}]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier_short,
            len(self.segments),
            self.length,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhHvacPipeElement
        """Move the pipe's segments along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A vector with the direction and distance to move.

        Returns:
        --------
            * PhHvacPipeElement: A new PhHvacPipeElement with the moved segments.
        """
        new_pipe_element = self.duplicate()
        new_pipe_element.clear_segments()
        for segment in self.segments:
            new_pipe_element.add_segment(segment.move(moving_vec3D))
        return new_pipe_element

    def rotate(self, axis_3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeElement
        """Rotate the pipe's segments by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis_3D has a positive orientation, rotation will be clockwise.
        If axis_3D has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_3D (Vector3D): A vector representing the axis of rotation.
            * angle_degrees (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeElement: A new PhHvacPipeElement with the rotated segments.
        """
        new_pipe_element = self.duplicate()
        new_pipe_element.clear_segments()
        for segment in self.segments:
            new_pipe_element.add_segment(segment.rotate(axis_3D, angle_degrees, origin_pt3D))
        return new_pipe_element

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhHvacPipeElement
        """Rotate the pipe's segments counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degrees (float): An angle in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeElement: A new PhHvacPipeElement with the rotated segments.
        """
        new_pipe_element = self.duplicate()
        new_pipe_element.clear_segments()
        for segment in self.segments:
            new_pipe_element.add_segment(segment.rotate_xy(angle_degrees, origin_pt3D))
        return new_pipe_element

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> PhHvacPipeElement
        """Reflect the pipe's segments across a plane with the input normal vector and origin.

        Arguments:
        ----------
            * normal_vec3D (Vector3D): The normal vector for the reflection plane. THIS VECTOR MUST BE NORMALIZED.
            * origin_pt3D (Point3D): The origin from which to reflect.

        Returns:
        --------
            * PhHvacPipeElement: A new PhHvacPipeElement with the reflected segments.
        """
        new_pipe_element = self.duplicate()
        new_pipe_element.clear_segments()
        for segment in self.segments:
            new_pipe_element.add_segment(segment.reflect(normal_vec3D, origin_pt3D))
        return new_pipe_element

    def scale(self, factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> PhHvacPipeElement
        """Scale the pipe's segments by a factor from an origin point.

        Arguments:
        ----------
            * factor (float): How much the segments should be scaled.
            * origin_pt3D (Optional[Point3D]): The origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * PhHvacPipeElement: A new PhHvacPipeElement with the scaled segments.
        """
        new_pipe_element = self.duplicate()
        new_pipe_element.clear_segments()
        for segment in self.segments:
            new_pipe_element.add_segment(segment.scale(factor, origin_pt3D))
        return new_pipe_element


class PhHvacPipeBranch(_base._PhHVACBase):
    """A 'Branch' Pipe which has geometry, and serves one or more 'Fixture' (Twig) pipe elements.

    Attributes:
        identifier (str): Unique identifier for the branch.
        display_name (str): User-facing display name for the branch.
        user_data (dict): User-defined metadata.
        pipe_element (PhHvacPipeElement): The pipe element representing the branch geometry.
        fixtures (List[PhHvacPipeElement]): The fixture (twig) pipe elements connected to this branch.
    """

    def __init__(self):
        # type: () -> None
        super(PhHvacPipeBranch, self).__init__()
        self.pipe_element = PhHvacPipeElement()
        self.fixtures = []  # type: (List[PhHvacPipeElement])

    @property
    def material_name(self):
        # type: () -> str
        """Return the material name of the pipe element."""
        return self.pipe_element.material_name

    @property
    def diameter_mm(self):
        # type: () -> float
        """Return the length-weighted diameter (MM) of the pipe element."""
        return self.pipe_element.diameter_mm

    @property
    def twigs(self):
        # type () -> List[PhPipeElement]
        """Alias for the 'fixtures' to better match Phius terminology."""
        return self.fixtures

    @property
    def segments(self):
        # type () -> List[PhPipeSegment]
        """Return a list of all the Pipe-Segments in the Branch."""
        return self.pipe_element.segments

    @property
    def length(self):
        # type: () -> float
        """Return the total length of the branch itself in model-units.
        For the total length of the Branch PLUS all fixtures, use 'total_length'.
        """
        return float(self.pipe_element.length)

    @property
    def water_temp_c(self):
        # type: () -> float
        """Return the length-weighted average water temperature of all the pipe segments."""
        return self.pipe_element.water_temp_c

    @property
    def daily_period(self):
        # type: () -> float
        """Return the length-weighted average daily period of all the pipe segments."""
        return self.pipe_element.daily_period

    @property
    def num_fixtures(self):
        # type: () -> int
        """Return the number of fixtures connected to the branch."""
        return len(self.fixtures)

    @property
    def total_length(self):
        # type: () -> float
        """Return the total length of the branch PLUS all fixture pipes in model-units."""
        return self.length + sum(f.length for f in self.fixtures)

    @property
    def total_home_run_fixture_length(self):
        # type: () -> float
        """Return the total length (in model-units) of all fixture pipes as measured from end to end.

        NOTE: This method will include the branch's length for EACH of
        the fixture pipes. The result will be a total hot-water transport length
        as if all the pipes were 'home-run' style. This value is used for the
        PHPP calculations and is not a true representation of the piping in the
        model.
        """
        return sum(fixture.length + self.length for fixture in self.fixtures)

    def add_fixture(self, _fixture):
        # type: (PhHvacPipeElement) -> None
        """Add a new fixture (twig) pipe element to the branch.

        Arguments:
        ----------
            * _fixture (PhHvacPipeElement): The fixture pipe element to add.
        """
        self.fixtures.append(_fixture)

    def __copy__(self):
        # type: () -> PhHvacPipeBranch
        new_obj = PhHvacPipeBranch()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data
        new_obj.pipe_element = self.pipe_element.duplicate()
        for fixture in self.fixtures:
            new_obj.add_fixture(fixture.duplicate())

        return new_obj

    def duplicate(self):
        # type: () -> PhHvacPipeBranch
        return self.__copy__()

    def to_dict(self, _include_properties=False):
        # type: (bool) -> Dict[str, Union[str, Dict]]
        d = super(PhHvacPipeBranch, self).to_dict()
        d["pipe_element"] = self.pipe_element.to_dict(_include_properties)
        d["fixtures"] = {}
        for branch in self.fixtures:
            d["fixtures"][branch.identifier] = branch.to_dict(_include_properties)

        if _include_properties:
            d["length"] = self.length
            d["water_temp_c"] = self.water_temp_c
            d["daily_period"] = self.daily_period
            d["num_fixtures"] = self.num_fixtures
            d["total_length"] = self.total_length
            d["total_home_run_fixture_length"] = self.total_home_run_fixture_length
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhHvacPipeBranch
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]
        new_obj.pipe_element = PhHvacPipeElement.from_dict(_input_dict["pipe_element"])
        for fixture_dict in _input_dict["fixtures"].values():
            new_obj.add_fixture(PhHvacPipeElement.from_dict(fixture_dict))

        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}: (display_name={}, identifier={} ) [{} segments, len={:.1f}, {} fixtures connected]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier_short,
            len(self.segments),
            float(self.length),
            len(self.fixtures),
        )

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return self.__repr__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhHvacPipeBranch
        """Move the pipe's elements along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A vector with the direction and distance to move.

        Returns:
        --------
            * PhHvacPipeBranch: A new PhHvacPipeBranch with the moved elements.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.move(moving_vec3D) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.move(moving_vec3D)
        return new_branch

    def rotate(self, axis_3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeBranch
        """Rotate the pipe's elements by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis_3D has a positive orientation, rotation will be clockwise.
        If axis_3D has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_3D (Vector3D): A vector representing the axis of rotation.
            * angle_degrees (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeBranch: A new PhHvacPipeBranch with the rotated elements.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.rotate(axis_3D, angle_degrees, origin_pt3D) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.rotate(axis_3D, angle_degrees, origin_pt3D)
        return new_branch

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhHvacPipeBranch
        """Rotate the pipe's elements counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degrees (float): An angle in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeBranch: A new PhHvacPipeBranch with the rotated elements.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.rotate_xy(angle_degrees, origin_pt3D) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.rotate_xy(angle_degrees, origin_pt3D)
        return new_branch

    def reflect(self, normal_vec3D, origin_pt3D):
        # type: (Vector3D, Point3D) -> PhHvacPipeBranch
        """Reflect the pipe's elements across a plane with the input normal vector and origin.

        Arguments:
        ----------
            * normal_vec3D (Vector3D): The normal vector for the reflection plane. THIS VECTOR MUST BE NORMALIZED.
            * origin_pt3D (Point3D): The origin from which to reflect.

        Returns:
        --------
            * PhHvacPipeBranch: A new PhHvacPipeBranch with the reflected elements.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.reflect(normal_vec3D, origin_pt3D) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.reflect(normal_vec3D, origin_pt3D)
        return new_branch

    def scale(self, factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> PhHvacPipeBranch
        """Scale the pipe's elements by a factor from an origin point.

        Arguments:
        ----------
            * factor (float): How much the elements should be scaled.
            * origin_pt3D (Optional[Point3D]): The origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * PhHvacPipeBranch: A new PhHvacPipeBranch with the scaled elements.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.scale(factor, origin_pt3D) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.scale(factor, origin_pt3D)
        return new_branch


class PhHvacPipeTrunk(_base._PhHVACBase):
    """A 'Trunk' Pipe which has geometry, and serves one or more 'Branches'.

    Attributes:
        identifier (str): Unique identifier for the trunk.
        display_name (str): User-facing display name for the trunk.
        user_data (dict): User-defined metadata.
        pipe_element (PhHvacPipeElement): The pipe element representing the trunk geometry.
        multiplier (int): A multiplier applied to the trunk for identical risers.
        branches (List[PhHvacPipeBranch]): The branch pipes connected to this trunk.
        demand_recirculation (bool): True if the trunk uses demand recirculation.
    """

    def __init__(self):
        # type: () -> None
        super(PhHvacPipeTrunk, self).__init__()
        self.pipe_element = PhHvacPipeElement()
        self.multiplier = 1  # type: int
        self.branches = []  # type: (List[PhHvacPipeBranch])
        self.demand_recirculation = False  # type: bool

    @property
    def material_name(self):
        # type: () -> str
        """Return the material name of the pipe element."""
        return self.pipe_element.material_name

    @property
    def diameter_mm(self):
        # type: () -> float
        """Return the length-weighted diameter (MM) name of the pipe element."""
        return self.pipe_element.diameter_mm

    @property
    def segments(self):
        # type () -> List[PhPipeSegment]
        """Return a list of all the Pipe-Segments in the Trunk."""
        return self.pipe_element.segments

    @property
    def length(self):
        # type: () -> float
        """Return the total length of the trunk itself in model-units."""
        return self.pipe_element.length

    @property
    def water_temp_c(self):
        # type: () -> float
        """Return the length-weighted average water temperature (deg-C) of all the pipe segments."""
        return self.pipe_element.water_temp_c

    @property
    def daily_period(self):
        # type: () -> float
        """Return the length-weighted average daily period of all the pipe segments."""
        return self.pipe_element.daily_period

    @property
    def num_fixtures(self):
        # type: () -> int
        """Return the number of fixtures connected to the trunk."""
        return sum(branch.num_fixtures for branch in self.branches)

    @property
    def total_length(self):
        # type: () -> float
        """Return the total length (in model-units) of the trunk PLUS all branches and fixture pipes in model-units."""
        return self.length + sum(branch.total_length for branch in self.branches)

    @property
    def total_home_run_fixture_length(self):
        # type: () -> float
        """Return the total length (in model-units) of all fixture pipes as measured from end to end.

        NOTE: This method will include the trunk's and branch's length for EACH of
        the fixture pipes. The result will be a total hot-water transport length
        as if all the pipes were 'home-run' style. This value is used for the
        PHPP calculations and is not a true representation of the piping in the
        model.
        """
        return sum(self.length + branch.total_home_run_fixture_length for branch in self.branches)

    def add_branch(self, _branch):
        # type: (PhHvacPipeBranch) -> None
        """Add a new branch pipe to the trunk.

        Arguments:
        ----------
            * _branch (PhHvacPipeBranch): The branch pipe to add.
        """
        self.branches.append(_branch)

    def __copy__(self):
        # type: () -> PhHvacPipeTrunk
        new_obj = PhHvacPipeTrunk()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data
        new_obj.pipe_element = self.pipe_element.duplicate()
        new_obj.multiplier = self.multiplier
        new_obj.demand_recirculation = self.demand_recirculation

        for branch in self.branches:
            new_obj.add_branch(branch.duplicate())

        return new_obj

    def duplicate(self):
        # type: () -> PhHvacPipeTrunk
        return self.__copy__()

    def to_dict(self, _include_properties=False):
        # type: (bool) -> Dict[str, Union[str, Dict]]
        d = super(PhHvacPipeTrunk, self).to_dict()
        d["pipe_element"] = self.pipe_element.to_dict(_include_properties)
        d["multiplier"] = self.multiplier
        d["demand_recirculation"] = self.demand_recirculation
        d["branches"] = {}
        for branch in self.branches:
            d["branches"][branch.identifier] = branch.to_dict(_include_properties)

        if _include_properties:
            d["length"] = self.length
            d["water_temp_c"] = self.water_temp_c
            d["daily_period"] = self.daily_period
            d["num_fixtures"] = self.num_fixtures
            d["total_length"] = self.total_length
            d["total_home_run_fixture_length"] = self.total_home_run_fixture_length
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhHvacPipeTrunk
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]
        new_obj.pipe_element = PhHvacPipeElement.from_dict(_input_dict["pipe_element"])
        new_obj.multiplier = _input_dict["multiplier"]
        new_obj.demand_recirculation = _input_dict.get("demand_recirculation", False)
        for branch_dict in _input_dict["branches"].values():
            new_obj.add_branch(PhHvacPipeBranch.from_dict(branch_dict))

        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}: (display_name={}, identifier={}, demand_recirculation={}, multiplier={}) [{} segments, len={:.1f}, {} branches connected]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier_short,
            self.demand_recirculation,
            self.multiplier,
            len(self.segments),
            float(self.length),
            len(self.branches),
        )

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return self.__repr__()

    def move(self, moving_vec3D):
        # type: (Vector3D) -> PhHvacPipeTrunk
        """Move the pipe's elements along a vector.

        Arguments:
        ----------
            * moving_vec3D (Vector3D): A vector with the direction and distance to move.

        Returns:
        --------
            * PhHvacPipeTrunk: A new PhHvacPipeTrunk with the moved elements.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.move(moving_vec3D) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.move(moving_vec3D)
        return new_trunk

    def rotate(self, axis_3D, angle_degrees, origin_pt3D):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeTrunk
        """Rotate the pipe's elements by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis_3D has a positive orientation, rotation will be clockwise.
        If axis_3D has a negative orientation, rotation will be counterclockwise.

        Arguments:
        ----------
            * axis_3D (Vector3D): A vector representing the axis of rotation.
            * angle_degrees (float): An angle for rotation in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeTrunk: A new PhHvacPipeTrunk with the rotated elements.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.rotate(axis_3D, angle_degrees, origin_pt3D) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.rotate(axis_3D, angle_degrees, origin_pt3D)
        return new_trunk

    def rotate_xy(self, angle_degrees, origin_pt3D):
        # type: (float, Point3D) -> PhHvacPipeTrunk
        """Rotate the pipe's elements counterclockwise in the XY plane by a certain angle.

        Arguments:
        ----------
            * angle_degrees (float): An angle in degrees.
            * origin_pt3D (Point3D): The origin around which the object will be rotated.

        Returns:
        --------
            * PhHvacPipeTrunk: A new PhHvacPipeTrunk with the rotated elements.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.rotate_xy(angle_degrees, origin_pt3D) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.rotate_xy(angle_degrees, origin_pt3D)
        return new_trunk

    def reflect(self, normal_vec3D, origin_pt3D):
        # type (Vector3D, Point3D) -> PhHvacPipeTrunk
        """Reflect the pipe's elements across a plane with the input normal vector and origin.

        Arguments:
        ----------
            * normal_vec3D (Vector3D): The normal vector for the reflection plane. THIS VECTOR MUST BE NORMALIZED.
            * origin_pt3D (Point3D): The origin from which to reflect.

        Returns:
        --------
            * PhHvacPipeTrunk: A new PhHvacPipeTrunk with the reflected elements.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.reflect(normal_vec3D, origin_pt3D) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.reflect(normal_vec3D, origin_pt3D)
        return new_trunk

    def scale(self, factor, origin_pt3D=None):
        # type: (float, Optional[Point3D]) -> PhHvacPipeTrunk
        """Scale the pipe's elements by a factor from an origin point.

        Arguments:
        ----------
            * factor (float): How much the elements should be scaled.
            * origin_pt3D (Optional[Point3D]): The origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).

        Returns:
        --------
            * PhHvacPipeTrunk: A new PhHvacPipeTrunk with the scaled elements.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.scale(factor, origin_pt3D) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.scale(factor, origin_pt3D)
        return new_trunk
