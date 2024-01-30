from honeybee_energy_ph.hvac import ventilation


def test_default_vent_system():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.PhVentilationSystem.from_dict(d)
    assert o2.to_dict() == d


def test_duplicate_default_vent_system():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ToString()

    o2 = o1.duplicate()
    assert o2.to_dict() == o1.to_dict()


def test_vent_system_with_ventilator():
    o1 = ventilation.PhVentilationSystem()
    v1 = ventilation.Ventilator()
    o1.ventilation_unit = v1
    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.PhVentilationSystem.from_dict(d)
    assert o2.to_dict() == d


def test_duplicate_vent_system_with_ventilator():
    o1 = ventilation.PhVentilationSystem()
    v1 = ventilation.Ventilator()
    o1.ventilation_unit = v1
    assert o1.ToString()

    o2 = o1.duplicate()
    assert o2.to_dict() == o1.to_dict()


def test_add_none_ventilator():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ventilation_unit == None

    o1.ventilation_unit = None
    assert o1.ventilation_unit == None
