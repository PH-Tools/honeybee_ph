# Bug fix: Phius MF custom MEL/Lighting loads export `reference_quantity = 2`

**Status:** Complete — archived 2026-08-25. Fix merged to `honeybee_grasshopper_ph` `main` in [PR #69](https://github.com/PH-Tools/honeybee_grasshopper_ph/pull/69) (`25a8d92`). Two follow-ups outlive this packet and are tracked in that repo's `planning/STATUS.md` — see §10.
**Kind:** Bug fix (cross-repo; **fix lands in `honeybee_grasshopper_ph`**, data owned here)
**Date:** 2026-08-25
**Author:** Ed May + Claude
**Found via:** WUFI-XML diff on 2441 Arverne East Building D, comparing a hand-edited
certification model against a fresh Grasshopper export.

---

## 1. Problem statement

The two Phius multi-family room-load components build their MEL and lighting objects with
bare constructors, so the objects keep the `PhEquipment` base-class value
`reference_quantity = 2` ("Zone occupants") instead of the value the Phius standards data
specifies for them, `5` ("User defined").

Every Phius MF model exported through these components carries six devices with the wrong
reference quantity:

| Comment | Class | Built by |
|---|---|---|
| `MEL_Dwelling` | `PhCustomAnnualMEL` | `set_phius_mf_res.py::build_mel` |
| `LIGHTS_Int_Dwelling` | `PhCustomAnnualLighting` | `set_phius_mf_res.py::build_lighting_int` |
| `LIGHTS_Ext_Dwelling` | `PhCustomAnnualLighting` | `set_phius_mf_res.py::build_lighting_ext` |
| `LIGHTS_Garage` | `PhCustomAnnualLighting` | `set_phius_mf_res.py::build_lighting_garage` |
| `MEL_Comm` | `PhCustomAnnualMEL` | `set_phius_mf_nonres.py::build_mel` |
| `LIGHTS_Int_Comm` | `PhCustomAnnualLighting` | `set_phius_mf_nonres.py::build_lighting_int` |

`reference_quantity` is the only wrong field on these objects. `quantity`,
`energy_demand`, `in_conditioned_space` and `reference_energy_norm` all export correctly.

---

## 2. Why 5 is the correct value

Two independent sources agree.

**This repo's own standards data.** `honeybee_ph_standards/programtypes/default_elec_equip.py`
sets `reference_quantity: 5` for `PhCustomAnnualMEL`, `PhCustomAnnualLighting` and
`PhCustomAnnualElectric`, under **both** the `PHI` and `PHIUS` keys (lines ~287–357).

**The certifier.** On 2441 Arverne East Building D, Phius signed off both entries in the
Design Certification feedback form with the same wording:

> Row 313, PHIUS+ MELS / Reference Quantity: "Ok, set to 'User defined' at 1."
> Row 319, PHIUS+ Int. Lighting / Reference Quantity: "Ok, set to 'User defined' at 1."

The hand-edited model that carried those reviewed values writes
`<ReferenceQuantity choice="User defined">5</ReferenceQuantity>` on all six devices.

---

## 3. Mechanism

`PhEquipment.__init__` (`honeybee_energy_ph/load/ph_equipment.py:95`):

```python
self.reference_quantity = 2  # Zone Occupants
```

The subclasses accept a `_defaults` dict and apply it, and `phius_default()`
(`ph_equipment.py:234-239`) is the accessor that pulls the right dict out of
`ph_default_equip`. The MF builders call neither:

`honeybee_grasshopper_ph/honeybee_ph_rhino/gh_compo_io/program/set_phius_mf_res.py:52-99`

```python
def build_mel(total_mel, number_of_rooms):
    mel_obj = ph_equipment.PhCustomAnnualMEL()      # <- no _defaults
    mel_obj.display_name = "Phius-MF-MEL"
    mel_obj.energy_demand = total_mel / number_of_rooms
    mel_obj.comment = "MEL_Dwelling"
    mel_obj.quantity = 1                            # <- transcribed by hand
    return mel_obj                                  # <- reference_quantity never set
```

`set_phius_mf_nonres.py:52-73` repeats the same shape for `MEL_Comm` and `LIGHTS_Int_Comm`.

The tell is that `quantity = 1` and (for ext/garage) `in_conditioned_space = False` *are*
assigned by hand in these builders. The defaults were transcribed one field at a time and
`reference_quantity` was missed. `apply_default_attr_values` returns early on an empty dict
(`ph_equipment.py:108-109`), so the bare constructor silently keeps the base value.

Observed, in the CPython venv at `honeybee_grasshopper_ph/.venv`:

```
                        phius_default()   bare constructor
PhCustomAnnualMEL          refQ = 5    →      refQ = 2
PhCustomAnnualLighting     refQ = 5    →      refQ = 2
PhCustomAnnualElectric     refQ = 5    →      refQ = 2
```

Downstream is a straight passthrough, so the base value reaches the file unmodified:
`PHX/model/elec_equip.py:66` casts to `int` and stores; `PHX/to_WUFI_XML/xml_schemas.py:1799`
writes `XML_Node("ReferenceQuantity", _d.reference_quantity)`;
`PHX/to_METr_JSON/metr_schemas.py:1105` writes the same value as `refQ`. **METr JSON exports
carry the same defect.**

---

## 4. Age and blast radius

`git log -S"reference_quantity"` over both component files returns nothing — the string has
never appeared in either. This has produced `reference_quantity = 2` on every Phius MF
export since the components were written, in both WUFI XML and METr JSON.

Not affected: the five appliance classes. `setup_ph_equipment` routes those through
`phius_default()`, which supplies `1` (PH case occupants) for dishwasher/washer/dryer/cooktop
and `4` (PH case Units) for the fridge/freezer. Projects that build appliances through
`HBPH - Create Custom Elec. Equipment` are also unaffected, since that component exposes a
`reference_quantity` input (`create_elec_equip.py:43`).

---

## 5. Recommended fix

Construct with the standards dict so the value keeps a single source of truth, rather than
re-hardcoding `5` in six places:

```python
from honeybee_ph_standards.programtypes.default_elec_equip import ph_default_equip

def build_mel(total_mel, number_of_rooms):
    mel_obj = ph_equipment.PhCustomAnnualMEL(_defaults=ph_default_equip["PhCustomAnnualMEL"]["PHIUS"])
    mel_obj.display_name = "Phius-MF-MEL"
    mel_obj.energy_demand = total_mel / number_of_rooms
    mel_obj.comment = "MEL_Dwelling"
    mel_obj.quantity = 1
    return mel_obj
```

Apply the same change to all six builders. The per-builder overrides that follow still win,
so `build_lighting_ext` and `build_lighting_garage` keep `in_conditioned_space = False` even
though the defaults dict says `True`.

**Do not use `phius_default()` here.** It returns a cached class-level singleton
(`ph_equipment.py:237-239`), so the returned object is shared with every other caller and
must not be mutated. `PhEquipment` has no `duplicate()` method, so there is no clean way to
copy it first.

Verified in the venv — the defaults dict reaches the object, the ext-lighting override still
wins, and the value survives `to_dict` / `from_dict`:

```
MEL   refQ=5 qty=1 inCond=True  refNorm=2
LGT   refQ=5 qty=1 inCond=False              (ext override still wins)
to_dict['reference_quantity'] = 5  ->  from_dict -> 5
```

Note: the defaults dicts carry a `frac_high_efficiency` key that these three classes do not
declare, so `apply_default_attr_values` sets a stray attribute on the instance. It is not
serialized by `to_dict` and this already happens today wherever `phius_default()` is used on
the appliance classes. Harmless, but worth knowing it is pre-existing and not introduced here.

---

## 6. Verification

1. **Unit** — ✅ done as a one-off check (2026-08-25), not as a committed test. All six
   builders return `reference_quantity = 5`, `quantity = 1`, `reference_energy_norm = 2`,
   and the per-builder overrides still win (`LIGHTS_Ext_Dwelling` and `LIGHTS_Garage` keep
   `in_conditioned_space = False`). See §9 for why this is not a committed test.
2. **Round trip** — ✅ `to_dict()` writes `5` and `from_dict()` reads `5` back on all six.
3. **Export** — ◻ **outstanding, needs Rhino.** Regenerate a Phius MF model on the canvas and
   confirm all six devices write `<ReferenceQuantity>5</ReferenceQuantity>` in the WUFI XML
   and `"refQ": 5` in the METr JSON.
4. **Regression guard** — ✅ appliance devices untouched: dishwasher/washer/dryer/cooktop
   stay at `1`, fridge/freezer at `4`.
5. **Lint gate** — ✅ `black==26.5.1 --check` and `isort==8.0.1 --check-only` clean across
   the repo (the CI `Lint` job).

---

## 7. Open question, not part of this fix

What WUFI-Passive actually does on import with `ReferenceQuantity = 2` on a device whose
`EnergyDemandNorm` is already a whole-building annual total has not been tested. If WUFI
applies the zone occupant count as a multiplier, existing exports overstate lighting and MEL
by a large factor; if it only affects how the entry is normalized for display, the delivered
results may be unaffected. Worth confirming in the GUI before deciding whether previously
submitted models need revisiting.

---

## 8. Files

| Repo | File | Role |
|---|---|---|
| `honeybee_grasshopper_ph` | `honeybee_ph_rhino/gh_compo_io/program/set_phius_mf_res.py:52-99` | Four builders to fix |
| `honeybee_grasshopper_ph` | `honeybee_ph_rhino/gh_compo_io/program/set_phius_mf_nonres.py:52-73` | Two builders to fix |
| `honeybee_ph` | `honeybee_ph_standards/programtypes/default_elec_equip.py:287-357` | Correct values — unchanged |
| `honeybee_ph` | `honeybee_energy_ph/load/ph_equipment.py:95, 104-109, 234-239` | Base default and defaults mechanism — unchanged |
| `PHX` | `PHX/to_WUFI_XML/xml_schemas.py:1799`, `PHX/to_METr_JSON/metr_schemas.py:1105` | Passthrough writers — unchanged |

---

## 9. Outcome (2026-08-25)

**Branch:** `honeybee_grasshopper_ph` → `fix/phius-mf-custom-load-reference-quantity`

Applied §5 verbatim. Both files gained the guarded `ph_default_equip` import in the repo's
standard form, and all six builders now construct with the PHIUS defaults dict:

```python
mel_obj = ph_equipment.PhCustomAnnualMEL(_defaults=ph_default_equip["PhCustomAnnualMEL"]["PHIUS"])
lighting_obj = ph_equipment.PhCustomAnnualLighting(_defaults=ph_default_equip["PhCustomAnnualLighting"]["PHIUS"])
```

This restores the idiom the pre-rewrite component already used — see
`gh_compo_io/program/_deprecated_/phius_MF_calc.py:334-389`, which passes the same defaults
dicts. That file is the strongest confirmation of the diagnosis in §3: the original
implementation was correct and the rewrite dropped the `_defaults=` argument.

Nothing changed in `honeybee_ph`, `honeybee_ph_standards`, or `PHX`. The PHX passthrough was
re-checked and still reads as §3 describes (`to_WUFI_XML/xml_schemas.py:1798`,
`to_METr_JSON/metr_schemas.py:1105`, `model/elec_equip.py:61-68`).

### No committed regression test

`honeybee_grasshopper_ph` has no test suite by design (`CLAUDE.md` hard rule 6: *"Tests live
upstream"*), and its CI runs lint only. The builders cannot be tested from `honeybee_ph`
either, since that package does not depend on `honeybee_ph_rhino`. So verification §6.1 was
run as a one-off script against the two source files rather than committed. **Adding a pytest
suite to the GH repo is a posture change for Ed to decide**, not something to slip in with a
bug fix.

### Residual, out of scope

`PhEquipment.__init__` still defaults `reference_quantity = 2` while all three custom-load
standards dicts say `5`. Any future bare `PhCustomAnnual*()` constructor hits the same trap —
which is exactly how this defect appeared. The clean upstream fix is a factory on the class
that returns a *fresh* instance from the defaults dict (unlike the cached `phius_default()`
singleton, see §5). Deliberately not done here: it would require a `honeybee_ph` release and a
`requirements.txt` pin bump before a six-line downstream fix could ship.

**Resolved 2026-08-25** in
[`archive/ph-equipment-reference-quantity-defaults/`](../ph-equipment-reference-quantity-defaults/README.md),
by a class-level default on every subclass rather than a factory — see
[decision 0007](../../../context/decisions/0007-reference-quantity-is-equipment-type-data.md).

---

## 10. Resolution and follow-ups

**Merged:** `honeybee_grasshopper_ph` PR
[#69](https://github.com/PH-Tools/honeybee_grasshopper_ph/pull/69), merge commit `25a8d92`,
2026-08-25. Branch deleted. No change shipped from `honeybee_ph`, `honeybee_ph_standards` or
`PHX`.

Three of the four verification items in §6 passed before merge; the fourth needs Rhino and is
follow-up 1 below. This packet is archived on the merge, not on the export check, because the
remaining work belongs to the downstream repo and to a question wider than this defect.

| # | Follow-up | Owner / where tracked |
|---|---|---|
| 1 | Canvas re-export of a Phius MF model; confirm `<ReferenceQuantity>5</ReferenceQuantity>` in the WUFI XML and `"refQ": 5` in the METr JSON (§6.3) | Ed, on the canvas — `honeybee_grasshopper_ph/planning/STATUS.md` |
| 2 | `honeybee_grasshopper_ph` release carrying the fix | release orchestrator — `honeybee_grasshopper_ph/planning/STATUS.md` |
| 3 | **§7 — what WUFI-Passive does on import with `ReferenceQuantity = 2`.** This is the higher-stakes half: if WUFI applies the zone occupant count as a multiplier, every previously submitted Phius MF model overstates MEL and lighting by a large factor. If it only affects display normalization, delivered results are unaffected. Decides whether submitted models need revisiting | open — GUI check, not a code question |
| 4 | ✅ **Done 2026-08-25.** Fixed upstream so a bare `PhCustomAnnual*()` constructor cannot silently reproduce this defect — every `PhEquipment` subclass now declares its own `DEFAULT_REFERENCE_QUANTITY` | [`archive/ph-equipment-reference-quantity-defaults/`](../ph-equipment-reference-quantity-defaults/README.md), [decision 0007](../../../context/decisions/0007-reference-quantity-is-equipment-type-data.md) |

### What made this findable, for the next one

The diagnosis was settled by a file nobody was looking at:
`gh_compo_io/program/_deprecated_/phius_MF_calc.py:334-389`, the pre-rewrite component, passes
exactly the defaults dicts the rewrite dropped. When a value is wrong in a rewritten
component, the deprecated original is the cheapest place to check what the rewrite lost.
