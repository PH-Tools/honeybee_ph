# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Properties classes for PH-ScheduleRuleset objects."""

try:
    pass
except:
    pass  # IronPython


class ScheduleRulesetPhProperties_FromDictError(Exception):
    def __init__(self, _expected_types, _input_type):
        self.msg = 'Error: Expected type of "{}". Got: {}'.format(
            _expected_types[0],
            _expected_types[1],
        )
        super(ScheduleRulesetPhProperties_FromDictError, self).__init__(self.msg)


class DailyOperationPeriod(object):
    """PH-Style Daily Operating Period."""

    def __init__(self):
        self.name = "_unnamed_op_period_"
        self.start_hour = 0.0
        self.end_hour = 24.0
        self.operation_fraction = 1.0

    @classmethod
    def from_annual_utilization_factor(cls, _ann_util_fac=1.0, _name=""):
        # type: (float, str) -> DailyOperationPeriod
        op_period = cls()

        op_period.name = _name
        op_period.start_hour = 0
        op_period.end_hour = 24
        op_period.operation_fraction = _ann_util_fac

        return op_period

    @classmethod
    def from_start_end_hours(cls, _start_hr=0, _end_hr=24, _op_frac=1.0, _name=""):
        # type: (float, float, float, str) -> DailyOperationPeriod
        op_period = cls()

        op_period.name = _name
        op_period.start_hour = _start_hr
        op_period.end_hour = _end_hr
        op_period.operation_fraction = _op_frac

        return op_period

    @classmethod
    def from_operating_hours(cls, _op_hours=24, _op_frac=1.0, _name=""):
        # type: (float, float, str) -> DailyOperationPeriod
        op_period = cls()

        op_period.name = _name
        op_period.start_hour = 12.0 - (_op_hours / 2.0)
        op_period.end_hour = 12.0 + (_op_hours / 2.0)
        op_period.operation_fraction = _op_frac

        return op_period

    @property
    def operation_hours(self):
        # type: () -> float
        return self.end_hour - self.start_hour

    @property
    def weighted_operation_hours(self):
        # type: () -> float
        return self.operation_hours * self.operation_fraction

    def to_dict(self):
        # type: () -> dict[str, float]
        d = {}
        d["name"] = self.name
        d["start_hour"] = self.start_hour
        d["end_hour"] = self.end_hour
        d["operation_fraction"] = self.operation_fraction
        return d

    @classmethod
    def from_dict(cls, _dict):
        # type: (dict[str, float]) -> DailyOperationPeriod
        new_op_period = cls()
        new_op_period.name = _dict["name"]
        new_op_period.start_hour = _dict["start_hour"]
        new_op_period.end_hour = _dict["end_hour"]
        new_op_period.operation_fraction = _dict["operation_fraction"]
        return new_op_period

    def ToString(self):
        """Overwrite .NET ToString."""
        return self.__repr__()

    def __repr__(self):
        """Properties representation."""
        return "{}(start_hour={}, end_hour={}, _operation_hours={}, _operation_fraction={})".format(
            self.__class__.__name__,
            self.start_hour,
            self.end_hour,
            self.operation_hours,
            self.operation_fraction,
        )


class DailyOperatingPeriodCollection(object):
    """A collection of DailyOperatingPeriods. Ventilation may have more than one period."""

    def __init__(self):
        self._collection = []

    def add_period_to_collection(self, _period):
        # type: (DailyOperationPeriod) -> None
        self._collection.append(_period)

    @property
    def fist_period(self):
        # type: () -> Optional[DailyOperationPeriod]
        """Returns the first Operating Period in the collection, or None if collection is empty."""
        if not self._collection:
            return None
        else:
            return self._collection[0]

    def __nonzero__(self):
        # type: () -> bool
        return bool(self._collection)

    def __bool__(self):
        return self.__nonzero__()

    def __iter__(self):
        # type: () -> Generator[DailyOperationPeriod, None, None]
        for _ in self._collection:
            yield _

    def to_dict(self):
        # type: () -> dict[str, Any]
        d = {}

        periods = []
        for op_period in self._collection:
            periods.append(op_period.to_dict())
        d["collection"] = periods

        return d

    @classmethod
    def from_dict(cls, _input_dict):
        # type: (dict[str, Any]) -> DailyOperatingPeriodCollection
        new_obj = DailyOperatingPeriodCollection()

        for period_dict in _input_dict["collection"]:
            new_obj.add_period_to_collection(DailyOperationPeriod.from_dict(period_dict))

        return new_obj

    def __str__(self):
        return "{}({} items)".format(self.__class__.__name__, len(self._collection))

    def ToString(self):
        return str(self)


class ScheduleRulesetPhProperties(object):
    """Honeybee-Energy-PH ScheduleRulesetPhProperties for managing PH-style schedule data."""

    def __init__(self, _host):
        self._host = _host  # type: Any
        self.id_num = 0
        self.operating_weeks_year = 52.1429
        self.operating_days_wk = 7.0
        self.daily_operating_periods = DailyOperatingPeriodCollection()

    @classmethod
    def from_days_per_week(cls, _days_per_wk, _wks_per_year, _host):
        # type: (float, float, Any) -> ScheduleRulesetPhProperties
        """Construct a new Schedule based on day-per-week usage data"""

        prop_obj = cls(_host)

        prop_obj.operating_days_wk = _days_per_wk
        prop_obj.operating_weeks_year = _wks_per_year

        return prop_obj

    @classmethod
    def from_days_per_year(cls, _days_per_year, _host):
        # type: (float, Any) -> ScheduleRulesetPhProperties
        """Construct a new Schedule based on day-per-year usage data."""

        prop_obj = cls(_host)

        prop_obj.operating_days_wk = (_days_per_year / 365.0) * 7.0
        prop_obj.operating_weeks_year = 52.1429

        return prop_obj

    @property
    def operating_days_year(self):
        # type: () -> float
        """The Schedule's total operating days per year."""
        return self.operating_weeks_year * self.operating_days_wk

    @property
    def host(self):
        return self._host

    @property
    def annual_average_operating_fraction(self):
        # type: () -> float
        """The annual average operating (utilization) fraction (0-1.0)."""

        wtd_total = 0.0
        for op_period in self.daily_operating_periods:
            wtd_total += op_period.weighted_operation_hours * self.operating_days_year

        annual_operating_hours = self.operating_days_year * 24.0
        try:
            wtd_annual_avg = wtd_total / annual_operating_hours
        except ZeroDivisionError:
            wtd_annual_avg = 0.0

        return wtd_annual_avg

    def validate_operating_period_hours(self, _total_period_hours=24.0):
        # type: (float) -> str | None
        """Returns a warning if the total daily operating period hours do not equal the specified _total_period_hours."""

        total_hours = 0
        for op_period in self.daily_operating_periods:
            total_hours += op_period.operation_hours

        if abs(_total_period_hours - total_hours) > 0.001:
            return "Error: Total Operating Hours={}, not {}?".format(total_hours, _total_period_hours)
        else:
            return None

    @property
    def first_operating_period(self):
        # type: () -> Optional[DailyOperationPeriod]
        return self.daily_operating_periods.fist_period

    def to_dict(self, abridged=False):
        # type: (bool) -> dict[str, Any]
        d = {}
        if abridged:
            d["type"] = "ScheduleRulesetPhPropertiesAbridged"
        else:
            d["type"] = "ScheduleRulesetPhProperties"

        d["id_num"] = self.id_num
        d["operating_weeks_year"] = self.operating_weeks_year
        d["operating_days_wk"] = self.operating_days_wk
        d["operating_periods"] = self.daily_operating_periods.to_dict()

        return {"ph": d}

    @classmethod
    def from_dict(cls, _dict, host):
        # type: (dict, Any) -> ScheduleRulesetPhProperties
        valid_types = (
            "ScheduleRulesetPhProperties",
            "ScheduleRulesetPhPropertiesAbridged",
        )
        if _dict["type"] not in valid_types:
            raise ScheduleRulesetPhProperties_FromDictError(valid_types, _dict["type"])

        new_prop = cls(host)
        new_prop.id_num = _dict["id_num"]
        new_prop.operating_weeks_year = _dict["operating_weeks_year"]
        new_prop.operating_days_wk = _dict["operating_days_wk"]
        new_prop.daily_operating_periods = DailyOperatingPeriodCollection.from_dict(_dict.get("operating_periods", {}))
        return new_prop

    def apply_properties_from_dict(self, abridged_data):
        return

    def ToString(self):
        """Overwrite .NET ToString."""
        return str(self)

    def __repr__(self):
        return str(self)

    def __str__(self):
        """Properties representation."""
        return "{}(_host={})".format(self.__class__.__name__, self.host)
