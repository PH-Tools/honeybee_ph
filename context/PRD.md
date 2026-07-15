---
DATE: 2026-07-15
STATUS: CANONICAL PRD
---

# honeybee-ph — Product Requirements

## 1. Goal

Let Passive House practitioners add detailed PHI- and Phius-style attributes to their Ladybug Tools / Honeybee models, so a single Honeybee model can carry everything needed to certify and export to the major PH energy tools (PHPP, WUFI-Passive). honeybee-ph is the **data-model layer** — it defines the objects and their HBJSON serialization; it does not do the export itself (that is PHX).

## 2. Who uses it

- **Passive House consultants** building models in Rhino/Grasshopper via `honeybee_grasshopper_ph` (the primary path — this is why the code must run in IronPython 2.7).
- **Python users** scripting against Ladybug Tools directly (`pip install honeybee-ph`), CPython 3.10+.
- **Downstream tools** (PHX, PH-Navigator) that consume the HBJSON these objects produce.

Not affiliated with or endorsed by PHI or Phius.

## 3. What belongs here

- New PH attributes on Honeybee/Honeybee-Energy objects (spaces, windows, constructions, HVAC, loads, certification thresholds).
- The object model + `to_dict()`/`from_dict()` HBJSON round-tripping for those attributes.
- Reference standards data (climates, assemblies, schedules) shipped as JSON.
- Shared utilities those objects need (unit handling via `PH-units`, colors, geometry helpers).

## 4. Non-goals

- **No file export/import of PHPP or WUFI formats** — that is [PHX](https://github.com/PH-Tools/PHX). honeybee-ph only produces/consumes HBJSON.
- **No Grasshopper UI** — components live in [honeybee_grasshopper_ph](https://github.com/PH-Tools/honeybee_grasshopper_ph). This repo is the pure library.
- **No 3D/web viewer** — that is PH-Navigator.
- **No CPython-only conveniences** that break IronPython 2.7 (dataclasses, f-strings, modern typing). See `CODING_STANDARDS.md`.

## 5. Success criteria

- A model built with these attributes round-trips losslessly through HBJSON — including old HBJSON produced by earlier versions (backward-compatible deserialization).
- The full model exports cleanly through PHX to both PHPP and WUFI-Passive.
- All code loads and runs inside Rhino/Grasshopper (IronPython 2.7) with no import or syntax errors.
- 100% test coverage maintained.

## 6. Current direction

- HVAC is migrating out of `honeybee_energy_ph` into the dedicated `honeybee_phhvac` package; `honeybee_energy_ph` is mostly deprecated for HVAC.
- See `decisions/` for design boundaries already settled (e.g. one ventilation system per room) and `planning/` for in-flight refactors.
