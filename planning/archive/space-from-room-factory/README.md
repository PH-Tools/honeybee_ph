# space-from-room-factory — router

**Status:** Complete · Released and live Grasshopper verification passed

**Scope:** Upstream the "create a default PH Space from a Honeybee Room"
logic — today implemented Rhino-side in `honeybee_grasshopper_ph`
(`honeybee_ph_rhino/make_spaces/` + `gh_compo_io/space_create_from_hb_rooms.py`)
— into honeybee-ph itself as an SDK-level factory, using pure
ladybug-geometry. The GH component becomes a thin wrapper.

**Cross-repo:** this repo is the **primary**. The factory shipped in
`honeybee-ph==1.33.36`; the companion wrapper shipped in
`honeybee_grasshopper_ph` v1.28.1 with a generated
`honeybee-ph>=1.33.36` pin.

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `PLAN.md` — phase sequence and release/handoff gates
3. `phases/phase-01-*` through `phase-04-*` — implementation handoff
4. `STATUS.md` — current state
5. `manual-test.ghx` — archived meter, foot, and multi-floor live verification canvas

**Origin:** ph-modeler POC application review (2026-08-14), PH floor-area
construction findings (`~/Desktop/ph-modeler/APP_REVIEW.md`).
