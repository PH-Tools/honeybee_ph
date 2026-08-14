# Phase 04 — PHX/OpenPH integration

**Status:** Complete · 2026-08-14

## Objective

Remove the downstream conditions that forced callers to create device ID `0`,
blank ventilators, and two artificial 1 m ducts.

## PHX work

1. Implement the accepted explicit assignment representation; default/unset is
   not integer `0`.
2. Create a PHX ventilator only when a real source mechanical unit exists.
3. Preserve zero, one, or multiple source duct elements and their directions.
4. Validate unresolved references before export and return all issues together.
5. Keep valid existing mechanical fixtures and target writes unchanged.

## OpenPH compatibility verification

OpenPH's archived `ventilation-input-semantics` work already accepts valid
no-mechanical and zero-exterior-duct states, rejects incomplete assignments,
and implements PHPP-faithful multi-element aggregation. Do not duplicate that
implementation. Verify the updated PHX model against the completed OpenPH
contract and retain its legacy PHX `0` input test until the published PHX pin
can make that compatibility path removable.

## End-to-end matrix

For every Phase 01 state, test:

```text
Honeybee Room/HVAC -> honeybee-ph HBJSON -> PHX -> OpenPH/target
```

Prove exact device count, references, duct count/equivalent, diagnostics, and
absence of placeholders.

## Exit checks

- `Device 0 not Found` is impossible for an unassigned state.
- Valid empty duct collections calculate without fabricated lengths.
- Existing valid mechanical reference outputs remain unchanged unless a
  separately documented fidelity fix was accepted.
- Full relevant suites in honeybee-ph and PHX pass; focused OpenPH and
  openph-demand compatibility suites pass against the updated PHX model.

## Outcome

PHX now represents no Space assignment as `None`, rejects source mechanical
systems without a real ventilation unit before any mutation, and aggregates
Space plus collection-scoped duct reference issues before export. PHPP skips
unassigned lookup; WUFI/METr adapt `None` to legacy numeric `0`; WUFI import
normalizes missing/blank/`0` back to `None`. PPP, PHPP, WUFI, and METr project
entry points preflight before generating output.

The affected PHX surface passes 516 tests with 3 expected skips. Against the
updated honeybee-ph + PHX source graph, 29 focused OpenPH tests and 4
openph-demand tests pass. A direct Honeybee Room/HVAC → HBJSON → PHX → OpenPH
matrix passes for no mechanical equipment and balanced systems with zero or
two supply/exhaust ducts; no placeholder units or duct lengths are created.
The full PHX gate passes with 901 tests, 3 skipped, and 1 deselected; the full
honeybee-ph gate passes with 1,016 tests and 80% aggregate coverage. All
simplify reuse, quality, and efficiency findings were resolved.
