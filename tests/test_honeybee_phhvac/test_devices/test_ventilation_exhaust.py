import pytest

from honeybee_phhvac import ventilation


# -----------------------------------------------------------------------------
# --- Default Objects
def test_default_exhaust_Dryer_dict_roundtrip():
    o1 = ventilation.ExhaustVentDryer()
    assert o1.ToString()
    d = o1.to_dict()
    o2 = ventilation.ExhaustVentDryer.from_dict(d)
    assert o2.to_dict() == d


def test_default_exhaust_Hood_dict_roundtrip():
    o1 = ventilation.ExhaustVentKitchenHood()
    assert o1.ToString()
    d = o1.to_dict()
    o2 = ventilation.ExhaustVentKitchenHood.from_dict(d)
    assert o2.to_dict() == d


def test_default_exhaust_User_Defined_dict_roundtrip():
    o1 = ventilation.ExhaustVentUserDefined()
    assert o1.ToString()
    d = o1.to_dict()
    o2 = ventilation.ExhaustVentUserDefined.from_dict(d)
    assert o2.to_dict() == d


# -----------------------------------------------------------------------------
# --- Custom Objects
def test_custom_exhaust_Dryer_dict_roundtrip():
    o1 = ventilation.ExhaustVentDryer()
    o1.annual_runtime_minutes = 1234.5
    o1.exhaust_flow_rate_m3s = 4567.8
    d = o1.to_dict()
    o2 = ventilation.ExhaustVentDryer.from_dict(d)
    assert o2.to_dict() == d


def test_custom_exhaust_Dryer_duplicate():
    o1 = ventilation.ExhaustVentDryer()
    o1.annual_runtime_minutes = 1234.5
    o1.exhaust_flow_rate_m3s = 4567.8
    o2 = o1.duplicate()
    assert o2.annual_runtime_minutes == 1234.5
    assert o2.exhaust_flow_rate_m3s == 4567.8
    assert id(o1) != id(o2)


def test_custom_exhaust_Hood_dict_roundtrip():
    o1 = ventilation.ExhaustVentKitchenHood()
    o1.annual_runtime_minutes = 1234.5
    o1.exhaust_flow_rate_m3s = 4567.8
    d = o1.to_dict()
    o2 = ventilation.ExhaustVentKitchenHood.from_dict(d)
    assert o2.to_dict() == d


def test_custom_exhaust_Hood_duplicate():
    o1 = ventilation.ExhaustVentKitchenHood()
    o1.annual_runtime_minutes = 1234.5
    o1.exhaust_flow_rate_m3s = 4567.8
    o2 = o1.duplicate()
    assert o2.annual_runtime_minutes == 1234.5
    assert o2.exhaust_flow_rate_m3s == 4567.8
    assert id(o1) != id(o2)


def test_custom_exhaust_User_Defined_dict_roundtrip():
    o1 = ventilation.ExhaustVentUserDefined()
    o1.annual_runtime_minutes = 1234.5
    o1.exhaust_flow_rate_m3s = 4567.8
    d = o1.to_dict()
    o2 = ventilation.ExhaustVentUserDefined.from_dict(d)
    assert o2.to_dict() == d


def test_custom_exhaust_User_Defined_duplicate():
    o1 = ventilation.ExhaustVentUserDefined()
    o1.annual_runtime_minutes = 1234.5
    o1.exhaust_flow_rate_m3s = 4567.8
    o2 = o1.duplicate()
    assert o2.annual_runtime_minutes == 1234.5
    assert o2.exhaust_flow_rate_m3s == 4567.8
    assert id(o1) != id(o2)


# -----------------------------------------------------------------------------
# -- Builder


def test_builder():
    b = ventilation.PhExhaustDeviceBuilder()
    assert b.ToString()


def test_builder_dryer():
    obj1 = ventilation.ExhaustVentDryer()
    d = obj1.to_dict()
    obj2 = ventilation.PhExhaustDeviceBuilder.from_dict(d)
    assert obj2.to_dict() == d


def test_builder_hood():
    obj1 = ventilation.ExhaustVentKitchenHood()
    d = obj1.to_dict()
    obj2 = ventilation.PhExhaustDeviceBuilder.from_dict(d)
    assert obj2.to_dict() == d


def test_builder_user_defined():
    obj1 = ventilation.ExhaustVentUserDefined()
    d = obj1.to_dict()
    obj2 = ventilation.PhExhaustDeviceBuilder.from_dict(d)
    assert obj2.to_dict() == d


def test_builder_error():
    d = {"device_class_name": "NotAnExhaustDevice"}
    with pytest.raises(ventilation.UnknownPhExhaustVentTypeError):
        obj2 = ventilation.PhExhaustDeviceBuilder.from_dict(d)
