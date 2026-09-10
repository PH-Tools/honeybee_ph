---
DATE: 2026-09-10
STATUS: Complete
AUTHOR: BLDGTYP
ISSUE: https://github.com/PH-Tools/honeybee_ph/issues/116
---

# Status — ISO 6946 mean-of-limits

Read order: [`PRD.md`](PRD.md) → [`phases/`](phases/).

| Phase | Title | Status |
|---|---|---|
| 01 | [`honeybee_ph_utils/iso_6946.py`](phases/phase-01-iso-6946-utils.md) | Complete |
| 02 | [Construction properties and docstring correction](phases/phase-02-construction-properties.md) | Complete |

Merged to `main` 2026-09-10 as [#117](https://github.com/PH-Tools/honeybee_ph/pull/117); issue #116
retitled and closed with the redirect recorded on it.

## Next step

None here. A follow-up in `ph-navigator-sketchup` (E4-1) can drop both exporters' local
mean-of-limits math once this is released to PyPI.

## Verification

- 1,072 tests pass; repository coverage 81 % against the 75 % floor; `iso_6946.py` at 91 %.
- The construction properties agree with the SketchUp editor's `Thermal.effective` to six decimals
  on the PRD's framed wall (R 4.729468, U 0.211440). Evidence in the phase 02 doc.

## Blockers

None.

## Open questions

- Issue #116 as filed asks for a grid-level method that cannot exist (see the PRD). The issue
  needs retitling and a comment recording the redirect when the work lands.
- `OpaqueConstructionPhProperties.__init__` keeps its `_host=None` default, so the new properties
  raise `OpaqueConstructionPhProperties_NoHostError` rather than the host being guaranteed at
  construction time (`WindowConstructionPhProperties` requires one). Tightening it would change a
  published constructor signature: left as a follow-up, not done here.
- `docs/nav.yml` has no `honeybee_ph_utils` section and its `api/` pages are untracked, so there is
  no nav entry to add for `iso_6946.py`. Docstrings are written in the ph-docs format regardless.
