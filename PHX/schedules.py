# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Schedule / Utilization Pattern classes."""

from __future__ import annotations
from dataclasses import dataclass, field

from honeybee.room import Room as HB_Room
from honeybee_ph_utils import schedules


@dataclass
class UtilPat_Vent_Collection:
    patterns: dict = field(default_factory=dict)

    def add_new_util_pattern(self, _util_pattern: UtilizationPatternVent) -> None:
        """Create and add a new Utilization Pattern based on the _hb_room input

        Arguments:
        ----------
            * _util_pattern (UtilizationPatternVent): The Utilization patten to add
                to the collection.

        Returns:
        --------
            * None
        """
        self.patterns[_util_pattern.identifier] = _util_pattern

    def key_is_in_collection(self, _id) -> bool:
        """Check if the id is in the collection."""
        return _id in self.patterns.keys()

    def __len__(self):
        return len(self.patterns.keys())

    def __iter__(self):
        for v in self.patterns.values():
            yield v


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
    _count = 0
    name: str = '__unamed_vent_pattern__'
    id_num: int = 0
    identifier = None
    operating_days: int = 7
    operating_weeks: int = 52
    operating_periods: Vent_UtilPeriods = field(default_factory=Vent_UtilPeriods)

    def __new__(cls, *args, **kwargs):
        cls._count += 1
        return super(UtilizationPatternVent, cls).__new__(cls, *args, **kwargs)

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

    @classmethod
    def from_hb_room(cls, _hb_room: HB_Room) -> UtilizationPatternVent:
        new_util_pattern = cls()

        # --
        new_util_pattern.identifier = _hb_room.properties.energy.ventilation.identifier
        new_util_pattern.id_num = new_util_pattern._count
        new_util_pattern.name = _hb_room.properties.energy.ventilation.display_name

        # --
        wufi_sched = schedules.calc_four_part_vent_sched_values_from_hb_room(_hb_room)
        new_util_pattern.operating_periods.high.period_operating_hours = wufi_sched.high.period_speed
        new_util_pattern.operating_periods.high.period_operation_speed = wufi_sched.high.period_operating_hours
        new_util_pattern.operating_periods.standard.period_operating_hours = wufi_sched.standard.period_speed
        new_util_pattern.operating_periods.standard.period_operation_speed = wufi_sched.standard.period_operating_hours
        new_util_pattern.operating_periods.basic.period_operating_hours = wufi_sched.basic.period_speed
        new_util_pattern.operating_periods.basic.period_operation_speed = wufi_sched.basic.period_operating_hours
        new_util_pattern.operating_periods.minimum.period_operating_hours = wufi_sched.minimum.period_speed
        new_util_pattern.operating_periods.minimum.period_operation_speed = wufi_sched.minimum.period_operating_hours

        # -- Ensure that the hours add up to 24
        new_util_pattern.force_max_utilization_hours()

        return new_util_pattern
