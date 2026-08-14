# STATUS — space-from-room-factory

**Status:** Implementing · Phase 03 complete; Phase 04 next · 2026-08-14

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
- Cross-repo: **this repo is primary and ships first.** The GH-side wrapper
  refactor (`honeybee_grasshopper_ph/planning/refactor/space-from-room-factory.md`)
  is blocked on this repo's release + pin bump.
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
- **Next step:** execute Phase 04 primary release and the blocked Grasshopper
  wrapper handoff.
- Blockers: none.
