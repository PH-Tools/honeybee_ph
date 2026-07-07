from honeybee_phhvac.supportive_device import (
    IHG_USAGE_PROFILE_ALL_YEAR,
    IHG_USAGE_PROFILE_NONE,
    IHG_USAGE_PROFILE_WINTER,
    PhSupportiveDevice,
    default_ihg_usage_profile,
)


def test_PhSupportiveDevice_to_dict():
    device = PhSupportiveDevice()
    device.display_name = "Test Device"
    device.device_type = 20
    device.quantity = 2
    device.in_conditioned_space = False
    device.norm_energy_demand_W = 500
    device.annual_period_operation_khrs = 2000

    expected_dict = {
        "identifier": device.identifier,
        "device_class_name": "PhSupportiveDevice",
        "display_name": "Test Device",
        "device_type": 20,
        "quantity": 2,
        "in_conditioned_space": False,
        "norm_energy_demand_W": 500,
        "annual_period_operation_khrs": 2000,
        "ihg_utilization_factor": 1.0,
        "ihg_usage_profile": 1,  # device_type 20 is unlisted -> ALL_YEAR default
        "user_data": {},
    }

    assert device.to_dict() == expected_dict


def test_PhSupportiveDevice_from_dict():
    input_dict = {
        "identifier": "1234",
        "device_class_name": "PhSupportiveDevice",
        "display_name": "Test Device",
        "device_type": 20,
        "quantity": 2,
        "in_conditioned_space": False,
        "norm_energy_demand_W": 500,
        "annual_period_operation_khrs": 2000,
        "ihg_utilization_factor": 0.0,
        "user_data": {},
    }

    device = PhSupportiveDevice.from_dict(input_dict)

    assert device.identifier == "1234"
    assert device.display_name == "Test Device"
    assert device.device_type == 20
    assert device.quantity == 2
    assert device.in_conditioned_space == False
    assert device.norm_energy_demand_W == 500
    assert device.annual_period_operation_khrs == 2000
    assert device.ihg_utilization_factor == 0.0


def test_PhSupportiveDevice_str():
    device = PhSupportiveDevice()
    device.display_name = "Test Device"
    device.device_type = 20
    device.quantity = 2

    expected_str = "PhSupportiveDevice(display_name='Test Device', device_type=20, quantity=2)"

    assert str(device) == expected_str


def test_PhSupportiveDevice_dict_roundtrip():
    device = PhSupportiveDevice()
    device.display_name = "Test Device"
    device.device_type = 20
    device.quantity = 2
    device.in_conditioned_space = False
    device.norm_energy_demand_W = 500
    device.annual_period_operation_khrs = 2000

    new_device = PhSupportiveDevice.from_dict(device.to_dict())

    assert device == new_device


def test_PhSupportiveDevice_duplicate():
    device = PhSupportiveDevice()
    device.display_name = "Test Device"
    device.device_type = 20
    device.quantity = 2
    device.in_conditioned_space = False
    device.norm_energy_demand_W = 500
    device.annual_period_operation_khrs = 2000

    new_device = device.duplicate()

    assert device == new_device
    assert id(device) != id(new_device)


# -- IHG Utilization Factor Tests --


def test_PhSupportiveDevice_ihg_utilization_factor_default():
    device = PhSupportiveDevice()
    assert device.ihg_utilization_factor == 1.0


def test_PhSupportiveDevice_ihg_utilization_factor_to_dict():
    device = PhSupportiveDevice()
    device.ihg_utilization_factor = 0.0
    d = device.to_dict()
    assert d["ihg_utilization_factor"] == 0.0


def test_PhSupportiveDevice_ihg_utilization_factor_from_dict():
    input_dict = {
        "identifier": "1234",
        "device_class_name": "PhSupportiveDevice",
        "display_name": "Test Device",
        "device_type": 10,
        "quantity": 1,
        "in_conditioned_space": True,
        "norm_energy_demand_W": 1.0,
        "annual_period_operation_khrs": 8.760,
        "ihg_utilization_factor": 0.5,
        "user_data": {},
    }
    device = PhSupportiveDevice.from_dict(input_dict)
    assert device.ihg_utilization_factor == 0.5


def test_PhSupportiveDevice_ihg_utilization_factor_roundtrip():
    device = PhSupportiveDevice()
    device.ihg_utilization_factor = 0.3
    new_device = PhSupportiveDevice.from_dict(device.to_dict())
    assert new_device.ihg_utilization_factor == 0.3
    assert device == new_device


def test_PhSupportiveDevice_ihg_utilization_factor_duplicate():
    device = PhSupportiveDevice()
    device.ihg_utilization_factor = 0.7
    new_device = device.duplicate()
    assert new_device.ihg_utilization_factor == 0.7
    assert device == new_device
    assert id(device) != id(new_device)


def test_PhSupportiveDevice_ihg_utilization_factor_backwards_compat():
    """Old serialized data without ihg_utilization_factor should default to 1.0."""
    input_dict = {
        "identifier": "1234",
        "device_class_name": "PhSupportiveDevice",
        "display_name": "Test Device",
        "device_type": 10,
        "quantity": 1,
        "in_conditioned_space": True,
        "norm_energy_demand_W": 1.0,
        "annual_period_operation_khrs": 8.760,
        "user_data": {},
    }
    # No "ihg_utilization_factor" key in dict
    device = PhSupportiveDevice.from_dict(input_dict)
    assert device.ihg_utilization_factor == 1.0


# -- IHG Usage-Profile (season/block) Tests --


def test_PhSupportiveDevice_ihg_usage_profile_default_is_all_year():
    """Default device (device_type 10 / Other) is an all-year IHG contributor."""
    device = PhSupportiveDevice()
    assert device.ihg_usage_profile == IHG_USAGE_PROFILE_ALL_YEAR


def test_PhSupportiveDevice_device_type_setter_reseeds_profile():
    """Create-then-assign: setting device_type to a DHW pump re-seeds the profile to NONE."""
    device = PhSupportiveDevice()  # device_type 10 -> ALL_YEAR
    assert device.ihg_usage_profile == IHG_USAGE_PROFILE_ALL_YEAR
    device.device_type = 6  # DHW Circulation Pump
    assert device.ihg_usage_profile == IHG_USAGE_PROFILE_NONE
    assert device.to_dict()["ihg_usage_profile"] == IHG_USAGE_PROFILE_NONE


def test_PhSupportiveDevice_explicit_profile_survives_when_set_after_device_type():
    """An explicit profile set after device_type is preserved (real construction order)."""
    device = PhSupportiveDevice()
    device.device_type = 10
    device.ihg_usage_profile = IHG_USAGE_PROFILE_WINTER
    assert device.ihg_usage_profile == IHG_USAGE_PROFILE_WINTER


def test_default_ihg_usage_profile_mapping():
    """Each device_type maps to the PHPP block it belongs to; unlisted -> ALL_YEAR."""
    assert default_ihg_usage_profile(4) == IHG_USAGE_PROFILE_WINTER  # Heat Circulation Pump
    assert default_ihg_usage_profile(6) == IHG_USAGE_PROFILE_NONE  # DHW Circulation Pump
    assert default_ihg_usage_profile(7) == IHG_USAGE_PROFILE_NONE  # DHW Storage Load Pump
    assert default_ihg_usage_profile(10) == IHG_USAGE_PROFILE_ALL_YEAR  # Other / Custom
    assert default_ihg_usage_profile(999) == IHG_USAGE_PROFILE_ALL_YEAR  # unknown -> fallback


def test_PhSupportiveDevice_ihg_usage_profile_roundtrip():
    device = PhSupportiveDevice()
    device.ihg_usage_profile = IHG_USAGE_PROFILE_WINTER
    new_device = PhSupportiveDevice.from_dict(device.to_dict())
    assert new_device.ihg_usage_profile == IHG_USAGE_PROFILE_WINTER
    assert device == new_device


def test_PhSupportiveDevice_ihg_usage_profile_duplicate():
    device = PhSupportiveDevice()
    device.ihg_usage_profile = IHG_USAGE_PROFILE_WINTER
    new_device = device.duplicate()
    assert new_device.ihg_usage_profile == IHG_USAGE_PROFILE_WINTER
    assert device == new_device
    assert id(device) != id(new_device)


def test_PhSupportiveDevice_ihg_usage_profile_backwards_compat_dhw():
    """A legacy DHW-pump dict with no profile key must default to NONE, not into the balance."""
    input_dict = {
        "identifier": "1234",
        "device_class_name": "PhSupportiveDevice",
        "display_name": "DHW Circulation Pump",
        "device_type": 6,  # DHW Circulation Pump
        "quantity": 1,
        "in_conditioned_space": True,
        "norm_energy_demand_W": 1.0,
        "annual_period_operation_khrs": 8.760,
        "ihg_utilization_factor": 1.0,
        "user_data": {},
    }
    # No "ihg_usage_profile" key in dict -> derive from device_type
    device = PhSupportiveDevice.from_dict(input_dict)
    assert device.ihg_usage_profile == IHG_USAGE_PROFILE_NONE


def test_PhSupportiveDevice_ihg_usage_profile_backwards_compat_other():
    """A legacy 'Other' dict with no profile key defaults to ALL_YEAR."""
    input_dict = {
        "identifier": "1234",
        "device_class_name": "PhSupportiveDevice",
        "display_name": "Humidifier",
        "device_type": 10,  # Other / Custom
        "quantity": 1,
        "in_conditioned_space": True,
        "norm_energy_demand_W": 1.0,
        "annual_period_operation_khrs": 8.760,
        "ihg_utilization_factor": 1.0,
        "user_data": {},
    }
    device = PhSupportiveDevice.from_dict(input_dict)
    assert device.ihg_usage_profile == IHG_USAGE_PROFILE_ALL_YEAR
