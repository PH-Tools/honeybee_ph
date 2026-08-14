# STATUS — ventilation-system-factories

**Status:** In progress · Phases 01–02 complete · 2026-08-14

- Phase 01 froze the shared honeybee-ph / PHX / OpenPH state contract in
  `STATE_TABLE.md`.
- Review revised the request: the current bare unit has 0% sensible recovery
  and the current default ducts each create a physical 1 m segment. Their
  composition is not a neutral balanced-HRV default.
- Public `balanced_hrv()` signature, ownership, empty-duct, validation, and
  no-mechanical contracts are fixed in `PRD.md`.
- Accepted absence is `None` in the domain models. Numeric `0` is limited to
  required target-format adaptation and temporary legacy OpenPH input support.
- Zero exterior duct elements is a valid lossless state; multiple elements are
  preserved to the PHPP boundary and summed in the PHPP exponent.
- Existing honeybee-ph window ACH describes summer ventilation only. Primary
  PHPP K12=3 window-only authoring is explicitly deferred rather than inferred.
- Phase 02 added the IronPython-safe `balanced_hrv()` classmethod with explicit
  unit, finite/range, collection/member, and duct-direction validation.
- `None` and empty duct collections remain empty; accepted caller children and
  nested `user_data` are independently duplicated; no legacy default-duct
  helper is called and no Room attachment occurs.
- **Next step:** Phase 03 serialization, duplication, Room, Model, and HBJSON
  round-trip coverage.
- The optional preliminary preset remains deferred because no complete set of
  performance, frost, location, and duct assumptions has been accepted.
- Phase 01 gate: simplify reuse/quality/efficiency findings resolved;
  docs-pass found no broken links or stale status language;
  `.venv/bin/python -m coverage run && ... coverage report` passed with
  **966 tests** and **80%** aggregate coverage.
- Phase 02 focused gates: **38 factory tests** pass with no uncovered lines in
  the new factory/helpers; **135 adjacent factory/duct/climate tests** pass;
  Black, Python 2 grammar parsing, and `git diff --check` pass.
- Phase 02 full gate: **1004 tests** pass with **80%** aggregate coverage.
