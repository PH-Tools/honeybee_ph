# Phase 04 — Release and Grasshopper handoff

## Objective

Release the primary implementation, re-point the GH default-space component,
and prove behavior parity before retiring duplicate orchestration.

## Primary release

1. Build/test the wheel, bump/release honeybee-ph, and record the version.
2. Install that release into the Ladybug Tools/Rhino environment and restart
   Rhino before GH verification.

## GH companion sequence

1. Raise the `honeybee_ph` minimum pin to the released version.
2. Keep GH-owned responsibilities only:
   - duplicate input Rooms;
   - convert the user-facing 2.5 m default to the Room/Rhino coordinate units;
   - call `Space.from_room(duplicated_room, converted_height)`;
   - attach the returned Space;
   - route errors/warnings through the GH interface.
3. Audit all imports of `honeybee_ph_rhino/make_spaces/`; delete only helpers
   made truly orphaned by the wrapper re-point.
4. Compare pre/post component outputs on meter and non-meter Rhino documents:
   Room count, Space names/counts, floor areas, iCFA/TFA, volumes, and HBJSON.

## Exit checks

- GH wrapper contains no duplicate default-space assembly logic.
- Meter and non-meter live definitions preserve the 2.5 m user-facing default.
- No still-imported `make_spaces` helper was removed.
- Both repo packets/statuses record the release, pin, and verification evidence.

## Evidence — 2026-08-14

- Primary PR #89 merged at `e456ca5`; release workflow 31818498356 succeeded
  and published `honeybee-ph==1.33.36` from tag/commit `3371ab2`.
- The release was installed and API-checked in the GH repo `.venv` and
  `/Users/em/ladybug_tools/python`. Rhino was not running, so no restart was
  required before the non-GUI checks.
- GH PR #61 merged at `9d2ae2a`; release workflow 31819524996 succeeded and
  published `honeybee_grasshopper_ph` v1.28.1 from `062402f`.
- Generated `requirements.txt` and `hbph_installer.ghx` both require
  `honeybee-ph>=1.33.36`.
- The wrapper now owns only Room duplication, one document-unit conversion per
  run, attachment, and IGH error routing. Import audit confirms every
  `make_spaces/` helper still has another detailed-space consumer.
- Headless meter/foot smoke verifies 2.5 m / 8.2020997375 ft heights, source
  Room non-mutation, 20 model-unit-squared floor and weighted floor area,
  volume, Room HBJSON round-trip, and no-floor/conversion error routing.
- Remaining exit check: live meter and non-meter Rhino/Grasshopper definitions,
  including multi-floor volume count and `Space.host` identity. No existing
  repo definition exercises this component, so the packet remains active.
