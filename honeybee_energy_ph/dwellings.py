# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Helpers for grouping Honeybee-Rooms into 'Dwellings'.

A 'Dwelling' is a household: the unit that Phius occupancy, lighting, appliance,
and hot-water calculations are normalized against. Dwelling identity is carried by
the `PhDwellings` object attached to a Room's HBE-People load:

    room.properties.energy.people.properties.ph.dwellings

Rooms that belong to the same dwelling share the *same* `PhDwellings` instance, so
identity is compared on `PhDwellings.identifier`. A single Room may also contain
several dwellings, in which case `PhDwellings.num_dwellings` is > 1. Both directions
matter:

    * N Rooms -> 1 dwelling   : one shared PhDwellings, num_dwellings == 1
    * 1 Room  -> N dwellings  : its own PhDwellings, num_dwellings == N

IMPORTANT: Dwelling identity must NOT be stored on `Room.zone`. That attribute is
read by honeybee-energy as an EnergyPlus thermal-zone grouping instruction: Rooms
sharing a `zone` value are merged into a single E+ Zone (with `Space` objects inside
it) and served by a single HVAC system. Using it as a dwelling tag silently changes
the physics of the energy model.
"""

try:
    from typing import Optional
except ImportError:
    pass  # IronPython 2.7

try:
    from honeybee.room import Room
except ImportError as e:
    raise ImportError("Failed to import honeybee: {}".format(e))

try:
    from honeybee_energy_ph.properties.load.people import PhDwellings
except ImportError as e:
    raise ImportError("Failed to import honeybee_energy_ph: {}".format(e))


def _is_default_dwelling(_dwelling):
    # type: (PhDwellings) -> bool
    """Is this the shared class-level 'default' PhDwellings object?

    `PeoplePhProperties.__init__` assigns `PhDwellings.default()` -- a single cached
    instance -- to every People load. So EVERY Room that has never been passed through
    the 'HBPH - Set Dwelling' component carries the same dwelling identifier. Those
    Rooms are 'untagged', not 'all one dwelling', and must not be grouped together.

    Compared by identifier rather than by `is`, since `PhDwellings.duplicate()` and
    `from_dict()` both produce new objects that keep the original identifier.
    """
    return _dwelling.identifier == PhDwellings.default().identifier


def get_dwelling_obj(_hb_room):
    # type: (Room) -> Optional[PhDwellings]
    """Return the HB-Room's PhDwellings object, or None if it has no dwelling set.

    Returns None when the Room has no energy properties, no People load, or is still
    carrying the un-set 'default' PhDwellings object.
    """
    prop_energy = getattr(_hb_room.properties, "energy", None)
    if prop_energy is None:
        return None

    people = getattr(prop_energy, "people", None)
    if people is None:
        return None

    prop_ph = getattr(people.properties, "ph", None)
    if prop_ph is None:
        return None

    dwelling = getattr(prop_ph, "dwellings", None)
    if dwelling is None:
        return None

    if _is_default_dwelling(dwelling):
        return None

    return dwelling


def dwelling_key(_hb_room):
    # type: (Room) -> str
    """Return the grouping key which identifies the dwelling an HB-Room belongs to.

    Rooms without a dwelling set fall back to their own identifier so that they group
    alone, rather than collapsing together into one spurious shared dwelling.
    """
    dwelling = get_dwelling_obj(_hb_room)
    if dwelling is None:
        return _hb_room.identifier
    return dwelling.identifier


def group_rooms_by_dwelling(_hb_rooms):
    # type: (list[Room]) -> list[list[Room]]
    """Group HB-Rooms into dwellings.

    Rooms sharing a PhDwellings object are returned together. Rooms with no dwelling
    set are each returned in a group of their own. Groups are ordered by first
    appearance, and Rooms keep their input order within each group, so that the
    result is stable across runs.

    Arguments:
    ----------
        * _hb_rooms (list[Room]): The HB-Rooms to group.

    Returns:
    --------
        * (list[list[Room]]): The groups of HB-Rooms, one group per dwelling.
    """
    ordered_keys = []  # type: list[str]
    groups = {}  # type: dict[str, list[Room]]

    for hb_room in _hb_rooms:
        key = dwelling_key(hb_room)
        if key not in groups:
            groups[key] = []
            ordered_keys.append(key)
        groups[key].append(hb_room)

    return [groups[k] for k in ordered_keys]


def unique_dwelling_objects(_hb_rooms):
    # type: (list[Room]) -> list[PhDwellings]
    """Return the unique PhDwellings objects found across a set of HB-Rooms.

    De-duplicated by identifier and ordered by first appearance. Rooms with no
    dwelling set contribute nothing.

    Arguments:
    ----------
        * _hb_rooms (list[Room]): The HB-Rooms to collect the dwellings from.

    Returns:
    --------
        * (list[PhDwellings]): The unique PhDwellings objects.
    """
    seen = set()  # type: set[str]
    dwellings_ = []  # type: list[PhDwellings]

    for hb_room in _hb_rooms:
        dwelling = get_dwelling_obj(hb_room)
        if dwelling is None:
            continue
        if dwelling.identifier in seen:
            continue
        seen.add(dwelling.identifier)
        dwellings_.append(dwelling)

    return dwellings_


def total_dwelling_count(_hb_rooms):
    # type: (list[Room]) -> int
    """Return the total number of dwelling units across a set of HB-Rooms.

    Sums `num_dwellings` over the UNIQUE PhDwellings objects, so that a dwelling
    spanning several Rooms is counted once. Rooms with no dwelling set contribute
    zero -- they are not counted as dwellings of their own.

    Arguments:
    ----------
        * _hb_rooms (list[Room]): The HB-Rooms to count the dwellings of.

    Returns:
    --------
        * (int): The total number of dwelling units.
    """
    return sum(int(d.num_dwellings) for d in unique_dwelling_objects(_hb_rooms))
