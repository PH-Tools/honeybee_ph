# Default dwelling identity across HBJSON round-trips

**Status:** Requested — reproduced downstream, not implemented
**Opened:** 2026-08-06
**Owner:** `honeybee_energy_ph/dwellings.py`

## Defect

`get_dwelling_obj()` identifies an unset dwelling by comparing its identifier with the current
process's cached `PhDwellings.default().identifier`. That identifier is a `uuid4`. An HBJSON
round-trip preserves the original process's default identifier, but a later process creates a
different default identifier. The deserialized unset dwelling is therefore mistaken for an
explicit dwelling.

Because every originally untagged Room in the HBJSON shares that serialized identifier,
`group_rooms_by_dwelling()` pools all of those Rooms into one dwelling. Occupancy entered for
one otherwise-untagged Room can then be spread across unrelated Rooms.

## Reproduction

1. Create two Rooms whose People PH properties still use `PhDwellings.default()`
   (`num_dwellings == 0`).
2. Serialize the model to HBJSON.
3. Reset `PhDwellings._default` to simulate a new process and deserialize the model.
4. `get_dwelling_obj(room)` returns a `PhDwellings` object instead of `None`, and both Rooms
   receive the same `dwelling_key`.

PHX encountered this while implementing dwelling-group occupancy gating and works around it by
treating `num_dwellings >= 1` as the serialization-stable definition of an explicit dwelling.

## Proposed correction

Make the unset/explicit distinction serialization-stable. The smallest compatible change is to
treat `num_dwellings < 1` as unset in `_is_default_dwelling()` rather than comparing a
process-local UUID. Preserve identifier comparison only for object identity among explicit
dwellings.

Before implementation, confirm whether an explicitly authored `PhDwellings(0)` has any supported
meaning. If it does, add an explicit serialized marker instead of inferring the state from the
count; that marker must default safely when older HBJSON files are read.

## Verification

- Add a real `to_dict()` / `from_dict()` round-trip test with `PhDwellings._default` reset
  between serialization and deserialization.
- Untagged Rooms remain separate groups after the round-trip.
- Explicit Rooms sharing one dwelling identifier still group together.
- `total_dwelling_count()` remains unchanged for explicit single- and multi-dwelling objects.
- `python3 -m pytest` passes with repository-wide coverage at or above 75%.
