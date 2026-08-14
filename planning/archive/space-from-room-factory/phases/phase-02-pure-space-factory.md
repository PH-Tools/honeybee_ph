# Phase 02 — Pure Space factory

**Status:** Complete · 2026-08-14

## Objective

Implement the tested Room -> segment/floor/volume/Space assembly with pure
Honeybee and ladybug-geometry dependencies.

## Implementation

1. Add the IronPython-safe `Space.from_room()` classmethod and comment-style
   type hints/docstring.
2. Validate the Room type and height before constructing children.
3. Collect Honeybee Floor-type faces in source order; validate every geometry
   before returning an object.
4. For each face:
   - create a `SpaceFloorSegment` with geometry, center reference point,
     weighting factor 1.0, and net-area factor 1.0;
   - create one `SpaceFloor` holding that segment and source geometry;
   - create one `SpaceVolume` with the floor, supplied height, and faces from
     `Polyface3D.from_offset_face()`.
5. Build one `Space(_host=hb_room)`, assign the fixed name, attach all volumes,
   and return it without changing `hb_room.properties.ph.spaces`.
6. Keep attachment and Room duplication out of the factory.

## Verification

- Run all Phase 01 tests.
- Compare areas/volumes against source geometry, not only object counts.
- Confirm a failing later face leaves the input Room unchanged and returns no
  partial result.
- Black and `git diff --check` pass.

## Exit checks

- Complete focused contract suite passes.
- No Rhino-specific import or implicit conversion exists.
- V1 does not merge floors or repair topology.

## Evidence

- `.venv/bin/python -m pytest tests/test_honeybee_ph/test_space/test_Space_from_room.py -q`
  → 18 passed.
- `.venv/bin/python -m pytest tests/` → 909 passed.
- `.venv/bin/black --check honeybee_ph/space.py tests/test_honeybee_ph/test_space/test_Space_from_room.py`
  → 2 files unchanged.
- `git diff --check` → pass.
