# honeybee-ph

Extends [Ladybug Tools' Honeybee](https://github.com/ladybug-tools/honeybee-core) with a Passive House data model. Published on PyPI as `honeybee-ph`. Source: https://github.com/PH-Tools/honeybee_ph

## Packages

| Package | Purpose |
|---------|---------|
| `honeybee_ph` | Core PH data model (spaces, certification, elec. equipment, etc.) |
| `honeybee_energy_ph` | PH extensions to honeybee-energy (constructions, materials, loads, HVAC) — **mostly deprecated**, migrating to `honeybee_phhvac` |
| `honeybee_phhvac` | PH-HVAC systems, devices, ducting, piping, properties |
| `honeybee_ph_standards` | Reference JSON datasets (climates, assemblies, etc.) |
| `honeybee_ph_utils` | Shared utilities (unit conversion helpers, color maps) |

## Downstream consumers

- **PHX** reads honeybee-ph models (HBJSON) and converts to/from PHPP and WUFI-Passive formats.
- **honeybee_grasshopper_ph** provides Rhino/Grasshopper components that create honeybee-ph objects.
- **PH-Navigator** renders honeybee-ph models in a web-based 3D viewer.

## Coding standards

### IronPython 2.7 compatibility

All code in this repo must run under **IronPython 2.7** (Rhino/Grasshopper runtime). This means:

- No f-strings. Use `"{}".format(...)` or `%` formatting.
- No walrus operator (`:=`), no `match`/`case`, no union type syntax (`X | Y`).
- No dataclasses or Pydantic — use plain classes with `__init__`.
- Imports from `typing` must be guarded:
  ```python
  try:
      from typing import Any, Dict, List, Optional
  except ImportError:
      pass  # IronPython 2.7
  ```

### Type hints (mypy py27-style)

Use **comment-style** type annotations (PEP 484 py2 syntax) so IronPython doesn't choke:

```python
def my_func(self, name, value):
    # type: (str, float) -> bool
    ...
```

Do not use inline annotations (`def my_func(self, name: str) -> bool:`).

### Formatting

- **Black** with `line-length = 120` (configured in `pyproject.toml`).

### Serialization pattern

Model classes implement `to_dict()` / `from_dict()` for HBJSON round-tripping. When adding new fields:
- Add the field in `__init__` with a sensible default.
- Serialize in `to_dict()`.
- Deserialize in `from_dict()` (or `base_attrs_from_dict`) using `_input_dict.get("key", default)` — never bare `[]` access — so old HBJSON without the key still loads.
- Copy the field in `duplicate()`.

### Testing

- **pytest** — run with `python3 -m pytest`.
- Coverage target: **100%** on all packages (`fail_under = 100` in pyproject.toml).
- Tests live in `tests/` mirroring the package structure.

## Versioning & release

- Version managed via `bump-my-version` (config in `pyproject.toml`).
- Current version: see `pyproject.toml` → `[project] version`.
- Tags follow `v{version}` format.

## Docs
- This package has auto-generated docs which are collected and displayed by the 'ph-docs' hub. For reference, please review `docs/.instructions.md`.
- Anytime a new class, module, method or function is added or updated - review the docs and be sure that it is properly included in the `docs/nav.yml` file.
- All docstrings must conform to the `ph-docs` format outlined in `docs/.instructions.md`