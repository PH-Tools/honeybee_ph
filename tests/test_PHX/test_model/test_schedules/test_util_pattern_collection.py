from PHX.model import schedules


def test_empty_util_collection(reset_class_counters):
    coll = schedules.UtilizationPatternVentCollection()

    assert not coll
    assert not coll.patterns


def test_add_no_pattern_to_collection(reset_class_counters):
    coll = schedules.UtilizationPatternVentCollection()
    coll.add_new_util_pattern(None)
    assert not coll
    assert not coll.patterns


def test_add_single_pattern_in_collection(reset_class_counters):
    coll = schedules.UtilizationPatternVentCollection()
    pat_1 = schedules.UtilizationPatternVent(
        operating_periods=schedules.Vent_UtilPeriods(
            high=schedules.Vent_OperatingPeriod(24, 0.0),
            standard=schedules.Vent_OperatingPeriod(0, 0.0),
            basic=schedules.Vent_OperatingPeriod(0, 0.0),
            minimum=schedules.Vent_OperatingPeriod(0, 0.0),
        )
    )
    coll.add_new_util_pattern(pat_1)

    assert len(coll) == 1
    assert pat_1.identifier in coll.patterns.keys()
    assert coll.key_is_in_collection(pat_1.identifier)

    for pat in coll:
        assert isinstance(pat, schedules.UtilizationPatternVent)


def test_add_multiple_pattern_in_collection(reset_class_counters):
    coll = schedules.UtilizationPatternVentCollection()
    pat_1 = schedules.UtilizationPatternVent(
        operating_periods=schedules.Vent_UtilPeriods(
            high=schedules.Vent_OperatingPeriod(24, 0.0),
            standard=schedules.Vent_OperatingPeriod(0, 0.0),
            basic=schedules.Vent_OperatingPeriod(0, 0.0),
            minimum=schedules.Vent_OperatingPeriod(0, 0.0),
        )
    )
    pat_2 = schedules.UtilizationPatternVent(
        operating_periods=schedules.Vent_UtilPeriods(
            high=schedules.Vent_OperatingPeriod(24, 0.0),
            standard=schedules.Vent_OperatingPeriod(0, 0.0),
            basic=schedules.Vent_OperatingPeriod(0, 0.0),
            minimum=schedules.Vent_OperatingPeriod(0, 0.0),
        )
    )
    coll.add_new_util_pattern(pat_1)
    coll.add_new_util_pattern(pat_2)

    assert len(coll) == 2
    assert pat_1.identifier in coll.patterns.keys()
    assert pat_2.identifier in coll.patterns.keys()
    assert coll.key_is_in_collection(pat_1.identifier)
    assert coll.key_is_in_collection(pat_2.identifier)

    for pat in coll:
        assert isinstance(pat, schedules.UtilizationPatternVent)
