# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Honeybee-PH-HVAC: Hot Water System."""

try:
    from typing import Any, Dict, Optional, Union, ValuesView
except:
    pass  # IronPython

from uuid import uuid4

from honeybee_phhvac import hot_water_devices as hwd
from honeybee_phhvac import hot_water_piping as hwp


class PhHotWaterSystem_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(_expected_types, _input_type)
        super(PhHotWaterSystem_FromDictError, self).__init__(self.msg)


class PhHotWaterSystem(object):
    """PH-HVAC: Hot Water System."""

    def __init__(self):
        self.identifier = str(uuid4())
        self.id_num = 0
        self.display_name = "_unnamed_hot_water_system_"

        self.tank_1 = None  # type: Optional[hwd.PhHvacHotWaterTank]
        self.tank_2 = None  # type: Optional[hwd.PhHvacHotWaterTank]
        self.tank_buffer = None  # type: Optional[hwd.PhHvacHotWaterTank]
        self.tank_solar = None  # type: Optional[hwd.PhHvacHotWaterTank]

        self._heaters = {}  # type: Dict[str, hwd.PhHvacHotWaterHeater]
        self._distribution_piping = {}  # type: Dict[str, hwp.PhHvacPipeTrunk]
        self._recirc_piping = {}  # type: Dict[str, hwp.PhHvacPipeElement]

        self._number_tap_points = None  # type: Optional[int]

    @property
    def total_distribution_pipe_length(self):
        # type: () -> float
        """Returns the total length of all trunk, branch, and fixture piping."""
        return sum(_.total_length_m for _ in self._distribution_piping.values())

    @property
    def total_home_run_fixture_pipe_length(self):
        # type: () -> float
        """Returns the total length of all fixture piping from end to end.

        NOTE: This method will count the branch and trunk lengths for EACH of
        the fixture pipes. The result will be a total hot-water transport length
        as if all the pipes were 'home-run' style. This value is used for the
        PHPP calculations and is not a true representation of the piping in the
        model.
        """
        return sum(_.total_home_run_fixture_length for _ in self._distribution_piping.values())

    @property
    def total_recirc_pipe_length(self):
        # type: () -> float
        """Returns the total length of all recirculation piping."""
        return sum(_.length_m for _ in self._recirc_piping.values())

    @property
    def recirc_temp(self):
        # type: () -> float
        """Return the length weighted average of recirculation piping temperatures"""
        if not self._recirc_piping or self.total_recirc_pipe_length == 0:
            return 60.0
        return sum([v.water_temp * v.length_m for v in self._recirc_piping.values()]) / self.total_recirc_pipe_length

    @property
    def recirc_hours(self):
        # type: () -> int
        """Return the length-weighted average of recirculation piping hours."""
        if not self._recirc_piping or self.total_recirc_pipe_length == 0:
            return 24
        return int(
            sum([v.daily_period * v.length_m for v in self._recirc_piping.values()]) / self.total_recirc_pipe_length
        )

    @property
    def number_tap_points(self):
        # type: () -> int
        """Unless set explicitly by the user, will return the number of Branch Pipe Elements."""
        if self._number_tap_points:
            return self._number_tap_points
        else:
            return sum(br.num_fixtures for br in self._distribution_piping.values())

    @number_tap_points.setter
    def number_tap_points(self, _input):
        # type: (Optional[int]) -> None
        if _input:
            self._number_tap_points = int(_input)

    @property
    def heaters(self):
        # type: () -> ValuesView[hwd.PhHvacHotWaterHeater]
        """Returns a list of all the heaters on the system."""
        return self._heaters.values()

    def clear_heaters(self):
        self._heaters = {}

    def add_heater(self, _h):
        # type: (Optional[hwd.PhHvacHotWaterHeater]) -> None
        """Adds a new hot-water heater to the system."""
        if not _h:
            return

        assert hasattr(_h, "to_dict"), 'Error: HW-Heater "{}" is not serializable?'.format(_h)
        self._heaters[_h.identifier] = _h

    def add_distribution_piping(self, _distribution_piping, _key=None):
        # type: (Union[hwp.PhHvacPipeTrunk, hwp.PhHvacPipeBranch, hwp.PhHvacPipeElement], Optional[str]) -> None
        """Add a new distribution (branch, trunk, fixture) to the system.

        If a branch or fixture pipe is passed, a 0-length trunk will be created and the
        branch or fixture will be added to it before adding to the system.
        """

        if isinstance(_distribution_piping, hwp.PhHvacPipeTrunk):
            # -- Add the trunk to the collection
            new_trunk = _distribution_piping
        elif isinstance(_distribution_piping, hwp.PhHvacPipeBranch):
            # -- Build a new Trunk and add the branch to it
            new_trunk = hwp.PhHvacPipeTrunk()
            new_trunk.add_branch(_distribution_piping)
        elif isinstance(_distribution_piping, hwp.PhHvacPipeElement):
            # -- Build a new Trunk and Branch, add the fixture to it
            new_branch = hwp.PhHvacPipeBranch()
            new_branch.add_fixture(_distribution_piping)
            new_trunk = hwp.PhHvacPipeTrunk()
            new_trunk.add_branch(new_branch)
        else:
            raise ValueError(
                'Error: Expected type of "PhPipeTrunk", "PhPipeBranch", or "PhPipeElement". Got: {}'.format(
                    type(_distribution_piping)
                )
            )

        self._distribution_piping[_key or new_trunk.identifier] = new_trunk

    def clear_distribution_piping(self):
        """Clear all distribution piping (Trunks) from the system."""
        self._distribution_piping = {}

    @property
    def distribution_piping(self):
        # type: () -> ValuesView[hwp.PhHvacPipeTrunk]
        """Returns a list of all the distribution-piping (Trunks) in the system."""
        return self._distribution_piping.values()

    def add_recirc_piping(self, _recirc_piping, _key=None):
        # type: (hwp.PhHvacPipeElement, Optional[str]) -> None
        self._recirc_piping[_key or _recirc_piping.identifier] = _recirc_piping

    def clear_recirc_piping(self):
        self._recirc_piping = {}

    @property
    def recirc_piping(self):
        # type: () -> ValuesView[hwp.PhHvacPipeElement]
        """Returns a list of all the recirculation-piping objects in the system."""
        return self._recirc_piping.values()

    @property
    def tanks(self):
        # type: () -> list[hwd.PhHvacHotWaterTank | None]
        """Return a list of the system tanks in order (1, 2, buffer, solar)."""
        return [self.tank_1, self.tank_2, self.tank_buffer, self.tank_solar]

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged:
            d["type"] = "PhHvacHotWaterSystemAbridged"
        else:
            d["type"] = "PhHvacHotWaterSystemPh"

        d["id_num"] = self.id_num
        d["identifier"] = self.identifier
        d["display_name"] = self.display_name
        if self.tank_1:
            d["tank_1"] = self.tank_1.to_dict()
        if self.tank_2:
            d["tank_2"] = self.tank_2.to_dict()
        if self.tank_buffer:
            d["tank_buffer"] = self.tank_buffer.to_dict()
        if self.tank_solar:
            d["tank_solar"] = self.tank_solar.to_dict()

        d["heaters"] = {}
        for heater in self.heaters:
            d["heaters"][heater.identifier] = heater.to_dict()

        d["distribution_piping"] = {}
        for distribution_piping in self.distribution_piping:
            d["distribution_piping"][distribution_piping.identifier] = distribution_piping.to_dict()

        d["recirc_piping"] = {}
        for recirc_piping in self.recirc_piping:
            d["recirc_piping"][recirc_piping.identifier] = recirc_piping.to_dict()

        d["number_tap_points"] = self._number_tap_points
        d["recirc_temp"] = self.recirc_temp
        d["recirc_hours"] = self.recirc_hours

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHotWaterSystem
        valid_types = ("PhHvacHotWaterSystemPh", "PhHvacHotWaterSystemAbridged")
        if _input_dict["type"] not in valid_types:
            raise PhHotWaterSystem_FromDictError(valid_types, _input_dict["type"])

        new_system = cls()
        new_system.identifier = _input_dict.get("identifier", str(uuid4()))
        new_system.id_num = _input_dict["id_num"]
        new_system.display_name = _input_dict["display_name"]

        if _input_dict.get("tank_1", None):
            new_system.tank_1 = hwd.PhHvacHotWaterTank.from_dict(_input_dict["tank_1"])
        if _input_dict.get("tank_2", None):
            new_system.tank_2 = hwd.PhHvacHotWaterTank.from_dict(_input_dict["tank_2"])
        if _input_dict.get("tank_buffer", None):
            new_system.tank_buffer = hwd.PhHvacHotWaterTank.from_dict(_input_dict["tank_buffer"])
        if _input_dict.get("tank_solar", None):
            new_system.tank_solar = hwd.PhHvacHotWaterTank.from_dict(_input_dict["tank_solar"])

        for heater_dict in _input_dict["heaters"].values():
            new_system.add_heater(hwd.PhHvacHotWaterHeaterBuilder.from_dict(heater_dict))

        for distribution_piping_dict in _input_dict["distribution_piping"].values():
            new_system.add_distribution_piping(hwp.PhHvacPipeTrunk.from_dict(distribution_piping_dict))

        for recirc_piping_dict in _input_dict["recirc_piping"].values():
            new_system.add_recirc_piping(hwp.PhHvacPipeElement.from_dict(recirc_piping_dict))

        new_system._number_tap_points = _input_dict["number_tap_points"]

        return new_system

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self):
        # type: () -> PhHotWaterSystem
        new_obj = PhHotWaterSystem()
        new_obj.id_num = self.id_num
        new_obj.display_name = self.display_name

        if self.tank_1:
            new_obj.tank_1 = self.tank_1.duplicate()
        if self.tank_2:
            new_obj.tank_2 = self.tank_2.duplicate()
        if self.tank_buffer:
            new_obj.tank_buffer = self.tank_buffer.duplicate()
        if self.tank_solar:
            new_obj.tank_solar = self.tank_solar.duplicate()

        for k, v in self._heaters.items():
            new_obj.add_heater(v)

        for k, v in self._distribution_piping.items():
            new_obj.add_distribution_piping(v.duplicate(), _key=k)

        for k, v in self._recirc_piping.items():
            new_obj.add_recirc_piping(v.duplicate(), _key=k)

        new_obj._number_tap_points = self._number_tap_points

        return new_obj

    def duplicate(self):
        # type: (Any) -> PhHotWaterSystem
        return self.__copy__()

    def __str__(self):
        return "{}: id={}".format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        """Properties representation."""
        return "{!r}(id_num={!r}, tank_1={!r}, tank_2={!r}, tank_buffer={!r}, tank_solar={!r})".format(
            self.__class__.__name__,
            self.id_num,
            self.tank_1,
            self.tank_2,
            self.tank_buffer,
            self.tank_solar,
        )

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __add__(self, other):
        # type: (PhHotWaterSystem) -> PhHotWaterSystem
        new_obj = self.duplicate()

        for heater in self.heaters:
            new_obj.add_heater(heater)
        for heater in other.heaters:
            new_obj.add_heater(heater)

        for distribution_pipe in self.distribution_piping:
            new_obj.add_distribution_piping(distribution_pipe)
        for distribution_pipe in other.distribution_piping:
            new_obj.add_distribution_piping(distribution_pipe)

        for recirc_pipe in self.recirc_piping:
            new_obj.add_recirc_piping(recirc_pipe)
        for recirc_pipe in other.recirc_piping:
            new_obj.add_recirc_piping(recirc_pipe)

        if self._number_tap_points or other._number_tap_points:
            # -- If either have their tap-points number set explicitly by the use
            # -- set the new object # as well
            new_obj.number_tap_points = self.number_tap_points + other.number_tap_points
        else:
            # -- If neither obj's have their tap-point number set explicitly by the user
            # -- Set as None, which will return the length of the Branch Piping dict by default.
            self._number_tap_points = None

        return new_obj

    def __radd__(self, other):
        # type: (PhHotWaterSystem) -> PhHotWaterSystem
        if isinstance(other, int):
            return self
        else:
            return self + other

    def __eq__(self, other):
        # type: (PhHotWaterSystem) -> bool
        if not isinstance(other, PhHotWaterSystem):
            return False

        if self.id_num != other.id_num:
            return False

        if self.tank_1 != other.tank_1:
            return False
        if self.tank_2 != other.tank_2:
            return False
        if self.tank_buffer != other.tank_buffer:
            return False
        if self.tank_solar != other.tank_solar:
            return False

        if len(self.heaters) != len(other.heaters):
            return False
        for heater in self.heaters:
            if heater not in other.heaters:
                return False

        if len(self.distribution_piping) != len(other.distribution_piping):
            return False
        for distribution_pipe in self.distribution_piping:
            if distribution_pipe not in other.distribution_piping:
                return False

        if len(self.recirc_piping) != len(other.recirc_piping):
            return False
        for recirc_pipe in self.recirc_piping:
            if recirc_pipe not in other.recirc_piping:
                return False

        if self.number_tap_points != other.number_tap_points:
            return False

        return True

    def move(self, moving_vec):
        """Move the System's piping along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the ray.
        """
        pass

    def rotate(self, axis, angle, origin):
        """Rotate the System's piping by a certain angle around an axis and origin.

        Right hand rule applies:
        If axis has a positive orientation, rotation will be clockwise.
        If axis has a negative orientation, rotation will be counterclockwise.

        Args:
            axis: A Vector3D axis representing the axis of rotation.
            angle: An angle for rotation in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        pass

    def rotate_xy(self, angle, origin):
        """Rotate the System's piping counterclockwise in the XY plane by a certain angle.

        Args:
            angle: An angle in radians.
            origin: A Point3D for the origin around which the object will be rotated.
        """
        pass

    def reflect(self, normal, origin):
        """Reflected the System's piping across a plane with the input normal vector and origin.

        Args:
            normal: A Vector3D representing the normal vector for the plane across
                which the line segment will be reflected. THIS VECTOR MUST BE NORMALIZED.
            origin: A Point3D representing the origin from which to reflect.
        """
        pass

    def scale(self, factor, origin=None):
        """Scale the System's piping by a factor from an origin point.

        Args:
            factor: A number representing how much the line segment should be scaled.
            origin: A Point3D representing the origin from which to scale.
                If None, it will be scaled from the World origin (0, 0, 0).
        """
        pass
