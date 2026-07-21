# Refactor: Decouple "Dwelling" from `Room.zone`

**Status:** Implemented (2026-07-21) — awaiting version bump, release, and install to
`ladybug_tools/`, after which `PHX` is unblocked. See §6.
**Date:** 2026-07-21
**Author:** Ed May + Claude
**Kind:** Cross-repo refactor. This repo (`honeybee_ph`) is the **primary** — it owns the
shared grouping helper the other two repos will consume.

**Companion docs (same slug in each repo):**
- `honeybee_grasshopper_ph/planning/dwelling-zone-decoupling.md` — the GH components (root cause)
- `PHX/planning/refactor/dwelling-zone-decoupling.md` — the downstream consumer

---

## 1. Problem Statement

Two unrelated concepts are sharing one attribute, `honeybee.room.Room.zone`:

| Concept | Question it answers | Correct home |
|---|---|---|
| **Dwelling** | "which rooms are one household? how many units?" | `People.properties.ph.dwellings` (`PhDwellings`) |
| **E+ Thermal Zone** | "which rooms share one air node + one HVAC?" | `Room.zone` |

`Room.zone` was inert when Honeybee-PH first adopted it as a convenient free-form tag for
dwelling identity. It is no longer inert: current `honeybee-energy` reads it as a real
translator instruction and groups Rooms into a single EnergyPlus Zone with multiple
`Space` objects.

The result is that tagging rooms as one *dwelling* silently merges them into one *thermal
zone* — a physical change to the energy model that nobody asked for.

### Why this repo is involved

`honeybee_ph` does not read `Room.zone` anywhere. It is nonetheless the right home for the
fix, because **three separate implementations of "aggregate by dwelling identity" now
exist**, and this repo already holds two of the ingredients (`PhDwellings` and one of the
implementations):

| # | Location | Mechanism | Correct? |
|---|---|---|---|
| 1 | `honeybee_energy_ph/load/phius_mf.py:120-123` `calc_num_dwellings()` | `set()` of `PhDwellings`, sum `num_dwellings` | Yes |
| 2 | `PHX/from_HBJSON/cleanup.py:196-216` `all_unique_ph_dwelling_objects()` | `set()` of `PhDwellings`, sum at `:234-238` | Yes |
| 3 | `honeybee_grasshopper_ph/.../set_res_program.py:79` `_group_rooms_by_dwellings()` | groups by `hb_room.zone` | **No — the outlier** |

Implementations 1 and 2 are byte-for-byte the same idea, duplicated across repos.
Implementation 3 is the one that forced `Room.zone` into service. Consolidating all three
onto one tested helper here removes both the duplication and the overload.

---

## 2. Evidence

### The behavior change that exposed it

| | 2514 MESH (working) | 2613 Ayers (broken) |
|---|---|---|
| hbjson schema | 1.58.6 | 2.1.2 |
| EnergyPlus | 23.2.0 | 25.1.0 |
| Rooms sharing one `zone` value | 6 (yes) | 6 (yes) |
| E+ `Zones` produced | **6** | **1** |

Identical model authoring; different translator behavior. `honeybee_energy/writer.py:555`:

```python
if room.identifier == room.zone:   # write the zone definition
```

…else the Room is written as a `Space` inside the shared Zone. Older versions ignored
`Room.zone` entirely.

### Downstream damage observed on 2613

- `in.idf`: **1** `Zone` object, **6** `Space` objects.
- `in.idf`: **1** `ZoneHVAC:IdealLoadsAirSystem` — the model authored six (one per Room,
  named from `host.identifier` per `honeybee_energy/properties/room.py:784`); **five were
  silently dropped** during translation.
- `HB Validate Model` reports the model invalid: *"The model has the following invalid zones
  served by different HVAC systems."*
- Zone-level E+ outputs (`Zone Heat Index`, `Zone Mean Air Temperature`, all
  `Zone Infiltration/Ventilation …`) collapse to a single series keyed `HBPH_DWELLING_…`.
  Only Space-keyed (`Enclosure …`) and People-keyed (`Zone Thermal Comfort Pierce Model
  SET`) outputs still report per-room.

This is a physics error, not a reporting error: the whole house simulated as one
perfectly-mixed air node under one HVAC system.

### Exhaustive attribute sweep

Both Grasshopper repos were swept for `Room.zone`, including the compiled user objects.
`.ghuser` files are **double raw-DEFLATE** (`zlib`, `wbits=-15`; outer at offset 0, inner
blob holds the `CodeInput` script) — a naive text grep returns a false negative on all of
them. Decompressed properly: **138 `.ghuser` scanned, 122 scripts extracted** (the 16
without scripts are value-list dropdowns: `Heating Types`, `Grid Regions`, etc.), plus all
283 `.py` and both `.ghx` installers.

**Total references to `Room.zone` across `honeybee_ph`, `honeybee_grasshopper_ph`,
`honeybee_REVIVE_grasshopper`, and `PHX`: exactly two** — the write at
`set_dwelling.py:113` and the read at `set_res_program.py:79`. PHX has zero. The map is
closed; there are no unknown consumers.

---

## 3. Design Decision

**`Room.zone` is reserved for EnergyPlus thermal zoning. Dwelling identity lives on
`People.properties.ph.dwellings`, always.**

The corollary, which resolves the long-standing "what *is* a Honeybee Room?" ambiguity:

> **An HB Room carries no intrinsic semantics. It is a geometry container. Every real
> concept — dwelling, thermal zone, building segment, TFA space — is expressed by its own
> explicit attribute, never inferred from Room granularity.**

This is already how PHX behaves (it merges Rooms away entirely and groups by
`ph_bldg_segment.identifier`). It accommodates every modeling case in use:

| Case | `zone` | `dwellings` |
|---|---|---|
| Whole SFH as one Room | own identifier | own `PhDwellings(1)` |
| SFH split into 6 floor-Rooms | own identifier each | one **shared** `PhDwellings(1)` |
| MF floor Room holding 4 apartments | own identifier | own `PhDwellings(4)` |
| One apartment spanning 2 Rooms | own identifier each | one **shared** `PhDwellings(1)` |
| Corridor / lobby (non-res) | own identifier | no People, or `PhDwellings(0)` |

`PhDwellings` carries **both** identity (shared object → one dwelling) and cardinality
(`num_dwellings` → N dwellings within one Room), which is what lets a single attribute
cover both the "N rooms → 1 dwelling" and "1 room → N dwellings" directions.

An ADR recording this belongs in `context/decisions/0002-*` once the work lands — see §6.

### Known limits (pre-existing; not introduced or fixed here)

1. **Partial overlap is inexpressible.** A duplex apartment spanning floors 3–4 in a
   building modeled floor-by-floor makes dwelling↔room many-to-many. `PhDwellings` cannot
   represent it; the count must be fudged. Out of scope — recorded so it is not
   rediscovered.
2. **Mixed-use rooms.** `PHX/from_HBJSON/cleanup.py:238` forces `max(total, 1)`, so a
   purely non-residential segment still reports 1 dwelling unit.

---

## 4. Scope for this repo

Add one tested, IronPython-safe helper and retire the local duplicate.

### 4.1 New module — `honeybee_energy_ph/dwellings.py`

Chosen over extending `properties/load/people.py` because grouping *Rooms* is a different
concern from the `PhDwellings` property object itself, and over `phius_mf.py` because the
helper is not MF-specific.

Public surface:

```python
def dwelling_key(hb_room):
    # type: (Room) -> str
    """Return the dwelling-grouping key for a HB-Room."""

def group_rooms_by_dwelling(hb_rooms):
    # type: (list[Room]) -> list[list[Room]]
    """Group HB-Rooms into dwellings, preserving input order."""

def unique_dwelling_objects(hb_rooms):
    # type: (list[Room]) -> list[PhDwellings]
    """Return the unique PhDwellings objects across a set of HB-Rooms."""

def total_dwelling_count(hb_rooms):
    # type: (list[Room]) -> int
    """Sum num_dwellings across unique PhDwellings objects."""
```

Required semantics:

- **Key** = `room.properties.energy.people.properties.ph.dwellings.identifier`.
- **`PhDwellings.default()` guard.** `PeoplePhProperties.__init__` assigns the
  class-level singleton `PhDwellings.default()`. Every Room never passed through
  *HBPH - Set Dwelling* therefore shares one identifier. Without a guard those Rooms would
  all collapse into a single fake dwelling — the mirror image of the bug being fixed.
  Rooms holding the default singleton must fall back to `room.identifier`.
- **Missing-People fallback.** Return `room.identifier` when `properties.energy` or
  `.people` is absent. Note `phius_mf.py:120-123` currently has *no* such guard and will
  raise `AttributeError` on a People-less Room — consolidating fixes that latent bug.
- **Order preservation.** Return groups in first-appearance order so GH branch output is
  deterministic across solves.

### 4.2 Constraint: IronPython 2.7

`honeybee_energy_ph` is imported by Grasshopper components running under IronPython 2.7 in
Rhino. Despite `pyproject.toml` declaring `requires-python = ">=3.10"`, every module in
this package carries `# -*- Python Version: 2.7 -*-` and must stay 2.7-compatible:

- type **comments**, never annotations
- `.format()`, never f-strings
- no `pathlib`, no `dataclasses`, no walrus

Verify against `honeybee_energy_ph/properties/load/people.py` as the reference style.

**This constraint is real, not vestigial** — verified two ways:

1. `honeybee_energy_ph` is currently **100% 2.7-clean**: zero f-strings, zero return
   annotations across the package.
2. Every GH component front-end calls the bare builtin `reload(...)`
   (`honeybee_grasshopper_ph/src/*.py`), which exists in IronPython 2.7 but **not** in
   Python 3. These components are running on the IronPython GHPython component.

The `ladybug_tools/python/lib/python3.10/site-packages/` install path is misleading on this
point — it is where the packages are *installed*, not the interpreter that imports them.

### 4.3 Install step

The Rhino runtime imports from
`/Users/em/ladybug_tools/python/lib/python3.10/site-packages/`, which holds **real installed
copies** (currently `honeybee_ph-1.33.28.dist-info`), not symlinks to this repo. Editing here
has no effect in Grasshopper until the package is installed/synced and Rhino is restarted.
Budget for that step before any GH-side verification.

### 4.4 Retire the local duplicate

Rewrite `honeybee_energy_ph/load/phius_mf.py:120-123` `calc_num_dwellings()` to delegate to
`total_dwelling_count()`. Behavior must be identical for the People-present case.

### 4.5 Tests — `tests/test_honeybee_energy_ph/test_dwellings.py`

This is the **only** repo of the three where this logic can be unit-tested. The GH component
module cannot be imported outside Rhino (`ph_gh_component_io.gh_io` raises `ImportError:
Failed to import System` — verified, unguarded). Moving the logic here is what makes it
testable at all.

Required cases:

| Case | Expectation |
|---|---|
| 6 Rooms sharing one `PhDwellings(1)` | 1 group; `total_dwelling_count == 1` |
| 4 Rooms with distinct `PhDwellings(1)` | 4 groups; total `== 4` |
| 1 Room with `PhDwellings(4)` | 1 group; total `== 4` |
| Mixed: 2 shared + 1 distinct | 2 groups |
| Rooms never through Set Dwelling (default singleton) | N groups, one per Room |
| Room with `people = None` | own group; no exception |
| Room with no `.properties.energy` | own group; no exception |
| Group ordering | first-appearance order, stable |

---

## 5. Sequence

**Landing order across the three repos (decided 2026-07-21):**

```
1. honeybee_ph   →  deploy/install  →  2. PHX   →  deploy/install  →  3. honeybee_grasshopper_ph
```

Each repo must be released and installed before the next begins, since each consumes the
previous. Do not batch them — the install step (§4.3) is what makes a change real, and
verifying repo N+1 against an un-updated install of repo N produces false results.

PHX lands **before** the Grasshopper repo (not after) because PHX has real test coverage: it
validates the shared helper against golden `NumberUnits` values while the GH side is still
untouched, isolating any helper defect from any component defect.

Within this repo:

1. `honeybee_energy_ph/dwellings.py` + tests → green.
2. `phius_mf.py` delegates to it → existing MF tests still green.
3. Full suite green; release/bump.
4. Install to `ladybug_tools/.../site-packages/`; hand off to `PHX`.

---

## 6. Definition of Done

- [x] `dwellings.py` added, IronPython-2.7-safe, full test coverage per §4.5 — **21 tests**
- [x] `phius_mf.calc_num_dwellings()` delegates; MF tests unchanged and green (62 passed)
- [x] Full `pytest` suite green — **761 passed**
- [x] ADR [`context/decisions/0002-dwelling-identity-not-room-zone.md`](../../context/decisions/0002-dwelling-identity-not-room-zone.md) recording §3
- [x] `context/ARCHITECTURE.md` — new "Grouping concepts" section
- [ ] Version bump + release
- [ ] Install to `ladybug_tools/.../site-packages/` (§4.3)
- [ ] `PHX` unblocked; row updated in `planning/STATUS.md`
- [ ] On completion of all three repos: move to `planning/archive/dwelling-zone-decoupling/`

### Implemented API (as built)

```python
from honeybee_energy_ph.dwellings import (
    get_dwelling_obj,          # (Room) -> PhDwellings | None
    dwelling_key,              # (Room) -> str
    group_rooms_by_dwelling,   # (list[Room]) -> list[list[Room]]
    unique_dwelling_objects,   # (list[Room]) -> list[PhDwellings]
    total_dwelling_count,      # (list[Room]) -> int
)
```

`get_dwelling_obj()` returns `None` for a Room with no energy properties, no People load,
or still carrying the `PhDwellings.default()` singleton. That single predicate drives the
agreed split in null handling:

- **grouping** — `dwelling_key()` falls back to `room.identifier`, so an untagged Room
  groups alone rather than collapsing with every other untagged Room;
- **counting** — untagged Rooms contribute **zero**, never a phantom dwelling.

---

## 7. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Helper accidentally uses py3-only syntax → breaks all GH components at import | **High** | Review against `people.py`; no annotations/f-strings |
| Default-singleton guard omitted → untagged Rooms collapse into one dwelling | **High** | Explicit test case; called out in §4.2 |
| `phius_mf` delegation changes MF load math | Medium | Existing MF tests must pass unchanged |
| Dwelling counts shift in WUFI/PHPP output | **High** | Verified downstream in the PHX companion doc |
