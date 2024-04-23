# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC: Hot Water Piping."""

from copy import copy

try:
    from typing import Any, Dict, List, Union, Optional
except ImportError:
    pass  # IronPython

try:
    from ladybug_geometry.geometry3d.polyline import LineSegment3D
    from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
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


class PhPipeDiameter(enumerables.CustomEnum):
    allowed = [
        "1-3/8in",
        "2-1/2in",
        "3-5/8in",
        "4-3/4in",
        "5-1in",
        "6-1-1/4in",
        "7-1-1/2in",
        "8-2in",
    ]

    def __init__(self, _value=2):
        # type: (Union[str, int]) -> None
        super(PhPipeDiameter, self).__init__(_value)

    def __eq__(self, other):
        # type: (PhPipeDiameter) -> bool
        return self.value == other.value

    def __ne__(self, other):
        # type: (PhPipeDiameter) -> bool
        return self.value != other.value

    def __hash__(self):
        # type: () -> int
        return hash(self.value)


class PhHvacPipeMaterial(enumerables.CustomEnum):
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
    """A single pipe segment (linear) with geometry and a diameter"""

    def __init__(
        self,
        _geom,
        _diameter=2,
        _insul_thickness=0.0127,
        _insul_conductivity=0.04,
        _insul_refl=True,
        _insul_quality=None,
        _daily_period=24,
        _water_temp=60.0,
        _material=2,
        *args,
        **kwargs
    ):
        # type: (LineSegment3D, int, float, float, bool, None, float, float, int, *Any, **Any) -> None
        super(PhHvacPipeSegment, self).__init__()
        self.geometry = _geom
        self.diameter = PhPipeDiameter(_diameter)
        self.insulation_thickness = _insul_thickness
        self.insulation_conductivity = _insul_conductivity
        self.insulation_reflective = _insul_refl
        self.insulation_quality = _insul_quality
        self.daily_period = _daily_period
        self.water_temp = _water_temp
        self.material = PhHvacPipeMaterial(_material)

    @property
    def length(self):
        # type: () -> float
        """Return the length of the pipe segment in model-units."""
        return self.geometry.length

    def __copy__(self):
        # type: () -> PhHvacPipeSegment
        new_obj = PhHvacPipeSegment(self.geometry)

        new_obj.diameter = PhPipeDiameter(self.diameter.value)
        new_obj.material = PhHvacPipeMaterial(self.material.value)
        new_obj.insulation_thickness = self.insulation_thickness
        new_obj.insulation_conductivity = self.insulation_conductivity
        new_obj.insulation_reflective = self.insulation_reflective
        new_obj.insulation_quality = self.insulation_quality
        new_obj.daily_period = self.daily_period
        new_obj.water_temp = self.water_temp
        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = copy(self.user_data)

        return self

    def duplicate(self):
        # type: () -> PhHvacPipeSegment
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, Dict]]
        d = super(PhHvacPipeSegment, self).to_dict()
        d["geometry"] = self.geometry.to_dict()
        d["diameter_value"] = self.diameter.value
        d["material_value"] = self.material.value
        d["insulation_thickness"] = self.insulation_thickness
        d["insulation_conductivity"] = self.insulation_conductivity
        d["insulation_reflective"] = self.insulation_reflective
        d["insulation_quality"] = self.insulation_quality
        d["daily_period"] = self.daily_period
        d["water_temp"] = self.water_temp
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhHvacPipeSegment
        new_obj = cls(_geom=LineSegment3D.from_dict(_input_dict["geometry"]))
        new_obj.diameter = PhPipeDiameter(_input_dict["diameter_value"])
        new_obj.material = PhHvacPipeMaterial(_input_dict["material_value"])
        new_obj.insulation_thickness = _input_dict["insulation_thickness"]
        new_obj.insulation_conductivity = _input_dict["insulation_conductivity"]
        new_obj.insulation_reflective = _input_dict["insulation_reflective"]
        new_obj.insulation_quality = _input_dict["insulation_quality"]
        new_obj.daily_period = _input_dict["daily_period"]
        new_obj.water_temp = _input_dict["water_temp"]
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]

        return new_obj

    def __str__(self):
        return "{}: diam={}, length={:.3f}".format(self.__class__.__name__, self.diameter.value, self.length)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()

    def move(self, moving_vec):
        """Move the pipe's geometry along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        self.geometry = self.geometry.move(moving_vec)

    def rotate(self, axis, angle, origin):
        """Rotate the pipe's geometry by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        self.geometry = self.geometry.rotate(axis, angle, origin)

    def rotate_xy(self, angle, origin):
        """Rotate the pipe's geometry counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        self.geometry = self.geometry.rotate_xy(angle, origin)

    def reflect(self, normal, origin):
        """Reflected the pipe's geometry across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        self.geometry = self.geometry.reflect(normal, origin)

    def scale(self, factor, origin=None):
        # type: (float, Union[None, Point3D]) -> PhHvacPipeSegment
        """Scale the pipe's geometry by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_pipe_segment = self.duplicate()
        new_pipe_segment.geometry = self.geometry.scale(factor, origin)
        new_pipe_segment.insulation_thickness *= factor
        return new_pipe_segment


class PhHvacPipeElement(_base._PhHVACBase):
    """A Pipe Element made up of one or more individual Pipe Segments."""

    def __init__(self):
        super(PhHvacPipeElement, self).__init__()
        self._segments = {}  # type: Dict[str, PhHvacPipeSegment]

    @property
    def segments(self):
        # type: () -> List[PhHvacPipeSegment]
        return list(self._segments.values())

    @property
    def length(self):
        # type: () -> float
        """Return the total length of the pipe element in model-units."""
        return sum(s.length for s in self.segments)

    @property
    def water_temp(self):
        # Return the length-weighted average water temperature of all the pipe segments
        return sum(s.length * s.water_temp for s in self.segments) / self.length

    @property
    def daily_period(self):
        # Return the length-weighted average daily period of all the pipe segments
        return sum(s.length * s.daily_period for s in self.segments) / self.length

    @property
    def segment_names(self):
        # type: () -> List[str]
        """Return a list of the names of all the PipeSegments in the PipeElement."""
        return [s.display_name for s in self.segments]

    @property
    def material_name(self):
        # type: () -> str
        materials = {s.material for s in self.segments}
        if len(materials) == 0:
            return PhHvacPipeMaterial.allowed[0]
        elif len(materials) == 1:
            mat = materials.pop()
            return mat.value
        else:
            raise ValueError("Pipe segments: {} have different materials.".format(self.segment_names))

    @property
    def diameter_name(self):
        # type: () -> str
        diameters = {s.diameter for s in self.segments}
        if len(diameters) == 0:
            return PhPipeDiameter.allowed[0]
        elif len(diameters) == 1:
            diam = diameters.pop()
            return diam.value
        else:
            raise ValueError("Pipe segments: {} have different diameters.".format(self.segment_names))

    def add_segment(self, _segment):
        # type: (PhHvacPipeSegment) -> None
        self._segments[_segment.identifier] = _segment

    def __copy__(self):
        # type: () -> PhHvacPipeElement
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

    def to_dict(self):
        # type: () -> dict[str, Union[str, dict]]
        d = super(PhHvacPipeElement, self).to_dict()
        d["segments"] = {}
        for segment in self.segments:
            d["segments"][segment.identifier] = segment.to_dict()
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

    def move(self, moving_vec):
        # type: (Vector3D) -> PhHvacPipeElement
        """Move the pipe's segments along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        new_segments = {}
        for k, segment in self._segments.items():
            new_segments[k] = segment.move(moving_vec)

        new_pipe_element = self.duplicate()
        new_pipe_element._segments = new_segments
        return new_pipe_element

    def rotate(self, axis, angle, origin):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeElement
        """Rotate the pipe's segments by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_segments = {}
        for k, segment in self._segments.items():
            new_segments[k] = segment.rotate(axis, angle, origin)

        new_pipe_element = self.duplicate()
        new_pipe_element._segments = new_segments
        return new_pipe_element

    def rotate_xy(self, angle, origin):
        # type: (float, Point3D) -> PhHvacPipeElement
        """Rotate the pipe's segments counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_segments = {}
        for k, segment in self._segments.items():
            new_segments[k] = segment.rotate_xy(angle, origin)

        new_pipe_element = self.duplicate()
        new_pipe_element._segments = new_segments
        return new_pipe_element

    def reflect(self, normal, origin):
        # type: (Vector3D, Point3D) -> PhHvacPipeElement
        """Reflected the pipe's segments across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        new_segments = {}
        for k, segment in self._segments.items():
            new_segments[k] = segment.reflect(normal, origin)

        new_pipe_element = self.duplicate()
        new_pipe_element._segments = new_segments
        return new_pipe_element

    def scale(self, factor, origin=None):
        # type: (float, Optional[Point3D]) -> PhHvacPipeElement
        """Scale the pipe's segments by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_segments = {}
        for k, segment in self._segments.items():
            new_segments[k] = segment.scale(factor, origin)

        new_pipe_element = self.duplicate()
        new_pipe_element._segments = new_segments
        return new_pipe_element


class PhHvacPipeBranch(_base._PhHVACBase):
    """A 'Branch' Pipe which has geometry, and serves one or more 'Fixture' (Twig) pipe elements."""

    def __init__(
        self,
    ):
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
    def diameter_name(self):
        # type: () -> str
        """Return the diameter name of the pipe element."""
        return self.pipe_element.diameter_name

    @property
    def twigs(self):
        # type () -> List[PhPipeElement]
        """Alias for the 'fixtures' to better match Phius terminology."""
        return self.fixtures

    @property
    def segments(self):
        # type () -> List[PhPipeSegment]
        return self.pipe_element.segments

    @property
    def length(self):
        # type: () -> float
        """Return the total length of the branch itself in model-units.
        For the total length of the Branch PLUS all fixtures, use 'total_length_m'.
        """
        return float(self.pipe_element.length)

    @property
    def water_temp(self):
        # type: () -> float
        return self.pipe_element.water_temp

    @property
    def daily_period(self):
        # type: () -> float
        return self.pipe_element.daily_period

    @property
    def num_fixtures(self):
        # type: () -> int
        return len(self.fixtures)

    @property
    def total_length(self):
        # type: () -> float
        """Return the total length of the branch PLUS all fixture pipes in model-units."""
        return self.length + sum(f.length for f in self.fixtures)

    @property
    def total_home_run_fixture_length(self):
        # type: () -> float
        """Return the total length of all fixture pipes as measured from end to end.

        NOTE: This method will include the branch's length for EACH of
        the fixture pipes. The result will be a total hot-water transport length
        as if all the pipes were 'home-run' style. This value is used for the
        PHPP calculations and is not a true representation of the piping in the
        model.
        """
        return sum(fixture.length + self.length for fixture in self.fixtures)

    def add_fixture(self, _fixture):
        # type: (PhHvacPipeElement) -> None
        """Add a new HBPH Fixture (twig) PhPipeBranch to the Trunk."""
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

    def to_dict(self):
        # type: () -> Dict[str, Union[str, Dict]]
        d = super(PhHvacPipeBranch, self).to_dict()
        d["pipe_element"] = self.pipe_element.to_dict()
        d["fixtures"] = {}
        for branch in self.fixtures:
            d["fixtures"][branch.identifier] = branch.to_dict()
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

    def move(self, moving_vec):
        # type: (Vector3D) -> PhHvacPipeBranch
        """Move the pipe's elements along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.move(moving_vec) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.move(moving_vec)
        return new_branch

    def rotate(self, axis, angle, origin):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeBranch
        """Rotate the pipe's elements by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.rotate(axis, angle, origin) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.rotate(axis, angle, origin)
        return new_branch

    def rotate_xy(self, angle, origin):
        # type: (float, Point3D) -> PhHvacPipeBranch
        """Rotate the pipe's elements counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.rotate_xy(angle, origin) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.rotate_xy(angle, origin)
        return new_branch

    def reflect(self, normal, origin):
        # type: (Vector3D, Point3D) -> PhHvacPipeBranch
        """Reflected the pipe's elements across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.reflect(normal, origin) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.reflect(normal, origin)
        return new_branch

    def scale(self, factor, origin=None):
        # type: (float, Optional[Point3D]) -> PhHvacPipeBranch
        """Scale the pipe's elements by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_branch = self.duplicate()
        new_branch.fixtures = [fixture.scale(factor, origin) for fixture in self.fixtures]
        new_branch.pipe_element = self.pipe_element.scale(factor, origin)
        return new_branch


class PhHvacPipeTrunk(_base._PhHVACBase):
    """A 'Trunk' Pipe which has geometry, and serves one or more 'Branches'."""

    def __init__(self):
        # type: () -> None
        super(PhHvacPipeTrunk, self).__init__()
        self.pipe_element = PhHvacPipeElement()
        self.multiplier = 1  # type: int
        self.branches = []  # type: (List[PhHvacPipeBranch])

    @property
    def material_name(self):
        # type: () -> str
        return self.pipe_element.material_name

    @property
    def diameter_name(self):
        # type: () -> str
        return self.pipe_element.diameter_name

    @property
    def segments(self):
        # type () -> List[PhPipeSegment]
        return self.pipe_element.segments

    @property
    def length(self):
        # type: () -> float
        """Return the total length of the trunk itself in model-units."""
        return self.pipe_element.length

    @property
    def water_temp(self):
        # type: () -> float
        return self.pipe_element.water_temp

    @property
    def daily_period(self):
        # type: () -> float
        return self.pipe_element.daily_period

    @property
    def num_fixtures(self):
        # type: () -> int
        return sum(branch.num_fixtures for branch in self.branches)

    @property
    def total_length(self):
        # type: () -> float
        """Return the total length of the trunk PLUS all branches and fixture pipes in model-units."""
        return self.length + sum(branch.total_length for branch in self.branches)

    @property
    def total_home_run_fixture_length(self):
        # type: () -> float
        """Return the total length of all fixture pipes as measured from end to end.

        NOTE: This method will include the trunk's and branch's length for EACH of
        the fixture pipes. The result will be a total hot-water transport length
        as if all the pipes were 'home-run' style. This value is used for the
        PHPP calculations and is not a true representation of the piping in the
        model.
        """
        return sum(self.length + branch.total_home_run_fixture_length for branch in self.branches)

    def add_branch(self, _branch):
        # type: (PhHvacPipeBranch) -> None
        """Add a new HBPH PhPipeBranch to the Trunk."""
        self.branches.append(_branch)

    def __copy__(self):
        # type: () -> PhHvacPipeTrunk
        new_obj = PhHvacPipeTrunk()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data
        new_obj.pipe_element = self.pipe_element.duplicate()
        new_obj.multiplier = self.multiplier
        for branch in self.branches:
            new_obj.add_branch(branch.duplicate())

        return new_obj

    def duplicate(self):
        # type: () -> PhHvacPipeTrunk
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, Dict]]
        d = super(PhHvacPipeTrunk, self).to_dict()
        d["pipe_element"] = self.pipe_element.to_dict()
        d["multiplier"] = self.multiplier
        d["branches"] = {}
        for branch in self.branches:
            d["branches"][branch.identifier] = branch.to_dict()
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
        for branch_dict in _input_dict["branches"].values():
            new_obj.add_branch(PhHvacPipeBranch.from_dict(branch_dict))

        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}: (display_name={}, identifier={} multiplier={}) [{} segments, len={:.1f}, {} branches connected]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier_short,
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

    def move(self, moving_vec):
        # type: (Vector3D) -> PhHvacPipeTrunk
        """Move the pipe's elements along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.move(moving_vec) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.move(moving_vec)
        return new_trunk

    def rotate(self, axis, angle, origin):
        # type: (Vector3D, float, Point3D) -> PhHvacPipeTrunk
        """Rotate the pipe's elements by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.rotate(axis, angle, origin) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.rotate(axis, angle, origin)
        return new_trunk

    def rotate_xy(self, angle, origin):
        # type: (float, Point3D) -> PhHvacPipeTrunk
        """Rotate the pipe's elements counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.rotate_xy(angle, origin) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.rotate_xy(angle, origin)
        return new_trunk

    def reflect(self, normal, origin):
        # type (Vector3D, Point3D) -> PhHvacPipeTrunk
        """Reflected the pipe's elements across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.reflect(normal, origin) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.reflect(normal, origin)
        return new_trunk

    def scale(self, factor, origin=None):
        # type: (float, Optional[Point3D]) -> PhHvacPipeTrunk
        """Scale the pipe's elements by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        new_trunk = self.duplicate()
        new_trunk.branches = [branch.scale(factor, origin) for branch in self.branches]
        new_trunk.pipe_element = self.pipe_element.scale(factor, origin)
        return new_trunk
