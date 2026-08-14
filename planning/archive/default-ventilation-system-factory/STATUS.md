# STATUS — ventilation-system-factories

**Status:** Complete · released and archived · 2026-08-14

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
- Phase 03 proves zero/one/many-duct dictionary round trips, full graph
  independence including geometry and nested metadata, explicit Room
  attachment, real HBJSON file transport, shared-system deduplication, and
  preservation of distinct system identifiers.
- Same-identifier/different-payload system graphs now fail with a targeted
  conflict instead of silently overwriting one graph during Model reload.
- Transform paths reuse metadata-only duplicates and no longer allocate and
  discard intermediate geometry graphs.
- Phase 04 gives PHX an explicit nullable assignment, mutation-free source
  preflight, aggregate Space/duct readiness, and target-specific mappings;
  OpenPH compatibility passes without fabricated equipment or duct lengths.
- Phase 05 adds the public constructor/state guide, migration guidance, and
  decision 0006; the optional preliminary preset remains deferred.
- honeybee-ph **v1.33.42** and PHX **v1.56.79** are published and pass clean
  installed-artifact smoke tests. PHX requires `honeybee-ph>=1.33.42`.
- The published compatibility matrix `honeybee-ph==1.33.42`, `PHX==1.56.79`,
  `openph==0.5.1`, and `openph-demand==0.5.0` installs and converts the
  no-mechanical, zero-duct, and multi-duct states successfully.
- Both active packets are archived. No release blocker or next implementation
  step remains in this feature.
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
- Phase 03 focused/adjacent gate: **115 tests** pass; Black, Python 2 grammar,
  and `git diff --check` pass before the full phase gate.
- Phase 03 full gate: **1016 tests** pass with **80%** aggregate coverage.
- Phase 04 affected PHX gate: **516 passed**, **3 skipped**; focused OpenPH
  **29 passed** and openph-demand **4 passed** against updated source paths.
- Phase 04 full PHX gate: **901 passed**, **3 skipped**, **1 deselected**;
  Black and `git diff --check` pass.
- Phase 04 full honeybee-ph gate: **1016 tests** pass with **80%** aggregate
  coverage.
- Phase 04 direct Honeybee → HBJSON → PHX → OpenPH matrix passes for no
  mechanical equipment and balanced systems with zero or two duct elements per
  direction.
- Phase 05 pre-release gate: both exact public examples execute independently;
  Black, Python 2 grammar parsing, and `git diff --check` pass; the full suite
  passes **1016 tests** with **80%** aggregate coverage.
