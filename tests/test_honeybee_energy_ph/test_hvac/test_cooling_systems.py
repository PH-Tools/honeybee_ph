from honeybee_energy_ph.hvac import cooling


def test_base_class():
    sys = cooling.PhCoolingSystem()
    assert sys.ToString()


# -----------------------------------------------------------------------------


def test_dict_roundtrip_recirculation():
    s1 = cooling.PhCoolingRecirculation()
    d = s1.to_dict()

    s2 = cooling.PhCoolingRecirculation.from_dict(d)
    assert s2.to_dict() == d

    s3 = cooling.PhCoolingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_dehumidification():
    s1 = cooling.PhCoolingDehumidification()
    d = s1.to_dict()

    s2 = cooling.PhCoolingDehumidification.from_dict(d)
    assert s2.to_dict() == d

    s3 = cooling.PhCoolingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_panel():
    s1 = cooling.PhCoolingPanel()
    d = s1.to_dict()

    s2 = cooling.PhCoolingPanel.from_dict(d)
    assert s2.to_dict() == d

    s3 = cooling.PhCoolingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_ventilation():
    s1 = cooling.PhCoolingVentilation()
    d = s1.to_dict()

    s2 = cooling.PhCoolingVentilation.from_dict(d)
    assert s2.to_dict() == d

    s3 = cooling.PhCoolingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d
