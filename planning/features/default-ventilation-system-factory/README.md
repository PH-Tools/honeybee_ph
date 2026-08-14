# ventilation-system-factories — router

**Status:** In progress · Phases 01–03 complete

**Scope:** Explicit constructors for valid ventilation states in
`honeybee_phhvac`, including a balanced HRV/ERV system without invented duct
lengths and a clearly named preliminary-model preset when one is genuinely
needed.

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `STATE_TABLE.md` — accepted cross-repo source/target contract
3. `PLAN.md` — cross-repo phase sequence and gates
4. `phases/phase-01-*` through `phase-05-*` — implementation handoff
5. `STATUS.md` — current state

**Origin:** ph-modeler POC application review (2026-08-14), ventilation and
duct-default findings (`~/Desktop/ph-modeler/APP_REVIEW.md`).
