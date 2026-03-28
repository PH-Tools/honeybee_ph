import pytest

from honeybee_energy_ph.hvac.heat_pumps import (
    PhHeatPumpAnnual,
    PhHeatPumpCombined,
    PhHeatPumpCoolingParams,
    PhHeatPumpCoolingParams_Base,
    PhHeatPumpCoolingParams_Dehumidification,
    PhHeatPumpCoolingParams_Panel,
    PhHeatPumpCoolingParams_Recirculation,
    PhHeatPumpCoolingParams_Ventilation,
    PhHeatPumpRatedMonthly,
    PhHeatPumpSystem,
    PhHeatPumpSystemBuilder,
)


def test_ph_heat_pump_system_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpSystem()


def test_ph_heat_pump_cooling_params_base_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCoolingParams_Base()


def test_ph_heat_pump_cooling_params_ventilation_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCoolingParams_Ventilation()


def test_ph_heat_pump_cooling_params_recirculation_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCoolingParams_Recirculation()


def test_ph_heat_pump_cooling_params_dehumidification_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCoolingParams_Dehumidification()


def test_ph_heat_pump_cooling_params_panel_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCoolingParams_Panel()


def test_ph_heat_pump_cooling_params_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCoolingParams()


def test_ph_heat_pump_annual_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpAnnual()


def test_ph_heat_pump_rated_monthly_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpRatedMonthly()


def test_ph_heat_pump_combined_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpCombined()


def test_ph_heat_pump_system_builder_raises_exception():
    with pytest.raises(Exception):
        PhHeatPumpSystemBuilder()
