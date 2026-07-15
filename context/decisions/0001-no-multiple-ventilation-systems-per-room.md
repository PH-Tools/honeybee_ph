# 0001 — Do NOT Add Multiple Ventilation Systems per Room (for now)

**Date:** 2026-07-14
**Status:** DECIDED — not implementing
**Decider:** Ed May
**Research:** [`planning/refactor/multiple-ventilation-systems.md`](../../planning/refactor/multiple-ventilation-systems.md)

## Context

`RoomPhHvacProperties` holds a single `_ventilation_system`
(`Optional[PhVentilationSystem]`), unlike the plural `set()` + `add_*()`
pattern used for heating, heat pumps, exhaust devices, etc. Real projects
occasionally need multiple ERV units serving one Space (supply from unit A /
extract via unit B; very large spaces with 2+ units; different units on
different schedules).

A full cross-repo investigation was completed (2026-07-14) covering
honeybee_ph, PHX, honeybee_grasshopper_ph, honeybee_grasshopper_ph_plus,
honeybee-ph-schema, and ph-navigator-v2. See the research doc for the
complete usage inventory, backward-compat design, serialization matrix, and
phased plan.

## Decision

**Do not implement the plural refactor at this time.**

## Rationale

1. **WUFI-Passive cannot represent it.** Verified by hand in WUFI-Passive
   itself (Ed, 2026-07-14): a single Space can **only** be served by a
   single Ventilator — the UI/data model does not allow multiple
   ventilator assignments per space. This is a hard ceiling, not a PHX
   modeling choice.
2. **METr has the same constraint** as WUFI-Passive (single ventilator per
   space).
3. **PHPP is the exception**: the Additional Ventilation worksheet *does*
   support multiple units per room/space. But PHPP-only support doesn't
   justify the change while WUFI (our primary Phius certification path)
   cannot consume it.
4. Pluralizing honeybee-ph alone would create a data model that can hold
   systems the downstream tools silently drop — worse than not holding
   them at all (silent data loss during certification modeling).

## What would reopen this decision

- WUFI-Passive adds multi-ventilator-per-space assignment (or Phius/METr
  workflow changes make PHPP-style multi-unit assignment the target).
- A compelling PHPP-only workflow need arises.

## Head start if reopened

The research doc is implementation-ready. Key facts (validated 2026-07-14):

- Total downstream surface is only **5 call sites across 4 repos** — 2 in
  PHX, 1 writer in honeybee_grasshopper_ph, 1 reader in
  honeybee_grasshopper_ph_plus, 1 in ph-navigator-v2 (which is otherwise
  already plural end-to-end). honeybee_energy_ph and honeybee-ph-schema
  need nothing.
- Recommended design: explicit ordered `PhVentilationSystemCollection`
  (identifier-unique, insertion-ordered → deterministic "primary");
  **plain compat property** returning first-or-None (NOT a
  `__getattr__` proxy — PHX writes attributes back onto the system, and
  all consumers use `get → truthiness → attribute` so a real object is
  strictly safer); dual-key HBJSON writing (`ventilation_systems` list +
  legacy `ventilation_system` echo) to protect mixed-version environments.
- The one genuinely hard work-package is PHX Phase 2b: emitting multiple
  WUFI room-ventilation rows per Space, plus a flow-apportionment rule
  (recommended: per-assignment supply/extract fractions). This is also the
  part now blocked by WUFI itself.

## Workaround in the meantime

For spaces genuinely served by two units, split the honeybee-ph Space (two
Spaces, one per ventilator, with apportioned airflows) — mirroring how it
must be modeled manually in WUFI-Passive anyway.
