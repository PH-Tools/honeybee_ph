import pytest

from honeybee_energy_ph.properties import ruleset


def test_default_dict_round_trip(op_period_default):
    d = op_period_default.to_dict()

    new_obj = ruleset.DailyOperationPeriod.from_dict(d)
    assert new_obj.to_dict() == d


def test_detailed_dict_round_trip(op_period_1_hour_factor_0):
    d = op_period_1_hour_factor_0.to_dict()

    new_obj = ruleset.DailyOperationPeriod.from_dict(d)
    assert new_obj.to_dict() == d


def test_make_from_start_end():
    op_period = ruleset.DailyOperationPeriod.from_start_end_hours(
        _start_hr=10, _end_hr=18, _op_frac=0.75, _name="test"
    )
    assert op_period.operation_hours == 8
    assert op_period.weighted_operation_hours == 6
