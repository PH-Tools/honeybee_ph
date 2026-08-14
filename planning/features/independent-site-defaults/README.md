# independent-site-defaults — router

**Status:** In progress · Phases 01–02 complete; Phase 03 next

**Scope:** Remove shared mutable constructor defaults and shallow climate copies
from `honeybee_ph.site`, so every `Site`/`Climate` instance and duplicate owns an
independent nested object graph.

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `PLAN.md` — phase sequence and gates
3. `phases/phase-01-*` through `phase-03-*` — implementation handoff
4. `STATUS.md` — current state

**Origin:** confirmed during the ph-modeler POC application review (2026-08-14).

**Downstream prerequisite:** This feature must ship before
[`../epw-derived-preliminary-climate/`](../epw-derived-preliminary-climate/README.md).
