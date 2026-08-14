# STATUS — ventilation-system-factories

**Status:** In progress · Phase 01 complete · 2026-08-14

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
- **Next step:** Phase 02 tests-first implementation of `balanced_hrv()` and
  its field/direction validation.
- The optional preliminary preset remains deferred because no complete set of
  performance, frost, location, and duct assumptions has been accepted.
- Phase 01 gate: simplify reuse/quality/efficiency findings resolved;
  docs-pass found no broken links or stale status language;
  `.venv/bin/python -m coverage run && ... coverage report` passed with
  **966 tests** and **80%** aggregate coverage.
