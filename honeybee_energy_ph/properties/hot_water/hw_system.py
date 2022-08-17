# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Properties classes for SHWSystem (System / Equipment) objects."""

try:
    from typing import Any, ValuesView, Dict
except:
    pass  # IronPython

from honeybee_energy_ph.hvac import hot_water


class SHWSystemPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types, _input_type)
        super(SHWSystemPhProperties_FromDictError, self).__init__(self.msg)


class SHWSystemPhProperties(object):
    """Honeybee-PH Properties for logging PH-style data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

        self.tank_1 = None  # Optional[PhSHWTank]
        self.tank_2 = None  # Optional[PhSHWTank]
        self.tank_buffer = None  # Optional[PhSHWTank]
        self.tank_solar = None  # Optional[PhSHWTank]

        self._heaters = {}  # type: Dict[str, hot_water.PhHotWaterHeater]
        self._branch_piping = {}  # type: Dict[str, hot_water.PhPipeElement]
        self._recirc_piping = {}  # type: Dict[str, hot_water.PhPipeElement]

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
            _h, 'to_dict'), 'Error: HW-Heater "{}" is not serializable?'.format(_h)
        self._heaters[_h.identifier] = _h

    def add_branch_piping(self, _branch_piping):
        # type: (hot_water.PhPipeElement) -> None
        self._branch_piping[_branch_piping.identifier] = _branch_piping

    def clear_branch_piping(self):
        self._branch_piping = {}

    @property
    def branch_piping(self):
        # type: () -> ValuesView[hot_water.PhPipeElement]
        """Returns a list of all the branch-piping objects in the system."""
        return self._branch_piping.values()

    def add_recirc_piping(self, _recirc_piping):
        # type: (hot_water.PhPipeElement) -> None
        self._recirc_piping[_recirc_piping.identifier] = _recirc_piping

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
        return [self.tank_1, self.tank_2,  self.tank_buffer, self.tank_solar]

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged:
            d['type'] = 'SHWSystemPhPropertiesAbridged'
        else:
            d['type'] = 'SHWSystemPhProperties'

        d['id_num'] = self.id_num
        if self.tank_1:
            d['tank_1'] = self.tank_1.to_dict()
        if self.tank_2:
            d['tank_2'] = self.tank_2.to_dict()
        if self.tank_buffer:
            d['tank_buffer'] = self.tank_buffer.to_dict()
        if self.tank_solar:
            d['tank_solar'] = self.tank_solar.to_dict()

        d['heaters'] = {}
        for heater in self.heaters:
            d['heaters'][id(heater)] = heater.to_dict()

        d['branch_piping'] = {}
        for branch_piping in self.branch_piping:
            d['branch_piping'][branch_piping.identifier] = branch_piping.to_dict()

        d['recirc_piping'] = {}
        for recirc_piping in self.recirc_piping:
            d['recirc_piping'][recirc_piping.identifier] = recirc_piping.to_dict()

        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, _host):
        # type: (dict, Any) -> SHWSystemPhProperties
        valid_types = ('SHWSystemPhProperties',
                       'SHWSystemPhPropertiesAbridged')
        if _input_dict['type'] not in valid_types:
            raise SHWSystemPhProperties_FromDictError(valid_types, _input_dict['type'])

        new_prop = cls(_host)
        new_prop.id_num = _input_dict['id_num']

        if _input_dict.get('tank_1', None):
            new_prop.tank_1 = hot_water.PhSHWTank.from_dict(
                _input_dict['tank_1'])
        if _input_dict.get('tank_2', None):
            new_prop.tank_2 = hot_water.PhSHWTank.from_dict(
                _input_dict['tank_2'])
        if _input_dict.get('tank_buffer', None):
            new_prop.tank_buffer = hot_water.PhSHWTank.from_dict(
                _input_dict['tank_buffer'])
        if _input_dict.get('tank_buffer', None):
            new_prop.tank_buffer = hot_water.PhSHWTank.from_dict(
                _input_dict['tank_buffer'])

        for heater_dict in _input_dict['heaters'].values():
            new_prop.add_heater(hot_water.PhSHWHeaterBuilder.from_dict(heater_dict))

        for branch_piping_dict in _input_dict['branch_piping'].values():
            new_prop.add_branch_piping(
                hot_water.PhPipeElement.from_dict(branch_piping_dict))

        for recirc_piping_dict in _input_dict['recirc_piping'].values():
            new_prop.add_recirc_piping(
                hot_water.PhPipeElement.from_dict(recirc_piping_dict))

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
            new_obj._heaters[k] = v

        for k, v in self._branch_piping.items():
            new_obj._branch_piping[k] = v.duplicate()

        for k, v in self._recirc_piping.items():
            new_obj._recirc_piping[k] = v.duplicate()

        return new_obj

    def duplicate(self, new_host=None):
        # type: (Any) -> SHWSystemPhProperties
        return self.__copy__(new_host)

    def __str__(self):
        return '{}: id={}'.format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        """Properties representation."""
        return '{!r}(id_num={!r}, tank_1={!r}, tank_2={!r}, tank_buffer={!r}, tank_solar={!r})'.format(
            self.__class__.__name__, self.id_num, self.tank_1, self.tank_2, self.tank_buffer, self.tank_solar)

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

        for branch_pipe in self.branch_piping:
            new_obj.add_branch_piping(branch_pipe)
        for branch_pipe in other.branch_piping:
            new_obj.add_branch_piping(branch_pipe)

        for recirc_pipe in self.recirc_piping:
            new_obj.add_recirc_piping(recirc_pipe)
        for recirc_pipe in other.recirc_piping:
            new_obj.add_recirc_piping(recirc_pipe)

        return new_obj

    def __radd__(self, other):
        # type: (SHWSystemPhProperties) -> SHWSystemPhProperties
        if isinstance(other, int):
            return self
        else:
            return self + other
