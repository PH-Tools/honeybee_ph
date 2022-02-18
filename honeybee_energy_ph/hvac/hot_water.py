# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House Service Hot Water Objects"""

try:
    from typing import Any
except ImportError:
    pass  # IronPython


class PhSHWTank(object):
    def __init__(self):
        self.name = '_unnamed_hw_tank_'
        self.tank_type = None
        self.for_solar = None
        self.heat_loss_rate = None
        self.volume = None
        self.standby_fraction = None
        self.location = None
        self.location_temp = None

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['tank_type'] = self.tank_type
        d['for_solar'] = self.for_solar
        d['heat_loss_rate'] = self.heat_loss_rate
        d['volume'] = self.volume
        d['standby_fraction'] = self.standby_fraction
        d['location'] = self.location
        d['location_temp'] = self.location_temp

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhSHWTank
        obj = cls()

        obj.tank_type = _input_dict['tank_type']
        obj.for_solar = _input_dict['for_solar']
        obj.heat_loss_rate = _input_dict['heat_loss_rate']
        obj.volume = _input_dict['volume']
        obj.standby_fraction = _input_dict['standby_fraction']
        obj.location = _input_dict['location']
        obj.location_temp = _input_dict['location_temp']

        return obj

    def __str__(self):
        return "{}: {}".format(self.__class__.__name__, self.tank_type)

    def __repr__(self):
        return "{}".format(self.__class__.__name__)

    def ToString(self):
        return self.__repr__()
