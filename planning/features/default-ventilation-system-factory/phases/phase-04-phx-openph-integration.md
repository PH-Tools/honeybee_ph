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

## OpenPH work

1. Accept valid no-mechanical and zero-exterior-duct states.
2. Reject incomplete mechanical systems before device-property access.
3. Implement the documented PHPP-faithful multi-element rule at the target
   boundary; do not collapse the PHX model prematurely.
4. Compare Ventilation, SummVent, Heating, and Cooling cells/results against a
   controlled PHPP reference.

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
- Full relevant suites in honeybee-ph, PHX, OpenPH, and openph-demand pass.

