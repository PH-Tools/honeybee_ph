from honeybee_energy_ph.properties import ruleset
import pytest


def test_empty_daily_periods():
    prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    assert int(prop.operating_days_year) == 365
    assert prop.annual_average_operating_fraction == 0


def test_empty_daily_periods_dict_roundtrip():
    prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    d = prop.to_dict()
    new_prop = ruleset.ScheduleRulesetPhProperties.from_dict(d["ph"], host=None)
    assert new_prop.to_dict() == d


def test_full_daily_periods_dict_roundtrip(op_period_collection_full):
    prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    prop.daily_operating_periods = op_period_collection_full
    d = prop.to_dict()
    new_prop = ruleset.ScheduleRulesetPhProperties.from_dict(d["ph"], host=None)
    assert new_prop.to_dict() == d


# -- Test Annual Utilization Factors....


def test_annual_util_factor_1(
    op_period_1_hour_factor_1: ruleset.DailyOperationPeriod,
    op_period_23_hour_factor_1: ruleset.DailyOperationPeriod,
):
    prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    prop.daily_operating_periods.add_period_to_collection(op_period_1_hour_factor_1)
    prop.daily_operating_periods.add_period_to_collection(op_period_23_hour_factor_1)
    assert prop.annual_average_operating_fraction == 1.0


def test_annual_util_factor_2(op_period_12_hour_factor_0_5: ruleset.DailyOperationPeriod):
    prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    prop.daily_operating_periods.add_period_to_collection(op_period_12_hour_factor_0_5)
    prop.daily_operating_periods.add_period_to_collection(op_period_12_hour_factor_0_5)
    assert prop.annual_average_operating_fraction == 0.5


def test_annual_util_factor_3(
    op_period_12_hour_factor_0_5: ruleset.DailyOperationPeriod,
    op_period_12_hour_factor_1: ruleset.DailyOperationPeriod,
):
    prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    prop.daily_operating_periods.add_period_to_collection(op_period_12_hour_factor_0_5)
    prop.daily_operating_periods.add_period_to_collection(op_period_12_hour_factor_1)
    assert prop.annual_average_operating_fraction == 0.75
