# space-from-room-factory — router

**Status:** Scoped · implementation not started

**Scope:** Upstream the "create a default PH Space from a Honeybee Room"
logic — today implemented Rhino-side in `honeybee_grasshopper_ph`
(`honeybee_ph_rhino/make_spaces/` + `gh_compo_io/space_create_from_hb_rooms.py`)
— into honeybee-ph itself as an SDK-level factory, using pure
ladybug-geometry. The GH component becomes a thin wrapper.

**Cross-repo:** this repo is the **primary** and ships first. Companion doc:
`honeybee_grasshopper_ph/planning/refactor/space-from-room-factory.md`
(re-points the component; blocked on this repo's release).

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `PLAN.md` — phase sequence and release/handoff gates
3. `phases/phase-01-*` through `phase-04-*` — implementation handoff
4. `STATUS.md` — current state

**Origin:** ph-modeler POC application review (2026-08-14), PH floor-area
construction findings (`~/Desktop/ph-modeler/APP_REVIEW.md`).
