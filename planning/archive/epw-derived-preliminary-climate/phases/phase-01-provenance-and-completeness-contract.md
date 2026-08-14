# Phase 01 — Provenance and completeness contract

**Status:** Complete · 2026-08-14

## Objective

Make approved, user-defined, EPW-derived, complete, incomplete, and legacy
unknown climate states distinguishable before adding any EPW conversion path.

## Preconditions

- The published `honeybee-ph>=1.33.35` artifact has been verified.
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

## Completion evidence

- PyPI lists `honeybee-ph 1.33.39`; the required `>=1.33.35` artifact is published.
- Focused climate and graph-independence suite: `114 passed`.
- Full coverage gate: `925 passed`, `79%` aggregate coverage.
- Black, `git diff --check`, and Python 2.7 grammar parsing pass.
- Default `Climate.to_dict()` remains provenance-free; missing peak loads retain
  the legacy populated default, while explicit unavailable peak loads serialize as null.
- `ClimateProvenance`, readiness issue ordering, zero-valued available data,
  recursive duplication, and `PHPPCodes.blank()` are pinned by focused tests.
- No EPW parser or fixture was added in this phase.

## Downstream audit

- PHX `phx/from_HBJSON/create_variant.py:417-456` dereferences all four peak-load
  records unconditionally. Before release it must call the upstream readiness
  contract and raise the specialized-data diagnostic instead of reading a null
  collection or constructing zero-filled peak loads.
- The same PHX mapping copies blank PHPP codes at lines 394-396; blank strings
  are structurally safe, but exporter behavior must be verified in Phase 05.
- No adjacent OpenPH checkout exists in this workspace; Phase 05 must verify its
  current consumer behavior from an available checkout or record that it has no
  honeybee-ph climate ingestion path.
