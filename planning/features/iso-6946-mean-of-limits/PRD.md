---
DATE: 2026-09-10
STATUS: Scoped
AUTHOR: BLDGTYP
ISSUE: https://github.com/PH-Tools/honeybee_ph/issues/116
---

# ISO 6946 mean-of-limits U-value for opaque constructions

## Why

Issue #116 asks `PhDivisionGrid` to carry the ISO 6946 mean of the upper and lower
resistance limits instead of only the area-weighted (claimed "lower limit") value, so that a
consumer reading the grid gets what designPH and PHPP report.

**The issue's premise does not hold.** For a single layer taken alone the two ISO 6946 §6.7
limits are the same number:

- upper limit (parallel path): each path is one section, `R_j = d / λ_j`, combined in parallel by
  area, so `1/R = Σ f_j·λ_j / d`.
- lower limit (isothermal planes): the layer is blended in parallel first, which is the same
  `1/R = Σ f_j·λ_j / d`.

Both give `R = d / Σ f_j·λ_j`, i.e. the area-weighted conductivity that
`PhDivisionGrid.get_equivalent_conductivity()` already returns. Verified numerically for a 38 mm
stud at 406 mm o.c. in 140 mm mineral wool: both limits return λ_eq = 0.046602 W/mK, bit-identical.
The grid's rows are in-plane too (the wood-framing component writes top and bottom plates into
rows), so every cell in a grid is a parallel path; nothing in the grid is in series.

The divergence the issue is chasing is a property of the **layer stack**, not of one layer. The
upper limit needs each path carried through *all* layers before the parallel combination. Same
cavity inside 12.7 gyp / 12.7 OSB / 50 EPS, films included:

| Limit | R [m²K/W] | U [W/m²K] |
|---|---|---|
| upper | 5.0300 | 0.1988 |
| lower | 4.7798 | 0.2092 |
| mean | 4.9049 | 0.2039 |

Reading the lower limit alone is 2.6 % pessimistic on U for that assembly. The cavity λ that would
make a plain series sum reproduce the mean is 0.04474 W/mK, not 0.04660 — and that value depends on
the other layers, so it cannot be stored on the layer's material either. The SketchUp record says
the same thing in its own words (E4-4, 2026-09-10): "a per-layer equivalent carries only the
isothermal limit, the whole-assembly value carries the mean of limits, which is what PHPP does."

So the capability is real and wanted; it belongs one level up, on the construction.

## What ships

An additive, read-only calculation on the opaque construction. No serialization change, no new
stored field, no change to any existing return value.

1. `honeybee_ph_utils/iso_6946.py` — pure functions over a list of honeybee-energy materials,
   in the same house style as `iso_10077_1.py` and `aisi_s250_21.py`:
   upper limit, lower limit, mean of limits, and designPH's Error %.
2. Read-only properties on `honeybee_energy_ph.properties.construction.opaque.OpaqueConstructionPhProperties`,
   which owns a host `OpaqueConstruction` and can therefore see the whole layer stack.
3. A docstring correction on `PhDivisionGrid.get_equivalent_conductivity()` naming what it
   actually returns, so the "lower limit" reading in the two exporters stops propagating.

### Public API

On `OpaqueConstructionPhProperties` (all materials-only, no air films, matching honeybee's
`r_value` / `u_value` convention; `r_factor` / `u_factor` are the film-inclusive names and are
deliberately not shadowed here):

| Member | Returns |
|---|---|
| `r_value_upper_limit` | ISO 6946 parallel-path R [m²K/W] |
| `r_value_lower_limit` | ISO 6946 isothermal-planes R [m²K/W] |
| `r_value_mean_of_limits` | mean of the two [m²K/W] |
| `u_value_mean_of_limits` | `1 / r_value_mean_of_limits` [W/m²K] |
| `iso_6946_error_percent` | `(R_upper - R_lower) / (2·R_mean) · 100`, the Error % designPH prints |
| `equivalent_conductivity_mean_of_limits` | `host.thickness / r_value_mean_of_limits` [W/mK] — the single equivalent layer for a whole assembly |

### Framing alignment

The upper limit reads framing in different layers as **staggered**: the paths are the cartesian
product of each gridded layer's cell fractions. Decided by Ed, 2026-09-10.

This matches the PH-Navigator web app and the SketchUp editor (`Assemblies::Thermal.parallel`),
works for row grids and column grids alike, and assumes nothing about bays in different layers
lining up. The alternative aligned reading — intersect the layers' column boundaries
geometrically, as `PHX/model/assembly_pathways.py` and designPH's packing do — is measured up to
0.0042 W/m²K away from it (SketchUp E4 record) and is not implemented here. The docstring says
which reading is in force.

## Air films

Found during phase 01, and it changes the API: ISO 6946 6.7.1 carries Rsi and Rse **inside** each
upper-limit path, so adding films to a film-free upper limit afterwards is not the same number. On
the wall above the two readings are 0.011 m2K/W apart (upper 5.0300 with films inside, 5.0192 with
them added after), which is 0.0002 W/m2K on U. The lower limit is unaffected either way.

`iso_6946.py` therefore takes optional `_r_si` / `_r_se` arguments, defaulting to 0.0:

- default (film-free): what the PH-Navigator web app and the SketchUp editor's `Thermal.effective`
  compute, and what the construction-level properties return, since an `OpaqueConstruction` does
  not know its own exposure.
- with films passed: the strict ISO 6946 value, which is what designPH's packed reading
  (`Thermal.packed`) and PHPP report.

## Out of scope
- Any change to what `get_equivalent_conductivity()` returns, or to `to_dict`/`from_dict` anywhere.
- Steel-stud correction (`is_a_steel_stud_cavity`, `steel_stud_spacing_mm` stay preview-only).
- PHX. Its `assembly_pathways.py` implements the aligned reading and keeps it; converging the two
  is a separate cross-repo item.

## Acceptance

- A uniform (ungridded) construction returns `r_value_upper_limit == r_value_lower_limit ==
  host.r_value`, and `iso_6946_error_percent == 0`.
- A single-gridded-layer construction reproduces the hand-computed table above to 1e-6.
- A two-gridded-layer construction produces the cross-product path count and the hand-computed R.
- `equivalent_conductivity_mean_of_limits` fed back as a single layer of `host.thickness`
  reproduces `u_value_mean_of_limits`.
- The values agree with the SketchUp editor's `Thermal.effective` on one synthetic framed assembly.
- IronPython 2.7 clean, black clean, coverage floor held.
