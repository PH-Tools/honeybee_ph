# Bug fix: `PhEquipment.__init__` gave every equipment type the same `reference_quantity`

**Status:** Complete — archived 2026-08-25
**Kind:** Bug fix (data model; ships from this repo)
**Date:** 2026-08-25
**Author:** Ed May + Claude
**Origin:** Follow-up 4 of
[`archive/phius-mf-custom-load-reference-quantity/`](../phius-mf-custom-load-reference-quantity/README.md) §10
**Decision:** [0007 — `reference_quantity` belongs to the equipment type](../../../context/decisions/0007-reference-quantity-is-equipment-type-data.md)

---

## 1. Problem

`PhEquipment.__init__` set `self.reference_quantity = 2` ("Zone occupants") for every
subclass. Subclasses were expected to overwrite it from a `_defaults` dict, so a bare
constructor silently produced `2` — a value that is correct for exactly one of the
seventeen equipment types.

That is the mechanism behind the Phius MF defect fixed in
`honeybee_grasshopper_ph#69`: six builders transcribed the defaults field by field,
missed this one, and shipped `2` on every Phius MF export for as long as those
components existed. Fixing the six call sites left the trap armed for the next caller.

Three elevator classes had the same problem with no fix available at the call site:
they have no `ph_default_equip` entry at all, so `2` was the only value they could ever
carry.

## 2. Why a class-level default is the right shape

**The value does not vary with the standard.** PHI and PHIUS carry the *same*
`reference_quantity` for all fourteen entries in `ph_default_equip`:

| Value | Types |
|---|---|
| 1 (PH case occupants) | `PhDishwasher`, `PhClothesWasher`, `PhClothesDryer`, `PhCooktop` |
| 2 (Zone occupants) | `PhPhiusLightingGarage` |
| 3 | `PhPhiusMEL` |
| 4 (PH case Units) | `PhRefrigerator`, `PhFreezer`, `PhFridgeFreezer` |
| 5 (User defined) | `PhCustomAnnualElectric`, `PhCustomAnnualLighting`, `PhCustomAnnualMEL` |
| 6 | `PhPhiusLightingInterior`, `PhPhiusLightingExterior` |

A property identical across both standards is type data, and type data belongs on the
type. `2` was never a fallback — it was a placeholder that read like a decision.

Selector labels for `3` and `6` are not documented in `phi-rules` (the PHPP "Reference
quantity" dropdown is a different control) or in the `wufi-xml` corpus. They are left
uncommented in the source rather than guessed at. **Worth capturing in `wufi-xml` next
time someone has the WUFI GUI open.**

## 3. What changed

`honeybee_energy_ph/load/ph_equipment.py`:

- `PhEquipment` gains a class-level `DEFAULT_REFERENCE_QUANTITY`, and `__init__`
  initializes the instance attribute from `self.DEFAULT_REFERENCE_QUANTITY`.
- All seventeen subclasses declare their own value.
- The three elevator classes declare `5` ("User defined") — Ed's call, 2026-08-25. Their
  `energy_demand` is an absolute whole-building annual total (1910 / 2150 / 2940 / 4120
  kWh), `quantity = 1`, and their `display_name` is literally
  `"User defined - Misc electric loads"`. Same shape as `PhCustomAnnualMEL`, so the same
  normalization. **This is the one behavior change that reaches existing models** — see §6.

`reference_quantity` deliberately stays an **instance** attribute. Two separate
mechanisms iterate `vars()` and would silently drop a class-only attribute:
`base_attrs_from_dict` (HBJSON loading) and PHX's `build_phx_elec_device` (model
conversion).

## 4. Tests

`tests/test_honeybee_energy_ph/test_load/test_ph_equipment.py`, four new tests:

| Test | Guards |
|---|---|
| `test_reference_quantity_defaults` | The value each of the seventeen types carries from a bare constructor |
| `test_every_equipment_subclass_declares_its_own_reference_quantity` | A new subclass cannot inherit the base value |
| `test_reference_quantity_matches_the_standards_data` | The class constants and `ph_default_equip` never drift |
| `test_reference_quantity_survives_a_round_trip` | An explicitly-set value is not reset by `from_dict` |

Each was negative-tested — a synthetic subclass with no declaration, a class constant
forced out of step with the standards dict, and the original defect reintroduced. All
three fired.

## 5. Verification

1. **Unit** — ✅ 1,028 tests pass; coverage 80% against the 75% floor.
2. **Lint** — ✅ `black==26.5.1 --check` and `isort==8.0.1 --check-only` clean.
3. **IronPython 2.7** — ✅ `ph_equipment.py` parses under the `lib2to3` py2 grammar. The
   change is class-level integer constants and comments only.
4. **End to end through PHX** — ✅ every one of the seventeen types, built with a **bare
   constructor**, carries its value through `build_phx_elec_device` into the
   `<ReferenceQuantity>` node emitted by `to_WUFI_XML/xml_schemas._PhxElectricalDevice`.
   This is the check the previous packet could not run without Rhino; it runs at the
   model layer with no canvas involved.

## 6. Blast radius

Every non-test construction site in the ecosystem already passes `_defaults=`, so for
the fourteen standards-backed types the new default is a safety net rather than a
behavior change. `to_dict` has always written `reference_quantity`, so `from_dict`
restores it and no existing HBJSON is affected.

The exception is the elevators. Any model with an elevator device now exports
`ReferenceQuantity = 5` instead of `2` on re-export. Older HBJSON files still round-trip
their stored value; the change appears when a model is rebuilt.

## 7. Left open

- **Selector labels for `3` and `6`** — a two-minute look at the WUFI GUI dropdown, and
  the answer belongs in the `wufi-xml` corpus.
- **`phius_default()` returns a cached class-level singleton.** `PhEquipment` has no
  `duplicate()`, so callers share one mutable object — `set_phius_mf_res.py` appends the
  singleton straight into per-room equipment collections. **Filed 2026-08-25** as
  [`bug_fixes/phius-default-shared-singleton.md`](../../bug_fixes/phius-default-shared-singleton.md).
  Note the finding there: the shared *identifier* is load-bearing in the PHX export, so
  the obvious fix multiplies appliance and MEL energy by the room count.
- **The stray `frac_high_efficiency` attribute** set by `apply_default_attr_values` on
  the three classes that do not declare it. Pre-existing, not serialized, harmless.
