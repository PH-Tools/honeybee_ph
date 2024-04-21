from honeybee_phhvac import heat_pumps, heating, supportive_device, ventilation
from honeybee_phhvac.properties.room import RoomPhHvacProperties
from honeybee_phhvac.renewable_devices import PhPhotovoltaicDevice


def test_default_empty_system_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


# -----------------------------------------------------------------------------
# -- Exhaust Ventilation Devices


def test_system_with_single_exhaust_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = ventilation.ExhaustVentDryer()
    p1.add_exhaust_vent_device(d1)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_exhaust_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = ventilation.ExhaustVentDryer()
    d2 = ventilation.ExhaustVentKitchenHood()
    d3 = ventilation.ExhaustVentUserDefined()
    p1.add_exhaust_vent_device(d1)
    p1.add_exhaust_vent_device(d2)
    p1.add_exhaust_vent_device(d3)
    p1.add_exhaust_vent_device(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_multiple_exhaust():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = ventilation.ExhaustVentDryer()
    d2 = ventilation.ExhaustVentKitchenHood()
    d3 = ventilation.ExhaustVentUserDefined()
    p1.add_exhaust_vent_device(d1)
    p1.add_exhaust_vent_device(d2)
    p1.add_exhaust_vent_device(d3)

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Exhaust Ventilation System


def test_system_with_vent_sys_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = ventilation.PhVentilationSystem()
    p1.set_ventilation_system(s1)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_vent_sys():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = ventilation.PhVentilationSystem()
    p1.set_ventilation_system(s1)

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Supportive Devices


def test_system_with_supportive_device_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = supportive_device.PhSupportiveDevice()
    p1.add_supportive_device(d1)

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_system_with_supportive_device_dict_duplicate():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = supportive_device.PhSupportiveDevice()
    p1.add_supportive_device(d1)

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Heating Systems


def test_system_with_single_heating_sys_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = heating.PhHeatingDirectElectric()
    p1.add_heating_system(s1)
    p1.add_heating_system(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_heating_sys_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = heating.PhHeatingDirectElectric()
    s2 = heating.PhHeatingDistrict()
    s3 = heating.PhHeatingFossilBoiler()
    s4 = heating.PhHeatingWoodBoiler()
    p1.add_heating_system(s1)
    p1.add_heating_system(s2)
    p1.add_heating_system(s3)
    p1.add_heating_system(s4)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_single_heating_sys():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = heating.PhHeatingDirectElectric()
    p1.add_heating_system(s1)
    assert p1.ToString()

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Heat Pump (Heating + Cooling) Systems


def test_system_with_multiple_heat_pump_sys_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)

    s1 = heat_pumps.PhHeatPumpAnnual()
    s2 = heat_pumps.PhHeatPumpRatedMonthly()
    p1.add_heat_pump_system(s1)
    p1.add_heat_pump_system(s2)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_system_with_single_heat_pump_sys_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = heat_pumps.PhHeatPumpAnnual()
    p1.add_heat_pump_system(s1)
    p1.add_heat_pump_system(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_single_cooling_sys():
    p1 = RoomPhHvacProperties(_host=None)
    s1 = heat_pumps.PhHeatPumpCoolingParams_Recirculation()
    p1.add_heat_pump_system(s1)
    assert p1.ToString()

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Renewable Devices


def test_system_with_single_renewable_device_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = PhPhotovoltaicDevice()
    p1.add_renewable_device(d1)
    p1.add_renewable_device(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_renewable_devices_dict_roundtrip():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = PhPhotovoltaicDevice()
    d2 = PhPhotovoltaicDevice()
    d3 = PhPhotovoltaicDevice()
    p1.add_renewable_device(d1)
    p1.add_renewable_device(d2)
    p1.add_renewable_device(d3)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = RoomPhHvacProperties.from_dict(d["ph_hvac"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_multiple_renewable_devices():
    p1 = RoomPhHvacProperties(_host=None)
    d1 = PhPhotovoltaicDevice()
    d2 = PhPhotovoltaicDevice()
    d3 = PhPhotovoltaicDevice()
    p1.add_renewable_device(d1)
    p1.add_renewable_device(d2)
    p1.add_renewable_device(d3)
    assert p1.ToString()

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()
