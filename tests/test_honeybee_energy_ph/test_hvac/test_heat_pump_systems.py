import pytest

from honeybee_energy_ph.hvac import heat_pumps


def test_base_class():
    sys = heat_pumps.PhHeatPumpSystem()
    assert sys.ToString()


# -----------------------------------------------------------------------------
# -- Heat Pump Systems


def test_dict_roundtrip_hp_annual_with_default_cooling():
    s1 = heat_pumps.PhHeatPumpAnnual()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpAnnual.from_dict(d)
    assert s2.to_dict() == d


def test_dict_roundtrip_hp_annual_with_custom_cooling():
    s1 = heat_pumps.PhHeatPumpAnnual()
    s1.cooling_params.recirculation.annual_COP = 124
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpAnnual.from_dict(d)
    assert s2.to_dict() == d
    assert s2.cooling_params.recirculation.annual_COP == 124


def test_dict_roundtrip_hp_monthly_with_default_cooling():
    s1 = heat_pumps.PhHeatPumpRatedMonthly()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpRatedMonthly.from_dict(d)
    assert s2.to_dict() == d


def test_dict_roundtrip_hp_monthly_with_custom_cooling():
    s1 = heat_pumps.PhHeatPumpRatedMonthly()
    s1.cooling_params.recirculation.annual_COP = 124
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpRatedMonthly.from_dict(d)
    assert s2.to_dict() == d
    assert s2.cooling_params.recirculation.annual_COP == 124


def test_hb_combined_raises_error():
    with pytest.raises(NotImplementedError):
        s1 = heat_pumps.PhHeatPumpCombined()


# -----
# -- Monthly Heat Pumps


def test_monthly_heat_pump_set_with_2_values():
    hp = heat_pumps.PhHeatPumpRatedMonthly()
    hp.monthly_COPS = [1, 2]

    assert hp.COP_1 == 1
    assert hp.COP_2 == 2
    assert hp.monthly_COPS == [1, 2]


def test_monthly_heat_pump_set_with_1_value():
    hp = heat_pumps.PhHeatPumpRatedMonthly()
    hp.monthly_COPS = [12]

    assert hp.COP_1 == 12
    assert hp.COP_2 == 12
    assert hp.monthly_COPS == [12, 12]


def test_monthly_heat_pump_set_temps_with_2_values():
    hp = heat_pumps.PhHeatPumpRatedMonthly()
    hp.monthly_temps = [1, 2]

    assert hp.ambient_temp_1 == 1
    assert hp.ambient_temp_2 == 2
    assert hp.monthly_temps == [1, 2]


def test_monthly_heat_pump_set_temps_with_1_value():
    hp = heat_pumps.PhHeatPumpRatedMonthly()
    hp.monthly_temps = [12]

    assert hp.ambient_temp_1 == 12
    assert hp.ambient_temp_2 == 12
    assert hp.monthly_temps == [12, 12]


# -----------------------------------------------------------------------------
# -- Heat Pump Builder


def test_hb_annual_builder():
    s1 = heat_pumps.PhHeatPumpRatedMonthly()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpSystemBuilder.from_dict(d)
    assert s2.to_dict() == d


def test_hb_monthly_builder():
    s1 = heat_pumps.PhHeatPumpRatedMonthly()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpSystemBuilder.from_dict(d)
    assert s2.to_dict() == d


def test_unsupported_heat_pump_type():
    s1 = heat_pumps.PhHeatPumpRatedMonthly()
    s1.heat_pump_class_name = "unsupported_type"
    d = s1.to_dict()

    with pytest.raises(heat_pumps.UnknownPhHeatPumpTypeError):
        s2 = heat_pumps.PhHeatPumpSystemBuilder.from_dict(d)


# -----------------------------------------------------------------------------
# -- Cooling Params


def test_dict_roundtrip_recirculation_params():
    s1 = heat_pumps.PhHeatPumpCoolingParams_Recirculation()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpCoolingParams_Recirculation.from_dict(d)
    assert s2.to_dict() == d


def test_dict_roundtrip_dehumidification():
    s1 = heat_pumps.PhHeatPumpCoolingParams_Dehumidification()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpCoolingParams_Dehumidification.from_dict(d)
    assert s2.to_dict() == d


def test_dict_roundtrip_panel():
    s1 = heat_pumps.PhHeatPumpCoolingParams_Panel()
    d = s1.to_dict()

    s2 = heat_pumps.PhHeatPumpCoolingParams_Panel.from_dict(d)
    assert s2.to_dict() == d
