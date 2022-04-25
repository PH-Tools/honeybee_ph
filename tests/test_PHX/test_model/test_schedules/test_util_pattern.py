from PHX.model import schedules


def test_UtilizationPatternVent_empty(reset_class_counters):
    obj_1 = schedules.UtilizationPatternVent()
    assert obj_1.id_num == 1
    obj_2 = schedules.UtilizationPatternVent()
    assert obj_2.id_num == 2
    assert obj_1 != obj_2


def test_UtilizationPatternVent_empty_force_24(reset_class_counters):
    obj = schedules.UtilizationPatternVent()
    obj.force_max_utilization_hours()
    assert obj.operating_periods.high.period_operating_hours == 24


def test_UtilizationPatternVent_custom(reset_class_counters):
    obj = schedules.UtilizationPatternVent(
        operating_periods=schedules.Vent_UtilPeriods(
            high=schedules.Vent_OperatingPeriod(10, 0.98),
            standard=schedules.Vent_OperatingPeriod(10, 0.77),
            basic=schedules.Vent_OperatingPeriod(2, 0.50),
            minimum=schedules.Vent_OperatingPeriod(2, 0.24),
        )
    )
    obj.force_max_utilization_hours()
    assert obj
    assert obj.operating_periods.high.period_operating_hours == 10


def test_UtilizationPatternVent_over_24_force_24(reset_class_counters):
    obj = schedules.UtilizationPatternVent(
        operating_periods=schedules.Vent_UtilPeriods(
            high=schedules.Vent_OperatingPeriod(25, 0.98),  # <-- over 24
            standard=schedules.Vent_OperatingPeriod(0, 0.0),
            basic=schedules.Vent_OperatingPeriod(0, 0.0),
            minimum=schedules.Vent_OperatingPeriod(0, 0.0),
        )
    )
    obj.force_max_utilization_hours()
    assert obj
    assert obj.operating_periods.high.period_operating_hours == 24


def test_UtilizationPatternVent_different_hash(reset_class_counters):
    obj_1 = schedules.UtilizationPatternVent()
    obj_2 = schedules.UtilizationPatternVent()

    assert hash(obj_1) != hash(obj_2)

    # -- try adding to a set
    s_1 = set()
    s_1.add(obj_1)
    s_1.add(obj_2)
    assert len(s_1) == 2
