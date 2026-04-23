# Docs Expansion Plan: Add remaining packages to autodoc

**Goal**: Include `honeybee_energy_ph`, `honeybee_ph_standards`, and `honeybee_ph_utils`
in the ph-docs autodoc pipeline alongside `honeybee_ph` and `honeybee_phhvac`.

**Three workstreams**:
1. Upgrade docstrings in each package to AUTODOC format (docs/.instructions.md Section 7)
2. Update `libraries.yml` in ph-docs to add `source_paths`
3. Update `nav.yml` in this repo to include generated API reference pages

---

## Phase 1: Docstring Upgrades

### 1A. `honeybee_ph_utils` (14 modules, ~8 classes — quickest win)

- [x] `enumerables.py`
- [x] `color.py`
- [x] `input_tools.py`
- [x] `face_tools.py`
- [x] `polygon2d_tools.py`
- [x] `vector3d_tools.py`
- [x] `histogram.py` (already compliant)
- [x] `occupancy.py` (already compliant)
- [x] `schedules.py`
- [x] `ventilation.py` (already compliant)
- [x] `sky_matrix.py`
- [x] `preview.py` (already compliant)
- [x] `iso_10077_1.py`
- [x] `aisi_s250_21.py`

### 1B. `honeybee_energy_ph` (18 modules, ~83 classes — biggest package)

- [x] `boundarycondition.py`
- [x] `construction/_base.py`
- [x] `construction/thermal_bridge.py`
- [x] `construction/window.py`
- [x] `hvac/_base.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/ducting.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/fuels.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/heat_pumps.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/heating.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/hot_water.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/renewable_devices.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/supportive_device.py` (DEPRECATED — exclude from autodoc)
- [x] `hvac/ventilation.py` (DEPRECATED — exclude from autodoc)
- [x] `library/programtypes.py`
- [x] `load/_base.py`
- [x] `load/ph_equipment.py`
- [x] `load/phius_mf.py`
- [x] `load/phius_residential.py` (already compliant)

### 1C. `honeybee_ph_standards` (5 modules, ~3 classes — smallest)

- [x] `sourcefactors/factors.py`
- [x] `sourcefactors/phius_CO2_factors.py` (data-only module, no classes)
- [x] `sourcefactors/phius_source_energy_factors.py` (data-only module, no classes)
- [x] `programtypes/default_elec_equip.py` (data-only module, no classes)
- [x] `programtypes/PHIUS_programs.py` (data-only module, no classes)

## Phase 2: Config Updates

- [x] Add `source_paths` to `libraries.yml` in ph-docs
- [x] Add `exclude_modules` for properties dirs and deprecated hvac in ph-docs
- [x] `nav.yml` — no manual update needed; `generate_api_docs.py` auto-merges API Reference at build time

## Phase 3: Verify

- [x] Run `python3 -m pytest` — 726 passed
- [ ] Dry-run autodoc generator against new packages (if possible)
