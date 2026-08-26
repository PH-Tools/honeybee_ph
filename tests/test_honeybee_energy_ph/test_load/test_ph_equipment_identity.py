"""The identity contract that the PHX energy totals depend on.

PHX creates one PhxZone per Honeybee-Room and keys each zone's electric-device
collection by the device 'identifier', upserting. The Phius multi-family builders
rely on that: they hand one device to every Room with the demand already divided by
the room count, the N per-room devices collapse to one device per zone, and the N
zones sum back to the building total.

So the identifier must stay shared across rooms while the objects themselves must
not be. These tests lock both halves. See
'context/decisions/0008-ph-equipment-duplicate-preserves-identifier.md'.
"""

import pytest
from honeybee.model import Model
from honeybee.room import Room
from honeybee_energy.lib.schedules import schedule_by_identifier
from honeybee_energy.load.process import Process

from honeybee_energy_ph.load import ph_equipment


def _rooms_with_shared_equipment(_room_count, _total_demand):
    # type: (int, float) -> list[Room]
    """Build N Rooms that all carry one Phius-MF style Process load."""
    equipment = ph_equipment.PhCustomAnnualMEL.phius_default()
    equipment.energy_demand = _total_demand / _room_count
    equipment.quantity = 1

    process = Process(
        identifier="HBPH_Process_MEL",
        watts=100,
        schedule=schedule_by_identifier("Always On"),
        fuel_type="Electricity",
        end_use_category="HBPH_Process",
    )
    process.properties.ph.ph_equipment = equipment

    rooms = []
    for i in range(_room_count):
        room = Room.from_box("Room_{}".format(i), 5, 5, 3)
        room.properties.energy.add_process_load(process)
        rooms.append(room)
    return rooms


def _equipment_of(_rooms):
    """The PhEquipment carried by every Room's Process loads."""
    return [pl.properties.ph.ph_equipment for rm in _rooms for pl in rm.properties.energy.process_loads]


@pytest.mark.parametrize("room_count", [1, 2, 10])
def test_the_per_room_devices_share_one_identifier(room_count):
    """One identifier across N rooms is what makes the N zones sum to the total."""
    rooms = _rooms_with_shared_equipment(room_count, 1000.0)
    equipment = _equipment_of(rooms)

    assert len(equipment) == room_count
    assert len(set(e.identifier for e in equipment)) == 1


@pytest.mark.parametrize("room_count", [1, 2, 10])
def test_the_room_count_invariant_holds(room_count):
    """Deduping by identifier and summing over the zones must return the total.

    This is the arithmetic PHX performs: one device per zone (the upsert), N zones.
    """
    total_demand = 1000.0
    rooms = _rooms_with_shared_equipment(room_count, total_demand)

    per_zone_device = {}
    for equip in _equipment_of(rooms):
        per_zone_device[equip.identifier] = equip  # -- the PHX upsert, per zone
    assert len(per_zone_device) == 1

    zone_total = sum(e.energy_demand for e in per_zone_device.values())
    assert zone_total * room_count == pytest.approx(total_demand)


@pytest.mark.parametrize("room_count", [1, 2, 10])
def test_the_identifier_survives_an_hbjson_round_trip(room_count):
    rooms = _rooms_with_shared_equipment(room_count, 1000.0)
    before = set(e.identifier for e in _equipment_of(rooms))

    model = Model("test_model", rooms)
    rebuilt = Model.from_dict(model.to_dict())

    after = set(e.identifier for e in _equipment_of(rebuilt.rooms))
    assert after == before
    assert len(after) == 1


def test_duplicating_a_process_load_no_longer_shares_the_equipment_object():
    """The copy must be independent, but must keep the identifier.

    NOTE: Honeybee's own Room.duplicate() shares the Process-Load objects themselves,
    so a duplicated Room still points at the same equipment. This test covers the
    layer honeybee-ph owns: duplicating the Process Load.
    """
    room = _rooms_with_shared_equipment(1, 1000.0)[0]
    original = _equipment_of([room])[0]

    copied = room.properties.energy.process_loads[0].duplicate().properties.ph.ph_equipment

    assert copied is not original
    assert copied.identifier == original.identifier

    copied.energy_demand = 0.0
    assert original.energy_demand == 1000.0
