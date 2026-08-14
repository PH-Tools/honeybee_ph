# Phase 01 — Provenance and completeness contract

## Objective

Make approved, user-defined, EPW-derived, complete, incomplete, and legacy
unknown climate states distinguishable before adding any EPW conversion path.

## Preconditions

- `independent-site-defaults` is complete and released.
- Decision 0004 remains in force.

## Implementation

1. Add `ClimateProvenance` in the site domain using plain IronPython-safe
   classes and comment-style type hints.
2. Add the optional/additive provenance slot to `Climate` and recursively copy
   it in `duplicate()`. Default/missing provenance is `None`, interpreted by
   readiness as legacy unknown, and omitted from serialization.
3. Permit `Climate.peak_loads` to be explicitly `None` while preserving the
   existing populated legacy default.
4. Define blank/non-library `PHPPCodes` construction for an EPW-derived Site;
   it must serialize as blank strings, not a real PHPP dataset identifier.
5. Add monthly-demand and peak-load readiness methods returning all issues in
   deterministic field order.
6. Audit PHX and other direct consumers for assumptions that provenance is
   absent, peak loads are always present, or PHPP codes are always populated.
   Record required downstream changes before Phase 04.

## Tests first

- Old Climate/Site dictionaries without provenance load with `None`; readiness
  reports the effective state as legacy unknown.
- Existing default `to_dict()` compatibility is pinned explicitly.
- Provenance values and `None` availability flags round-trip.
- `peak_loads=None` round-trips without becoming a zero-filled collection.
- Duplicate graphs do not share provenance, assumptions, or climate children.
- Readiness distinguishes zero-valued-but-available data from unavailable data.

## Exit checks

- Omit-when-`None` provenance serialization is captured in tests.
- No old HBJSON fixture regresses.
- Downstream assumptions and follow-up touchpoints are listed in Phase 04/05.
- No EPW parsing code has been added yet.
