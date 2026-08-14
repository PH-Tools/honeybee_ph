# Phase 03 — Integration, docs, and release

**Status:** Pending

## Objective

Prove the fix through host-object/HBJSON paths, document the ownership rule,
and release the prerequisite needed by EPW conversion.

## Implementation and verification

1. Test Site graphs carried by `BldgSegment`, Room properties, duplication,
   and complete HBJSON round-trips.
2. Run the full repository suite at 100% coverage and warnings-as-errors.
3. Run Black, `git diff --check`, and an IronPython 2.7 syntax/import audit.
4. Update affected public docstrings; update `docs/nav.yml` only if a public
   symbol was added or renamed (none expected).
5. Record the constructor ownership rule in canonical context documentation if
   it is not already explicit.
6. Build the wheel and run a clean-environment smoke test against the built
   artifact.
7. Release, record the version in this packet and the EPW prerequisite, update
   `planning/STATUS.md`, then archive only after artifact verification.

## Exit checks

- Full suite passes at 100% coverage.
- Default serialization snapshots remain unchanged.
- Built artifact reproduces independent default/duplicate graphs.
- `epw-derived-preliminary-climate` records the released minimum version and is
  unblocked.
