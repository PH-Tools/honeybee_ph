# PRD — Independent `Site` and `Climate` defaults

**Status:** In progress · 2026-08-14
**Author:** Ed May + Codex
**Kind:** Correctness feature / defect repair (this repo only)

---

## WHAT

Make every default-constructed and duplicated site/climate object independent.
No nested monthly collection, radiation collection, peak-load collection,
ground object, location, climate, PHPP code object, or backing value collection
may be shared accidentally between instances.

The confirmed hazardous signatures include:

```python
Climate(
    _monthly_temps=Climate_MonthlyTempCollection(),
    _monthly_radiation=Climate_MonthlyRadiationCollection(),
    _peak_loads=Climate_PeakLoadCollection(),
)

Site(
    _location=Location(),
    _climate=Climate(),
    _phpp_library_codes=PHPPCodes(),
)
```

The review also found list-valued constructed defaults such as
`Climate_MonthlyValueSet(_values=[0.0] * 12)` and a `Climate.__copy__()` method
that assigns nested attributes by reference.

### Behavior contract

1. Constructor arguments that create mutable/nested objects default to `None`.
   Each constructor creates fresh child objects inside the method.
2. User-supplied child objects retain the existing ownership behavior unless an
   explicit duplication policy is documented; do not silently change that
   contract while fixing defaults.
3. `duplicate()`/`__copy__()` produces an independent nested object graph while
   preserving all values, identifiers, display names, and user data according
   to existing library conventions.
4. Mutating any nested value on one default instance cannot change another
   default instance or its duplicate.
5. `to_dict()` output for an untouched default remains backward-compatible.
6. `from_dict()` continues to load old HBJSON and creates independent objects.
7. Apply the audit to the whole `site.py` object graph, not only the two
   signatures reproduced by the POC.

### Constraints

- IronPython 2.7 compatible: use `None` plus construction in the method; no
  dataclasses/default factories.
- Preserve public positional/keyword behavior where possible.
- No serialized schema change is required for the fix.
- Add regression tests before changing constructors.

## WHY

The POC reproduced that two calls to `Site()` shared the same nested `Climate`.
Mutating one site's climate changed the other. This can leak climate data across
calculations, tests, Rooms, or projects and makes results depend on object
construction order.

The risk is especially high for a web service that builds several models in one
process. It is also independent of the proposed climate dataset library: even a
perfect dataset loader is unsafe if duplicates or defaults share mutable nested
state.

## Acceptance criteria

- Identity tests prove all default nested objects are distinct across two
  `Site()` and two `Climate()` instances.
- Mutation tests cover monthly temperatures, radiation, peak loads, ground,
  location, and PHPP codes.
- `duplicate()` is value-equal but recursively independent for all mutable
  children.
- Existing default serialization snapshots remain unchanged.
- Old serialized site dictionaries still load and remain independent.
- Full `python3 -m pytest` passes at the repository's coverage threshold.
