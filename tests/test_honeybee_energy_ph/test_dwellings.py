from honeybee.room import Room
from honeybee_energy.load.people import People
from honeybee_energy.schedule.ruleset import ScheduleRuleset

from honeybee_energy_ph.dwellings import (
    dwelling_key,
    get_dwelling_obj,
    group_rooms_by_dwelling,
    total_dwelling_count,
    unique_dwelling_objects,
)
from honeybee_energy_ph.properties.load.people import PhDwellings


# -----------------------------------------------------------------------------
# -- Helpers


def _schedule():
    return ScheduleRuleset.from_constant_value("occ_schedule", 1.0)


def _room(_name, _dwelling=None):
    # type: (str, PhDwellings | None) -> Room
    """Build a HB-Room with a People load, optionally carrying a PhDwellings object."""
    room = Room.from_box(_name, 5, 5, 3)
    people = People("{}_People".format(_name), 0.01, _schedule())
    if _dwelling is not None:
        people.properties.ph.dwellings = _dwelling
    room.properties.energy.people = people
    return room


def _room_without_people(_name):
    # type: (str) -> Room
    """Build a HB-Room with no People load at all."""
    return Room.from_box(_name, 5, 5, 3)


class _FakeProperties(object):
    """Stands in for a Room whose properties have no 'energy' extension."""

    pass


class _FakeRoom(object):
    def __init__(self, identifier):
        self.identifier = identifier
        self.properties = _FakeProperties()


# -----------------------------------------------------------------------------
# -- get_dwelling_obj / dwelling_key


def test_room_with_no_people_has_no_dwelling():
    room = _room_without_people("rm_1")
    assert get_dwelling_obj(room) is None
    assert dwelling_key(room) == room.identifier


def test_room_with_default_dwelling_has_no_dwelling():
    """A People load that never went through 'Set Dwelling' carries the default singleton."""
    room = _room("rm_1")
    assert room.properties.energy.people.properties.ph.dwellings.identifier == PhDwellings.default().identifier
    assert get_dwelling_obj(room) is None
    assert dwelling_key(room) == room.identifier


def test_room_with_no_energy_properties_has_no_dwelling():
    room = _FakeRoom("rm_1")
    assert get_dwelling_obj(room) is None
    assert dwelling_key(room) == "rm_1"


def test_room_with_dwelling_returns_the_dwelling_identifier():
    dwelling = PhDwellings(_num_dwellings=1)
    room = _room("rm_1", dwelling)
    assert get_dwelling_obj(room) is dwelling
    assert dwelling_key(room) == dwelling.identifier


def test_duplicated_dwelling_keeps_the_same_key():
    """duplicate() makes a new object with the same identifier -- it must still match."""
    dwelling = PhDwellings(_num_dwellings=1)
    room_a = _room("rm_1", dwelling)
    room_b = _room("rm_2", dwelling.duplicate())

    assert get_dwelling_obj(room_b) is not dwelling
    assert dwelling_key(room_a) == dwelling_key(room_b)


# -----------------------------------------------------------------------------
# -- group_rooms_by_dwelling


def test_group_no_rooms():
    assert group_rooms_by_dwelling([]) == []


def test_group_single_family_home_is_one_dwelling():
    """6 Rooms sharing ONE PhDwellings object -> a single dwelling."""
    dwelling = PhDwellings(_num_dwellings=1)
    rooms = [_room("rm_{}".format(i), dwelling) for i in range(6)]

    groups = group_rooms_by_dwelling(rooms)

    assert len(groups) == 1
    assert len(groups[0]) == 6


def test_group_multifamily_distinct_dwellings():
    """4 Rooms each with their OWN PhDwellings -> four dwellings."""
    rooms = [_room("rm_{}".format(i), PhDwellings(_num_dwellings=1)) for i in range(4)]

    groups = group_rooms_by_dwelling(rooms)

    assert len(groups) == 4
    assert all(len(g) == 1 for g in groups)


def test_group_mixed_shared_and_distinct():
    shared = PhDwellings(_num_dwellings=1)
    rooms = [
        _room("rm_1", shared),
        _room("rm_2", shared),
        _room("rm_3", PhDwellings(_num_dwellings=1)),
    ]

    groups = group_rooms_by_dwelling(rooms)

    assert len(groups) == 2
    assert len(groups[0]) == 2
    assert len(groups[1]) == 1


def test_group_untagged_rooms_do_not_collapse_together():
    """Rooms still holding the default singleton must NOT be grouped as one dwelling."""
    rooms = [_room("rm_{}".format(i)) for i in range(4)]

    groups = group_rooms_by_dwelling(rooms)

    assert len(groups) == 4
    assert all(len(g) == 1 for g in groups)


def test_group_rooms_without_people_do_not_collapse_together():
    rooms = [_room_without_people("rm_{}".format(i)) for i in range(3)]

    groups = group_rooms_by_dwelling(rooms)

    assert len(groups) == 3


def test_group_ordering_is_by_first_appearance_and_stable():
    dwelling_a = PhDwellings(_num_dwellings=1)
    dwelling_b = PhDwellings(_num_dwellings=1)
    rooms = [
        _room("rm_a1", dwelling_a),
        _room("rm_b1", dwelling_b),
        _room("rm_a2", dwelling_a),
        _room("rm_b2", dwelling_b),
    ]

    groups = group_rooms_by_dwelling(rooms)

    assert [[rm.identifier for rm in g] for g in groups] == [
        ["rm_a1", "rm_a2"],
        ["rm_b1", "rm_b2"],
    ]
    # -- stable across repeated calls
    assert group_rooms_by_dwelling(rooms) == groups


# -----------------------------------------------------------------------------
# -- unique_dwelling_objects


def test_unique_dwelling_objects_dedups_by_identifier():
    dwelling = PhDwellings(_num_dwellings=1)
    rooms = [_room("rm_{}".format(i), dwelling) for i in range(6)]

    assert unique_dwelling_objects(rooms) == [dwelling]


def test_unique_dwelling_objects_ignores_untagged_rooms():
    rooms = [_room("rm_1"), _room_without_people("rm_2")]

    assert unique_dwelling_objects(rooms) == []


# -----------------------------------------------------------------------------
# -- total_dwelling_count


def test_count_no_rooms():
    assert total_dwelling_count([]) == 0


def test_count_single_family_home():
    """N Rooms -> 1 dwelling. The shared object must only be counted once."""
    dwelling = PhDwellings(_num_dwellings=1)
    rooms = [_room("rm_{}".format(i), dwelling) for i in range(6)]

    assert total_dwelling_count(rooms) == 1


def test_count_one_room_holding_many_dwellings():
    """1 Room -> N dwellings, via num_dwellings."""
    room = _room("rm_1", PhDwellings(_num_dwellings=4))

    assert total_dwelling_count([room]) == 4


def test_count_multifamily_distinct_dwellings():
    rooms = [_room("rm_{}".format(i), PhDwellings(_num_dwellings=1)) for i in range(4)]

    assert total_dwelling_count(rooms) == 4


def test_count_mixed_shared_and_distinct():
    shared = PhDwellings(_num_dwellings=2)
    rooms = [
        _room("rm_1", shared),
        _room("rm_2", shared),
        _room("rm_3", PhDwellings(_num_dwellings=3)),
    ]

    assert total_dwelling_count(rooms) == 5


def test_count_untagged_rooms_contribute_zero():
    """Untagged Rooms group alone, but must NOT be counted as dwellings."""
    rooms = [_room("rm_{}".format(i)) for i in range(4)]

    assert len(group_rooms_by_dwelling(rooms)) == 4
    assert total_dwelling_count(rooms) == 0


def test_count_rooms_without_people_contribute_zero():
    rooms = [_room_without_people("rm_{}".format(i)) for i in range(3)]

    assert total_dwelling_count(rooms) == 0
