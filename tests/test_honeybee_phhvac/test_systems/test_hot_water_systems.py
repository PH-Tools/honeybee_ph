from honeybee_phhvac import hot_water_devices


def test_base_class():
    sys = hot_water_devices.PhHvacHotWaterHeater()
    assert sys.ToString()


# -----------------------------------------------------------------------------


def test_dict_roundtrip_PhHvacHotWaterHeaterElectric():
    s1 = hot_water_devices.PhHvacHotWaterHeaterElectric()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterElectric.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhHvacHotWaterHeaterBoiler():
    s1 = hot_water_devices.PhHvacHotWaterHeaterBoiler()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterBoiler.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhHvacHotWaterHeaterBoilerWood():
    s1 = hot_water_devices.PhHvacHotWaterHeaterBoilerWood()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterBoilerWood.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhHvacHotWaterHeaterDistrict():
    s1 = hot_water_devices.PhHvacHotWaterHeaterDistrict()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterDistrict.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


def test_dict_roundtrip_PhHvacHotWaterHeaterHeatPump():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterHeatPump.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


# -----------------------------------------------------------------------------


def test_hw_builder_PhHvacHotWaterHeaterElectric():
    s1 = hot_water_devices.PhHvacHotWaterHeaterElectric()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhHvacHotWaterHeaterBoiler():
    s1 = hot_water_devices.PhHvacHotWaterHeaterBoiler()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhHvacHotWaterHeaterBoilerWood():
    s1 = hot_water_devices.PhHvacHotWaterHeaterBoilerWood()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhHvacHotWaterHeaterDistrict():
    s1 = hot_water_devices.PhHvacHotWaterHeaterDistrict()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()


def test_hw_builder_PhHvacHotWaterHeaterHeatPump():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()
