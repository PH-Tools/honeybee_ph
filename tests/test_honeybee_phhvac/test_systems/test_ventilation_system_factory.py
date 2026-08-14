import math

import pytest

from honeybee_phhvac import ventilation
from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment
from honeybee_phhvac.properties.room import RoomPhHvacProperties


def _valid_ventilator():
    unit = ventilation.Ventilator()
    unit.display_name = "Selected ERV"
    unit.sensible_heat_recovery = 0.82
    unit.latent_heat_recovery = 0.45
    unit.electric_efficiency = 0.35
    return unit


def test_balanced_hrv_requires_a_ventilator():
    with pytest.raises(TypeError, match="ventilator"):
        ventilation.PhVentilationSystem.balanced_hrv(None)

    with pytest.raises(TypeError, match="ventilator"):
        ventilation.PhVentilationSystem.balanced_hrv(object())


def test_balanced_hrv_with_no_exterior_ducts():
    unit = _valid_ventilator()

    system = ventilation.PhVentilationSystem.balanced_hrv(unit)

    assert system.sys_type == 1
    assert system.supply_ducting == []
    assert system.exhaust_ducting == []
    assert system.ventilation_unit.to_dict() == unit.to_dict()
    assert system.ventilation_unit is not unit


def test_balanced_hrv_treats_none_and_empty_duct_collections_equally():
    unit = _valid_ventilator()

    with_none = ventilation.PhVentilationSystem.balanced_hrv(unit, supply_ducting=None, exhaust_ducting=None)
    with_empty = ventilation.PhVentilationSystem.balanced_hrv(unit, supply_ducting=[], exhaust_ducting=[])

    assert with_none.supply_ducting == with_empty.supply_ducting == []
    assert with_none.exhaust_ducting == with_empty.exhaust_ducting == []


def test_balanced_hrv_accepts_and_duplicates_multiple_typed_ducts():
    unit = _valid_ventilator()
    supply_1 = PhDuctElement("Supply 1", _duct_type=1)
    supply_2 = PhDuctElement("Supply 2", _duct_type=1)
    exhaust_1 = PhDuctElement("Exhaust 1", _duct_type=2)
    exhaust_2 = PhDuctElement("Exhaust 2", _duct_type=2)

    system = ventilation.PhVentilationSystem.balanced_hrv(
        unit,
        supply_ducting=(supply_1, supply_2),
        exhaust_ducting=[exhaust_1, exhaust_2],
        display_name="Apartment ERV",
    )

    assert system.display_name == "Apartment ERV"
    assert [d.to_dict() for d in system.supply_ducting] == [
        supply_1.to_dict(),
        supply_2.to_dict(),
    ]
    assert [d.to_dict() for d in system.exhaust_ducting] == [
        exhaust_1.to_dict(),
        exhaust_2.to_dict(),
    ]
    assert system.supply_ducting[0] is not supply_1
    assert system.supply_ducting[1] is not supply_2
    assert system.exhaust_ducting[0] is not exhaust_1
    assert system.exhaust_ducting[1] is not exhaust_2


def test_balanced_hrv_does_not_rename_caller_owned_ventilator():
    unit = _valid_ventilator()
    unit.display_name = "_unnamed_ventilator_"

    system = ventilation.PhVentilationSystem.balanced_hrv(unit, display_name="Apartment ERV")

    assert unit.display_name == "_unnamed_ventilator_"
    assert system.ventilation_unit.display_name == "Apartment ERV"


def test_balanced_hrv_uses_default_system_name_for_unnamed_child():
    unit = _valid_ventilator()
    unit.display_name = "_unnamed_ventilator_"

    system = ventilation.PhVentilationSystem.balanced_hrv(unit)

    assert system.display_name == "_unnamed_ph_vent_system_"
    assert system.ventilation_unit.display_name == system.display_name


def test_balanced_hrv_returns_fresh_independent_children():
    unit = _valid_ventilator()
    supply = PhDuctElement("Supply", _duct_type=1)

    system_1 = ventilation.PhVentilationSystem.balanced_hrv(unit, [supply])
    system_2 = ventilation.PhVentilationSystem.balanced_hrv(unit, [supply])

    assert system_1 is not system_2
    assert system_1.ventilation_unit is not system_2.ventilation_unit
    assert system_1.supply_ducting[0] is not system_2.supply_ducting[0]


def test_balanced_hrv_children_own_nested_user_data():
    unit = _valid_ventilator()
    unit.user_data = {"selection": {"source": "caller"}}
    segment = PhDuctSegment.default()
    segment.user_data = {"geometry": {"source": "caller"}}
    supply = PhDuctElement("Supply", _duct_type=1)
    supply.user_data = {"element": {"source": "caller"}}
    supply.add_segment(segment)

    system = ventilation.PhVentilationSystem.balanced_hrv(unit, [supply])
    system.ventilation_unit.user_data["selection"]["source"] = "result"
    system.supply_ducting[0].user_data["element"]["source"] = "result"
    system.supply_ducting[0].segments[0].user_data["geometry"]["source"] = "result"

    assert unit.user_data["selection"]["source"] == "caller"
    assert supply.user_data["element"]["source"] == "caller"
    assert segment.user_data["geometry"]["source"] == "caller"
    assert system.supply_ducting[0].segments[0] is not segment


def test_balanced_hrv_does_not_attach_to_room_properties():
    room_properties = RoomPhHvacProperties(_host=None)

    system = ventilation.PhVentilationSystem.balanced_hrv(_valid_ventilator())

    assert system is not None
    assert room_properties.ventilation_system is None


@pytest.mark.parametrize(
    "value",
    [0.0, -0.1, 1.1, math.nan, math.inf, -math.inf, None, True, "0.8"],
)
def test_balanced_hrv_rejects_invalid_sensible_heat_recovery(value):
    unit = _valid_ventilator()
    unit.sensible_heat_recovery = value

    with pytest.raises(ValueError, match="sensible_heat_recovery"):
        ventilation.PhVentilationSystem.balanced_hrv(unit)


@pytest.mark.parametrize(
    "value",
    [-0.1, 1.1, math.nan, math.inf, -math.inf, None, "0.4"],
)
def test_balanced_hrv_rejects_invalid_latent_heat_recovery(value):
    unit = _valid_ventilator()
    unit.latent_heat_recovery = value

    with pytest.raises(ValueError, match="latent_heat_recovery"):
        ventilation.PhVentilationSystem.balanced_hrv(unit)


@pytest.mark.parametrize(
    "value",
    [-0.1, math.nan, math.inf, -math.inf, None, "0.35"],
)
def test_balanced_hrv_rejects_invalid_electric_efficiency(value):
    unit = _valid_ventilator()
    unit.electric_efficiency = value

    with pytest.raises(ValueError, match="electric_efficiency"):
        ventilation.PhVentilationSystem.balanced_hrv(unit)


def test_balanced_hrv_accepts_performance_boundaries():
    unit = _valid_ventilator()
    unit.sensible_heat_recovery = 1.0
    unit.latent_heat_recovery = 0.0
    unit.electric_efficiency = 0.0
    ventilation.PhVentilationSystem.balanced_hrv(unit)

    unit.latent_heat_recovery = 1.0
    ventilation.PhVentilationSystem.balanced_hrv(unit)


@pytest.mark.parametrize("ducts", [object(), 1, "supply"])
def test_balanced_hrv_rejects_invalid_duct_collections(ducts):
    with pytest.raises(TypeError, match="supply_ducting"):
        ventilation.PhVentilationSystem.balanced_hrv(_valid_ventilator(), supply_ducting=ducts)


def test_balanced_hrv_rejects_non_duct_collection_members():
    with pytest.raises(TypeError, match="exhaust_ducting"):
        ventilation.PhVentilationSystem.balanced_hrv(_valid_ventilator(), exhaust_ducting=[object()])


def test_balanced_hrv_rejects_wrong_duct_direction():
    exhaust = PhDuctElement("Wrong supply direction", _duct_type=2)
    supply = PhDuctElement("Wrong exhaust direction", _duct_type=1)

    with pytest.raises(ValueError, match="supply_ducting"):
        ventilation.PhVentilationSystem.balanced_hrv(_valid_ventilator(), supply_ducting=[exhaust])

    with pytest.raises(ValueError, match="exhaust_ducting"):
        ventilation.PhVentilationSystem.balanced_hrv(_valid_ventilator(), exhaust_ducting=[supply])


def test_balanced_hrv_never_calls_legacy_default_duct_helpers(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("legacy default duct helper called")

    monkeypatch.setattr(PhDuctElement, "default_supply_duct", fail)
    monkeypatch.setattr(PhDuctElement, "default_exhaust_duct", fail)

    system = ventilation.PhVentilationSystem.balanced_hrv(_valid_ventilator())

    assert system.supply_ducting == []
    assert system.exhaust_ducting == []
