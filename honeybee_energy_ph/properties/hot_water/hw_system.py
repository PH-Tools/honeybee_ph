# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Properties classes for SHWSystem (System / Equipment) objects."""

try:
    from typing import Any, ValuesView
except:
    pass  # IronPython

from honeybee_energy_ph.hvac import hot_water


class SHWSystemPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types[0], _expected_types[1], _input_type)
        super(SHWSystemPhProperties_FromDictError, self).__init__(self.msg)


class SHWSystemPhProperties(object):
    """Honeybee-PH Properties for logging PH-style data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

        self.tank_1 = None
        self.tank_2 = None
        self.tank_buffer = None
        self.tank_solar = None

        self._heaters = {}

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
            new_heater = hot_water.PhSHWHeaterBuilder.from_dict(heater_dict)
            new_prop.add_heater(hot_water.PhSHWHeaterBuilder.from_dict(heater_dict))

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def duplicate(self, new_host=None):
        # type: (Any) -> SHWSystemPhProperties
        return self.__copy__(new_host)

    def __copy__(self, new_host=None):
        # type: (Any) -> SHWSystemPhProperties
        _host = new_host or self._host
        new_obj = SHWSystemPhProperties(_host)

        new_obj.id_num = self.id_num
        new_obj.tank_1 = self.tank_1
        new_obj.tank_2 = self.tank_2
        new_obj.tank_buffer = self.tank_buffer
        new_obj.tank_solar = self.tank_solar

        for k, v in self._heaters.items():
            new_obj._heaters[k] = v

        return new_obj

    def __str__(self):
        return '{}: id={}'.format(self.__class__.__name__, self.id_num)

    def __repr__(self):
        """Properties representation."""
        return '{!r}(id_num={!r}, tank_1={!r}, tank_2={!r}, tank_buffer={!r}, tank_solar={!r})'.format(
            self.__class__.__name__, self.id_num, self.tank_1, self.tank_2, self.tank_buffer, self.tank_solar)

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()
