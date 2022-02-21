# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House Service Hot Water Objects"""

from honeybee_energy_ph.hvac import _base

try:
    from typing import Any
except ImportError:
    pass  # IronPython


class UnknownPhHeaterTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        self.msg = 'Error: Unknown SHW Heater Type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types)
        super(UnknownPhHeaterTypeError, self).__init__(self.msg)


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


# -- Heaters ------------------------------------------------------------------


class PhHotWaterHeater(_base._Base):
    """Base class for all PH Hot-Water Heaters."""

    def __init__(self):
        super(PhHotWaterHeater, self).__init__()

    def to_dict(self):
        # type: () -> dict
        d = {}
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHotWaterHeater
        new_obj = cls()
        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhSHWHeaterElectric(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterElectric, self).__init__()
        self.name = '_unnamed_hot_water_elec_heater_'

    def to_dict(self):
        # type: () -> dict
        d = {}
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhSHWHeaterElectric
        new_obj = cls()
        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhSHWHeaterGasBoiler(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterGasBoiler, self).__init__()
        self.name = '_unnamed_hot_water_gas_boiler_heater_'

    def to_dict(self):
        # type: () -> dict
        d = {}
        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhSHWHeaterGasBoiler
        new_obj = cls()
        return new_obj

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)


class PhSHWHeaterBuilder(object):
    """Constructor class for Hot-Water-Heater objects"""

    heaters = {
        'PhSHWHeaterGasBoiler': PhSHWHeaterGasBoiler,
        'PhSHWHeaterElectric': PhSHWHeaterElectric,
    }

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhHotWaterHeater

        heater_type = _input_dict.get('heater_type')
        if heater_type is None:
            raise UnknownPhHeaterTypeError(cls.heaters.keys(), heater_type)

        heater_class = cls.heaters[heater_type]
        new_heater = heater_class.from_dict(_input_dict)

        return new_heater

    def __str__(self):
        return '{}()'.format(self.__class__.__name__)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return str(self)
