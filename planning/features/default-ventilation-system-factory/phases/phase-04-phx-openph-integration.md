# Phase 04 — PHX/OpenPH integration

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
