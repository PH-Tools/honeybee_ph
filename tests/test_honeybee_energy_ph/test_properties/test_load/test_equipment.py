import json
import os

from honeybee.model import Model
from honeybee.room import Room

from honeybee_energy_ph.properties.load.equipment import (
    ElectricEquipmentPhProperties,
    migrate_legacy_equipment_collections,
)

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "legacy_fixtures")
MODEL_FIXTURE = os.path.join(FIXTURE_DIR, "legacy_equipment_collection_model.hbjson")
ROOM_FIXTURE = os.path.join(FIXTURE_DIR, "legacy_equipment_collection_room.json")


def _load_fixture(path):
    with open(path) as fixture_file:
        return json.load(fixture_file)


def _load_model():
    fixture = _load_fixture(MODEL_FIXTURE)
    return fixture, Model.from_dict(fixture)


def _load_room():
    fixture = _load_fixture(ROOM_FIXTURE)
    return fixture, Room.from_dict(fixture)


def _fixture_equipment_set(electric_equipment_dict):
    return electric_equipment_dict["properties"]["ph"]["equipment_collection"]["equipment_set"]


def _model_fixture_electric_equipment(fixture):
    return fixture["properties"]["energy"]["program_types"][0]["electric_equipment"]


def _room_fixture_electric_equipment(fixture):
    return fixture["properties"]["energy"]["electric_equipment"]


def _equipment_processes(hb_room):
    return tuple(
        process for process in hb_room.properties.energy.process_loads if process.properties.ph.ph_equipment is not None
    )


def _contains_key(value, expected_key):
    if isinstance(value, dict):
        return expected_key in value or any(_contains_key(item, expected_key) for item in value.values())
    if isinstance(value, list):
        return any(_contains_key(item, expected_key) for item in value)
    return False


def test_model_load_migrates_every_legacy_equipment_collection():
    fixture, model = _load_model()
    expected_ids = set(_fixture_equipment_set(_model_fixture_electric_equipment(fixture)))

    for hb_room in model.rooms:
        processes = _equipment_processes(hb_room)
        assert len(processes) == 2
        assert {process.properties.ph.ph_equipment.identifier for process in processes} == expected_ids


def test_migration_preserves_quantity_and_reference_quantity():
    fixture, model = _load_model()
    expected = _fixture_equipment_set(_model_fixture_electric_equipment(fixture))

    for hb_room in model.rooms:
        migrated = {
            process.properties.ph.ph_equipment.identifier: process.properties.ph.ph_equipment
            for process in _equipment_processes(hb_room)
        }
        for identifier, equipment_dict in expected.items():
            assert migrated[identifier].quantity == equipment_dict["quantity"]
            assert migrated[identifier].reference_quantity == equipment_dict["reference_quantity"]


def test_migrated_processes_are_zero_watt_and_keep_the_legacy_schedule():
    fixture, model = _load_model()
    expected_schedule = _model_fixture_electric_equipment(fixture)["schedule"]

    for hb_room in model.rooms:
        for process in _equipment_processes(hb_room):
            assert process.watts == 0
            assert process.schedule.identifier == expected_schedule


def test_model_load_empties_override_and_program_type_legacy_collections():
    _, model = _load_model()

    for hb_room in model.rooms:
        collection = hb_room.properties.energy.electric_equipment.properties.ph.equipment_collection
        assert list(collection.keys()) == []


def test_migrated_rooms_do_not_share_process_or_equipment_objects():
    _, model = _load_model()
    processes = [process for hb_room in model.rooms for process in _equipment_processes(hb_room)]
    equipment = [process.properties.ph.ph_equipment for process in processes]

    assert len({id(process) for process in processes}) == len(processes)
    assert len({id(item) for item in equipment}) == len(equipment)


def test_room_from_dict_migrates_legacy_equipment_collection():
    fixture, hb_room = _load_room()
    electric_equipment = _room_fixture_electric_equipment(fixture)
    expected = _fixture_equipment_set(electric_equipment)
    processes = _equipment_processes(hb_room)

    assert len(processes) == 2
    assert {process.properties.ph.ph_equipment.identifier for process in processes} == set(expected)
    assert all(process.watts == 0 for process in processes)
    assert all(process.schedule.identifier == electric_equipment["schedule"]["identifier"] for process in processes)


def test_migration_is_idempotent():
    _, model = _load_model()
    process_ids_before = {
        hb_room.identifier: tuple(id(process) for process in _equipment_processes(hb_room)) for hb_room in model.rooms
    }

    migrate_legacy_equipment_collections(model.rooms)

    process_ids_after = {
        hb_room.identifier: tuple(id(process) for process in _equipment_processes(hb_room)) for hb_room in model.rooms
    }
    assert process_ids_after == process_ids_before


def test_legacy_collection_is_not_written_and_round_trip_does_not_duplicate():
    properties = ElectricEquipmentPhProperties(_host="test")
    assert "equipment_collection" not in properties.to_dict()["ph"]

    _, model = _load_model()
    model_dict = model.to_dict()
    assert not _contains_key(model_dict, "equipment_collection")

    reloaded_model = Model.from_dict(model_dict)
    assert all(len(_equipment_processes(hb_room)) == 2 for hb_room in reloaded_model.rooms)


def test_electric_equipment_properties_from_dict_accepts_missing_collection():
    properties = ElectricEquipmentPhProperties.from_dict({"type": "ElectricEquipmentPhProperties"}, _host="test")

    assert list(properties.equipment_collection.keys()) == []
