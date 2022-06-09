# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Passive House Service Hot Water Objects"""

try:
    from typing import Any, Union
except ImportError:
    pass  # IronPython

from honeybee_energy_ph.hvac import _base
from honeybee_ph_utils import enumerables


class UnknownPhHeaterTypeError(Exception):
    def __init__(self, _heater_types, _received_type):
        self.msg = 'Error: Unknown SHW Heater Type? Got: "{}" but only types: {} are allowed?'.format(
            _received_type, _heater_types)
        super(UnknownPhHeaterTypeError, self).__init__(self.msg)


class PhSHWTankType(enumerables.CustomEnum):
    allowed = [
        "0-No storage tank",
        "1-DHW and heating",
        "2-DHW only"
    ]

    def __init__(self, _value=1, _index_offset=0):
        super(PhSHWTankType, self).__init__(_value, _index_offset)


class PhSHWTank(object):
    def __init__(self):
        self.display_name = '_unnamed_hw_tank_'  # type: str
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
        self.water_temp = 55.0  # type: float

    @property
    def tank_type(self):
        # type () -> str
        return self._tank_type.value

    @tank_type.setter
    def tank_type(self, _in):
        # type: (Union[str, int]) -> None
        self._tank_type = PhSHWTankType(_in)

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        d['display_name'] = self.display_name
        d['quantity'] = self.quantity
        d['_tank_type'] = self._tank_type.to_dict()
        d['in_conditioned_space'] = self.in_conditioned_space
        d['solar_connection'] = self.solar_connection
        d['solar_losses'] = self.solar_losses
        d['storage_loss_rate'] = self.storage_loss_rate
        d['storage_capacity'] = self.storage_capacity
        d['standby_losses'] = self.standby_losses
        d['standby_fraction'] = self.standby_fraction
        d['room_temp'] = self.room_temp
        d['water_temp'] = self.water_temp

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> PhSHWTank
        obj = cls()

        obj.display_name = _input_dict['display_name']
        obj.quantity = _input_dict['quantity']
        obj._tank_type = PhSHWTankType.from_dict(_input_dict['_tank_type'])
        obj.in_conditioned_space = _input_dict['in_conditioned_space']
        obj.solar_connection = _input_dict['solar_connection']
        obj.solar_losses = _input_dict['solar_losses']
        obj.storage_loss_rate = _input_dict['storage_loss_rate']
        obj.storage_capacity = _input_dict['storage_capacity']
        obj.standby_losses = _input_dict['standby_losses']
        obj.standby_fraction = _input_dict['standby_fraction']
        obj.room_temp = _input_dict['room_temp']
        obj.water_temp = _input_dict['water_temp']

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

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['heater_type'] = self.__class__.__name__
        d['identifier'] = self.identifier
        d['display_name'] = self.display_name
        d['percent_coverage'] = self.percent_coverage
        d['in_conditioned_space'] = self.in_conditioned_space

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhSHWHeaterElectric
        new_obj = cls()

        new_obj.identifier = _input_dict['identifier']
        new_obj.display_name = _input_dict['display_name']
        new_obj.percent_coverage = _input_dict['percent_coverage']
        new_obj.in_conditioned_space = _input_dict['in_conditioned_space']

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
        d = {}

        d['heater_type'] = self.__class__.__name__
        d['identifier'] = self.identifier
        d['display_name'] = self.display_name
        d['percent_coverage'] = self.percent_coverage
        d['in_conditioned_space'] = self.in_conditioned_space

        d['fuel'] = self.fuel
        d['condensing'] = self.condensing
        d['effic_at_30_perc_load'] = self.effic_at_30_perc_load
        d['effic_at_nominal_load'] = self.effic_at_nominal_load
        d['avg_return_temp_at_30_perc_load'] = self.avg_return_temp_at_30_perc_load
        d['avg_boiler_temp_at_70_55'] = self.avg_boiler_temp_at_70_55
        d['avg_boiler_temp_at_55_45'] = self.avg_boiler_temp_at_55_45
        d['avg_boiler_temp_at_35_28'] = self.avg_boiler_temp_at_35_28

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict) -> PhSHWHeaterBoiler
        new_obj = cls()

        new_obj.identifier = _input_dict['identifier']
        new_obj.display_name = _input_dict['display_name']
        new_obj.percent_coverage = _input_dict['percent_coverage']
        new_obj.in_conditioned_space = _input_dict['in_conditioned_space']

        new_obj.fuel = _input_dict['fuel']
        new_obj.condensing = _input_dict['condensing']
        new_obj.effic_at_30_perc_load = _input_dict['effic_at_30_perc_load']
        new_obj.effic_at_nominal_load = _input_dict['effic_at_nominal_load']
        new_obj.avg_return_temp_at_30_perc_load = _input_dict['avg_return_temp_at_30_perc_load']
        new_obj.avg_boiler_temp_at_70_55 = _input_dict['avg_boiler_temp_at_70_55']
        new_obj.avg_boiler_temp_at_55_45 = _input_dict['avg_boiler_temp_at_55_45']
        new_obj.avg_boiler_temp_at_35_28 = _input_dict['avg_boiler_temp_at_35_28']

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
        # type: () -> dict
        d = {}

        d['heater_type'] = self.__class__.__name__
        d['identifier'] = self.identifier
        d['display_name'] = self.display_name
        d['percent_coverage'] = self.percent_coverage
        d['in_conditioned_space'] = self.in_conditioned_space

        d['fuel'] = self.fuel
        d['effic_in_basic_cycle'] = self.effic_in_basic_cycle
        d['effic_in_const_operation'] = self.effic_in_const_operation
        d['avg_frac_heat_released'] = self.avg_frac_heat_released
        d['on_off_temp_diff'] = self.on_off_temp_diff

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.identifier = _input_dict['identifier']
        new_obj.display_name = _input_dict['display_name']
        new_obj.percent_coverage = _input_dict['percent_coverage']
        new_obj.in_conditioned_space = _input_dict['in_conditioned_space']

        new_obj.fuel = _input_dict['fuel']
        new_obj.effic_in_basic_cycle = _input_dict['effic_in_basic_cycle']
        new_obj.effic_in_const_operation = _input_dict['effic_in_const_operation']
        new_obj.avg_frac_heat_released = _input_dict['avg_frac_heat_released']
        new_obj.on_off_temp_diff = _input_dict['on_off_temp_diff']

        return new_obj


class PhSHWHeaterDistrict(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterDistrict, self).__init__()
        self.energy_carrier = 1
        self.solar_fraction = 0
        self.util_fact_heat_transfer = 1

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['heater_type'] = self.__class__.__name__
        d['identifier'] = self.identifier
        d['display_name'] = self.display_name
        d['percent_coverage'] = self.percent_coverage
        d['in_conditioned_space'] = self.in_conditioned_space

        d['energy_carrier'] = self.energy_carrier
        d['solar_fraction'] = self.solar_fraction
        d['util_fact_heat_transfer'] = self.util_fact_heat_transfer

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.identifier = _input_dict['identifier']
        new_obj.display_name = _input_dict['display_name']
        new_obj.percent_coverage = _input_dict['percent_coverage']
        new_obj.in_conditioned_space = _input_dict['in_conditioned_space']

        new_obj.energy_carrier = _input_dict['energy_carrier']
        new_obj.solar_fraction = _input_dict['solar_fraction']
        new_obj.util_fact_heat_transfer = _input_dict['util_fact_heat_transfer']

        return new_obj


class PhSHWHeaterHeatPump(PhHotWaterHeater):
    def __init__(self):
        super(PhSHWHeaterHeatPump, self).__init__()
        self.annual_COP = None
        self.annual_system_perf_ratio = None
        self.annual_energy_factor = None

    def to_dict(self):
        # type: () -> dict
        d = {}

        d['heater_type'] = self.__class__.__name__
        d['identifier'] = self.identifier
        d['display_name'] = self.display_name
        d['percent_coverage'] = self.percent_coverage
        d['in_conditioned_space'] = self.in_conditioned_space

        d['annual_COP'] = self.annual_COP
        d['annual_system_perf_ratio'] = self.annual_system_perf_ratio
        d['annual_energy_factor'] = self.annual_energy_factor

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        new_obj = cls()

        new_obj.identifier = _input_dict['identifier']
        new_obj.display_name = _input_dict['display_name']
        new_obj.percent_coverage = _input_dict['percent_coverage']
        new_obj.in_conditioned_space = _input_dict['in_conditioned_space']

        new_obj.annual_COP = _input_dict['annual_COP']
        new_obj.annual_system_perf_ratio = _input_dict['annual_system_perf_ratio']
        new_obj.annual_energy_factor = _input_dict['annual_energy_factor']

        return new_obj


# -----------------------------------------------------------------------------


class PhSHWHeaterBuilder(object):
    """Constructor class for Hot-Water-Heater objects"""

    heaters = {
        'PhSHWHeaterElectric': PhSHWHeaterElectric,
        'PhSHWHeaterBoiler': PhSHWHeaterBoiler,
        'PhSHWHeaterBoilerWood': PhSHWHeaterBoilerWood,
        'PhSHWHeaterDistrict': PhSHWHeaterDistrict,
        'PhSHWHeaterHeatPump': PhSHWHeaterHeatPump,
    }

    @ classmethod
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
