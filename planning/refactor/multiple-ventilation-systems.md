# Refactor: Multiple Ventilation Systems per Room

**Status:** NOT IMPLEMENTED — see decision record
[`context/decisions/0001-no-multiple-ventilation-systems-per-room.md`](../../context/decisions/0001-no-multiple-ventilation-systems-per-room.md).
WUFI-Passive (and METr) only allow ONE ventilator per space (hand-verified in
WUFI-Passive, 2026-07-14); PHPP Additional Ventilation supports multiple, but
that alone doesn't justify the change. Research below retained as a head
start if WUFI ever adds multi-unit assignment.
**Date:** 2026-07-14
**Author:** Ed May + Claude (research fan-out across all 6 repos)

---

## 1. Problem Statement

`RoomPhHvacProperties` (`honeybee_phhvac/properties/room.py`) holds a **single**
`_ventilation_system` (`Optional[PhVentilationSystem]`), while every other
multi-capable system on the same class uses a `set()` + `add_*()` pattern
(`_heating_systems`, `_heat_pump_systems`, `_exhaust_vent_devices`,
`_supportive_devices`, `_renewable_devices`).

Real-world cases requiring **multiple ventilation systems per Space**:

1. **Split supply/extract** — supply air from ERV-A, extract air via ERV-B.
2. **Large space, multiple units** — one big volume served by 2+ ERVs.
3. **Time-of-day / seasonal units** — different units operating on different
   schedules.

The single-unit case remains the overwhelming norm and must stay simple.

---

## 2. Current State (honeybee_ph)

### The single-system API surface (`honeybee_phhvac/properties/room.py`)

| Line | What | Category |
|---|---|---|
| 50 | `self._ventilation_system = None` | storage |
| 63–66 | `ventilation_system` property (returns `Optional[PhVentilationSystem]`) | read |
| 98–101 | `set_ventilation_system()` (overwrite) | write |
| 140 | `clear_systems()` → `= None` | clear |
| 159 | `to_dict()` → singular key `"ventilation_system"` (dict-or-None) | serialize |
| 192–194 | `from_dict()` reads singular key, truthiness-guarded | deserialize |
| 228–239 | `apply_properties_from_dict()` (abridged path): single id lookup | deserialize |
| 270 | `duplicate()` — single, truthiness-guarded | copy |
| 305–306, 347–348, 385–386, 422–423, 460–461 | `move / rotate / rotate_xy / reflect / scale` | transforms |
| 513–519 | `get_ventilation_system_from_space()` module helper — **public API, zero in-repo callers** (consumers are PHX + GH) | read |

**Ventilation is the ONLY system with live geometry transforms** (it carries
`supply_ducting` / `exhaust_ducting` `PhDuctElement` geometry). The
heating/heat-pump/etc. transform loops are all commented out ("Not
Implemented"). Each transform reassigns the *returned* transformed object
(`self.set_ventilation_system(self._ventilation_system.move(vec))`) — the
collection version must iterate-and-rebuild.

### Model-level abridged round-trip (`honeybee_phhvac/properties/model.py`)

`_build_mechanical_devices_from_dict()` (L71–110) scans all room dicts,
deserializing each system once into an **identifier-keyed dict** — this is the
dedup mechanism. Ventilation reads the **singular** room-dict key at L87–89
into the (already-plural-named!) model-level bucket
`mechanical_systems["ventilation_systems"]`. Heating at L91–92 is the exact
list-iteration template to copy.

### The target pattern (heating, to mirror)

- storage `set()`; property returns `Set[...]`; `add_*()` guards falsy then `.add()`
- `to_dict()`: **sorted** list (via `__lt__` on identifier), None-filtered, plural key
- `from_dict()`: `for d in _input_dict.get("heating_systems", []): add_*(...)`
- abridged: id-list → loop lookup in model-level dict
- space helper returns `set()` (never `None`)

`PhVentilationSystem` already inherits `__hash__` (by identifier), `__eq__`,
and `__lt__` (by identifier) from `_PhHVACBase` — **it is set-safe and
sort-safe today, no class changes needed.**

### Not affected (confirmed)

- `honeybee_energy_ph` (deprecated pkg): **zero** parallel pattern; its
  "ventilation" refs are honeybee-energy loads/programs. No changes.
- `honeybee_ph/bldg_segment.py` `ventilation_system_ach` /
  summer-bypass: unrelated segment-level scalars. No changes.
- Tests: only `tests/test_honeybee_phhvac/test_properties/test_room.py:66,77`
  touch the API (round-trip + duplicate assertions on dict equality).

---

## 3. Downstream Usage Inventory (complete)

The total downstream surface is remarkably small: **5 code sites across 4 repos.**

### 3.1 PHX — 2 sites (the critical consumer)

| Site | What it does | Breaks if property → collection? |
|---|---|---|
| `PHX/from_HBJSON/create_rooms.py:136–138` | `if space_ph_hvac.ventilation_system:` → assigns `.id_num` / `.display_name` to `PhxSpace.vent_unit_id_num` (a **scalar**) | Yes (`AttributeError`) — unless compat property retained |
| `PHX/from_HBJSON/create_variant.py:522` (in `add_ventilation_systems_from_hb_rooms`, L505–550; imports helper at L23) | `get_ventilation_system_from_space(space)` → `if not x: continue` → `.key`, `.ventilation_unit`, `.supply_ducting`, `.exhaust_ducting`; get-or-build `PhxDeviceVentilator` (dedup by `.key` via `get_mech_device_by_key`), aligns `id_num` back onto the HBPH objects, adds ducting | Yes — unless helper stays singular |

- PHX **never writes** `ventilation_system` back to honeybee-ph (no
  `to_HBJSON` exists). One-directional risk only.
- PHX never reads the HBJSON **key** directly — it consumes deserialized
  attributes, so the wire-format change is a honeybee-ph-internal concern.
- Multi-system templates already in PHX to mirror:
  `add_heating_systems_from_hb_rooms` (L601–633),
  `add_heat_pump_systems_from_hb_rooms` (L636–668),
  `add_exhaust_vent_devices_from_hb_rooms` (L553–598).

### 3.2 ⚠️ Hard constraint: WUFI/PHPP are single-ventilator-per-space

The downstream model **cannot represent multiple ventilators per space** today:

- `PhxSpace` (`PHX/model/spaces.py:98–99`): scalar `vent_unit_id_num` +
  `vent_unit_display_name`. Space-merging logic keys on it (L36–56, 130–156).
- PHX ducts (`model/hvac/ducting.py:101`): single `vent_unit_id` each.
- WUFI XML (`to_WUFI_XML/xml_schemas.py:936`): one `IdentNrVentilationUnit`
  per room row; `merge_spaces_by_erv` groups by the single id (L200–215).
- PHPP (`PHPP/phpp_app.py:611–648`): one ventilator resolved per
  `VentSpaceRow` from `room.vent_unit_id_num`.
- METr JSON: same pattern (`to_METr_JSON/metr_schemas.py:961–972`).

**Consequence:** pluralizing honeybee-ph alone gets the *devices and ducting*
into the PHX mech-collection (WUFI Systems tab), but a space can still only
*reference* one unit. Truly expressing "supply from A / extract from B"
requires new PhxSpace-level representation — most naturally by **emitting
multiple WUFI room-ventilation rows per Space** (row 1: unit A,
supply-flow only; row 2: unit B, extract-flow only), which is exactly how
one would model it manually in WUFI. That is Phase-2 design work in PHX
(see §7).

### 3.3 honeybee_grasshopper_ph — 1 site (writer)

- `honeybee_ph_rhino/gh_compo_io/hvac/add_systems.py:30,46–47,51` —
  **"HBPH - Add Mech Systems"** component: single `_vent_sys` input →
  `new_hvac.set_ventilation_system(...)`. The heating branch in the *same*
  `run()` (L55–59: list input + `add_heating_system` loop) is the exact
  UI template to mirror.
- `create_vent_sys.py` ("HBPH - Create Ventilation System") only *produces*
  a `PhVentilationSystem` — unaffected.
- `.ghuser` binaries contain no plaintext references — only the
  `gh_compo_io` source needs changes (+ regenerated components).

### 3.4 honeybee_grasshopper_ph_plus — 1 site (reader)

- `honeybee_ph_plus_rhino/gh_compo_io/reporting/build_erv_duct_objects.py:117`
  — **"HBPH+ - Create ERV Duct Model Objects"**: reads
  `room.properties.ph_hvac.ventilation_system` per room, dedupes by
  `display_name`, renders duct geometry. With a first-only compat shim it
  keeps working but silently omits 2nd+ systems' ducting from previews —
  should be updated to iterate in the GH phase.
- SQL/reporting packages: no other hits (the `_v_sup`/`_v_eta` refs are
  space airflow *loads*, unrelated).

### 3.5 ph-navigator-v2 — 1 site

- `backend/features/model_viewer/extraction.py:248` — sole load-bearing
  line (`system = room.properties.ph_hvac.ventilation_system`, deduped by
  `display_name`). **Everything downstream of it is already plural**:
  `CombinedModelDataSchema.ventilation_systems: list[...]`, the
  `/ventilation_systems` route, MCP tools, frontend TS types, and the 3D duct
  renderer (`lineElements.ts:27–36`) all iterate lists. Migration = ~3-line
  loop change + honeybee-ph pin bump. It never reads HBJSON keys directly
  (parses via `Model.from_dict`), so the compat property alone keeps it
  running (first-system-only) with zero edits.

### 3.6 honeybee-ph-schema — nothing to migrate (greenfield)

The repo is an early-stage, hand-authored Pydantic-v2 scaffold:
`PhHvacProperties` is a one-field placeholder with `extra="allow"`; no
`ventilation_system` field exists; the "sync-from-runtime" scripts are no-op
stubs; primary intended consumer is C# codegen. When room-level HVAC gets
modeled there, author it **plural-first** with an optional deprecated
singular field. No blocking work for this refactor.

---

## 4. Design Decision A — Collection Type

### Options

1. **Plain `set()`** — exact mirror of `_heating_systems`.
2. **Explicit `PhVentilationSystemCollection` class** — identifier-keyed,
   insertion-ordered, iterable.

### Recommendation: explicit `PhVentilationSystemCollection` ✓

The decisive argument is **deterministic "primary system" semantics**. The
backwards-compat `ventilation_system` property (§5) must return *the* system
for single-system models and a *stable, meaningful* choice for multi-system
models. A `set()` makes that nondeterministic (or forces sort-by-UUID, which
is stable but arbitrary). An ordered collection gives **primary = first
assigned**, which is what users will intuitively expect and what the GH
component input order will naturally produce.

Secondary arguments:

- **Room for growth**: per-assignment metadata (flow fractions,
  supply-only/extract-only role, operating schedule — see §6.1) can later be
  attached at the collection/assignment level without another breaking change.
- **Precedent**: PHX already uses this shape
  (`PhxMechanicalSystemCollection`, `PHX/model/hvac/collection.py:498`).
- Dedup-by-identifier on `add()` (same guarantee the model-level dict
  provides today).

IronPython 2.7 note: plain dicts do **not** preserve insertion order — the
collection must keep an explicit internal `list` (with identifier-membership
check on add), not rely on dict ordering.

Sketch:

```python
class PhVentilationSystemCollection(object):
    """Ordered, identifier-unique collection of PhVentilationSystems serving a Room."""

    def __init__(self):
        self._systems = []  # type: list[PhVentilationSystem]  # insertion-ordered

    def add(self, _system):        # dedup by identifier, falsy-guard
    def clear(self):
    def __iter__(self):            # iterate in insertion order
    def __len__(self):
    def __contains__(self, key_or_system):
    def __bool__(self) / __nonzero__(self):   # IronPython 2.7 needs __nonzero__
    @property
    def primary(self):             # -> Optional[PhVentilationSystem]  (first or None)
    def to_dict(self) / from_dict() / duplicate()
    def move/rotate/rotate_xy/reflect/scale(...)  # loop over systems, rebuild
```

### Convert the other system collections (heating, heat-pumps, …) too?

**Not in this refactor.** They work, nothing downstream needs it, and it
triples the blast radius for zero functional gain (violates the surgical-change
rule). Instead: design `PhVentilationSystemCollection` so its shape *could*
be generalized into a shared `_PhHVACSystemCollection` base later, and note
the consistency cleanup as an optional follow-on (Phase 5, unscheduled).
One nuance if ever done: heating's `to_dict()` sorts by identifier, so its
serialization order is already stable — migrating it to insertion-order would
churn dict-equality tests.

---

## 5. Design Decision B — Backwards Compatibility Mechanism

### The question asked: `__getattr__` / `__getattribute__` proxying?

Idea: `ventilation_system` returns the *collection*, which delegates unknown
attribute access (`.id_num`, `.key`, `.ventilation_unit`, …) to its primary
system, so downstream code "just works".

### Recommendation: NO proxy — use a plain compat property instead ✓

The research makes this an easy call. **Every one of the 5 downstream call
sites follows the identical pattern**:

```python
x = ph_hvac.ventilation_system          # (or get_ventilation_system_from_space)
if not x: ...                           # truthiness / None guard
x.id_num / x.key / x.display_name / x.supply_ducting / ...   # attribute reads
```

A compat **property returning `primary` (first-or-None, a real
`PhVentilationSystem`)** satisfies 100% of observed usage with zero magic.
The proxy would deliver *the same* single-system behavior (it can only
delegate to one system) while adding real failure modes:

- `x is None` checks fail (proxy is never `None`) — the exact idiom
  `.get(vent_system_id, None)` patterns produce.
- `isinstance(x, PhVentilationSystem)` fails.
- `type(x)`, `copy`, pickling, `sorted([...])`, dict-keying by the object,
  and `__eq__`/`__hash__` semantics all become ambiguous.
- Attribute *writes* (PHX does `hbph_vent_sys.id_num = phx_ventilator.id_num`
  at `create_variant.py:539–541`!) would need `__setattr__` delegation too —
  deep magic territory.
- `__getattribute__` specifically: intercepts *every* lookup including
  internals; a perf and debugging trap. Never justified here.

Both approaches share the same semantic ceiling — old code sees only the
primary system — so choose the one that is transparent about it.

### The compat surface (Phase 1 API)

| API | Behavior |
|---|---|
| `ventilation_systems` (new property) | returns the `PhVentilationSystemCollection` |
| `add_ventilation_system(sys)` (new) | append (dedup by identifier, falsy-guard) |
| `ventilation_system` (kept) | **deprecated read**: returns `collection.primary` (first-or-None) — keeps PHX, GH-plus, ph-navigator working unchanged |
| `set_ventilation_system(sys)` (kept) | **deprecated write**: `clear()` then `add()` (preserves overwrite semantics); `set_ventilation_system(None)` → `clear()` — keeps the GH writer working unchanged |
| `get_ventilation_system_from_space(space)` (kept) | deprecated: returns primary-or-None — keeps PHX `create_variant.py:522` working unchanged |
| `get_ventilation_systems_from_space(space)` (new) | returns the collection (empty when no host), mirroring `get_heating_systems_from_space` |

Deprecation signaling: docstring `.. deprecated::` notes + optional
`warnings.warn(DeprecationWarning)` (works in IronPython 2.7; keep it quiet —
Rhino users see stderr).

---

## 6. Serialization / HBJSON Compatibility

### The version-pairing matrix

| HBJSON written by | Read by | Outcome |
|---|---|---|
| old (singular key) | **new** | ✅ `from_dict` falls back to singular key → 1-item collection |
| new (plural key) | **new** | ✅ reads plural key |
| new | **old** honeybee-ph | ⚠️ old code does `.get("ventilation_system")` → `None` → **entire vent system + ducting silently vanish** from the model |
| old | old | ✅ unaffected |

The third row is the dangerous one, and it is a *real* scenario: mixed
package versions across office machines / a certifier re-opening an HBJSON /
GH plugin updated but PHX env not (PHX pins `honeybee-ph>=…`, ph-navigator
pins `honeybee-ph>=1.33.19`).

### Recommendation: dual-key writing for a transition period ✓

`to_dict()` writes **both**:

- `"ventilation_systems"`: `[sys.to_dict() for sys in collection]` (new,
  authoritative, insertion order)
- `"ventilation_system"`: `collection.primary.to_dict() or None` (legacy
  echo)

Old readers degrade gracefully to the primary system (perfect fidelity for
the normal single-system case — the vast majority of every model in
production). New readers **prefer the plural key and ignore the singular when
plural is present** (avoid double-add; the identifier-dedup on `add()` makes
this safe anyway). Cost: a small duplicated dict in HBJSON. Remove the legacy
key in a later major release.

Same dual-read logic needed in all three deserialization paths:

1. `RoomPhHvacProperties.from_dict()` (room.py:192)
2. `RoomPhHvacProperties.apply_properties_from_dict()` (room.py:228–239) —
   plural id-list with singular-key fallback
3. `ModelPhHvacProperties._build_mechanical_devices_from_dict()`
   (model.py:87–89) — note the pre-existing model-level bucket is *already*
   named `"ventilation_systems"`; the room-level plural key will now match it
   (fine — different dict scopes — but call it out in review comments)

### honeybee-ph-schema

Greenfield (§3.6): model plural-first, include optional
`ventilation_system` marked `Field(deprecated=True)`, regenerate
`schemas/*` artifacts, classify PR as "backward-compatible-drift".

---

## 7. Edge Cases & Open Design Questions

### 7.1 ❓ Flow apportionment (THE open question — needs Ed's call)

When a Space has 2+ ventilation systems, how do its supply/extract airflows
divide among the units? This doesn't matter for honeybee-ph storage but is
unavoidable the moment PHX writes WUFI/PHPP:

- **(a) Even split** — PHX divides `V_sup`/`V_eta` equally across systems.
  Simple, wrong for asymmetric cases.
- **(b) Role flags** — supply-from-A/extract-from-B needs per-assignment
  role metadata (`supply`, `extract`, `both`). Covers use-case 1 exactly.
- **(c) Explicit fractions** — per-assignment `flow_fraction` covers
  use-cases 1 AND 2 (`supply_fraction` / `extract_fraction` per system,
  default `1/n`).
- **(d) Punt to v2** — Phase 1 stores bare systems; PHX splits evenly (a);
  richer assignment metadata added later *on the collection* (the collection
  class makes this a non-breaking addition — a key §4 argument).

Leaning: **(d) now, designing toward (c)** — per-system
`supply_fraction`/`extract_fraction` on an assignment wrapper covers both
split-role (1.0/0.0) and shared-load (0.5/0.5) cases with one mechanism.
**To discuss before Phase 2.**

WUFI mapping for multi-unit spaces: emit **one WUFI room-ventilation row per
(space × system)** with apportioned flows — matches how it's modeled manually
in WUFI. PHPP: multiple `VentSpaceRow`s per space likewise.

### 7.2 Time-of-day / seasonal units (use-case 3)

WUFI room rows carry utilization patterns (days/weeks factors); apportionment
by *time* would map to per-row operation factors rather than flow fractions.
Out of scope for Phase 1; note as a future extension of the assignment
metadata. **To discuss.**

### 7.3 Silent-drop windows during migration

Until each consumer's "iterate" update ships, multi-system rooms degrade to
primary-only in: PHX output (2nd+ units AND their ducting missing from
WUFI/PHPP — **worst case, do PHX first**), GH-plus duct previews,
ph-navigator viewer/MCP. Mitigation: don't advertise/enable the multi-system
GH input until PHX support ships (Phase ordering, §8); optionally have PHX
log a warning when it encounters >1 system pre-Phase-2.

### 7.4 Mechanical details to not miss in Phase 1

- **Transforms**: all 5 (`move/rotate/rotate_xy/reflect/scale`) must
  iterate-and-rebuild the collection (transform methods return new objects).
  Ventilation is the only system with live transform code — don't drop it.
- **`clear_systems()`** (room.py:140) → `collection.clear()`.
- **`duplicate()`** → duplicate every system, preserve order.
- **Truthiness trap**: if any old code path receives the collection where it
  expects the single object, a *non-empty* collection is truthy and falls
  through to attribute access → crash. The compat property prevents this;
  grep-verify no internal path leaks the collection into old guards.
- **PHX id_num write-back** (`create_variant.py:539–541`) mutates the HBPH
  system objects — collection must hand out the *actual* stored objects, not
  copies.
- **Duplicate identifiers**: two *different* systems sharing an identifier
  silently overwrite in the model-level dict today; collection `add()` keeps
  the same last-wins (or first-wins — pick and document) semantics.
- **Tests**: `test_room.py:66,77` assert dict equality — update for the new
  shape (incl. dual-key output); add: multi-system round-trip, order
  preservation, dedup-on-add, legacy-key-only load, dual-key no-double-read,
  transforms over multiple systems, compat property/setter behavior.
  Coverage target is 100% (`fail_under = 100`).
- **Docs**: new collection class + changed methods into `docs/nav.yml`,
  AUTODOC-format docstrings per `docs/.instructions.md`.

---

## 8. Phased Implementation Plan (outline — detail each before starting)

Dependency-ordered; each phase ships independently behind the compat shim.

### Phase 1 — honeybee_ph (foundation; everything keeps working)
1. `honeybee_phhvac/ventilation.py` (or new `ventilation_collection.py`):
   `PhVentilationSystemCollection` (ordered, identifier-unique, transforms,
   to/from_dict, duplicate, `primary`).
2. `properties/room.py`: swap storage; new `ventilation_systems` /
   `add_ventilation_system`; compat `ventilation_system` /
   `set_ventilation_system`; dual-key `to_dict`; dual-read `from_dict` +
   `apply_properties_from_dict`; transforms loop; `clear_systems`;
   new + compat space helpers.
3. `properties/model.py`: dual-read `_build_mechanical_devices_from_dict`.
4. Tests (§7.4), docs, `bump-my-version` minor bump, release.
   **Gate: full test suite + round-trip of a real project HBJSON.**

### Phase 2 — PHX (the real feature)
- 2a (safe, immediate): `add_ventilation_systems_from_hb_rooms` iterates
  `get_ventilation_systems_from_space` (mirror heating loop) — all units +
  ducting reach the mech collection; `create_rooms.py` keeps primary for
  `vent_unit_id_num`; warn on >1 system. Bump honeybee-ph pin.
- 2b (design first — flow apportionment §7.1): multi-row space→ventilation
  representation through `PhxSpace` → WUFI XML rooms → PHPP VentSpaceRows →
  METr; `merge_spaces_by_erv` interaction.
- Hand off as a PHX feature-request doc, or do it ourselves — 2a is trivial,
  2b is the one genuinely hard work-package in this whole refactor.

### Phase 3 — Grasshopper UIs (after Phase 2a ships)
- `honeybee_grasshopper_ph` "HBPH - Add Mech Systems": `_ventilation_system`
  input → list, loop `add_ventilation_system` (mirror heating input directly
  above it); regenerate component.
- `honeybee_grasshopper_ph_plus` `build_erv_duct_objects.py:117`: iterate all
  systems so duct previews are complete.

### Phase 4 — ph-navigator-v2 + schema
- `extraction.py:248` → loop; bump honeybee-ph pin. (3 lines.)
- honeybee-ph-schema: when HVAC modeling lands, plural-first (§6).

### Phase 5 (optional, unscheduled) — collection-class consistency
Generalize to `_PhHVACSystemCollection`; migrate heating/heat-pump/etc.
Pure consistency cleanup; no functional driver.

---

## 9. Key File Reference

| Repo | Files |
|---|---|
| honeybee_ph | `honeybee_phhvac/properties/room.py`, `honeybee_phhvac/properties/model.py`, `honeybee_phhvac/ventilation.py`, `honeybee_phhvac/_base.py`, `tests/test_honeybee_phhvac/test_properties/test_room.py` |
| PHX | `from_HBJSON/create_variant.py` (505–550, 993), `from_HBJSON/create_rooms.py` (136–138), `from_HBJSON/create_hvac.py` (72–162), `model/spaces.py` (98–99), `model/hvac/ducting.py` (101), `model/hvac/collection.py` (498), `to_WUFI_XML/xml_schemas.py` (200–215, 936, 1500), `PHPP/phpp_app.py` (611–648), `to_METr_JSON/metr_schemas.py` (961–972) |
| honeybee_grasshopper_ph | `honeybee_ph_rhino/gh_compo_io/hvac/add_systems.py` (30, 46–51) |
| honeybee_grasshopper_ph_plus | `honeybee_ph_plus_rhino/gh_compo_io/reporting/build_erv_duct_objects.py` (117–133) |
| ph-navigator-v2 | `backend/features/model_viewer/extraction.py` (246–265), `backend/pyproject.toml` (pin) |
| honeybee-ph-schema | `honeybee_ph_schema/ph_hvac.py` (greenfield) |
