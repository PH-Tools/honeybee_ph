import pytest

from honeybee_energy_ph.hvac.ventilation import (
    ExhaustVentDryer,
    ExhaustVentKitchenHood,
    ExhaustVentUserDefined,
    PhExhaustDeviceBuilder,
    PhVentilationSystem,
    Ventilator,
    _ExhaustVentilatorBase,
)


def test_Ventilator_raises_exception():
    with pytest.raises(Exception):
        Ventilator()


def test_PhVentilationSystem_raises_exception():
    with pytest.raises(Exception):
        PhVentilationSystem()


def test__ExhaustVentilatorBase_raises_exception():
    with pytest.raises(Exception):
        _ExhaustVentilatorBase()


def test_ExhaustVentDryer_raises_exception():
    with pytest.raises(Exception):
        ExhaustVentDryer()


def test_ExhaustVentKitchenHood_raises_exception():
    with pytest.raises(Exception):
        ExhaustVentKitchenHood()


def test_ExhaustVentUserDefined_raises_exception():
    with pytest.raises(Exception):
        ExhaustVentUserDefined()


def test_PhExhaustDeviceBuilder_raises_exception():
    with pytest.raises(Exception):
        PhExhaustDeviceBuilder()
