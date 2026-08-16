# honeybee-ph

Extends [Ladybug Tools' Honeybee](https://github.com/ladybug-tools/honeybee-core) with a Passive House data model. Published on PyPI as `honeybee-ph`. Source: https://github.com/PH-Tools/honeybee_ph

> **Runtime constraint:** all shipping code must run under **IronPython 2.7** (the Rhino/Grasshopper runtime) as well as CPython 3.10+. This is the single most important thing to know before writing code here — see `context/CODING_STANDARDS.md`.

## What this repo is

A set of five sub-packages that layer Passive House (PHI + Phius) attributes onto Honeybee / Honeybee-Energy models:

| Package | Purpose |
|---------|---------|
| `honeybee_ph` | Core PH data model (spaces, certification, building segments, elec. equipment) |
| `honeybee_energy_ph` | PH extensions to honeybee-energy (constructions, materials, loads) — **mostly deprecated**, HVAC migrating to `honeybee_phhvac` |
| `honeybee_phhvac` | PH-HVAC systems, devices, ducting, piping, properties |
| `honeybee_ph_standards` | Reference JSON datasets (climates, assemblies, schedules, etc.) |
| `honeybee_ph_utils` | Shared utilities (unit conversion, color maps, geometry helpers) |

## Where things live — read before working

| Working on… | Read |
|-------------|------|
| Product scope, what belongs in this repo | `context/PRD.md` |
| How the packages fit together, data flow | `context/ARCHITECTURE.md` |
| Writing/changing any code (IPy2.7 rules, typing, serialization) | `context/CODING_STANDARDS.md` |
| Dependencies, packaging, tests, CI, release | `context/TECH_STACK.md` |
| Why a past design choice was made | `context/decisions/` |
| Current / in-flight work | `planning/STATUS.md` |
| The public docs site (autodoc spoke — do not restructure) | `docs/.instructions.md` |

Full context index: `context/README.md`.

## Hard rules

1. **IronPython 2.7 compatibility is mandatory.** No f-strings, no walrus, no `match`/`case`, no `X | Y` unions, no dataclasses/Pydantic. Comment-style type hints only (`# type: (str) -> bool`). Guard `typing` imports. Full detail: `context/CODING_STANDARDS.md`.
2. **Serialization must be backward-compatible.** New fields get a default in `__init__`, are written in `to_dict()`, read with `_input_dict.get("key", default)` in `from_dict()`, and copied in `duplicate()`. Old HBJSON must still load.
3. **Docs are an autodoc spoke.** When you add/change a class, module, method, or function, update `docs/nav.yml` and keep docstrings in the `ph-docs` format (`docs/.instructions.md`). Never restructure `docs/`.
4. **Verify before closeout.** Run `python3 -m coverage run && python3 -m coverage report`; the repository-wide coverage floor is 75% (`fail_under = 75`). Tests mirror the package layout under `tests/`.

## Ecosystem / downstream consumers

- **PHX** reads honeybee-ph models (HBJSON) and converts to/from PHPP and WUFI-Passive.
- **honeybee_grasshopper_ph** provides the Rhino/Grasshopper components that create these objects (this is why IPy2.7 matters).
- **PH-Navigator** renders honeybee-ph models in a web-based 3D viewer.
