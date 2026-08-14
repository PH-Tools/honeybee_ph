# STATUS — space-from-room-factory

**Status:** Released · Phase 04 handoff substantially complete; live GH canvas
verification remains · 2026-08-14

- Phase 01 contract suite added: focused failures reproduced only the
  missing `Space.from_room()` API/import before implementation.
- Phase 02 pure-Ladybug factory implemented; all 18 focused contract tests
  pass.
- Phase 02 repository gate: 909 tests pass; Black and `git diff --check`
  pass.
- Phase 03 integration suite covers attachment/weighted area, duplicate host
  rebinding and child independence, direct Space deserialization, and Room +
  Model HBJSON round-trips; 23 focused tests pass.
- Phase 03 full gate: 914 tests pass; aggregate coverage is 79% and clears the
  user-approved 75% repository floor; Black, compatibility parser,
  `git diff --check`, sdist/wheel build, and wheel API inspection pass.
- Primary release: PR #89 merged as `e456ca5`; release workflow 31818498356
  published `honeybee-ph==1.33.36` from `3371ab2`.
- Cross-repo handoff: the GH wrapper refactor merged in PR #61 and shipped in
  `honeybee_grasshopper_ph` v1.28.1. Its generated `requirements.txt` and
  installer both require `honeybee-ph>=1.33.36`.
- Key contracts are fixed in `PRD.md`: v1 preserves one floor/volume per
  source floor face, uses the Honeybee Room as `Space.host`, normalizes the
  usual Honeybee `-Z` floor winding only for `+Z` extrusion, and rejects
  unsupported/ambiguous geometry rather than silently changing it.
- Public entry point is fixed as `Space.from_room(room,
  avg_ceiling_height)`.
- Unit contract is fixed: height is required and uses the Room geometry's
  coordinate units; the upstream factory performs no conversion.
- `docs/nav.yml` already exposes the `space` API module; no method-level nav
  entry is required. The classmethod and model-unit semantics are documented
  in source for autodoc.
- Phase 04 headless wrapper evidence covers meter/foot unit conversion, source
  Room non-mutation, floor area/volume, Room HBJSON round-trip, and IGH error
  routing. The wrapper no longer performs duplicate default-space assembly;
  all `make_spaces/` helpers remain because other detailed-space components
  still import them.
- **Next step / closeout blocker:** run the released component on meter and
  non-meter Rhino canvases and record iCFA/HBJSON parity plus the intentional
  multi-floor volume-count and `Space.host` corrections. No existing repo
  verification definition was found; headless evidence is not labeled as the
  live canvas check.
