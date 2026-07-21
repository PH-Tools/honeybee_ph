# 0002 — Dwelling Identity Lives on `PhDwellings`, NOT on `Room.zone`

**Date:** 2026-07-21
**Status:** DECIDED — implementing
**Decider:** Ed May
**Research:** [`planning/refactor/dwelling-zone-decoupling.md`](../../planning/refactor/dwelling-zone-decoupling.md)
**Companion repos:** `honeybee_grasshopper_ph/planning/dwelling-zone-decoupling.md`,
`PHX/planning/refactor/dwelling-zone-decoupling.md`

## Context

Honeybee-PH adopted `honeybee.room.Room.zone` as a convenient free-form tag for
dwelling identity: `HBPH - Set Dwelling` wrote the dwelling name to `Room.zone`, and
`HBPH - Set Residential Program` read it back to group Rooms into dwellings.

That was safe while `Room.zone` was inert. It no longer is. Current honeybee-energy
reads `Room.zone` as an **EnergyPlus thermal-zone grouping instruction**
(`honeybee_energy/writer.py`: `if room.identifier == room.zone:` → write a Zone, else
write a `Space` inside the shared Zone). Rooms sharing a `zone` value are merged into
one E+ Zone — one air node, one HVAC system.

Observed on project 2613 Ayers (hbjson 2.1.2 / EnergyPlus 25.1.0): six Rooms tagged as
one dwelling produced **1 `Zone` + 6 `Space` objects**, and **1**
`ZoneHVAC:IdealLoadsAirSystem` where the model authored six — five were silently
dropped in translation. `HB Validate Model` reported the model invalid. The same
definition under hbjson 1.58.6 / E+ 23.2.0 (project 2514) produced six Zones correctly.

So tagging Rooms as one *dwelling* silently merged them into one *thermal zone*: a
physics change to the energy model that nobody requested, and a passive-survivability
simulation run on a single perfectly-mixed air node.

## Decision

**`Room.zone` is reserved exclusively for EnergyPlus thermal zoning. Dwelling identity
is carried by `PhDwellings`, always** — reached via
`room.properties.energy.people.properties.ph.dwellings`.

The corollary, which resolves the recurring "what *is* a Honeybee Room?" ambiguity:

> An HB Room carries no intrinsic semantics. It is a geometry container. Every real
> concept — dwelling, thermal zone, building segment, TFA space — is expressed by its
> own explicit attribute, never inferred from Room granularity.

| Concept | Question it answers | Attribute |
|---|---|---|
| Dwelling | which rooms are one household? how many units? | `People.properties.ph.dwellings` |
| E+ Thermal Zone | which rooms share one air node + one HVAC? | `Room.zone` |
| Building Segment | which WUFI case / PHPP file? | `Room.properties.ph.ph_bldg_segment` |
| TFA Space | which PHPP room? | `Room.properties.ph.spaces` |

Grouping is implemented once, in `honeybee_energy_ph/dwellings.py`, and consumed by
both `honeybee_grasshopper_ph` and `PHX`.

## Rationale

1. **`PhDwellings` was already the real carrier.** `HBPH - Set Dwelling` has always
   built a `PhDwellings` object and attached it to every Room's People load. The
   `Room.zone` write was redundant — and, on 2613, its *only* surviving effect, since
   the REVIVE program assignment replaced the People object entirely.
2. **PHX never read `Room.zone`.** Verified: zero references across the repo. PHPP,
   WUFI XML, METr, and PPP are all blind to it, so nothing downstream depended on the
   overload. PHX groups by `ph_bldg_segment.identifier` and counts dwellings by
   `PhDwellings` identity.
3. **`PhDwellings` already handles both cardinality directions.** Shared instance →
   N Rooms form 1 dwelling; `num_dwellings > 1` → 1 Room holds N dwellings. That covers
   every modeling case in use (whole-house single Room, split floors, MF floor holding
   several apartments, apartment spanning several Rooms, non-residential rooms).
4. **Three implementations existed; one was the outlier.**
   `honeybee_energy_ph/load/phius_mf.py` and `PHX/from_HBJSON/cleanup.py` both already
   aggregated by `PhDwellings` identity. Only the Grasshopper component used
   `Room.zone`. Consolidating removes the duplication and the overload together.
5. **It makes the logic testable.** The Grasshopper module cannot be imported outside
   Rhino (`ph_gh_component_io.gh_io` raises on missing .NET `System`). Moving grouping
   into `honeybee_energy_ph` is what allows real pytest coverage.

## Known limits (accepted, not fixed)

1. **Partial overlap is inexpressible.** A duplex apartment spanning floors 3–4 in a
   building modeled floor-by-floor makes dwelling↔room many-to-many. `PhDwellings`
   cannot represent it; the count must be approximated.
2. **Mixed-use Rooms.** `PHX/from_HBJSON/cleanup.py` floors the total at
   `max(total, 1)`, so a purely non-residential segment still reports one dwelling unit.

Both pre-date this decision and are unchanged by it.

## What would reopen this

- honeybee-core giving `Room` a first-class dwelling/occupancy-group attribute, making
  a dedicated Honeybee-PH carrier redundant.
- A certification path requiring dwelling↔room many-to-many (limit 1 above) — that
  needs a real relational model, not a tag on either side.
- honeybee-energy changing `Room.zone` semantics again. Note the failure mode was
  silent: the attribute gained meaning without any error at the Honeybee-PH boundary.
  If HB-PH ever adopts another honeybee-core attribute as a tag, record it here.
