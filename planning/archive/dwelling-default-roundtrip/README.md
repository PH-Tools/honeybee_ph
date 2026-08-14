# Default dwelling identity across HBJSON round-trips

**Status:** Complete — implemented and verified; release pending
**Opened:** 2026-08-06
**Investigated:** 2026-08-14
**Completed:** 2026-08-14
**Implementation commit:** `3903a86`
**Owner:** `honeybee_energy_ph/dwellings.py`
**Downstream witness:** `PHX/from_HBJSON/_dwelling_occupancy.py`

## 1. Conclusion

The bug was still present when re-investigated on 2026-08-14 and the fix remained
necessary. The count-based correction and focused regressions are implemented in
`3903a86`; the full repository gate passes.

Before this correction, `get_dwelling_obj()` decided whether a Room was untagged by comparing the
Room's serialized `PhDwellings.identifier` with the current process's
`PhDwellings.default().identifier`. The default identifier is a `uuid4`, so that
comparison is valid only within the process that created the object. It fails after an
HBJSON round-trip in a later process.

The repository already has a serialization-stable contract that resolves the defect:

- `num_dwellings >= 1` means the Room has an explicit residential dwelling assignment.
- `num_dwellings < 1` means no dwelling is assigned.
- `identifier` distinguishes explicit dwelling groups; it does not determine whether an
  assignment exists.

No new serialized marker is needed. `PeoplePhProperties.is_residential` already uses
`num_dwellings >= 1`, the established dwelling-zone decision records a corridor/lobby as
either having no People or `PhDwellings(0)`, and PHX already uses the same count-based
test at the HBJSON boundary.

## 2. Defect and impact

`PeoplePhProperties.__init__()` assigns the process-wide
`PhDwellings.default()` object to every new People load. All Rooms that have not passed
through *HBPH - Set Dwelling* therefore serialize the same default identifier and a
`num_dwellings` value of `0`.

During deserialization, `PhDwellings.from_dict()` correctly preserves that serialized
identifier. A new process, however, has a newly generated default identifier. The
pre-fix `_is_default_dwelling()` comparison missed, so `get_dwelling_obj()` returned the
deserialized zero-count object as though it were an explicit dwelling.

The error propagates through the shared helpers:

1. `dwelling_key()` returns the stale default identifier instead of the Room identifier.
2. `group_rooms_by_dwelling()` collapses all originally untagged Rooms into one group.
3. A consumer performing dwelling-group occupancy logic can pool or gate occupancy
   across unrelated Rooms.
4. `unique_dwelling_objects()` also exposes the zero-count object as an assigned
   dwelling, although `total_dwelling_count()` happens to remain numerically unchanged
   because the object's count is zero.

PHX encountered the first three effects while implementing dwelling-group occupancy
gating. Its local count-based test prevents the bad grouping there, but the shared
honeybee-ph helper remains incorrect for every other caller.

## 3. Reproduction confirmed on the current checkout

The defect was reproduced on 2026-08-14 with real Honeybee model serialization, not a
hand-built `PhDwellings` dictionary:

1. Create two Rooms with People loads that retain `PhDwellings.default()`.
2. Create a `honeybee.model.Model` and call `Model.to_dict()`.
3. Set `PhDwellings._default = None` to simulate a new process.
4. Call `Model.from_dict()`.
5. Pass the deserialized Rooms to the dwelling helpers.

Observed result:

| Check | Expected | Pre-fix result |
|---|---:|---:|
| Deserialized `num_dwellings` | `[0, 0]` | `[0, 0]` |
| `get_dwelling_obj(room) is not None` | `[False, False]` | `[True, True]` |
| `group_rooms_by_dwelling()` group sizes | `[1, 1]` | `[2]` |

The serialized Rooms retain the original default UUID; the reset class singleton has a
different UUID. This isolates the defect to classification in
`_is_default_dwelling()`, not serialization loss or identifier corruption.

## 4. Behavioral contract

The helper must implement the following distinction consistently before and after
serialization:

| `PhDwellings` state | Assignment state | Grouping key | Count contribution |
|---|---|---|---:|
| Process default, count `0` | Unset | Room identifier | 0 |
| Deserialized former default, count `0` | Unset | Room identifier | 0 |
| Independently constructed `PhDwellings(0)` | Unset / non-residential | Room identifier | 0 |
| `PhDwellings(1)` | Explicit dwelling | Dwelling identifier | 1 per unique identifier |
| `PhDwellings(N)`, `N > 1` | Explicit block of dwellings | Dwelling identifier | N per unique identifier |

For explicit dwellings, Rooms with equal dwelling identifiers remain in one group even
when deserialization or `duplicate()` has produced distinct Python objects. Identifier
comparison remains load-bearing for that identity function.

### Why an explicit marker is rejected

An `is_default` / `is_assigned` field would change the HBJSON contract, require a
backward-compatibility inference for all existing files, and introduce two possible
sources of truth. No supported state needs it: a zero-count object is already
non-residential according to `PeoplePhProperties.is_residential`, regardless of whether
it originated from the singleton or was constructed directly.

## 5. Implemented scope

### Shipping change

Implemented in `honeybee_energy_ph/dwellings.py`:

1. Change `_is_default_dwelling()` to classify `_dwelling.num_dwellings < 1` as
   unset instead of comparing against `PhDwellings.default().identifier`.
2. Rewrite its docstring to state the count-based assignment contract and the reason the
   process-local UUID cannot be used across HBJSON boundaries.
3. Keep `dwelling_key()`, `group_rooms_by_dwelling()`,
   `unique_dwelling_objects()`, and `total_dwelling_count()` otherwise unchanged.

The minimal implementation is intentionally equivalent to:

```python
def _is_default_dwelling(_dwelling):
    # type: (PhDwellings) -> bool
    return _dwelling.num_dwellings < 1
```

The private helper may retain its existing name to keep the patch surgical; its revised
docstring must make clear that "default" means the serialized unset state, not object
identity with the current singleton.

### Test changes

Added focused cases to `tests/test_honeybee_energy_ph/test_dwellings.py`:

1. **Real unset round-trip regression:** serialize a two-Room `Model`, reset
   `PhDwellings._default`, deserialize, and assert that each Room falls back to its own
   key and group. Use pytest's `monkeypatch` fixture or `try/finally` so the class cache is
   restored after the test.
2. **Explicit shared-dwelling round-trip:** two Rooms sharing `PhDwellings(1)` remain one
   group after `Model.to_dict()` / `Model.from_dict()` and contribute a total count of 1.
3. **Explicit multi-unit round-trip:** one Room with `PhDwellings(4)` remains explicit and
   contributes 4.
4. **Independent zero-count object:** `PhDwellings(0)` with a non-default identifier is
   treated as unset. This locks the resolved semantic question and prevents regression
   back to identifier-based classification.

Keep the existing in-memory default, missing-People, duplicate-identifier, stable-order,
and count tests. The new tests cover the missing process boundary rather than replacing
those unit cases.

### Documentation and serialization

- No `PhDwellings.to_dict()` / `from_dict()` change.
- No schema migration or HBJSON version change.
- No public API addition or rename.
- No `docs/nav.yml` change because the edited helper is private.
- The existing dwelling grouping section in `context/ARCHITECTURE.md` and decision 0002
  remain valid; no new ADR is required for this defect repair.

## 6. Downstream handling

`PHX/from_HBJSON/_dwelling_occupancy.py` already uses
`number_dwelling_units >= 1` as its explicit-assignment test. Keep that guard in place
for compatibility with older honeybee-ph releases.

Replacing the PHX-local key logic with `honeybee_energy_ph.dwellings.dwelling_key()` is
an optional follow-up only after PHX raises its minimum honeybee-ph version to the
release containing this fix. It is not required to correct this repository and should
not expand the implementation patch.

## 7. Non-goals

- Changing how *HBPH - Set Dwelling* creates or shares explicit dwelling objects.
- Validating or coercing the type/range of `num_dwellings`.
- Changing `PhDwellings.identifier`, equality, hashing, duplication, or serialization.
- Repairing occupancy values already written after Rooms were incorrectly pooled.
- Addressing the existing PHX `max(total_ph_dwellings, 1)` behavior for purely
  non-residential merged segments.

## 8. Verification and acceptance

Focused verification:

```bash
.venv/bin/python -m pytest tests/test_honeybee_energy_ph/test_dwellings.py
```

Repository closeout:

```bash
.venv/bin/python -m coverage run
.venv/bin/python -m coverage report
```

Acceptance criteria:

- [x] The real two-Room unset regression fails before the code change and passes after it.
- [x] Untagged Rooms remain separate groups after a new-process HBJSON round-trip.
- [x] Any `PhDwellings` object with `num_dwellings < 1` contributes no assigned dwelling.
- [x] Explicit Rooms sharing one dwelling identifier still group together after round-trip.
- [x] Explicit single- and multi-dwelling counts remain unchanged.
- [x] The full suite passes with repository-wide coverage at or above the configured 75% floor.
- [x] Shipping code remains IronPython 2.7 compatible.

Final evidence, using the repository-local Python environment:

```text
.venv/bin/black --check honeybee_energy_ph/dwellings.py \
    tests/test_honeybee_energy_ph/test_dwellings.py
    2 files would be left unchanged

.venv/bin/python -m coverage run
    1020 passed in 57.10s

.venv/bin/python -m coverage report
    TOTAL 9858 statements, 80% coverage (75% required)
```

## 9. Closeout

- The implementation is complete and archived; no HBJSON field or migration was added.
- PHX retains its local `number_dwelling_units >= 1` compatibility guard.
- No package version was bumped and no release was published in this implementation loop.
- The release version should be recorded here when this branch is released.
