# Phase 04 — Site integration and readiness

**Status:** Complete · 2026-08-14

## Objective

Expose the supported one-call API and prove that EPW-derived state remains
honest through duplication and HBJSON.

## Preconditions

- Temperature, radiation, ground-selection, provenance, and issue collection
  are complete.

## Implementation

1. Add `Site.from_epw()` with the exact PRD arguments and return type.
2. Build fresh `Location`, `Climate`, monthly collections, ground data,
   provenance, and blank `PHPPCodes` on every call.
3. Set `peak_loads=None` and `peak_load_data_available=False` unconditionally
   for the EPW-only path.
4. Make monthly readiness fail if any required source/derived value is absent;
   make peak-load readiness fail with the specialized-data diagnostic.
5. Round-trip the result through Site/BuildingSegment/Room HBJSON and duplicate
   each host path without shared children.
6. Update any in-repo consumer that assumes non-null peak loads or nonblank
   PHPP codes; do not make downstream exporters invent values.

Downstream touchpoint identified in Phase 01: PHX
`phx/from_HBJSON/create_variant.py:417-456` unconditionally dereferences the
four peak-load sets. Its HBJSON conversion boundary must reject monthly-only
climates with `Climate.peak_load_readiness_issues()` before those reads.

## Tests

- End-to-end EPW -> Site -> dict -> Site preserves values and provenance.
- Two calls from one file are recursively independent.
- A Room/BuildingSegment carrying the result round-trips.
- Monthly readiness succeeds for the complete fixture.
- Peak-load readiness always fails for EPW-only conversion.
- No output contains `US0055c-New York` or another PHI/Phius identifier unless
  it came through a separately supplied authorized record outside this API.

## Exit checks

- `Site.from_epw()` is the only public one-call EPW entry point.
- Serialization is backward compatible and explicit for new unavailable data.
- Downstream changes required for safe conversion are implemented or block
  release in Phase 05.

## Completion evidence

- `52 passed` across converter, public integration, and readiness tests.
- `Site.from_epw()` forwards every documented option and returns a fresh graph.
- JSON encoding with `allow_nan=False`, Site/BuildingSegment/Room paths,
  duplication, and mutation isolation pass.
- EPW output uses `climate_zone=None`, blank PHPP codes, and `peak_loads=None`;
  no source field is invented from a legacy default.
- Repository audit found no additional in-repo peak-load or PHPP-code consumer;
  the PHX boundary remains the Phase 05 release blocker.
- Full repository suite: `966 passed`; aggregate coverage: `80%`.
- Black, Python 2 grammar parsing, and `git diff --check` pass.
