# Bug: `phius_default()` / `phi_default()` hand out a shared mutable singleton

**Status:** Scoped — investigated, not implemented
**Kind:** Bug (data model; fix ships from this repo)
**Date:** 2026-08-25
**Author:** Ed May + Claude
**Origin:** §7 of
[`archive/ph-equipment-reference-quantity-defaults/`](../archive/ph-equipment-reference-quantity-defaults/README.md)

> **Read §4 before designing a fix.** The obvious fix — return a fresh copy — multiplies
> appliance, MEL and lighting energy by the room count. The shared identity is
> load-bearing downstream.

---

## 1. Problem

`PhEquipment.phius_default()` and `.phi_default()` cache one instance per class and return
that same object to every caller, forever:

```python
@classmethod
def phius_default(cls):
    if not cls._phius_default:
        cls._phius_default = cls(_defaults=ph_default_equip[cls.__name__]["PHIUS"])
    return cls._phius_default
```

`PhEquipment` has no `duplicate()`, so a caller who wants an independent object has no
supported way to get one. Anything a caller writes to the returned object is visible to
every later caller, for the life of the Python process.

Verified (`honeybee_ph/.venv`, 2026-08-25):

```
PhDishwasher.phius_default() is PhDishwasher.phius_default()   -> True
cached per subclass, PHI and PHIUS distinct                    -> True
hasattr(obj, "duplicate")                                      -> False

caller A: PhCooktop.phius_default().energy_demand = 999.0
caller B: PhCooktop.phius_default().energy_demand              -> 999.0
          PhCooktop.phius_default().display_name               -> "MUTATED BY CALLER A"
```

## 2. Where the shared object reaches the model

`set_phius_mf_res.py::setup_ph_equipment` appends the singletons straight into the
equipment list that becomes per-room Process loads:

```python
self.ph_equipment.append(ph_equipment.PhDishwasher.phius_default())
self.ph_equipment.append(ph_equipment.PhClothesWasher.phius_default())
...
```

Those become `Process` objects, and the *same* `Process` object is added to every room.
Verified with 4 rooms:

```
before HBJSON round trip: 4 equipment refs, 1 distinct object, 1 distinct identifier
after  HBJSON round trip: 4 equipment refs, 4 distinct objects, 1 distinct identifier
Room.duplicate() still yields the same shared object
```

So the object identity is process-wide, and the **`identifier` is shared and survives
serialization**.

## 3. Why it is a real hazard

1. **Mutation bleed.** Any caller that writes to a default corrupts it for every other
   caller in the process — demonstrated in §1.
2. **Rhino session lifetime.** The cache is a class attribute, so it lives as long as the
   module stays imported. In Rhino that spans canvas solutions *and* different `.3dm`
   files opened in one session. A mutation in one model silently follows you into the next.
3. **No supported escape.** Without `duplicate()`, a caller who needs an independent copy
   must reach for `copy.deepcopy` or rebuild from `ph_default_equip` by hand — which is
   exactly the transcription pattern that produced the
   [`reference_quantity`](../archive/phius-mf-custom-load-reference-quantity/README.md) defect.
4. **Silent drop on collection add.** `PhEquipmentCollection.add_equipment` keys by
   `identifier` and returns early on a duplicate key, so adding the same singleton twice
   yields a collection of one.

## 4. Why the obvious fix is wrong — read this first

**PHX creates one `PhxZone` per Honeybee Room** (`create_variant.py:113`), and
`add_elec_equip_from_hb_room` is called once per room, adding that room's devices to
**every** zone, keyed by `str(phx_elec_device.identifier)`
(`create_variant.py:899, 913`). `add_new_device` is an upsert.

The current arithmetic depends on all of that lining up:

| | today (shared identifier) | naive fix (fresh copy per room) |
|---|---|---|
| devices per zone after N rooms | 1 (N upserts onto one key) | N (N distinct keys) |
| demand on each | `total / N` | `total / N` |
| zones | N | N |
| **exported total** | **`total`** ✅ | **`N × total`** ❌ |

`build_mel` sets `energy_demand = total_mel / number_of_rooms` precisely because the
per-room devices collapse to one per zone and the N zones then sum back to the total.
Handing every room its own object with its own identifier breaks that by a factor of N.

Checked and ruled out as compensating mechanisms: `get_quantity()` returns 1 for the
custom types, and `get_energy_demand()` is `energy_demand * quantity` with no room-count
term (`PHX/model/elec_equip.py:90-100, 336-342`).

**So the shared *identity* is load-bearing, while the shared *mutable state* is the
defect.** A fix has to separate the two.

## 5. Fix options

**A. `duplicate()` that preserves the identifier.** Add `PhEquipment.duplicate()` copying
every attribute including `identifier`, and have `phius_default()` return
`cls._phius_default.duplicate()`. Callers get independent objects; the downstream dedup
keeps working because the identifier is unchanged. Cheap, surgical, IronPython 2.7 safe.
The wrinkle is a `duplicate()` that deliberately does *not* re-key, which is unusual
enough to need a comment and a test saying why.

**B. Return a fresh instance built from the defaults dict, and make the PHX device key
explicit.** `phius_default()` becomes `cls(_defaults=...)` with no cache, and PHX keys its
zone collection by something stable and intentional (equipment type, or an explicit key
the component sets) rather than by whichever identifier happens to arrive. Cleaner
separation of concerns, but it is a cross-repo change to a working export path and needs
its own round-trip verification.

**C. Keep the cache, add `duplicate()`, and change the callers.** Leave
`phius_default()` alone as a "read-only prototype", document it as such, and have
`set_phius_mf_res.py` call `.duplicate()`. Smallest blast radius, but it leaves a
loaded gun for the next caller — the same reasoning that made
[decision 0007](../../context/decisions/0007-reference-quantity-is-equipment-type-data.md)
reject a base-class default nobody should accept.

Recommendation: **A**, with the identifier semantics written into a decision record. It
fixes the hazard without touching the export path, and B stays available if the PHX
keying is ever revisited on its own merits.

## 6. Verification a fix must pass

1. Two `phius_default()` calls return independent objects; mutating one does not affect
   the other.
2. The identifier contract, whichever way it lands, is asserted by a test — this is the
   part that silently breaks energy totals.
3. **Room-count invariant:** build a Phius MF model with N rooms, export, and assert the
   summed MEL / lighting / appliance demand equals the input total, for N = 1, 2 and 10.
   No such test exists today in either repo; the arithmetic in §4 is currently held up by
   nothing but the shared identifier.
4. HBJSON round trip preserves whatever identity contract is chosen.
5. Appliance `reference_quantity` values still hold (1 / 4 per
   [decision 0007](../../context/decisions/0007-reference-quantity-is-equipment-type-data.md)).

## 7. Files

| Repo | File | Role |
|---|---|---|
| `honeybee_ph` | `honeybee_energy_ph/load/ph_equipment.py:243-256` | `phius_default()` / `phi_default()` — the cache |
| `honeybee_ph` | `honeybee_energy_ph/load/ph_equipment.py` (`PhEquipment`) | No `duplicate()` |
| `honeybee_ph` | `honeybee_energy_ph/load/ph_equipment.py` (`PhEquipmentCollection.add_equipment`) | Keys by identifier, early-returns on duplicates |
| `honeybee_grasshopper_ph` | `gh_compo_io/program/set_phius_mf_res.py::setup_ph_equipment` | Appends the singletons into per-room loads |
| `PHX` | `from_HBJSON/create_variant.py:113` | One `PhxZone` per HB Room |
| `PHX` | `from_HBJSON/create_variant.py:899, 913` | Zone device collection keyed by identifier — the load-bearing dedup |
| `PHX` | `model/elec_equip.py:90-100, 336-342` | `get_quantity()` / `get_energy_demand()` — no room-count term |

## 8. Not part of this fix

The stray `frac_high_efficiency` attribute that `apply_default_attr_values` sets on the
three classes that do not declare it. Pre-existing, not serialized, harmless.
