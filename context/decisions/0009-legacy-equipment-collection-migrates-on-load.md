# 0009 — Legacy `equipment_collection` Migrates onto Process Loads When a Room Is Loaded

**Date:** 2026-09-12
**Status:** DECIDED
**Decider:** Ed May
**Issue:** [#79](https://github.com/PH-Tools/honeybee_ph/issues/79)

## Context

`PhEquipment` has two storage locations on a Honeybee-Room. The older one hangs a
`PhEquipmentCollection` off the Room's `ElectricEquipment` load
(`ElectricEquipmentPhProperties.equipment_collection`). The newer one (Jan 2025) hangs
one `PhEquipment` off each `Process` load (`ProcessPhProperties.ph_equipment`). Every live
Grasshopper component writes the Process path; only the `_deprecated_` component wrote
the collection. The collection is being retired.

Old HBJSON must keep loading, so the legacy data has to be lifted onto Process loads
somewhere during deserialization. `ElectricEquipmentPhProperties.from_dict()` cannot do
it: its host is the load, and a load has no reference to its Room.

Verified by round-tripping legacy models written with the pre-change writer:

- A load's `ph` data is rebuilt inside honeybee-energy, in the load's own `from_dict`.
- Honeybee applies extensions in `dir()` order, so `energy` always runs before `ph`.
  When `ModelPhProperties.apply_properties_from_dict` runs, every Room's loads, with
  their legacy collections, already exist.
- A standalone `Room.from_dict` never reaches the Model hook; it reaches
  `RoomPhProperties.from_dict`, where the Room's loads also already exist.
- `RoomPhProperties.apply_properties_from_dict` is skipped for rooms without a ph dict,
  so it is not a reliable hook on its own.
- An `ElectricEquipment` reached through a `ProgramType` is **one object shared by every
  room** using that program after load.

## Decision

1. One function, `migrate_legacy_equipment_collection(room)`, in
   `honeybee_energy_ph/properties/load/equipment.py`, lifts each device in the Room's
   legacy collection onto its own `Process` load on that Room.
2. It is called from the two `ph` hooks that see a loaded Room:
   `ModelPhProperties.apply_properties_from_dict` (every room, before the ph-dict gate)
   and `RoomPhProperties.from_dict`.
3. The migrated `Process` has `watts=0`. The legacy component had already rolled the
   equipment wattage into `ElectricEquipment.watts_per_area`; a non-zero Process would
   double-count it in EnergyPlus. PHX does not read `Process.watts`.
4. The migrated device is `PhEquipment.duplicate()`, which keeps its identifier
   ([decision 0008](0008-ph-equipment-duplicate-preserves-identifier.md)). PHX keys and
   counts both paths by that identifier, so quantity and `reference_quantity` export
   unchanged.
5. The migration is idempotent (an identifier already on one of the Room's Process loads
   is skipped), and the collection is emptied only after every Room has migrated, because
   a ProgramType's load is shared.
6. `to_dict()` stops writing `equipment_collection`. The attribute stays until PHX has
   dropped its reads and released; removing it is a later step of #79.

## Rationale

- The hooks honeybee-ph already owns see both the Room and its loads, so no opt-in call
  is needed from PHX or Grasshopper, and a file cannot be read without migrating.
- A Model-level sweep alone would miss `Room.from_dict`; a per-room function called from
  both hooks covers both paths with one implementation.
- The released PHX already reads the Process path, so emptying the collection does not
  break it.

## What would reopen this

- honeybee-core changes extension application order, so `ph` could run before `energy`.
- A consumer needs the legacy collection populated after load.
- Legacy equipment is found whose collection key differs from its identifier.
