---
DATE: 2026-07-15
STATUS: CANONICAL ENGINEERING STANDARD
---

# honeybee-ph — Coding Standards

The one rule that shapes everything else: **all shipping code must run under IronPython 2.7** (Rhino/Grasshopper) *and* CPython 3.10+. Write to the intersection.

## 1. IronPython 2.7 compatibility

The generic dual-runtime rules (banned syntax and modules, comment-style type
hints, guarded `typing` imports, defensive third-party imports, and the lint
settings they imply) live in the **ironpython-27-compatibility** skill. Apply it
before editing anything on the Rhino load path. Only this repo's specifics are
recorded below.

All shipping code must run under IronPython 2.7 (Rhino/Grasshopper) *and*
CPython 3.10+. Write to the intersection. Tests under `tests/` are CPython-only.

## 2. Serialization pattern (backward-compatible HBJSON)

The HBJSON round-trip contract (four steps for a new field, when `.get()` is
required, mutable constructor ownership, `duplicate()` recursion) and the
`_extend`/`properties` attachment mechanism live in the
**hbjson-serialization-contract** skill. Apply it before adding or changing any
field on a model class.

Model classes round-trip through HBJSON, the ecosystem interchange format, so
deserialization must tolerate files written by older versions. This repo also
provides the `base_attrs_from_dict` helper and the `_Base` attribute convention
that `duplicate()` must preserve.

## 3. The `_extend_*` / `properties` pattern


PH data is attached through Honeybee's `properties` extension API, registered by
each package's `_extend_*.py` on import. New host-object attributes belong in
the relevant `properties/` sub-package, which owns that host's serialization.

## 4. Formatting

- **Black**, `line-length = 120` (configured in `pyproject.toml`).

## 5. Testing

- **pytest + coverage** — `python3 -m coverage run` executes the configured
  full suite; `python3 -m coverage report` enforces the repository floor.
- Repository-wide coverage floor: **75%** (`fail_under = 75`). New behavior
  still needs focused tests for its public, validation, serialization, and
  compatibility contracts.
- `filterwarnings = ["error", ...]` — a warning fails the suite. Fix the cause, don't silence it broadly.
- Tests mirror the package structure under `tests/` (`test_honeybee_ph/`, `test_honeybee_phhvac/`, …).

## 6. Docstrings & docs

Docstrings feed the autodoc site — keep them in the `ph-docs` format described in `docs/.instructions.md`. When you add or rename a public class/module/method/function, update `docs/nav.yml` so it appears on the site.

## Closeout checklist

- [ ] Code loads under IronPython 2.7 (no f-strings/walrus/match/unions/dataclasses; guarded `typing`; comment-style hints).
- [ ] New fields follow the backward-compatible serialization pattern (default + `.get()` + `duplicate()`).
- [ ] `python3 -m coverage run && python3 -m coverage report` passes with
      repository-wide coverage at or above 75%.
- [ ] `black` clean.
- [ ] `docs/nav.yml` + docstrings updated for any new/renamed public API.
