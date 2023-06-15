from honeybee_energy_ph.properties.hvac import idealair
from honeybee_energy_ph.hvac import (
    ventilation,
    heating,
    cooling,
    supportive_device,
)
from honeybee_energy_ph.hvac.renewable_devices import PhPhotovoltaicDevice


def test_default_empty_system_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


# -----------------------------------------------------------------------------
# -- Exhaust Ventilation Devices


def test_system_with_single_exhaust_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = ventilation.ExhaustVentDryer()
    p1.exhaust_vent_devices.add(d1)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_exhaust_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = ventilation.ExhaustVentDryer()
    d2 = ventilation.ExhaustVentKitchenHood()
    d3 = ventilation.ExhaustVentUserDefined()
    p1.exhaust_vent_devices.add(d1)
    p1.exhaust_vent_devices.add(d2)
    p1.exhaust_vent_devices.add(d3)
    p1.exhaust_vent_devices.add(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_multiple_exhaust():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = ventilation.ExhaustVentDryer()
    d2 = ventilation.ExhaustVentKitchenHood()
    d3 = ventilation.ExhaustVentUserDefined()
    p1.exhaust_vent_devices.add(d1)
    p1.exhaust_vent_devices.add(d2)
    p1.exhaust_vent_devices.add(d3)

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Exhaust Ventilation System


def test_system_with_vent_sys_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = ventilation.PhVentilationSystem()
    p1.ventilation_system = s1
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_vent_sys():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = ventilation.PhVentilationSystem()
    p1.ventilation_system = s1

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Supportive Devices


def test_system_with_supportive_device_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = supportive_device.PhSupportiveDevice()
    p1.supportive_devices.add(d1)

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_system_with_supportive_device_dict_ducplicate():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = supportive_device.PhSupportiveDevice()
    p1.supportive_devices.add(d1)

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Heating Systems


def test_system_with_single_heating_sys_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = heating.PhHeatingDirectElectric()
    p1.heating_systems.add(s1)
    p1.heating_systems.add(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_heating_sys_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = heating.PhHeatingDirectElectric()
    s2 = heating.PhHeatingDistrict()
    s3 = heating.PhHeatingFossilBoiler()
    s4 = heating.PhHeatingHeatPumpAnnual()
    s5 = heating.PhHeatingHeatPumpRatedMonthly()
    s6 = heating.PhHeatingWoodBoiler()
    p1.heating_systems.add(s1)
    p1.heating_systems.add(s2)
    p1.heating_systems.add(s3)
    p1.heating_systems.add(s4)
    p1.heating_systems.add(s5)
    p1.heating_systems.add(s6)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_single_heating_sys():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = heating.PhHeatingDirectElectric()
    p1.heating_systems.add(s1)
    assert p1.ToString()

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Cooling Systems


def test_system_with_single_cooling_sys_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = cooling.PhCoolingRecirculation()
    p1.cooling_systems.add(s1)
    p1.cooling_systems.add(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_cooling_sys_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = cooling.PhCoolingRecirculation()
    s2 = cooling.PhCoolingPanel()
    s3 = cooling.PhCoolingDehumidification()
    s4 = cooling.PhCoolingVentilation()
    p1.cooling_systems.add(s1)
    p1.cooling_systems.add(s2)
    p1.cooling_systems.add(s3)
    p1.cooling_systems.add(s4)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_single_cooling_sys():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    s1 = cooling.PhCoolingRecirculation()
    p1.cooling_systems.add(s1)
    assert p1.ToString()

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


# -----------------------------------------------------------------------------
# -- Renewable Devices


def test_system_with_single_renewable_device_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = PhPhotovoltaicDevice()
    p1.renewable_devices.add(d1)
    p1.renewable_devices.add(None)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_system_with_multiple_renewable_devices_dict_roundtrip():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = PhPhotovoltaicDevice()
    d2 = PhPhotovoltaicDevice()
    d3 = PhPhotovoltaicDevice()
    p1.renewable_devices.add(d1)
    p1.renewable_devices.add(d2)
    p1.renewable_devices.add(d3)
    assert p1.ToString()

    d = p1.to_dict()
    p2 = idealair.IdealAirSystemPhProperties.from_dict(d["ph"], p1.host)
    assert p2.to_dict() == d


def test_duplicate_system_with_multiple_renewable_devices():
    p1 = idealair.IdealAirSystemPhProperties(_host=None)
    d1 = PhPhotovoltaicDevice()
    d2 = PhPhotovoltaicDevice()
    d3 = PhPhotovoltaicDevice()
    p1.renewable_devices.add(d1)
    p1.renewable_devices.add(d2)
    p1.renewable_devices.add(d3)
    assert p1.ToString()

    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()
