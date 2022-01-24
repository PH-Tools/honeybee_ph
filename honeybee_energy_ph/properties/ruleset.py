# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties classes for PH-ScheduleRuleset objects."""

try:
    from typing import Any
except:
    pass  # IronPython

from honeybee import properties


class ScheduleRulesetPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types[0], _expected_types[1], _input_type)
        super(ScheduleRulesetPhProperties_FromDictError, self).__init__(self.msg)


class OperationPeriod(object):
    """Operating Period PH info (operation-hours/day and operation-fraction)"""

    def __init__(self, _operation_hours=0, _operation_fraction=0.0):
        self.operation_hours = _operation_hours
        self.operation_fraction = _operation_fraction

    def to_dict(self):
        # type: () -> dict[str, float]
        d = {}
        d['operation_hours'] = self.operation_hours
        d['operation_fraction'] = self.operation_fraction
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, float]) -> OperationPeriod
        new_op_period = cls()
        new_op_period.operation_hours = _dict['operation_hours']
        new_op_period.operation_fraction = _dict['operation_fraction']
        return new_op_period

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return '{}: (_operation_hours={}, _operation_fraction={})'.format(
            self.__class__.__name__, self.operation_hours, self.operation_fraction)


class ScheduleRulesetPhProperties(object):
    """Honeybee-PH ScheduleRulesetPhProperties for logging PH-style schedule data."""

    def __init__(self, _host):
        self._host = _host
        self.operating_days_wk = 7.0
        self.operating_wks_yr = 24.0

        self.operating_period_high = OperationPeriod()
        self.operating_period_standard = OperationPeriod()
        self.operating_period_basic = OperationPeriod()
        self.operating_period_minimum = OperationPeriod()

    @property
    def host(self):
        return self._host

    @property
    def annual_average_operating_fraction(self):
        # type: () -> float
        """Returns the annual average operating fraction."""
        annual_oprating_days = self.operating_days_wk * self.operating_wks_yr

        wtd_high = self.operating_period_high.operation_hours * \
            self.operating_period_high.operation_fraction * annual_oprating_days
        wtd_standard = self.operating_period_standard.operation_hours * \
            self.operating_period_standard.operation_fraction * annual_oprating_days
        wtd_basic = self.operating_period_basic.operation_hours * \
            self.operating_period_basic.operation_fraction * annual_oprating_days
        wtd_minimum = self.operating_period_minimum.operation_hours * \
            self.operating_period_minimum.operation_fraction * annual_oprating_days

        wtd_total = wtd_high + wtd_standard + wtd_basic + wtd_minimum
        annual_operating_hours = annual_oprating_days * 24
        wtd_annual_avg = wtd_total / annual_operating_hours

        return wtd_annual_avg

    def validate_operating_period_hours(self):
        # type: () -> str | None
        """Returns a warning if the total operating period hours do not equal 24."""
        total_hours = self.operating_period_high.operation_hours +\
            self.operating_period_standard.operation_hours +\
            self.operating_period_basic.operation_hours +\
            self.operating_period_minimum.operation_hours

        if abs(24 - total_hours) > 0.001:
            return 'Error: Total Operating Hours={}, not 24?'.format(total_hours)
        else:
            return None

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}
        if abridged:
            d['type'] = 'ScheduleRulesetPhPropertiesAbridged'
        else:
            d['type'] = 'ScheduleRulesetPhProperties'

        d['operating_days_wk'] = self.operating_days_wk
        d['operating_wks_yr'] = self.operating_wks_yr
        d['operation_period_high'] = self.operating_period_high.to_dict()
        d['operation_period_standard'] = self.operating_period_standard.to_dict()
        d['operation_period_basic'] = self.operating_period_basic.to_dict()
        d['operation_period_minimum'] = self.operating_period_minimum.to_dict()

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> ScheduleRulesetPhProperties
        valid_types = ('ScheduleRulesetPhProperties',
                       'ScheduleRulesetPhPropertiesAbridged')
        if _dict['type'] not in valid_types:
            raise ScheduleRulesetPhProperties_FromDictError(valid_types, _dict['type'])

        new_prop = cls(host)
        new_prop.operating_days_wk = _dict['operating_days_wk']
        new_prop.operating_wks_yr = _dict['operating_wks_yr']
        new_prop.operating_period_high = OperationPeriod.from_dict(
            _dict['operation_period_high'])
        new_prop.operating_period_standard = OperationPeriod.from_dict(
            _dict['operation_period_standard'])
        new_prop.operating_period_basic = OperationPeriod.from_dict(
            _dict['operation_period_basic'])
        new_prop.operating_period_minimum = OperationPeriod.from_dict(
            _dict['operation_period_minimum'])

        return new_prop

    def apply_properties_from_dict(self, abridged_data):

        return

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return '{}'.format(self.__class__.__name__)


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
