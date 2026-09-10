---
DATE: 2026-09-10
STATUS: Scoped
AUTHOR: BLDGTYP
ISSUE: https://github.com/PH-Tools/honeybee_ph/issues/116
---

# Status — ISO 6946 mean-of-limits

Read order: [`PRD.md`](PRD.md) → [`phases/`](phases/).

| Phase | Title | Status |
|---|---|---|
| 01 | [`honeybee_ph_utils/iso_6946.py`](phases/phase-01-iso-6946-utils.md) | Scoped |
| 02 | [Construction properties and docstring correction](phases/phase-02-construction-properties.md) | Scoped |

## Next step

Phase 01.

## Blockers

None.

## Open questions

- Issue #116 as filed asks for a grid-level method that cannot exist (see the PRD). The issue
  needs retitling and a comment recording the redirect when the work lands.
- `docs/nav.yml` has no `honeybee_ph_utils` section and its `api/` pages are untracked, so there is
  no nav entry to add for `iso_6946.py`. Docstrings are written in the ph-docs format regardless.
