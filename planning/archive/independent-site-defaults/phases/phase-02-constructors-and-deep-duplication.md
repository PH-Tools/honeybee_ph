# Phase 02 — Constructors and deep duplication

**Status:** Complete · 2026-08-14

## Objective

Remove shared constructed defaults throughout `site.py` and make duplicate/copy
operations recursively independent without changing caller-supplied ownership.

## Implementation

1. Replace every mutable/nested constructor default with `None` followed by
   per-call construction inside `__init__`.
2. Include the list-valued `Climate_MonthlyValueSet` default in the audit even
   though its setter currently copies values into attributes.
3. Preserve public positional argument order and keyword names.
4. Rewrite `Climate.__copy__()` to duplicate `ground`, `monthly_temps`,
   `monthly_radiation`, and `peak_loads` rather than assigning references.
5. Audit every site-graph `__copy__()` for nested `user_data`, list, and dict
   sharing; follow the repo's existing base-attribute copy convention.
6. Keep `to_dict()` output unchanged and use tolerant `.get()` behavior for
   old optional fields where the Phase 01 legacy fixtures require it.

## Verification

- Run the Phase 01 identity/mutation suite after each constructor layer.
- Confirm explicitly supplied child identity remains unchanged.
- Confirm duplicate identifiers and values remain equal while nested mutable
  identities differ.
- Run Black and `git diff --check` on the focused change.

## Exit checks

- [x] Every Phase 01 regression passes; the expanded focused matrix is 95/95.
- [x] No new serialized key or default value exists.
- [x] No CPython-only syntax or dependency was introduced.

## Verification evidence

```text
./.venv/bin/python -m pytest -q tests/test_honeybee_ph/test_site/test_site_graph_independence.py
95 passed

./.venv/bin/python -m pytest -q tests/test_honeybee_ph/test_site/test_site_graph_independence.py tests/test_honeybee_ph/test_site tests/test_honeybee_ph/test_bldg_segment.py tests/test_honeybee_ph/test_properties/test_room.py
186 passed

./.venv/bin/black honeybee_ph/site.py tests/test_honeybee_ph/test_site/test_site_graph_independence.py
2 files left unchanged
```
