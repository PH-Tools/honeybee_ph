---
DATE: 2026-09-10
STATUS: Complete
AUTHOR: BLDGTYP
ISSUE: https://github.com/PH-Tools/honeybee_ph/issues/116
---

# Phase 01 — `honeybee_ph_utils/iso_6946.py`

Pure functions over an ordered list of honeybee-energy opaque materials. No honeybee host
objects, no properties plumbing: that is phase 02.

## Build

New module `honeybee_ph_utils/iso_6946.py`, IronPython 2.7 clean, ph-docs docstrings.

```python
MAX_HEAT_FLOW_PATHS = 10000

class TooManyHeatFlowPathsError(Exception): ...

def get_layer_paths(_hb_material):
    # type: (Any) -> List[Tuple[float, float]]
    """Return the [(area_fraction, r_value), ...] parallel paths through one layer."""

def get_r_value_lower_limit(_hb_materials, _r_si=0.0, _r_se=0.0):
def get_r_value_upper_limit(_hb_materials, _r_si=0.0, _r_se=0.0):
def get_r_value_mean_of_limits(_hb_materials, _r_si=0.0, _r_se=0.0):
def get_error_percent(_hb_materials, _r_si=0.0, _r_se=0.0):
def get_equivalent_conductivity(_r_value, _thickness):  # type: (float, float) -> float
```

### `get_layer_paths` rules

- `EnergyMaterialNoMass` (no `properties.ph.divisions` grid, no thickness): one path,
  `[(1.0, material.r_value)]`.
- `EnergyMaterial` with an empty grid: one path, `[(1.0, thickness / conductivity)]`.
- `EnergyMaterial` with a populated grid: one path per cell.
  `fraction = cell_area / total_cell_area`; `r = host_layer.thickness / cell_material.conductivity`.
  The **host layer's** thickness is used for every cell — the grid divides the layer in-plane
  (columns are widths, rows are heights, e.g. the top and bottom plates the wood-framing component
  writes), so every cell spans the full layer thickness.
- A cell with no assigned material, or a non-positive conductivity, falls back to the host layer's
  own material (the same fallback `PHX/model/assembly_pathways.py` uses). honeybee validates
  `conductivity > 0` on `EnergyMaterial`, so this is defensive only.
- A layer whose total cell area is zero returns the single ungridded path.

### `get_r_value_lower_limit` (isothermal planes)

Sum over layers of `1 / Σ(f_j / R_j)`. A single-path layer contributes its own R. This equals
`OpaqueConstruction.r_value` whenever each hybrid layer's material conductivity is the
area-weighted value the Grasshopper components write, but it is computed from the grid rather than
trusting that, so a hand-edited conductivity cannot skew it.

### Surface resistances

Optional `_r_si` / `_r_se`, default 0.0, added to the series sum for the lower limit and carried
**inside each path** for the upper limit, per ISO 6946 6.7.1. See the PRD's air-films section: the
two conventions are 0.011 m2K/W apart on the test wall, and this is why the argument exists rather
than the caller adding films afterwards.

### `get_r_value_upper_limit` (parallel path, staggered framing)

Iteratively accumulate the cartesian product of the per-layer paths:

```
combos = [(0.0, 1.0)]                     # (r_total, fraction)
for paths in layer_paths:
    combos = [(r + r_p, f * f_p) for (r, f) in combos for (f_p, r_p) in paths]
u = sum(f / r for (r, f) in combos if r > 0)
return 1 / u if u > 0 else 0.0
```

Before each expansion, check `len(combos) * len(paths)` against `MAX_HEAT_FLOW_PATHS` and raise
`TooManyHeatFlowPathsError` with the layer index and the running count if it would be exceeded.
Real assemblies have at most two or three gridded layers; the guard exists so a pathological model
fails loudly instead of hanging.

### The rest

- `get_r_value_mean_of_limits` = `(upper + lower) / 2`, computing the per-layer paths once.
- `get_error_percent` = `(upper - lower) / (2 * mean) * 100`, `0.0` when `mean <= 0`.
- `get_equivalent_conductivity(_r_value, _thickness)` = `thickness / r_value`, `0.0` when either is
  non-positive.
- Empty material list: every R function returns `0.0`.

## Test — `tests/test_honeybee_ph_utils/test_iso_6946.py`

One focused test per stated behavior, sized like `test_aisi_s250_21.py`:

1. Empty list returns 0.0 from each function.
2. A single uniform layer: upper == lower == `d / λ`.
3. A stack of uniform layers: upper == lower == the series sum; error percent 0.
4. One gridded layer alone: upper == lower == `d / Σ f·λ`, and equal to
   `PhDivisionGrid.get_equivalent_conductivity()` — the fact that makes issue #116's premise wrong,
   asserted so it cannot regress.
5. The PRD's stud-cavity assembly with films passed in: upper 5.029968 / lower 4.779778 / mean
   4.904873 to 1e-6.
5b. The same assembly with films added afterwards instead: upper 5.019157 / mean 4.899468 — the two
   conventions are not the same number, and the lower limit is unaffected.
6. Two gridded layers: the hand-computed cross-product R, and a path count of `n1 * n2`.
7. A `EnergyMaterialNoMass` layer contributes its `r_value` to both limits.
8. A grid with an unassigned cell falls back to the host material.
9. `MAX_HEAT_FLOW_PATHS` exceeded raises `TooManyHeatFlowPathsError`.
10. `get_equivalent_conductivity` round-trips: `t / R_mean` fed back as one layer reproduces R_mean.

## Done when

`pytest tests/test_honeybee_ph_utils/test_iso_6946.py` passes, black clean, no banned IPy 2.7
syntax.
