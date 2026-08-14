# climate-dataset-library — superseded router

**Status:** Superseded 2026-08-14 by
[`epw-derived-preliminary-climate`](../epw-derived-preliminary-climate/README.md).

**Scope:** Ship real PHPP climate-dataset *values* inside honeybee-ph and add a
one-line constructor (`Site.from_dataset("US0055c-New York")`), so a
programmatically-built model gets a usable climate without hand-plumbing ~40
attributes.

**Read order:**
1. `PRD.md` — what / why (behavior contract)
2. `STATUS.md` — current state

**Outcome:** Do not bundle or redistribute PHI/Phius climate datasets without
an explicit redistribution grant. The replacement feature converts a
user-supplied EPW into clearly labeled preliminary monthly climate data and
does not claim certification approval or synthesize PHI/Phius peak-load data.

See decision
[`0004-no-bundled-licensed-climate-data`](../../../context/decisions/0004-no-bundled-licensed-climate-data.md).
