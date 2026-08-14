# Phase 04 — Site integration and readiness

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

