import pytest

from honeybee_energy_ph.hvac.renewable_devices import (
    PhPhotovoltaicDevice,
    PhRenewableEnergyDevice,
    PhRenewableEnergyDeviceBuilder,
)


def test_PhRenewableEnergyDevice_raises_exception():
    with pytest.raises(Exception):
        PhRenewableEnergyDevice()


def test_PhPhotovoltaicDevice_raises_exception():
    with pytest.raises(Exception):
        PhPhotovoltaicDevice()


def test_PhRenewableEnergyDeviceBuilder_raises_exception():
    with pytest.raises(Exception):
        PhRenewableEnergyDeviceBuilder()
