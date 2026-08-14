# Phase 03 — Integration, docs, and release

**Status:** Complete · archived; `v1.33.35` publish verification follows merge

## Objective

Prove the fix through host-object/HBJSON paths, document the ownership rule,
and release the prerequisite needed by EPW conversion.

## Implementation and verification

1. [x] Test Site graphs carried by `BldgSegment`, Room properties, duplication,
   and complete HBJSON round-trips.
2. [x] Run the full repository suite and record the authorized existing
   coverage-baseline exception: 891 tests pass; aggregate coverage is 79%
   against the currently configured 100% target.
3. [x] Run Black, `git diff --check`, Python 2.7 grammar parsing, and installed
   IronPython compilation. A direct IronPython 2.7 import runtime is not
   installed locally; the built artifact import is verified under CPython 3.10.
4. [x] Update affected public docstrings; update `docs/nav.yml` only if a public
   symbol was added or renamed (none expected).
5. [x] Record the constructor ownership rule in canonical context documentation if
   it is not already explicit.
6. [x] Build the wheel and run a clean-environment smoke test against the built
   artifact.
7. [x] Archive the completed packet, record `honeybee-ph>=1.33.35` as the EPW
   prerequisite, and hand release ownership to the merge-to-`main` workflow.

## Exit checks

- [x] Full suite passes: 891/891. The repository-wide 79% existing coverage
  baseline exception was explicitly authorized on 2026-08-14.
- [x] Default serialization snapshots remain unchanged.
- [x] Built artifact reproduces independent default/duplicate graphs.
- [x] `epw-derived-preliminary-climate` records `honeybee-ph>=1.33.35` as its
  minimum prerequisite and remains blocked until artifact verification.

## Verification evidence

```text
./.venv/bin/python -m pytest
891 passed

./.venv/bin/python -m pytest -q tests/test_honeybee_ph/test_site/test_site_graph_independence.py
98 passed

./.venv/bin/black --check honeybee_ph/site.py tests/test_honeybee_ph/test_site/test_site_graph_independence.py
2 files would be left unchanged

typed_ast.ast27.parse(honeybee_ph/site.py)
Python 2.7 grammar parse: OK

ipy compile(honeybee_ph/site.py)
IronPython compile: OK

uv build --wheel --out-dir dist .
Successfully built dist/honeybee_ph-1.33.34-py3-none-any.whl

uv pip install --python <fresh-venv>/bin/python dist/honeybee_ph-1.33.34-py3-none-any.whl
artifact smoke: honeybee-ph 1.33.34 OK
```

The wheel build emits the repository's existing setuptools warning that the
TOML-table form of `project.license` is deprecated for removal after
2027-02-18. This is unrelated to the site-default fix.

## Release boundary

Merge to `main` triggers `.github/workflows/ci.yml`, which owns the version
bump, tag, PyPI publish, and GitHub release. This packet is archived as the
release handoff; do not begin the EPW feature until `v1.33.35` is published and
verified.
