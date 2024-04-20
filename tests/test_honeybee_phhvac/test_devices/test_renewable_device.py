from honeybee_phhvac.renewable_devices import (
    PhPhotovoltaicDevice,
    PhRenewableEnergyDevice,
    PhRenewableEnergyDeviceBuilder,
)


def test_base_class():
    sys = PhRenewableEnergyDevice()
    assert sys.ToString()


# -----------------------------------------------------------------------------


def test_dict_roundtrip_PhPhotovoltaicDevice():
    s1 = PhPhotovoltaicDevice()
    s1.array_size = 100
    s1.photovoltaic_renewable_energy = 50
    s1.utilization_factor = 0.5
    d = s1.to_dict()

    s2 = PhPhotovoltaicDevice.from_dict(d)
    assert s2.to_dict() == d

    # -- add user data
    s2.user_data["test_key"] = "test_value"
    assert "test_key" in s2.user_data
    assert "test_key" not in s1.user_data
    assert s1.to_dict() != s2.to_dict()


# -----------------------------------------------------------------------------


def test_device_builder_PhPhotovoltaicDevice():
    s1 = PhPhotovoltaicDevice()
    s1.array_size = 100
    s1.photovoltaic_renewable_energy = 50
    s1.utilization_factor = 0.5
    d1 = s1.to_dict()
    s2 = PhRenewableEnergyDeviceBuilder.from_dict(d1)
    assert s1.to_dict() == s2.to_dict()
