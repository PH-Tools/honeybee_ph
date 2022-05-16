# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Schedule / Utilization Pattern classes."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import ClassVar, Union, Dict
import uuid

# TODO: Refactor names: these are not only for Vent...


@dataclass
class Vent_OperatingPeriod:
    period_operating_hours: float = 0.0  # hours/period
    period_operation_speed: float = 0.0  # % of peak design airflow


@dataclass
class Vent_UtilPeriods:
    high: Vent_OperatingPeriod = field(default_factory=Vent_OperatingPeriod)
    standard: Vent_OperatingPeriod = field(default_factory=Vent_OperatingPeriod)
    basic: Vent_OperatingPeriod = field(default_factory=Vent_OperatingPeriod)
    minimum: Vent_OperatingPeriod = field(default_factory=Vent_OperatingPeriod)


@dataclass
class UtilizationPatternVent:
    _count: ClassVar[int] = 0
    id_num: int = field(init=False, default=0)
    name: str = '__unamed_vent_pattern__'
    identifier: Union[uuid.UUID, str] = field(default_factory=uuid.uuid4)
    operating_days: int = 7
    operating_weeks: int = 52
    operating_periods: Vent_UtilPeriods = field(default_factory=Vent_UtilPeriods)
    holiday_days: int = 0

    def __post_init__(self) -> None:
        self.__class__._count += 1
        self.id_num = self.__class__._count

    def force_max_utilization_hours(self, _max_hours: float = 24.0, _tol: int = 2) -> None:
        """Ensure that the total utilization hours never exceed target (default=24).
        Will adjust the minimum daily_op_sched as needed.
        """

        b = round(self.operating_periods.standard.period_operating_hours, _tol)
        c = round(self.operating_periods.basic.period_operating_hours, _tol)
        a = round(self.operating_periods.minimum.period_operating_hours, _tol)
        total = a + b + c
        remainder = round(_max_hours - total, _tol)
        self.operating_periods.high.period_operating_hours = remainder

    def __hash__(self):
        return hash(self.identifier)


@dataclass
class UtilizationPatternVentCollection:
    patterns: Dict[str, UtilizationPatternVent] = field(init=False, default_factory=dict)

    def add_new_util_pattern(self, _util_pattern: UtilizationPatternVent) -> None:
        """Add a new Utilization Pattern to the Collection.

        Arguments:
        ----------
            * _util_pattern (UtilizationPatternVent): The UtilizationPatternVent pattern to add
                to the collection.

        Returns:
        --------
            * None
        """
        if _util_pattern is None:
            return

        self.patterns[str(_util_pattern.identifier)] = _util_pattern

    def key_is_in_collection(self, _id) -> bool:
        """Check if the id is in the collection."""
        return _id in self.patterns.keys()

    def get_pattern_by_id_num(self, _id_num: int) -> UtilizationPatternVent:
        """Return a UtilizationPattern from the collection with an id-num matching the target."""
        for pattern in self.patterns.values():
            if pattern.id_num == _id_num:
                return pattern
        msg = f"Error: Cannot locate the UtilizationPattern with id-number: {_id_num}"
        raise Exception(msg)

    def __len__(self):
        return len(self.patterns.keys())

    def __iter__(self):
        for v in self.patterns.values():
            yield v

    def __bool__(self):
        return bool(self.patterns)
