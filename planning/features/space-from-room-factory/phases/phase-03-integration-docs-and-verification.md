# Phase 03 — Integration, docs, and verification

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
7. Run full pytest at 100% coverage, Black, `git diff --check`, and the repo's
   IronPython compatibility checks.

## Exit checks

- Focused and full repository gates pass.
- Public docs show required height and model-unit semantics explicitly.
- The built wheel exposes `Space.from_room()`.

