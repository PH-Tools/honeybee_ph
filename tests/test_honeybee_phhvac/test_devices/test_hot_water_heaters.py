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


def test_dict_roundtrip_PhHvacHotWaterHeaterHeatPump_Inside():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Inside()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Inside.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()

    # -- customize values
    s1.annual_COP = 3.32
    s1.total_system_perf_ratio = 1_000
    s1.annual_energy_factor = 0.9
    d2 = s1.to_dict()

    s3 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Inside.from_dict(d2)
    assert s3.annual_COP == 3.32
    assert s3.total_system_perf_ratio == 1_000
    assert s3.annual_energy_factor == 0.9
    assert s3.to_dict() == d2


def test_dict_roundtrip_PhHvacHotWaterHeaterHeatPump_Annual():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Annual()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Annual.from_dict(d)
    assert s2.annual_COP == None
    assert s2.total_system_perf_ratio == None
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()

    # -- customize values
    s1.annual_COP = 3.32
    s1.total_system_perf_ratio = 1_000
    d2 = s1.to_dict()

    s3 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Annual.from_dict(d2)
    assert s3.annual_COP == 3.32
    assert s3.total_system_perf_ratio == 1_000
    assert s3.to_dict() == d2


def test_dict_roundtrip_PhHvacHotWaterHeaterHeatPump_Monthly():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Monthly()
    d = s1.to_dict()

    s2 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Monthly.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()

    # -- customize values
    s1.COP_1 = 4.56
    s1.ambient_temp_1 = 14.5
    s1.COP_2 = 3.21
    s1.ambient_temp_2 = 24.5
    d2 = s1.to_dict()

    s3 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Monthly.from_dict(d2)
    assert s3.COP_1 == 4.56
    assert s3.ambient_temp_1 == 14.5
    assert s3.COP_2 == 3.21
    assert s3.ambient_temp_2 == 24.5
    assert s3.to_dict() == d2


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


def test_hw_builder_PhHvacHotWaterHeaterHeatPump_Inside():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Inside()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()
    assert type(s1) == type(s2)


def test_hw_builder_PhHvacHotWaterHeaterHeatPump_Annual():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Annual()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()
    assert type(s1) == type(s2)


def test_hw_builder_PhHvacHotWaterHeaterHeatPump_Monthly():
    s1 = hot_water_devices.PhHvacHotWaterHeaterHeatPump_Monthly()
    d1 = s1.to_dict()
    s2 = hot_water_devices.PhHvacHotWaterHeaterBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()
    assert type(s1) == type(s2)
