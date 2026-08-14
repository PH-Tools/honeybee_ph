import pytest
from honeybee.model import Model
from honeybee.room import Room
from ladybug_geometry.geometry3d.pointvector import Vector3D

from honeybee_phhvac import ventilation
from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment
from honeybee_phhvac.properties.room import RoomPhHvacProperties


def _factory_system(duct_count=0, display_name="Balanced ERV"):
    unit = ventilation.Ventilator()
    unit.display_name = "Selected ERV"
    unit.sensible_heat_recovery = 0.82
    unit.latent_heat_recovery = 0.45
    unit.electric_efficiency = 0.35
    unit.user_data = {"selection": {"status": "selected"}}

    supply_ducts = []
    exhaust_ducts = []
    for index in range(duct_count):
        supply = PhDuctElement("Supply {}".format(index + 1), _duct_type=1)
        supply.user_data = {"element": {"index": index}}
        supply_segment = PhDuctSegment.default()
        supply_segment.user_data = {"segment": {"index": index}}
        supply.add_segment(supply_segment)
        supply_ducts.append(supply)

        exhaust = PhDuctElement("Exhaust {}".format(index + 1), _duct_type=2)
        exhaust.user_data = {"element": {"index": index}}
        exhaust_segment = PhDuctSegment.default()
        exhaust_segment.user_data = {"segment": {"index": index}}
        exhaust.add_segment(exhaust_segment)
        exhaust_ducts.append(exhaust)

    system = ventilation.PhVentilationSystem.balanced_hrv(
        unit,
        supply_ducting=supply_ducts,
        exhaust_ducting=exhaust_ducts,
        display_name=display_name,
    )
    system.user_data = {"system": {"source": "factory"}}
    return system


@pytest.mark.parametrize("duct_count", [0, 1, 2])
def test_factory_system_dict_round_trip(duct_count):
    system = _factory_system(duct_count)

    restored = ventilation.PhVentilationSystem.from_dict(system.to_dict())

    assert restored.to_dict() == system.to_dict()
    assert len(restored.supply_ducting) == duct_count
    assert len(restored.exhaust_ducting) == duct_count


def test_factory_system_duplicate_owns_full_graph():
    system = _factory_system(2)

    duplicate = system.duplicate()

    assert duplicate.to_dict() == system.to_dict()
    assert duplicate is not system
    assert duplicate.ventilation_unit is not system.ventilation_unit
    assert duplicate.supply_ducting[0] is not system.supply_ducting[0]
    assert duplicate.supply_ducting[0].segments[0] is not system.supply_ducting[0].segments[0]
    assert duplicate.supply_ducting[0].segments[0].geometry is not system.supply_ducting[0].segments[0].geometry

    duplicate.user_data["system"]["source"] = "duplicate"
    duplicate.ventilation_unit.user_data["selection"]["status"] = "duplicate"
    duplicate.supply_ducting[0].user_data["element"]["index"] = 99
    duplicate.supply_ducting[0].segments[0].user_data["segment"]["index"] = 99

    assert system.user_data["system"]["source"] == "factory"
    assert system.ventilation_unit.user_data["selection"]["status"] == "selected"
    assert system.supply_ducting[0].user_data["element"]["index"] == 0
    assert system.supply_ducting[0].segments[0].user_data["segment"]["index"] == 0


@pytest.mark.parametrize("abridged", [False, True])
def test_factory_system_room_properties_round_trip(abridged):
    properties = RoomPhHvacProperties(_host=None)
    properties.set_ventilation_system(_factory_system(2))

    payload = properties.to_dict(abridged=abridged)
    restored = RoomPhHvacProperties.from_dict(payload["ph_hvac"], host=None)

    assert restored.to_dict(abridged=abridged) == payload


def test_factory_system_hbjson_model_round_trip(tmp_path):
    room = Room.from_box("FactoryRoom")
    room.properties.ph_hvac.set_ventilation_system(_factory_system(2))
    model = Model("FactoryModel", rooms=[room])

    hbjson_path = model.to_hbjson(name="factory-model.hbjson", folder=str(tmp_path))
    restored = Model.from_hbjson(hbjson_path)

    restored_system = restored.rooms[0].properties.ph_hvac.ventilation_system
    assert restored_system.to_dict() == room.properties.ph_hvac.ventilation_system.to_dict()
    assert len(restored_system.supply_ducting) == 2
    assert len(restored_system.exhaust_ducting) == 2


def test_hbjson_model_round_trip_deduplicates_shared_identifier():
    shared_system = _factory_system(1)
    first = Room.from_box("SharedFirst")
    second = Room.from_box("SharedSecond")
    first.properties.ph_hvac.set_ventilation_system(shared_system)
    second.properties.ph_hvac.set_ventilation_system(shared_system.duplicate())
    model = Model("SharedSystemModel", rooms=[first, second])

    restored = Model.from_dict(model.to_dict())
    restored_first = restored.rooms[0].properties.ph_hvac.ventilation_system
    restored_second = restored.rooms[1].properties.ph_hvac.ventilation_system

    assert restored_first is restored_second
    assert restored_first.identifier == shared_system.identifier


def test_hbjson_model_round_trip_preserves_distinct_systems():
    first_system = _factory_system(1, "First ERV")
    second_system = _factory_system(1, "Second ERV")
    first = Room.from_box("DistinctFirst")
    second = Room.from_box("DistinctSecond")
    first.properties.ph_hvac.set_ventilation_system(first_system)
    second.properties.ph_hvac.set_ventilation_system(second_system)
    model = Model("DistinctSystemModel", rooms=[first, second])

    restored = Model.from_dict(model.to_dict())
    restored_first = restored.rooms[0].properties.ph_hvac.ventilation_system
    restored_second = restored.rooms[1].properties.ph_hvac.ventilation_system

    assert restored_first is not restored_second
    assert {restored_first.identifier, restored_second.identifier} == {
        first_system.identifier,
        second_system.identifier,
    }


def test_room_duplicate_and_transform_do_not_mutate_source_system():
    room = Room.from_box("TransformRoom")
    room.properties.ph_hvac.set_ventilation_system(_factory_system(1))
    source_system = room.properties.ph_hvac.ventilation_system
    source_geometry = source_system.supply_ducting[0].segments[0].geometry.to_dict()

    duplicate = room.duplicate()
    duplicate.move(Vector3D(2, 0, 0))
    duplicate_system = duplicate.properties.ph_hvac.ventilation_system

    assert source_system.supply_ducting[0].segments[0].geometry.to_dict() == source_geometry
    assert duplicate_system.supply_ducting[0].segments[0].geometry.to_dict() != source_geometry
    assert duplicate_system.ventilation_unit.to_dict() == source_system.ventilation_unit.to_dict()
    assert duplicate_system.identifier == source_system.identifier
    assert duplicate_system is not source_system


def test_hbjson_rejects_same_identifier_with_conflicting_system_graphs():
    source = Room.from_box("CollisionSource")
    source.properties.ph_hvac.set_ventilation_system(_factory_system(1))
    moved = source.duplicate()
    moved.identifier = "CollisionMoved"
    moved.move(Vector3D(2, 0, 0))
    model = Model("ConflictingSystemModel", rooms=[source, moved])

    with pytest.raises(Exception, match="Conflicting ventilation systems share identifier"):
        Model.from_dict(model.to_dict())


def test_legacy_system_dict_without_optional_metadata_loads():
    payload = ventilation.PhVentilationSystem().to_dict()
    payload.pop("user_data")
    payload.pop("id_num")

    restored = ventilation.PhVentilationSystem.from_dict(payload)

    assert restored.sys_type == 1
    assert restored.user_data == {}
    assert restored.id_num == 0
    assert restored.ventilation_unit is None
    assert restored.supply_ducting == []
    assert restored.exhaust_ducting == []
