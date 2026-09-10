---
DATE: 2026-09-10
STATUS: Scoped
AUTHOR: BLDGTYP
ISSUE: https://github.com/PH-Tools/honeybee_ph/issues/116
---

# Phase 02 — construction properties and the docstring correction

Expose phase 01 where a caller already has the object: the PH properties of an
`OpaqueConstruction`.

## Build

### `honeybee_energy_ph/properties/construction/opaque.py`

Six read-only members on `OpaqueConstructionPhProperties`, delegating to `honeybee_ph_utils.iso_6946`:

| Member | Returns |
|---|---|
| `r_value_upper_limit` | ISO 6946 parallel-path R [m²K/W] |
| `r_value_lower_limit` | ISO 6946 isothermal-planes R [m²K/W] |
| `r_value_mean_of_limits` | mean of the two [m²K/W] |
| `u_value_mean_of_limits` | `1 / r_value_mean_of_limits`, `0.0` when R is non-positive |
| `iso_6946_error_percent` | designPH's Error % |
| `equivalent_conductivity_mean_of_limits` | `host.thickness / r_value_mean_of_limits` [W/mK] |

All are materials-only (no air films), matching honeybee's `r_value` / `u_value` convention;
`r_factor` / `u_factor` mean film-inclusive in honeybee and are not shadowed. Each docstring states
that the upper limit reads framing as staggered, and that the caller adds Rsi/Rse.

A property called with `self.host is None` raises `ValueError` naming the property — these read the
whole layer stack and have no meaningful answer without one. No silent zeros.

Import `honeybee_ph_utils` defensively at module top in the repo's house style
(`try: ... except ImportError as e: raise ImportError(...)`).

Serialization is untouched: nothing new is stored, `to_dict`/`from_dict`/`__copy__` are unchanged,
and every existing HBJSON still loads.

### `honeybee_energy_ph/properties/materials/opaque.py`

Docstring only on `PhDivisionGrid.get_equivalent_conductivity()`: it returns the ISO 6946 value for
the layer, where the upper and lower limits coincide because every cell in the grid is a parallel
in-plane path. Point at `OpaqueConstructionPhProperties.r_value_mean_of_limits` for the
assembly-level number. No behavior change.

## Test — `tests/test_honeybee_energy_ph/test_properties/test_construction/test_opaque.py`

Added to the existing file, sized like its neighbors:

1. Uniform construction: upper == lower == `construction.r_value`, error percent 0.
2. Framed construction (the PRD's assembly): the three R values and the error percent.
3. `equivalent_conductivity_mean_of_limits` fed back as a one-layer construction reproduces
   `u_value_mean_of_limits` to 1e-6.
4. A hostless properties object raises `ValueError`.
5. HBJSON round-trip of a construction carrying a framed layer returns the same three values —
   the additive-change guarantee.

## Cross-check against the SketchUp editor

Not a committed test: a scratch run comparing `u_value_mean_of_limits` plus films against
`Bldgtyp::PhNavigatorSketchup::Assemblies::Thermal.effective` on the PRD's assembly. Record the two
numbers in this file when it passes.

## Closeout

- `python3 -m coverage run && python3 -m coverage report` at or above the 75 % floor.
- `black` clean.
- `planning/STATUS.md` gets a row; this packet's `STATUS.md` moves to `Implemented on branch`.
- Comment on issue #116 with the redirect (grid-level limits are identical; the capability shipped
  on the construction) and retitle it to match what was built.
- No `context/` decision record: nothing was closed off that the PRD does not already carry.
