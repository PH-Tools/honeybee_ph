import pytest

from honeybee_energy_ph.hvac.supportive_device import PhSupportiveDevice


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
