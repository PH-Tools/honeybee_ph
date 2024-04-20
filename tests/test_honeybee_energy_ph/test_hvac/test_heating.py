import pytest
from honeybee_energy_ph.hvac.heating import (
    PhHeatingDirectElectric,
    PhHeatingFossilBoiler,
    PhHeatingWoodBoiler,
    PhHeatingDistrict,
    PhHeatingSystemBuilder,
)


def test_ph_heating_direct_electric():
    with pytest.raises(Exception):
        PhHeatingDirectElectric()


def test_ph_heating_fossil_boiler():
    with pytest.raises(Exception):
        PhHeatingFossilBoiler()


def test_ph_heating_wood_boiler():
    with pytest.raises(Exception):
        PhHeatingWoodBoiler()


def test_ph_heating_district():
    with pytest.raises(Exception):
        PhHeatingDistrict()


def test_ph_heating_system_builder():
    with pytest.raises(Exception):
        PhHeatingSystemBuilder()
