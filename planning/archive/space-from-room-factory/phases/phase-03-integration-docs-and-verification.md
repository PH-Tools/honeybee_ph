# Phase 03 — Integration, docs, and verification

**Status:** Complete · 2026-08-14

## Objective

Prove the factory through the actual Room property, duplication, and HBJSON
paths and expose one documented public entry point.

## Implementation and tests

1. Explicitly attach a factory-built Space with
   `room.properties.ph.add_new_space()` and verify iCFA/TFA aggregation.
2. Duplicate the Room and prove Space host identity is rebound to the duplicated
   Honeybee Room while volumes/floors/segments are independent.
3. Round-trip a complete Room/Model HBJSON carrying the factory-built Space.
4. Verify `Space.from_dict(..., _host=room)` and factory host contracts agree.
5. Add public docstring coverage and update `docs/nav.yml` for the new
   classmethod.
6. Update `SpaceVolume.avg_ceiling_height` documentation from an unconditional
   meters claim to model/geometry units, matching existing scale behavior.
7. Run full pytest at or above the 75% repository coverage floor, Black,
   `git diff --check`, and the repo's
   IronPython compatibility checks.

## Exit checks

- Focused and full repository gates pass.
- Public docs show required height and model-unit semantics explicitly.
- The built wheel exposes `Space.from_room()`.

## Evidence

- `.venv/bin/python -m pytest tests/test_honeybee_ph/test_space/test_Space_from_room.py -q`
  → 23 passed.
- `docs/nav.yml` already lists `api/space.md`; autodoc discovers the new
  classmethod from its public source docstring, so no method-level nav entry
  exists to add.
- Full coverage run → 914 passed; 79% aggregate coverage clears the configured
  75% repository floor.
- Black, `git diff --check`, and the compatibility parser pass.
- `uvx --from build pyproject-build` successfully built the 1.33.35 sdist and
  wheel; wheel inspection finds `Space.from_room()` and its model-unit
  contract.
