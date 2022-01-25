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

    def __init__(self, _operation_hours=0.0, _operation_fraction=0.0):
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


class OperatingPeriodCollection(object):
    def __init__(self):
        self.high = None
        self.standard = None
        self.basic = None
        self.minimum = None

    def __nonzero__(self):
        # type: () -> bool
        if not self.high and not self.standard and not self.basic and not self.minimum:
            return False
        else:
            return True

    def __bool__(self):
        return self.__nonzero__()

    def __iter__(self):
        # type: () -> OperationPeriod
        for _ in [self.high, self.standard, self.basic, self.minimum]:
            yield _

    def __len__(self):
        return 4

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        if self.high:
            d['high'] = self.high.to_dict()
        if self.standard:
            d['standard'] = self.standard.to_dict()
        if self.basic:
            d['basic'] = self.basic.to_dict()
        if self.minimum:
            d['minimum'] = self.minimum.to_dict()

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> OperatingPeriodCollection
        new_obj = OperatingPeriodCollection()

        high_dict = _input_dict.get('high', None)
        if high_dict:
            new_obj.high = OperationPeriod.from_dict(high_dict)

        standard_dict = _input_dict.get('standard', None)
        if standard_dict:
            new_obj.standard = OperationPeriod.from_dict(standard_dict)

        basic_dict = _input_dict.get('basic', None)
        if basic_dict:
            new_obj.basic = OperationPeriod.from_dict(basic_dict)

        minimum_dict = _input_dict.get('minimum', None)
        if minimum_dict:
            new_obj.minimum = OperationPeriod.from_dict(minimum_dict)

        return new_obj


class ScheduleRulesetPhProperties(object):
    """Honeybee-PH ScheduleRulesetPhProperties for logging PH-style schedule data."""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0
        self.operating_days_wk = 7.0
        self.operating_wks_yr = 24.0
        self.operating_periods = OperatingPeriodCollection()

    @property
    def host(self):
        return self._host

    @property
    def annual_average_operating_fraction(self):
        # type: () -> float
        """Returns the annual average operating fraction."""
        if not self.operating_periods:
            return 0

        annual_oprating_days = self.operating_days_wk * self.operating_wks_yr
        wtd_total = 0
        for op_period in self.operating_periods:
            if op_period:
                wtd_total += op_period.operation_hours * op_period.operation_fraction * annual_oprating_days
        annual_operating_hours = annual_oprating_days * 24
        wtd_annual_avg = wtd_total / annual_operating_hours

        return wtd_annual_avg

    def validate_operating_period_hours(self):
        # type: () -> str | None
        """Returns a warning if the total operating period hours do not equal 24."""
        total_hours = 0
        for op_period in self.operating_periods:
            if op_period:
                total_hours += op_period.operation_hours

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

        d['id_num'] = self.id_num
        d['operating_days_wk'] = self.operating_days_wk
        d['operating_wks_yr'] = self.operating_wks_yr
        d['operating_periods'] = self.operating_periods.to_dict()

        return {'ph': d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> ScheduleRulesetPhProperties
        valid_types = ('ScheduleRulesetPhProperties',
                       'ScheduleRulesetPhPropertiesAbridged')
        if _dict['type'] not in valid_types:
            raise ScheduleRulesetPhProperties_FromDictError(valid_types, _dict['type'])

        new_prop = cls(host)
        new_prop.id_num = _dict['id_num']
        new_prop.operating_days_wk = _dict['operating_days_wk']
        new_prop.operating_wks_yr = _dict['operating_wks_yr']
        new_prop.operating_periods = OperatingPeriodCollection.from_dict(
            _dict.get('operating_periods', {}))
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
