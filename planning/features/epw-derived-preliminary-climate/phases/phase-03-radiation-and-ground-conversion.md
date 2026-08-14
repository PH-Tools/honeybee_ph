# Phase 03 — Radiation and ground conversion

## Objective

Complete preliminary monthly-demand inputs with documented directional solar
radiation and explicit EPW ground-temperature selection.

## Preconditions

- Phase 02 conversion result and validation framework are stable.

## Implementation

1. Build a Ladybug `Wea` from EPW direct-normal and diffuse-horizontal data.
2. Calculate vertical-plane total irradiance at azimuths 0, 90, 180, and 270
   degrees via `Wea.directional_irradiance()`.
3. Aggregate directional and global-horizontal radiation to monthly kWh/m2.
4. Validate `ground_reflectance` and `diffuse_model`; record both in
   provenance assumptions.
5. Read EPW monthly ground-temperature series and apply the PRD selection rule:
   automatic only when exactly one series exists; otherwise require the
   requested available depth.
6. Keep ground data unavailable, with a targeted issue, when the EPW supplies
   none. Do not substitute air temperature or zero.

## Tests

- Cardinal orientations map to Ladybug azimuth conventions exactly.
- Monthly Wh/m2 to kWh/m2 totals are exact for controlled fixture values.
- Isotropic/anisotropic choice and ground reflectance change results and are
  retained in provenance.
- One, zero, multiple, exact-depth, and unavailable-depth ground cases follow
  the contract.
- Every output list contains exactly 12 finite values when available.

## Exit checks

- All monthly demand fields are either valid or explicitly unavailable.
- No PHI/Phius peak-load field has been synthesized.
- Focused tests and `git diff --check` pass.

