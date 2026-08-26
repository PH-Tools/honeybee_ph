# 0008 — `PhEquipment.duplicate()` Preserves the Identifier; the Default Factories Hand Out Copies

**Date:** 2026-08-25
**Status:** DECIDED
**Decider:** Ed May
**Research:** [`planning/archive/phius-default-shared-singleton/`](../../planning/archive/phius-default-shared-singleton/README.md)

## Context

`PhEquipment.phius_default()` and `.phi_default()` cached one instance per class and
returned that same object to every caller for the life of the Python process. There was
no `duplicate()` on `PhEquipment`, so a caller who wanted an independent object had no
supported way to get one.

Two consequences, both real:

1. **Mutation bleed.** Anything a caller wrote to a default was visible to every later
   caller. In Rhino the class attribute outlives a canvas solution *and* the open `.3dm`,
   so a mutation in one model silently followed the user into the next.
2. **No supported escape.** Getting an independent copy meant `copy.deepcopy` or
   re-transcribing `ph_default_equip` by hand — the same transcription pattern that
   produced the `reference_quantity` defect behind
   [decision 0007](0007-reference-quantity-is-equipment-type-data.md).

The obvious fix — return a fresh instance with a fresh identifier — is wrong, and that is
the part worth writing down. PHX creates **one `PhxZone` per Honeybee-Room**
(`from_HBJSON/create_variant.py`) and adds every room's devices to **every** zone, keyed
by the device `identifier`, as an upsert. The Phius multi-family builders in
`honeybee_grasshopper_ph` depend on that: `build_mel` sets
`energy_demand = total_mel / number_of_rooms` and hands one device to every room.

| | shared identifier | fresh identifier per room |
|---|---|---|
| devices per zone after N rooms | 1 (N upserts onto one key) | N (N distinct keys) |
| demand on each | `total / N` | `total / N` |
| zones | N | N |
| **exported total** | **`total`** | **`N × total`** |

Nothing else compensates: `get_quantity()` returns 1 for the custom types and
`get_energy_demand()` carries no room-count term. The shared **identity** is
load-bearing; only the shared **mutable state** was the defect.

## Decision

1. `PhEquipment.duplicate(new_host=None)` returns an independent copy that **keeps the
   original's `identifier`**. It is implemented as a `to_dict()` / `from_dict()` round
   trip, which is already the repo's idiom for copying equipment and already preserves
   the identifier.
2. `phius_default()` / `phi_default()` keep their per-class cache but return
   `prototype.duplicate()`. The cache is what makes the returned identifier stable for
   the life of the process; the duplicate is what makes the object safe to write to. The
   cached prototype is never handed to a caller.
3. `PhEquipmentCollection.__copy__` duplicates its equipment instead of re-using the
   references, so two Rooms never share one mutable device. The collection keys are
   unchanged, because `duplicate()` does not re-key.
4. The identity contract is asserted by tests, not left to reading: identifier stability
   across factory calls, independence of the returned objects, and a room-count invariant
   over N = 1, 2 and 10 rooms
   (`tests/test_honeybee_energy_ph/test_load/test_ph_equipment_identity.py`).

## Rationale

- A `duplicate()` that re-keys would be the conventional choice and would silently
  multiply every exported appliance, MEL and lighting figure by the room count. Unusual
  semantics with a test and a comment beat conventional semantics with a wrong number.
- Fixing the hazard inside `honeybee_ph` leaves the working PHX export path untouched.
  The alternative — dropping the cache and making PHX key its zone collection by
  something explicit (equipment type, or a key the component sets) — is the cleaner
  separation of concerns and stays available, but it is a cross-repo change to a working
  export path and should be taken on its own merits, not as a side effect of a
  mutation-safety fix.
- Leaving `phius_default()` as a documented "read-only prototype" and fixing only the
  callers was rejected for the reason decision 0007 rejected an inherited
  `reference_quantity`: it leaves a default that no caller should accept sitting there
  looking acceptable.

## What would reopen this

- PHX stops keying `PhxZone.elec_equipment_collection` by the device identifier, or stops
  creating one zone per Honeybee-Room. Either removes the reason for the shared
  identifier, and `duplicate()` should then re-key like every other `duplicate()` in the
  ecosystem.
- The Phius multi-family builders stop dividing the building total by the room count.
- Honeybee-core changes `Room.duplicate()` to deep-copy Process Loads, which would make
  the per-room devices independent objects without anything in this repo changing.
