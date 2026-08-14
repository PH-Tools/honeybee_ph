# epw-derived-preliminary-climate — router

**Status:** Scoped · implementation not started

**Scope:** Convert a caller-supplied EPW into a provenance-bearing,
explicitly preliminary `Site` suitable for monthly design exploration. Bundle
no weather files, claim no PHI/Phius approval, and leave certification/load
climate data explicitly unavailable.

**Read order:**

1. `PRD.md` — behavior and safety contract
2. `PLAN.md` — phase sequence and gates
3. `phases/phase-01-*` through `phase-05-*` — implementation handoff
4. `STATUS.md` — current state and next action

**Prerequisite:**
[`../independent-site-defaults/`](../independent-site-defaults/README.md) must
be complete and released first so every converted Site owns an independent
nested graph.

**Supersedes:**
[`planning/archive/climate-dataset-library/`](../../archive/climate-dataset-library/README.md).
Canonical boundary: decision
[`0004-no-bundled-licensed-climate-data`](../../../context/decisions/0004-no-bundled-licensed-climate-data.md).

