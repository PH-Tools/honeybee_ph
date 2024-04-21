import pytest

from honeybee_energy_ph.properties.hvac.allair import AllAirSystemPhProperties
from honeybee_energy_ph.properties.hvac.doas import DOASSystemPhProperties
from honeybee_energy_ph.properties.hvac.heatcool import HeatCoolSystemPhProperties
from honeybee_energy_ph.properties.hvac.idealair import IdealAirSystemPhProperties


def test_all_air_system_raises_exception():
    with pytest.raises(Exception):
        AllAirSystemPhProperties()


def test_doas_system_raises_exception():
    with pytest.raises(Exception):
        DOASSystemPhProperties()


def test_heat_cool_system_raises_exception():
    with pytest.raises(Exception):
        HeatCoolSystemPhProperties()


def test_ideal_air_system_raises_exception():
    with pytest.raises(Exception):
        IdealAirSystemPhProperties()
