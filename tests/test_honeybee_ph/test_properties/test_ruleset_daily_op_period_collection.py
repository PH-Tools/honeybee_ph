from honeybee_energy_ph.properties import ruleset
import pytest


def test_empty_collection_dict_round_trip(
        op_period_collection_empty: ruleset.DailyOperatingPeriodCollection):
    d = op_period_collection_empty.to_dict()
    new_coll = ruleset.DailyOperatingPeriodCollection.from_dict(d)
    assert new_coll.to_dict() == d


def test_full_collection_dict_round_trip(
        op_period_collection_full: ruleset.DailyOperatingPeriodCollection):
    d = op_period_collection_full.to_dict()
    new_coll = ruleset.DailyOperatingPeriodCollection.from_dict(d)
    assert new_coll.to_dict() == d


def test_collection_bool_empty(
        op_period_collection_empty: ruleset.DailyOperatingPeriodCollection):
    if op_period_collection_empty:
        assert False
    else:
        assert True


def test_collection_bool_full(
        op_period_collection_full: ruleset.DailyOperatingPeriodCollection):
    if op_period_collection_full:
        assert True
    else:
        assert False


def test_collection_iteration(
        op_period_collection_full: ruleset.DailyOperatingPeriodCollection):

    flag = 0
    for daily_period in op_period_collection_full:
        flag += 1

    assert flag != 0
