# Phase 01 — Cross-repo ventilation state contract

**Status:** Complete · 2026-08-14

## Objective

Derive one reviewed state table for honeybee-ph, PHX, PHPP/WUFI export, and
OpenPH before naming factories or encoding absence.

## Required research

1. Read the applicable PHPP Ventilation/SummVent inputs and WUFI/METr
   assignment constraints.
2. Define, for each supported system type:
   - whether a mechanical device is required, optional, or forbidden;
   - whether supply/exhaust exterior ducts are optional or required;
   - the target meaning of zero exterior duct length;
   - how multiple duct elements/segments are preserved or aggregated;
   - how natural/window and no-mechanical states are represented.
3. Reconcile these packets so they describe the same contract:
   - this packet;
   - `PHX/planning/archive/ventilation-assignment-semantics/`;
   - `openph-workspace/planning/archive/dated/2026-08-14/ventilation-input-semantics/`.
4. Remove the stale OpenPH planning statement that describes the honeybee-ph
   factory as a default ventilator plus default ducts.

## Minimum accepted source matrix

| Source state | honeybee-ph representation | Required result |
|---|---|---|
| No mechanical system | Room ventilation system is `None` | no device, no device ID |
| Natural/window ventilation | existing explicit non-mechanical source data | no mechanical device |
| Balanced HRV/ERV with device, no exterior ducts | `balanced_hrv(unit, [], [])` | valid mechanical assignment; zero duct loss |
| Balanced with one/many duct elements | factory with typed duct collections | preserve elements until target boundary |
| Mechanical system missing device | invalid/incomplete source | targeted diagnostic; no placeholder |
| Unresolved device reference | invalid downstream state | diagnostic naming Space and device |

## Exit checks

- State names and meanings are accepted across all three repos.
- `0` is not the absence sentinel anywhere in the accepted contract.
- No 1 m duct or zero-recovery device is a fallback.
- Target-specific aggregation formulas are cited or explicitly deferred.
- The local `balanced_hrv()` signature in the PRD remains compatible with the
  accepted matrix.

## Outcome

All exit checks are recorded in `../STATE_TABLE.md`. The accepted model uses
`None` for no assignment, optional empty exterior-duct collections, and
PHPP-faithful multi-element aggregation. Summer window ACH remains supported;
primary PHPP K12=3 window-only authoring is deferred because honeybee-ph has no
source field carrying that choice. The optional preliminary preset is also
deferred pending accepted physical assumptions.

Verification: the three simplify reviews were resolved, docs-pass found no
broken links or stale status statements, and the full honeybee-ph coverage gate
passed with 966 tests and 80% aggregate coverage. The coordinated PHX full gate
passed with 881 tests, 3 skipped, and 1 deselected.
