import pytest

from honeybee_energy_ph.properties import ruleset

# -- Daily Operating Periods


@pytest.fixture
def op_period_default() -> ruleset.DailyOperationPeriod:
    op_period = ruleset.DailyOperationPeriod()
    return op_period


@pytest.fixture
def op_period_1_hour_factor_1() -> ruleset.DailyOperationPeriod:
    op_period = ruleset.DailyOperationPeriod()
    op_period.start_hour = 0
    op_period.end_hour = 1
    op_period.operation_fraction = 1.0
    return op_period


@pytest.fixture
def op_period_1_hour_factor_0() -> ruleset.DailyOperationPeriod:
    op_period = ruleset.DailyOperationPeriod()
    op_period.start_hour = 0
    op_period.end_hour = 1
    op_period.operation_fraction = 0.0
    return op_period


@pytest.fixture
def op_period_23_hour_factor_1() -> ruleset.DailyOperationPeriod:
    op_period = ruleset.DailyOperationPeriod()
    op_period.start_hour = 0
    op_period.end_hour = 23
    op_period.operation_fraction = 1.0
    return op_period


@pytest.fixture
def op_period_12_hour_factor_0_5() -> ruleset.DailyOperationPeriod:
    op_period = ruleset.DailyOperationPeriod()
    op_period.start_hour = 0
    op_period.end_hour = 12
    op_period.operation_fraction = 0.5
    return op_period


@pytest.fixture
def op_period_12_hour_factor_1() -> ruleset.DailyOperationPeriod:
    op_period = ruleset.DailyOperationPeriod()
    op_period.start_hour = 0
    op_period.end_hour = 12
    op_period.operation_fraction = 1.0
    return op_period


# -- Daily Operating Period Collections


@pytest.fixture
def op_period_collection_empty() -> ruleset.DailyOperatingPeriodCollection:
    return ruleset.DailyOperatingPeriodCollection()


@pytest.fixture
def op_period_collection_full() -> ruleset.DailyOperatingPeriodCollection:
    coll = ruleset.DailyOperatingPeriodCollection()

    coll.add_period_to_collection(ruleset.DailyOperationPeriod.from_start_end_hours(0, 1, 1, "period 1"))
    coll.add_period_to_collection(ruleset.DailyOperationPeriod.from_start_end_hours(0, 23, 1, "period 2"))

    return coll
