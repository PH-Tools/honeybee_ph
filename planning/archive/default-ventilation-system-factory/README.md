# ventilation-system-factories — router

**Status:** Complete · released and archived · 2026-08-14

**Scope:** Explicit constructors for valid ventilation states in
`honeybee_phhvac`, including a balanced HRV/ERV system without invented duct
lengths. A preliminary-model preset is explicitly deferred until its complete
assumption set is separately accepted.

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `STATE_TABLE.md` — accepted cross-repo source/target contract
3. `PLAN.md` — cross-repo phase sequence and gates
4. `phases/phase-01-*` through `phase-05-*` — implementation handoff
5. `STATUS.md` — current state

**Origin:** ph-modeler POC application review (2026-08-14), ventilation and
duct-default findings (`~/Desktop/ph-modeler/APP_REVIEW.md`).
