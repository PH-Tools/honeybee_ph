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

