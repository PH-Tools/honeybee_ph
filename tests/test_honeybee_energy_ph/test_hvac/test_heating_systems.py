from honeybee_energy_ph.hvac import heating


def test_base_class():
    sys = heating.PhHeatingSystem()
    assert sys.ToString()


# -----------------------------------------------------------------------------


def test_dict_roundtrip_direct_electric():
    s1 = heating.PhHeatingDirectElectric()
    d = s1.to_dict()

    s2 = heating.PhHeatingDirectElectric.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_fossil_boiler():
    s1 = heating.PhHeatingFossilBoiler()
    d = s1.to_dict()

    s2 = heating.PhHeatingFossilBoiler.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_wood_boiler():
    s1 = heating.PhHeatingWoodBoiler()
    d = s1.to_dict()

    s2 = heating.PhHeatingWoodBoiler.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_heat_pump_annual():
    s1 = heating.PhHeatingHeatPumpAnnual()
    d = s1.to_dict()

    s2 = heating.PhHeatingHeatPumpAnnual.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d


def test_dict_roundtrip_heat_pump_monthly():
    s1 = heating.PhHeatingHeatPumpRatedMonthly()
    d = s1.to_dict()

    s2 = heating.PhHeatingHeatPumpRatedMonthly.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d
