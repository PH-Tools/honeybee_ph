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
        self.quantity = 1
        self.tank_type = None

        self.for_solar = False
        self.heat_loss_rate = None
        self.volume = None
        self.standby_fraction = None

        self.in_conditioned_space = True
        self.location_temp = 20
        self.water_temp = 55

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['tank_type'] = self.tank_type
        d['quantity'] = self.quantity
        d['name'] = self.name
        d['for_solar'] = self.for_solar
        d['heat_loss_rate'] = self.heat_loss_rate
        d['volume'] = self.volume
        d['standby_fraction'] = self.standby_fraction
        d['in_conditioned_space'] = self.in_conditioned_space
        d['location_temp'] = self.location_temp
        d['water_temp'] = self.water_temp

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhSHWTank
        obj = cls()

        obj.tank_type = _input_dict['tank_type']
        obj.quantity = _input_dict['quantity']
        obj.name = _input_dict['name']
        obj.for_solar = _input_dict['for_solar']
        obj.heat_loss_rate = _input_dict['heat_loss_rate']
        obj.volume = _input_dict['volume']
        obj.standby_fraction = _input_dict['standby_fraction']
        obj.in_conditioned_space = _input_dict['in_conditioned_space']
        obj.location_temp = _input_dict['location_temp']
        obj.water_temp = _input_dict['water_temp']

        return obj

    def __str__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.tank_type, self.name)

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.name)

    def ToString(self):
        return self.__repr__()
