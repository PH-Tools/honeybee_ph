---
DATE: 2026-07-15
STATUS: CANONICAL ENGINEERING STANDARD
---

# honeybee-ph — Coding Standards

The one rule that shapes everything else: **all shipping code must run under IronPython 2.7** (Rhino/Grasshopper) *and* CPython 3.10+. Write to the intersection.

## 1. IronPython 2.7 compatibility

Do **not** use:

- f-strings — use `"{}".format(...)` or `%` formatting.
- The walrus operator `:=`, `match`/`case`, or `X | Y` union syntax.
- `dataclasses` or `pydantic` — use plain classes with `__init__`.
- Any CPython-3-only stdlib module or syntax.

Guard `typing` imports so IronPython does not choke:

```python
try:
    from typing import Any, Dict, List, Optional
except ImportError:
    pass  # IronPython 2.7
```

## 2. Type hints — comment style (PEP 484 py2)

Use comment-style annotations, not inline annotations:

```python
def my_func(self, name, value):
    # type: (str, float) -> bool
    ...
```

Do **not** write `def my_func(self, name: str) -> bool:` — inline annotations are not IronPython-2.7 safe.

## 3. Serialization pattern (backward-compatible HBJSON)

Model classes round-trip through HBJSON via `to_dict()` / `from_dict()`. HBJSON is the ecosystem interchange format, so deserialization must tolerate files written by older versions. When adding a field:

1. Add it in `__init__` with a sensible **default**.
2. Write it in `to_dict()`.
3. Read it in `from_dict()` (or `base_attrs_from_dict`) with `_input_dict.get("key", default)` — **never** bare `_input_dict["key"]` access, so old HBJSON without the key still loads.
4. Copy it in `duplicate()`.

## 4. The `_extend_*` / `properties` pattern

PH data is attached to Honeybee objects through Honeybee's `properties` extension API, registered by each package's `_extend_*.py` on import. New host-object attributes belong in the relevant `properties/` sub-package, which owns that host's `to_dict()`/`from_dict()`. Do not attach PH data by monkey-patching around this mechanism.

## 5. Formatting

- **Black**, `line-length = 120` (configured in `pyproject.toml`).

## 6. Testing

- **pytest** — `python3 -m pytest`.
- Coverage target: **100%** (`fail_under = 100`). New code needs tests that keep coverage at 100%.
- `filterwarnings = ["error", ...]` — a warning fails the suite. Fix the cause, don't silence it broadly.
- Tests mirror the package structure under `tests/` (`test_honeybee_ph/`, `test_honeybee_phhvac/`, …).

## 7. Docstrings & docs

Docstrings feed the autodoc site — keep them in the `ph-docs` format described in `docs/.instructions.md`. When you add or rename a public class/module/method/function, update `docs/nav.yml` so it appears on the site.

## Closeout checklist

- [ ] Code loads under IronPython 2.7 (no f-strings/walrus/match/unions/dataclasses; guarded `typing`; comment-style hints).
- [ ] New fields follow the backward-compatible serialization pattern (default + `.get()` + `duplicate()`).
- [ ] `python3 -m pytest` passes at 100% coverage.
- [ ] `black` clean.
- [ ] `docs/nav.yml` + docstrings updated for any new/renamed public API.
