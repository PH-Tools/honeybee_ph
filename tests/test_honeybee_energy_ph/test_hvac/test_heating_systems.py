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

    # -- User data
    s3.user_data["test_key"] = "test_value"
    d1 = s3.to_dict()
    s4 = heating.PhHeatingSystemBuilder.from_dict(d1)
    
    assert "test_key" in s4.user_data
    assert s4.to_dict() == s3.to_dict()

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
