# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties classes for PH-ScheduleRuleset objects."""

try:
    from typing import Any
except:
    pass  # IronPython

from honeybee_energy_ph.hvac import ventilation


class IdealAirSystemPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types[0], _expected_types[1], _input_type)
        super(IdealAirSystemPhProperties_FromDictError, self).__init__(self.msg)


class IdealAirSystemPhProperties(object):
    """Honeybee-PH ScheduleRulesetPhProperties for logging PH-style schedule data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.ventilator_id_num = 0
        self.ventilation_system = None

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, dict]
        d = {}
        if abridged:
            d['type'] = 'IdealAirSystemPhPropertiesAbridged'
        else:
            d['type'] = 'IdealAirSystemPhProperties'

        d['id_num'] = self.id_num
        d['ventilator_id_num'] = self.id_num
        if self.ventilation_system is not None:
            d['ventilation_system'] = self.ventilation_system.to_dict()
        else:
            d['ventilation_system'] = None

        return {'ph': d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (dict, Any) -> IdealAirSystemPhProperties
        valid_types = ('IdealAirSystemPhProperties',
                       'IdealAirSystemPhPropertiesAbridged')
        if _input_dict['type'] not in valid_types:
            raise IdealAirSystemPhProperties_FromDictError(
                valid_types, _input_dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _input_dict['id_num']
        new_prop.ventilator_id_num = _input_dict['ventilator_id_num']

        vent_system_dict = _input_dict.get('ventilation_system', None)
        if vent_system_dict:
            new_prop.ventilation_system = ventilation.PhVentilationSystem.from_dict(
                vent_system_dict)

        return new_prop

    def apply_properties_from_dict(self, abridged_data):

        return

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return '{}'.format(self.__class__.__name__)
