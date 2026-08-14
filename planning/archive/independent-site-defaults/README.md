# independent-site-defaults — router

**Status:** Complete · archived 2026-08-14 · release target `v1.33.35`

**Scope:** Remove shared mutable constructor defaults and shallow climate copies
from `honeybee_ph.site`, so every `Site`/`Climate` instance and duplicate owns an
independent nested object graph.

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `PLAN.md` — phase sequence and gates
3. `phases/phase-01-*` through `phase-03-*` — implementation handoff
4. `STATUS.md` — current state

**Origin:** confirmed during the ph-modeler POC application review (2026-08-14).

**Downstream prerequisite:** The published `honeybee-ph>=1.33.35` artifact must
be verified before work begins on
[`epw-derived-preliminary-climate`](../epw-derived-preliminary-climate/README.md).
