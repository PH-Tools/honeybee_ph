from honeybee_phhvac import hot_water


def test_base_class():
    sys = hot_water.PhHotWaterHeater()
    assert sys.ToString()


# -----------------------------------------------------------------------------


def test_dict_roundtrip_PhSHWHeaterElectric():
    s1 = hot_water.PhSHWHeaterElectric()
    d = s1.to_dict()

    s2 = hot_water.PhSHWHeaterElectric.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhSHWHeaterBoiler():
    s1 = hot_water.PhSHWHeaterBoiler()
    d = s1.to_dict()

    s2 = hot_water.PhSHWHeaterBoiler.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhSHWHeaterBoilerWood():
    s1 = hot_water.PhSHWHeaterBoilerWood()
    d = s1.to_dict()

    s2 = hot_water.PhSHWHeaterBoilerWood.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhSHWHeaterDistrict():
    s1 = hot_water.PhSHWHeaterDistrict()
    d = s1.to_dict()

    s2 = hot_water.PhSHWHeaterDistrict.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhSHWHeaterHeatPump():
    s1 = hot_water.PhSHWHeaterHeatPump()
    d = s1.to_dict()

    s2 = hot_water.PhSHWHeaterHeatPump.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


# -----------------------------------------------------------------------------


def test_hw_builder_PhSHWHeaterElectric():
    s1 = hot_water.PhSHWHeaterElectric()
    d1 = s1.to_dict()
    s2 = hot_water.PhSHWHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhSHWHeaterBoiler():
    s1 = hot_water.PhSHWHeaterBoiler()
    d1 = s1.to_dict()
    s2 = hot_water.PhSHWHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhSHWHeaterBoilerWood():
    s1 = hot_water.PhSHWHeaterBoilerWood()
    d1 = s1.to_dict()
    s2 = hot_water.PhSHWHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhSHWHeaterDistrict():
    s1 = hot_water.PhSHWHeaterDistrict()
    d1 = s1.to_dict()
    s2 = hot_water.PhSHWHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhSHWHeaterHeatPump():
    s1 = hot_water.PhSHWHeaterHeatPump()
    d1 = s1.to_dict()
    s2 = hot_water.PhSHWHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()
