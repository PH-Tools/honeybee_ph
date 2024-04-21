import pytest

from honeybee_energy_ph.hvac.supportive_device import PhSupportiveDevice


def test_PhSupportiveDevice_raises_exception():
    with pytest.raises(Exception):
        PhSupportiveDevice()
