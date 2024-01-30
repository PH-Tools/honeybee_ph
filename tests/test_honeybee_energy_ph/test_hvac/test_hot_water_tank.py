from honeybee_energy_ph.hvac.hot_water import PhSHWTank


def test_dict_roundtrip_PhSHWTank():
    s1 = PhSHWTank()
    d = s1.to_dict()

    s2 = PhSHWTank.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_duplicate_PhSHWTank():
    t1 = PhSHWTank()
    t2 = t1.duplicate()
    assert t1 == t2
    assert t1.to_dict() == t2.to_dict()
    assert t1 is not t2
    assert t1.user_data is not t2.user_data
    assert t1.user_data == t2.user_data
