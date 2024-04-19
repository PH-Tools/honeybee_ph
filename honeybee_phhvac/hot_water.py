# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC-Equipment: Service Hot Water Devices."""

from copy import copy

try:
    from typing import Any, Dict, List, Union
except ImportError:
    pass  # IronPython

try:
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


class UnknownPhHeaterTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        self.msg = 'Error: Unknown SHW Heater Type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types
        )
        super(UnknownPhHeaterTypeError, self).__init__(self.msg)


# -- Piping ---------------------------------------------------------------------


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


class PhPipeMaterial(enumerables.CustomEnum):
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
        super(PhPipeMaterial, self).__init__(_value)

    def __eq__(self, other):
        # type: (PhPipeMaterial) -> bool
        return self.value == other.value

    def __ne__(self, other):
        # type: (PhPipeMaterial) -> bool
        return self.value != other.value

    def __hash__(self):
        # type: () -> int
        return hash(self.value)


class PhPipeSegment(_base._PhHVACBase):
    """A single pipe segment (linear) with geometry and a diameter"""

    def __init__(
        self,
        _geom,
        _diameter=2,
        _insul_thickness_m=0.0127,
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
        super(PhPipeSegment, self).__init__()
        self.geometry = _geom
        self.diameter = PhPipeDiameter(_diameter)
        self.insulation_thickness_m = _insul_thickness_m
        self.insulation_conductivity = _insul_conductivity
        self.insulation_reflective = _insul_refl
        self.insulation_quality = _insul_quality
        self.daily_period = _daily_period
        self.water_temp = _water_temp
        self.material = PhPipeMaterial(_material)

    @property
    def length_m(self):
        # type: () -> float
        return self.geometry.length

    def __copy__(self):
        # type: () -> PhPipeSegment
        new_obj = PhPipeSegment(self.geometry)

        new_obj.diameter = PhPipeDiameter(self.diameter.value)
        new_obj.material = PhPipeMaterial(self.material.value)
        new_obj.insulation_thickness_m = self.insulation_thickness_m
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
        # type: () -> PhPipeSegment
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, Dict]]
        d = super(PhPipeSegment, self).to_dict()
        d["geometry"] = self.geometry.to_dict()
        d["diameter_value"] = self.diameter.value
        d["material_value"] = self.material.value
        d["insulation_thickness_m"] = self.insulation_thickness_m
        d["insulation_conductivity"] = self.insulation_conductivity
        d["insulation_reflective"] = self.insulation_reflective
        d["insulation_quality"] = self.insulation_quality
        d["daily_period"] = self.daily_period
        d["water_temp"] = self.water_temp
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhPipeSegment
        new_obj = cls(_geom=LineSegment3D.from_dict(_input_dict["geometry"]))
        new_obj.diameter = PhPipeDiameter(_input_dict["diameter_value"])
        new_obj.material = PhPipeMaterial(_input_dict["material_value"])
        new_obj.insulation_thickness_m = _input_dict["insulation_thickness_m"]
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
        return "{}: diam={}, length={:.3f}".format(self.__class__.__name__, self.diameter.value, self.length_m)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()


class PhPipeElement(_base._PhHVACBase):
    """A Pipe Element made up of one or more individual Pipe Segments."""

    def __init__(self):
        super(PhPipeElement, self).__init__()
        self._segments = {}  # type: Dict[str, PhPipeSegment]

    @property
    def segments(self):
        # type: () -> List[PhPipeSegment]
        return list(self._segments.values())

    @property
    def length_m(self):
        # type: () -> float
        return sum(s.length_m for s in self.segments)

    @property
    def water_temp(self):
        # Return the length-weighted average water temperature of all the pipe segments
        return sum(s.length_m * s.water_temp for s in self.segments) / self.length_m

    @property
    def daily_period(self):
        # Return the length-weighted average daily period of all the pipe segments
        return sum(s.length_m * s.daily_period for s in self.segments) / self.length_m

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
            return PhPipeMaterial.allowed[0]
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
        # type: (PhPipeSegment) -> None
        self._segments[_segment.identifier] = _segment

    def __copy__(self):
        # type: () -> PhPipeElement
        new_obj = PhPipeElement()

        for segment in self.segments:
            new_obj.add_segment(segment.duplicate())

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data

        return new_obj

    def duplicate(self):
        # type: () -> PhPipeElement
        return self.__copy__()

    def to_dict(self):
        # type: () -> dict[str, Union[str, dict]]
        d = super(PhPipeElement, self).to_dict()
        d["segments"] = {}
        for segment in self.segments:
            d["segments"][segment.identifier] = segment.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhPipeElement
        new_obj = cls()

        for seg_dict in _input_dict["segments"].values():
            new_obj._segments[seg_dict["identifier"]] = PhPipeSegment.from_dict(seg_dict)
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
            self.length_m,
        )

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()


class PhPipeBranch(_base._PhHVACBase):
    """A 'Branch' Pipe which has geometry, and serves one or more 'Fixture' (Twig) pipe elements."""

    def __init__(
        self,
    ):
        # type: () -> None
        super(PhPipeBranch, self).__init__()
        self.pipe_element = PhPipeElement()
        self.fixtures = []  # type: (List[PhPipeElement])

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
    def length_m(self):
        # type: () -> float
        """Return the total length of the branch itself.
        For the total length of the Branch PLUS all fixtures, use 'total_length_m'.
        """
        return float(self.pipe_element.length_m)

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
    def total_length_m(self):
        # type: () -> float
        """Return the total length of the branch PLUS all fixture pipes."""
        return self.length_m + sum(f.length_m for f in self.fixtures)

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
        return sum(fixture.length_m + self.length_m for fixture in self.fixtures)

    def add_fixture(self, _fixture):
        # type: (PhPipeElement) -> None
        """Add a new HBPH PhPipeBranch to the Trunk."""
        self.fixtures.append(_fixture)

    def __copy__(self):
        # type: () -> PhPipeBranch
        new_obj = PhPipeBranch()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data
        new_obj.pipe_element = self.pipe_element.duplicate()
        for fixture in self.fixtures:
            new_obj.add_fixture(fixture.duplicate())

        return new_obj

    def duplicate(self):
        # type: () -> PhPipeBranch
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, Dict]]
        d = super(PhPipeBranch, self).to_dict()
        d["pipe_element"] = self.pipe_element.to_dict()
        d["fixtures"] = {}
        for branch in self.fixtures:
            d["fixtures"][branch.identifier] = branch.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhPipeBranch
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]
        new_obj.pipe_element = PhPipeElement.from_dict(_input_dict["pipe_element"])
        for fixture_dict in _input_dict["fixtures"].values():
            new_obj.add_fixture(PhPipeElement.from_dict(fixture_dict))

        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}: (display_name={}, identifier={} ) [{} segments, len={:.1f}, {} fixtures connected]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier_short,
            len(self.segments),
            float(self.length_m),
            len(self.fixtures),
        )

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return self.__repr__()


class PhPipeTrunk(_base._PhHVACBase):
    """A 'Trunk' Pipe which has geometry, and serves one or more 'Branches'."""

    def __init__(self):
        # type: () -> None
        super(PhPipeTrunk, self).__init__()
        self.pipe_element = PhPipeElement()
        self.multiplier = 1  # type: int
        self.branches = []  # type: (List[PhPipeBranch])

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
    def length_m(self):
        # type: () -> float
        return self.pipe_element.length_m

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
    def total_length_m(self):
        # type: () -> float
        """Return the total length of the trunk PLUS all branches and fixture pipes."""
        return self.length_m + sum(branch.total_length_m for branch in self.branches)

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
        return sum(self.length_m + branch.total_home_run_fixture_length for branch in self.branches)

    def add_branch(self, _branch):
        # type: (PhPipeBranch) -> None
        """Add a new HBPH PhPipeBranch to the Trunk."""
        self.branches.append(_branch)

    def __copy__(self):
        # type: () -> PhPipeTrunk
        new_obj = PhPipeTrunk()

        new_obj.identifier = self.identifier
        new_obj.display_name = self.display_name
        new_obj.user_data = self.user_data
        new_obj.pipe_element = self.pipe_element.duplicate()
        new_obj.multiplier = self.multiplier
        for branch in self.branches:
            new_obj.add_branch(branch.duplicate())

        return new_obj

    def duplicate(self):
        # type: () -> PhPipeTrunk
        return self.__copy__()

    def to_dict(self):
        # type: () -> Dict[str, Union[str, Dict]]
        d = super(PhPipeTrunk, self).to_dict()
        d["pipe_element"] = self.pipe_element.to_dict()
        d["multiplier"] = self.multiplier
        d["branches"] = {}
        for branch in self.branches:
            d["branches"][branch.identifier] = branch.to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict) -> PhPipeTrunk
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict["user_data"]
        new_obj.pipe_element = PhPipeElement.from_dict(_input_dict["pipe_element"])
        new_obj.multiplier = _input_dict["multiplier"]
        for branch_dict in _input_dict["branches"].values():
            new_obj.add_branch(PhPipeBranch.from_dict(branch_dict))

        return new_obj

    def __str__(self):
        # type: () -> str
        return "{}: (display_name={}, identifier={} multiplier={}) [{} segments, len={:.1f}, {} branches connected]".format(
            self.__class__.__name__,
            self.display_name,
            self.identifier_short,
            self.multiplier,
            len(self.segments),
            float(self.length_m),
            len(self.branches),
        )

    def __repr__(self):
        # type: () -> str
        return str(self)

    def ToString(self):
        # type: () -> str
        return self.__repr__()


# -- Tank ---------------------------------------------------------------------


class PhSHWTankType(enumerables.CustomEnum):
    allowed = ["0-No storage tank", "1-DHW and heating", "2-DHW only"]

    def __init__(self, _value=1, _index_offset=0):
        # type: (Union[str, int], int) -> None
        super(PhSHWTankType, self).__init__(_value, _index_offset)


class PhSHWTank(_base._PhHVACBase):
    def __init__(self):
        super(PhSHWTank, self).__init__()
        self.display_name = "_unnamed_hw_tank_"  # type: str
        self.quantity = 1  # type: int
        self._tank_type = PhSHWTankType("2-DHW only")  # type: enumerables.CustomEnum
        self.in_conditioned_space = True  # type: bool
        self.solar_connection = False  # type: bool
        self.solar_losses = 0.0  # type: float
        self.storage_loss_rate = 0.0  # type: float
        self.storage_capacity = 300  # type: float
        self.standby_losses = 4.0  # type: float
        self.standby_fraction = 0.30  # type: float
        self.room_temp = 20.0  # type: float
        self.water_temp = 60.0  # type: float

    @property
    def tank_type(self):
        # type () -> str
        return self._tank_type.value

    @tank_type.setter
    def tank_type(self, _in):
        # type: (Union[str, int]) -> None
        self._tank_type = PhSHWTankType(_in)

    def __copy__(self):
        # type: () -> PhSHWTank
        new_obj = PhSHWTank()

        new_obj.display_name = self.display_name
        new_obj.identifier = self.identifier
        new_obj.user_data = copy(self.user_data)
        new_obj.quantity = self.quantity
        new_obj._tank_type = self._tank_type
        new_obj.in_conditioned_space = self.in_conditioned_space
        new_obj.solar_connection = self.solar_connection
        new_obj.solar_losses = self.solar_losses
        new_obj.storage_loss_rate = self.storage_loss_rate
        new_obj.storage_capacity = self.storage_capacity
        new_obj.standby_losses = self.standby_losses
        new_obj.standby_fraction = self.standby_fraction
        new_obj.room_temp = self.room_temp
        new_obj.water_temp = self.water_temp

        return new_obj

    def duplicate(self):
        # type: () -> PhSHWTank
        return self.__copy__()

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = super(PhSHWTank, self).to_dict()
        d["quantity"] = self.quantity
        d["_tank_type"] = self._tank_type.to_dict()
        d["in_conditioned_space"] = self.in_conditioned_space
        d["solar_connection"] = self.solar_connection
        d["solar_losses"] = self.solar_losses
        d["storage_loss_rate"] = self.storage_loss_rate
        d["storage_capacity"] = self.storage_capacity
        d["standby_losses"] = self.standby_losses
        d["standby_fraction"] = self.standby_fraction
        d["room_temp"] = self.room_temp
        d["water_temp"] = self.water_temp

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhSHWTank
        obj = cls()

        obj.display_name = _input_dict["display_name"]
        obj.identifier = _input_dict["identifier"]
        obj.user_data = _input_dict["user_data"]
        obj.quantity = _input_dict["quantity"]
        obj._tank_type = PhSHWTankType.from_dict(_input_dict["_tank_type"])
        obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        obj.solar_connection = _input_dict["solar_connection"]
        obj.solar_losses = _input_dict["solar_losses"]
        obj.storage_loss_rate = _input_dict["storage_loss_rate"]
        obj.storage_capacity = _input_dict["storage_capacity"]
        obj.standby_losses = _input_dict["standby_losses"]
        obj.standby_fraction = _input_dict["standby_fraction"]
        obj.room_temp = _input_dict["room_temp"]
        obj.water_temp = _input_dict["water_temp"]

        return obj

    def __str__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.tank_type, self.display_name)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.display_name)

    def ToString(self):
        return self.__repr__()


# -- Heaters ------------------------------------------------------------------


class PhHotWaterHeater(_base._PhHVACBase):
    """Base class for all PH Hot-Water Heaters."""

    def __init__(self):
        super(PhHotWaterHeater, self).__init__()
        self.percent_coverage = 1.0
        self.in_conditioned_space = True

    def to_dict(self):
        # type: () -> dict
        d = super(PhHotWaterHeater, self).to_dict()
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhHotWaterHeater
        new_obj = cls()
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict.get("user_data", {})
        return new_obj

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhSHWHeaterElectric(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterElectric, self).__init__()

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhSHWHeaterElectric, self).to_dict()
        d["heater_type"] = self.__class__.__name__
        d["percent_coverage"] = self.percent_coverage
        d["in_conditioned_space"] = self.in_conditioned_space
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhSHWHeaterElectric
        new_obj = cls()
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.percent_coverage = _input_dict["percent_coverage"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        return new_obj


class PhSHWHeaterBoiler(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterBoiler, self).__init__()
        self.fuel = 1  # Gas
        self.condensing = True
        self.effic_at_30_perc_load = 0.98
        self.effic_at_nominal_load = 0.94
        self.avg_return_temp_at_30_perc_load = 30
        self.avg_boiler_temp_at_70_55 = 41
        self.avg_boiler_temp_at_55_45 = 35
        self.avg_boiler_temp_at_35_28 = 24

    def to_dict(self):
        # type: () -> dict
        d = super(PhSHWHeaterBoiler, self).to_dict()
        d["heater_type"] = self.__class__.__name__
        d["percent_coverage"] = self.percent_coverage
        d["in_conditioned_space"] = self.in_conditioned_space
        d["fuel"] = self.fuel
        d["condensing"] = self.condensing
        d["effic_at_30_perc_load"] = self.effic_at_30_perc_load
        d["effic_at_nominal_load"] = self.effic_at_nominal_load
        d["avg_return_temp_at_30_perc_load"] = self.avg_return_temp_at_30_perc_load
        d["avg_boiler_temp_at_70_55"] = self.avg_boiler_temp_at_70_55
        d["avg_boiler_temp_at_55_45"] = self.avg_boiler_temp_at_55_45
        d["avg_boiler_temp_at_35_28"] = self.avg_boiler_temp_at_35_28
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhSHWHeaterBoiler
        new_obj = cls()
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.percent_coverage = _input_dict["percent_coverage"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        new_obj.fuel = _input_dict["fuel"]
        new_obj.condensing = _input_dict["condensing"]
        new_obj.effic_at_30_perc_load = _input_dict["effic_at_30_perc_load"]
        new_obj.effic_at_nominal_load = _input_dict["effic_at_nominal_load"]
        new_obj.avg_return_temp_at_30_perc_load = _input_dict["avg_return_temp_at_30_perc_load"]
        new_obj.avg_boiler_temp_at_70_55 = _input_dict["avg_boiler_temp_at_70_55"]
        new_obj.avg_boiler_temp_at_55_45 = _input_dict["avg_boiler_temp_at_55_45"]
        new_obj.avg_boiler_temp_at_35_28 = _input_dict["avg_boiler_temp_at_35_28"]
        return new_obj


class PhSHWHeaterBoilerWood(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterBoilerWood, self).__init__()
        self.fuel = 1  # Pellet
        self.effic_in_basic_cycle = 0.72
        self.effic_in_const_operation = 0.80
        self.avg_frac_heat_released = 0.5
        self.on_off_temp_diff = 30

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhSHWHeaterBoilerWood, self).to_dict()
        d["heater_type"] = self.__class__.__name__
        d["percent_coverage"] = self.percent_coverage
        d["in_conditioned_space"] = self.in_conditioned_space
        d["fuel"] = self.fuel
        d["effic_in_basic_cycle"] = self.effic_in_basic_cycle
        d["effic_in_const_operation"] = self.effic_in_const_operation
        d["avg_frac_heat_released"] = self.avg_frac_heat_released
        d["on_off_temp_diff"] = self.on_off_temp_diff
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhSHWHeaterBoilerWood
        new_obj = cls()
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.percent_coverage = _input_dict["percent_coverage"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        new_obj.fuel = _input_dict["fuel"]
        new_obj.effic_in_basic_cycle = _input_dict["effic_in_basic_cycle"]
        new_obj.effic_in_const_operation = _input_dict["effic_in_const_operation"]
        new_obj.avg_frac_heat_released = _input_dict["avg_frac_heat_released"]
        new_obj.on_off_temp_diff = _input_dict["on_off_temp_diff"]
        return new_obj


class PhSHWHeaterDistrict(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterDistrict, self).__init__()
        self.energy_carrier = 1
        self.solar_fraction = 0
        self.util_fact_heat_transfer = 1

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhSHWHeaterDistrict, self).to_dict()
        d["heater_type"] = self.__class__.__name__
        d["percent_coverage"] = self.percent_coverage
        d["in_conditioned_space"] = self.in_conditioned_space
        d["energy_carrier"] = self.energy_carrier
        d["solar_fraction"] = self.solar_fraction
        d["util_fact_heat_transfer"] = self.util_fact_heat_transfer
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.percent_coverage = _input_dict["percent_coverage"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]

        new_obj.energy_carrier = _input_dict["energy_carrier"]
        new_obj.solar_fraction = _input_dict["solar_fraction"]
        new_obj.util_fact_heat_transfer = _input_dict["util_fact_heat_transfer"]

        return new_obj


class PhSHWHeaterHeatPump(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterHeatPump, self).__init__()
        self.annual_COP = None
        self.annual_system_perf_ratio = None
        self.annual_energy_factor = None

    def to_dict(self):
        # type: () -> Dict[str, Any]
        d = super(PhSHWHeaterHeatPump, self).to_dict()
        d["heater_type"] = self.__class__.__name__
        d["percent_coverage"] = self.percent_coverage
        d["in_conditioned_space"] = self.in_conditioned_space
        d["annual_COP"] = self.annual_COP
        d["annual_system_perf_ratio"] = self.annual_system_perf_ratio
        d["annual_energy_factor"] = self.annual_energy_factor
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (Dict[str, Any]) -> PhSHWHeaterHeatPump
        new_obj = cls()
        new_obj.identifier = _input_dict["identifier"]
        new_obj.display_name = _input_dict["display_name"]
        new_obj.user_data = _input_dict.get("user_data", {})
        new_obj.percent_coverage = _input_dict["percent_coverage"]
        new_obj.in_conditioned_space = _input_dict["in_conditioned_space"]
        new_obj.annual_COP = _input_dict["annual_COP"]
        new_obj.annual_system_perf_ratio = _input_dict["annual_system_perf_ratio"]
        new_obj.annual_energy_factor = _input_dict["annual_energy_factor"]
        return new_obj


# -- Heater Builder -----------------------------------------------------------


class PhSHWHeaterBuilder(object):
    """Constructor class for Hot-Water-Heater objects"""

    heaters = {
        "PhSHWHeaterElectric": PhSHWHeaterElectric,
        "PhSHWHeaterBoiler": PhSHWHeaterBoiler,
        "PhSHWHeaterBoilerWood": PhSHWHeaterBoilerWood,
        "PhSHWHeaterDistrict": PhSHWHeaterDistrict,
        "PhSHWHeaterHeatPump": PhSHWHeaterHeatPump,
    }

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHotWaterHeater

        heater_type = _input_dict.get("heater_type")
        if heater_type is None:
            raise UnknownPhHeaterTypeError(cls.heaters.keys(), heater_type)

        heater_class = cls.heaters[heater_type]
        new_heater = heater_class.from_dict(_input_dict)

        return new_heater

    def __str__(self):
        return "{}()".format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
