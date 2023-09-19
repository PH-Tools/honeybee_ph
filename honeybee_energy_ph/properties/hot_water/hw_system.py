# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Properties classes for SHWSystem (System / Equipment) objects."""

try:
    from typing import Any, ValuesView, Dict, Optional, Union
except:
    pass  # IronPython

from honeybee_energy_ph.hvac import hot_water


class SHWSystemPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type
        )
        super(SHWSystemPhProperties_FromDictError, self).__init__(self.msg)


class SHWSystemPhProperties(object):
    """Honeybee-PH Properties for logging PH-style data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

        self.tank_1 = None  # type: Optional[hot_water.PhSHWTank]
        self.tank_2 = None  # type: Optional[hot_water.PhSHWTank]
        self.tank_buffer = None  # type: Optional[hot_water.PhSHWTank]
        self.tank_solar = None  # type: Optional[hot_water.PhSHWTank]

        self._heaters = {}  # type: Dict[str, hot_water.PhHotWaterHeater]
        self._distribution_piping = {}  # type: Dict[str, hot_water.PhPipeTrunk]
        self._recirc_piping = {}  # type: Dict[str, hot_water.PhPipeElement]

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
        return sum(
            _.total_home_run_fixture_length for _ in self._distribution_piping.values()
        )

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
        return (
            sum([v.water_temp * v.length_m for v in self._recirc_piping.values()])
            / self.total_recirc_pipe_length
        )

    @property
    def recirc_hours(self):
        # type: () -> int
        """Return the length-weighted average of recirculation piping hours."""
        if not self._recirc_piping or self.total_recirc_pipe_length == 0:
            return 24
        return int(
            sum([v.daily_period * v.length_m for v in self._recirc_piping.values()])
            / self.total_recirc_pipe_length
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
        # type: () -> ValuesView[hot_water.PhHotWaterHeater]
        """Returns a list of all the heaters on the system."""
        return self._heaters.values()

    def clear_heaters(self):
        self._heaters = {}

    def add_heater(self, _h):
        # type: (hot_water.PhHotWaterHeater) -> None
        """Adds a new hot-water heater to the system."""
        if not _h:
            return

        assert hasattr(
            _h, "to_dict"
        ), 'Error: HW-Heater "{}" is not serializable?'.format(_h)
        self._heaters[_h.identifier] = _h

    def add_distribution_piping(self, _distribution_piping, _key=None):
        # type: (Union[hot_water.PhPipeTrunk, hot_water.PhPipeBranch, hot_water.PhPipeElement], Optional[str]) -> None
        """Add a new distribution (branch, trunk, fixture) to the system.

        If a branch or fixture pipe is passed, a 0-length trunk will be created and the
        branch or fixture will be added to it before adding to the system.
        """

        if isinstance(_distribution_piping, hot_water.PhPipeTrunk):
            # -- Add the trunk to the collection
            new_trunk = _distribution_piping
        elif isinstance(_distribution_piping, hot_water.PhPipeBranch):
            # -- Build a new Trunk and add the branch to it
            new_trunk = hot_water.PhPipeTrunk()
            new_trunk.add_branch(_distribution_piping)
        elif isinstance(_distribution_piping, hot_water.PhPipeElement):
            # -- Build a new Trunk and Branch, add the fixture to it
            new_branch = hot_water.PhPipeBranch()
            new_branch.add_fixture(_distribution_piping)
            new_trunk = hot_water.PhPipeTrunk()
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
        # type: () -> ValuesView[hot_water.PhPipeTrunk]
        """Returns a list of all the distribution-piping (Trunks) in the system."""
        return self._distribution_piping.values()

    def add_recirc_piping(self, _recirc_piping, _key=None):
        # type: (hot_water.PhPipeElement, Optional[str]) -> None
        self._recirc_piping[_key or _recirc_piping.identifier] = _recirc_piping

    def clear_recirc_piping(self):
        self._recirc_piping = {}

    @property
    def recirc_piping(self):
        # type: () -> ValuesView[hot_water.PhPipeElement]
        """Returns a list of all the recirculation-piping objects in the system."""
        return self._recirc_piping.values()

    @property
    def host(self):
        return self._host

    @property
    def tanks(self):
        # type: () -> list[hot_water.PhSHWTank | None]
        """Return a list of the system tanks in order (1, 2, buffer, solar)."""
        return [self.tank_1, self.tank_2, self.tank_buffer, self.tank_solar]

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged:
            d["type"] = "SHWSystemPhPropertiesAbridged"
        else:
            d["type"] = "SHWSystemPhProperties"

        d["id_num"] = self.id_num
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
            d["heaters"][id(heater)] = heater.to_dict()

        d["distribution_piping"] = {}
        for distribution_piping in self.distribution_piping:
            d["distribution_piping"][
                distribution_piping.identifier
            ] = distribution_piping.to_dict()

        d["recirc_piping"] = {}
        for recirc_piping in self.recirc_piping:
            d["recirc_piping"][recirc_piping.identifier] = recirc_piping.to_dict()

        d["number_tap_points"] = self._number_tap_points
        d["recirc_temp"] = self.recirc_temp
        d["recirc_hours"] = self.recirc_hours

        return {"ph": d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> SHWSystemPhProperties
        valid_types = ("SHWSystemPhProperties", "SHWSystemPhPropertiesAbridged")
        if _input_dict["type"] not in valid_types:
            raise SHWSystemPhProperties_FromDictError(valid_types, _input_dict["type"])

        new_prop = cls(_host)
        new_prop.id_num = _input_dict["id_num"]

        if _input_dict.get("tank_1", None):
            new_prop.tank_1 = hot_water.PhSHWTank.from_dict(_input_dict["tank_1"])
        if _input_dict.get("tank_2", None):
            new_prop.tank_2 = hot_water.PhSHWTank.from_dict(_input_dict["tank_2"])
        if _input_dict.get("tank_buffer", None):
            new_prop.tank_buffer = hot_water.PhSHWTank.from_dict(
                _input_dict["tank_buffer"]
            )
        if _input_dict.get("tank_buffer", None):
            new_prop.tank_buffer = hot_water.PhSHWTank.from_dict(
                _input_dict["tank_buffer"]
            )

        for heater_dict in _input_dict["heaters"].values():
            new_prop.add_heater(hot_water.PhSHWHeaterBuilder.from_dict(heater_dict))

        for distribution_piping_dict in _input_dict["distribution_piping"].values():
            new_prop.add_distribution_piping(
                hot_water.PhPipeTrunk.from_dict(distribution_piping_dict)
            )

        for recirc_piping_dict in _input_dict["recirc_piping"].values():
            new_prop.add_recirc_piping(
                hot_water.PhPipeElement.from_dict(recirc_piping_dict)
            )

        new_prop._number_tap_points = _input_dict["number_tap_points"]

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def __copy__(self, new_host=None):
        # type: (Any) -> SHWSystemPhProperties
        _host = new_host or self._host
        new_obj = SHWSystemPhProperties(_host)
        new_obj.id_num = self.id_num

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

    def duplicate(self, new_host=None):
        # type: (Any) -> SHWSystemPhProperties
        return self.__copy__(new_host)

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
        # type: (SHWSystemPhProperties) -> SHWSystemPhProperties
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
        # type: (SHWSystemPhProperties) -> SHWSystemPhProperties
        if isinstance(other, int):
            return self
        else:
            return self + other
