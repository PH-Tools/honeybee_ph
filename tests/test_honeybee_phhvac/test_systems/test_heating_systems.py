from honeybee_phhvac import fuels, heating


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

    # -- User data
    s3.user_data["test_key"] = "test_value"
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)

    assert "test_key" in s4.user_data
    assert s4.to_dict() == s3.to_dict()

    # -- percent_covered
    s3.percent_coverage = 0.5
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)
    assert s4.percent_coverage == 0.5


def test_duplicate_direct_electric():
    s1 = heating.PhHeatingDirectElectric()
    s2 = s1.duplicate()
    assert s1.to_dict() == s2.to_dict()
    assert id(s1) != id(s2)

    s2.percent_coverage = 0.5
    s3 = s2.duplicate()
    assert s2.to_dict() == s3.to_dict()
    assert id(s2) != id(s3)


def test_dict_roundtrip_fossil_boiler():
    s1 = heating.PhHeatingFossilBoiler()
    d = s1.to_dict()

    s2 = heating.PhHeatingFossilBoiler.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d

    # -- User data
    s3.user_data["test_key"] = "test_value"
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)

    assert "test_key" in s4.user_data
    assert s4.to_dict() == s3.to_dict()

    # -- percent_covered
    s3.percent_coverage = 0.5
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)
    assert s4.percent_coverage == 0.5


def test_duplicate_fossil_boiler():
    s1 = heating.PhHeatingFossilBoiler()
    s1.display_name = "A Test"
    s1.fuel = fuels.OIL
    s2 = s1.duplicate()
    assert s1.to_dict() == s2.to_dict()
    assert id(s1) != id(s2)

    # -- percent_covered
    s2.percent_coverage = 0.5
    s3 = s2.duplicate()
    assert s2.to_dict() == s3.to_dict()
    assert id(s2) != id(s3)


def test_dict_roundtrip_wood_boiler():
    s1 = heating.PhHeatingWoodBoiler()
    d = s1.to_dict()

    s2 = heating.PhHeatingWoodBoiler.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d

    # -- User data
    s3.user_data["test_key"] = "test_value"
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)

    assert "test_key" in s4.user_data
    assert s4.to_dict() == s3.to_dict()

    # -- percent_covered
    s3.percent_coverage = 0.5
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)
    assert s4.percent_coverage == 0.5


def test_duplicate_wood_boiler():
    s1 = heating.PhHeatingWoodBoiler()
    s1.display_name = "A Test"
    s1.fuel = fuels.WOOD_PELLET
    s1.in_conditioned_space = False
    s2 = s1.duplicate()
    assert s1.to_dict() == s2.to_dict()
    assert id(s1) != id(s2)

    # -- percent_covered
    s2.percent_coverage = 0.5
    s3 = s2.duplicate()
    assert s2.to_dict() == s3.to_dict()
    assert id(s2) != id(s3)


def test_dict_roundtrip_district_heat():
    s1 = heating.PhHeatingDistrict()
    s1.fuel = fuels.NATURAL_GAS
    d = s1.to_dict()

    s2 = heating.PhHeatingDistrict.from_dict(d)
    assert s2.to_dict() == d

    s3 = heating.PhHeatingSystemBuilder.from_dict(d)
    assert s3.to_dict() == d

    # -- User data
    s3.user_data["test_key"] = "test_value"
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)

    assert "test_key" in s4.user_data
    assert s4.to_dict() == s3.to_dict()

    # -- percent_covered
    s3.percent_coverage = 0.5
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)
    assert s4.percent_coverage == 0.5


def test_duplicate_district_heat():
    s1 = heating.PhHeatingDistrict()
    s1.display_name = "A Test"
    s1.fuel = fuels.NATURAL_GAS
    s2 = s1.duplicate()
    assert s1.to_dict() == s2.to_dict()
    assert id(s1) != id(s2)

    # -- percent_covered
    s2.percent_coverage = 0.5
    s3 = s2.duplicate()
    assert s2.to_dict() == s3.to_dict()
    assert id(s2) != id(s3)
