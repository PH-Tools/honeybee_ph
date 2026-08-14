# Phase 01 — Regression and compatibility contract

**Status:** Complete · 2026-08-14

## Objective

Reproduce the full shared-mutable graph and pin the unchanged serialized
default before modifying constructors or copy behavior.

## Touchpoints

- `honeybee_ph/site.py`
- `honeybee_ph/bldg_segment.py`
- `tests/test_honeybee_ph/test_site/`
- BuildingSegment/Room serialization tests that carry a Site

## Tests first

1. Build two instances of every site-graph class and assert distinct identity
   for all mutable default children:
   - monthly value sets and temperature/radiation collections;
   - peak-load value sets and collection;
   - ground, climate, location, PHPP codes, and Site.
2. Mutate one leaf in each branch and prove the peer instance is unchanged.
3. Duplicate a populated Site/Climate and prove recursive independence while
   preserving values, identifiers, display names, and user data.
4. Create two `BldgSegment()` objects and prove their complete site graphs are
   independent.
5. Pin `to_dict()` for an untouched default Site and Climate.
6. Round-trip current and legacy dictionaries, including missing optional base
   attributes, and prove separately loaded objects do not share children.
7. Pin caller-supplied ownership: an explicitly supplied child remains the
   instance stored by the constructor; only defaults and duplication create
   copies.

## Exit checks

- [x] Tests fail for the currently reproduced shared paths and pass for
  already independent paths: 66 strict expected failures / 26 passes.
- [x] The intended default `Site` and `Climate` serialized payloads are
  recorded exactly after canonicalizing generated identifiers only.
- [x] No production code changed in this phase.

## Verification evidence

```text
./.venv/bin/python -m pytest -q tests/test_honeybee_ph/test_site/test_site_graph_independence.py
26 passed, 66 xfailed

./.venv/bin/python -m pytest -q --runxfail tests/test_honeybee_ph/test_site/test_site_graph_independence.py
66 failed, 26 passed
```
