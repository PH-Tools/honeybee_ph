# Phase 05 — Docs, downstream verification, and release

**Status:** In progress · local implementation and downstream guard complete;
release verification pending · 2026-08-14

## Objective

Ship the EPW-derived path without bundled data, misleading certification
claims, IronPython regressions, or downstream zero fallbacks.

## Preconditions

- Phases 01–04 are implemented and focused tests pass.

## Implementation and verification

1. Update public docstrings and `docs/nav.yml` for every new public symbol.
2. Document units, directional-radiation assumptions, ground-depth selection,
   availability flags, and the non-certification boundary.
3. Inspect the built sdist/wheel and prove that no `.epw` or copied climate
   dataset is included.
4. Verify import/conversion under the supported CPython environment and run an
   IronPython syntax/import compatibility check appropriate to this repo.
5. Coordinate PHX/OpenPH behavior so `peak_loads=None` produces a targeted
   readiness diagnostic and never zero-filled load inputs.
   - PHX audit target: `phx/from_HBJSON/create_variant.py:394-456` (blank PHPP
     codes plus unconditional peak-load dereferences).
   - OpenPH: no adjacent checkout was present during Phase 01; locate and audit
     its current honeybee-ph climate ingestion path before release.
6. Run focused tests, `python3 -m pytest` at or above the 75% repository
   coverage floor, Black, and `git diff --check`.
7. Fold the stable provenance/readiness contract into `context/`, update
   `planning/STATUS.md`, release, then archive this packet only after the
   released artifact and downstream diagnostic are verified.

## Exit checks

- Wheel inspection proves no weather dataset is distributed.
- Full repository gates pass.
- PHX/OpenPH either safely consume monthly-only state or reject it precisely.
- Docs never use `approved`, `certification`, `PHPP dataset`, or `Phius
  dataset` to describe EPW-derived values except to state the exclusion.
- Release version and downstream minimum-version requirements are recorded.

## Current evidence

- Public EPW guide documents units, cardinal azimuths, radiation options,
  ground-depth selection, readiness/provenance, PHX rejection, and the
  non-certification/no-zero boundary.
- `uv build` produced the `1.33.39` development sdist and wheel in a temporary
  directory. Archive inspection found no `.epw` or copied climate dataset;
  both `honeybee_ph/_epw.py` and `honeybee_ph/site.py` are present.
- Import/conversion from the built wheel succeeds under CPython 3.10:
  monthly ready, peak not ready, `source_type=epw_derived`, `peak_loads=None`.
- Final honeybee-ph gate remains `966 passed` with `80%` aggregate coverage;
  Black, Python 2 grammar parsing, and `git diff --check` pass.
- PHX branch `codex/epw-derived-preliminary-climate-readiness`, commit
  `2e8864c`, rejects explicit monthly or peak readiness issues before any
  substantive variant builder. Legacy populated climate remains supported and
  blank PHPP codes remain blank.
- PHX verification: `881 passed, 3 skipped, 1 deselected` against its locked
  `honeybee-ph`; 5 focused tests also pass against this feature checkout.
- OpenPH workspace audit found no direct honeybee-ph climate ingestion. Its
  canonical path consumes a PHX `PhxVariant`; the new PHX boundary rejects the
  monthly-only state before OpenPH construction.
- Expected upstream release target is `honeybee-ph==1.33.40`. Before the PHX
  branch merges/releases, its downstream minimum must be raised to
  `honeybee-ph>=1.33.40` and locked against the published artifact.
- Remaining blocker: merge/release authorization, published-artifact
  verification, PHX pin/release verification, then packet archive.
