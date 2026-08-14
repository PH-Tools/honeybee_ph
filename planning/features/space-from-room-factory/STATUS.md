# STATUS — space-from-room-factory

**Status:** Scoped · 2026-08-14

- Filed from the ph-modeler POC architecture review; implementation not
  started.
- Cross-repo: **this repo is primary and ships first.** The GH-side wrapper
  refactor (`honeybee_grasshopper_ph/planning/refactor/space-from-room-factory.md`)
  is blocked on this repo's release + pin bump.
- Key contracts are now fixed in `PRD.md`: v1 preserves one floor/volume per
  source floor face, uses the Honeybee Room as `Space.host`, and rejects
  unsupported/ambiguous geometry rather than silently changing it.
- Public entry point is fixed as `Space.from_room(room,
  avg_ceiling_height)`.
- Unit contract is fixed: height is required and uses the Room geometry's
  coordinate units; the upstream factory performs no conversion.
- **Next step:** execute Phase 01 contract tests, including meter/foot-scaled
  geometry and unsupported floor geometry, before adding the classmethod.
- Blockers: none.
