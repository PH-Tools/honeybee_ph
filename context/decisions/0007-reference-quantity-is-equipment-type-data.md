# 0007 — `reference_quantity` Belongs to the Equipment Type, Declared per Class

**Date:** 2026-08-25
**Status:** DECIDED
**Decider:** Ed May
**Research:** [`planning/archive/ph-equipment-reference-quantity-defaults/`](../../planning/archive/ph-equipment-reference-quantity-defaults/README.md)

## Context

`PhEquipment.__init__` set `self.reference_quantity = 2` ("Zone occupants") for
every equipment type, and each subclass was expected to overwrite it by way of a
`_defaults` dict pulled from `honeybee_ph_standards`. A caller that constructed a
subclass bare got `2` with no error and no warning.

That is exactly how the Phius multi-family MEL and lighting defect happened: six
builders in `honeybee_grasshopper_ph` transcribed the defaults one field at a time,
missed `reference_quantity`, and shipped `2` on every Phius MF export in both WUFI
XML and METr JSON for as long as those components existed. See
[`planning/archive/phius-mf-custom-load-reference-quantity/`](../../planning/archive/phius-mf-custom-load-reference-quantity/README.md).

Two facts decide the shape of the fix:

1. **The value is standard-independent.** PHI and PHIUS carry the *same*
   `reference_quantity` for all fourteen entries in `ph_default_equip`. Nothing
   about it varies with the certification standard.
2. **`2` is not a sensible fallback for anything.** No type in the standards data
   uses it except `PhPhiusLightingGarage`. As a base-class default it was a
   placeholder that read like a decision.

## Decision

1. Every concrete `PhEquipment` subclass declares its own class-level
   `DEFAULT_REFERENCE_QUANTITY`. `PhEquipment.__init__` initializes the instance
   attribute from it.
2. Inheriting `DEFAULT_REFERENCE_QUANTITY` is always a mistake, not a fallback.
   `test_every_equipment_subclass_declares_its_own_reference_quantity` fails when a
   new subclass forgets.
3. `ph_default_equip` keeps its `reference_quantity` key — it is published data with
   downstream consumers — and `test_reference_quantity_matches_the_standards_data`
   asserts the two representations never drift.
4. `reference_quantity` stays an **instance** attribute set in `__init__`. It must
   not become class-only: `base_attrs_from_dict` iterates `vars(self)`, and PHX's
   `build_phx_elec_device` iterates `vars(_hbph_device)`. A class-only attribute
   would silently drop out of both HBJSON loading and PHX conversion.
5. The three elevator classes have no `ph_default_equip` entry and now declare `5`
   ("User defined"), matching `PhCustomAnnualMEL`: their energy demand is an
   absolute whole-building annual total, not a per-occupant figure.

## Rationale

- A property that is identical across both standards is type data, and type data
  belongs on the type.
- A default that no caller should ever accept must fail loudly rather than sit there
  looking deliberate.
- Keeping the standards dict authoritative *and* tested against the class constants
  gives a single source of truth without breaking a published data structure.

## What would reopen this

- WUFI-Passive changes the meaning of a `Reference Quantity` selector value.
- Phius or PHI publish a `reference_quantity` that differs between the two standards
  for the same equipment type, which would move the value back into the defaults dict.
- A verified selector label for `3` or `6` turns up and contradicts the values the
  Phius RESNET types carry today.
