# Phase 05 — Docs, downstream verification, and release

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
6. Run focused tests, `python3 -m pytest` at 100% coverage, Black, and
   `git diff --check`.
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

