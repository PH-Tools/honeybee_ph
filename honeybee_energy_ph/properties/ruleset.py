# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties classes for PH-ScheduleRuleset objects."""

try:
    from typing import Any
except:
    pass  # IronPython

from honeybee import properties


class ScheduleRulesetPhProperties_FromDictError(Exception):
    def __init__(self, _input_type):
        self.msg = 'Error: Expected "type" of "" or "". Got: {}'.format(_input_type)
        super(DataTypeError, self).__init__(self, msg)


class ScheduleRulesetPhProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.operating_days_wk = 7.0
        self.operating_wks_yr = 24.0

    @property
    def host(self):
        return self._host

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}
        if abridged:
            d['type'] = 'ScheduleRulesetPhPropertiesAbridged'
        else:
            d['type'] = 'ScheduleRulesetPhProperties'

        d['operating_days_wk'] = self.operating_days_wk
        d['operating_wks_yr'] = self.operating_wks_yr

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> ScheduleRulesetPhProperties
        if _dict['type'] != 'ScheduleRulesetPhProperties':
            raise ScheduleRulesetPhProperties_FromDictError(_dict['type'])

        new_prop = cls(host)
        new_prop.operating_days_wk = _dict['operating_days_wk']
        new_prop.operating_wks_yr = _dict['operating_wks_yr']

        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return '{}: {}'.format(self.__class__.__name__, self.host.display_name)


class ScheduleRulesetProperties(properties._Properties):
    """Honeybee-Energy Ruleset Properties.

    Ruleset properties. This class will be extended by extensions.

    Usage:

    .. code-block:: python

        ruleset = PH_ScheduleRuleset()
        ruleset.properties -> ScheduleRulesetProperties
        ruleset.properties.ph -> ScheduleRulesetPhProperties
    """

    def to_dict(self, abridged=False, include=None):
        # type: (bool, Any | None) -> dict[str, Any]
        """Convert properties to dictionary.

        Args:
            abridged: Boolean to note whether the full dictionary describing the
                object should be returned (False) or just an abridged version (True).
                Default: False.
            include: A list of keys to be included in dictionary.
                If None all the available keys will be included.
        """
        d = {}
        if abridged == False:
            d['type'] = 'ScheduleRulesetProperties'
        else:
            d['type'] = 'SchdeduleRulesetPropertiesAbridged'

        d = self._add_extension_attr_to_dict(d, abridged, include)
        return d

    def __repr__(self):
        """Properties representation."""
        return '{}'.format(self.__class__.__name__)
