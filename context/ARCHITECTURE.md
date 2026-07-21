---
DATE: 2026-07-15
STATUS: CANONICAL
---

# honeybee-ph — Architecture

## Big picture

honeybee-ph is a **Ladybug Tools extension**. It does not replace Honeybee objects; it *attaches* Passive House data to them using Honeybee's `properties` extension mechanism. A Honeybee `Room`, `Aperture`, `Face`, or `Model` gains a `.properties.ph` (or `.properties.phhvac`) slot that holds the PH data, and that data serializes into the standard HBJSON alongside everything else.

```
Honeybee model  ──.properties.ph──►  honeybee-ph objects  ──to_dict()──►  HBJSON
       ▲                                                                     │
       └──────────────── from_dict() ◄──────────────────────────────────────┘
                                   │
                                   ▼
                         PHX → PHPP / WUFI-Passive
```

## The five packages

| Package | Role | Key modules |
|---------|------|-------------|
| `honeybee_ph` | Core PH model attached to base Honeybee objects | `space.py` (interior spaces/iCFA), `bldg_segment.py`, `phi.py` / `phius.py` (certification), `site.py`, `team.py`, `foundations.py`, `_extend_honeybee_ph.py` (registers `.properties.ph`) |
| `honeybee_energy_ph` | PH model attached to honeybee-**energy** objects | `construction/`, `load/`, `library/`, `hvac/` (deprecated), `_extend_honeybee_energy_ph.py` |
| `honeybee_phhvac` | Dedicated PH-HVAC model (the migration target for HVAC) | `ventilation.py`, `heating.py`, `heat_pumps.py`, `hot_water_*.py`, `ducting.py`, `renewable_devices.py`, `_extend_honeybee_ph_hvac.py` |
| `honeybee_ph_standards` | Reference data as shipped JSON | `constructions/`, `constructionsets/`, `programtypes/`, `schedules/`, `sourcefactors/` |
| `honeybee_ph_utils` | Cross-cutting helpers | `color.py`, `enumerables.py`, geometry (`face_tools.py`, `polygon2d_tools.py`, `vector3d_tools.py`), `iso_10077_1.py`, `aisi_s250_21.py`, `occupancy.py` |

## The `_extend_*` pattern

Each package has an `_extend_*.py` module that runs on import and registers the PH property set onto the corresponding Honeybee object type (via Honeybee's `_properties` extension API). This is what makes `room.properties.ph` exist. Importing the package is what wires it up — do not bypass this.

## The `properties/` sub-packages

Within `honeybee_ph`, `honeybee_energy_ph`, and `honeybee_phhvac`, the `properties/` folder holds the per-object property classes (e.g. the `RoomPhProperties` that hangs off a `Room`). These are the objects that own the `to_dict()`/`from_dict()` for that host type.

## Serialization contract

Every model class implements `to_dict()` / `from_dict()` (and usually `duplicate()`). HBJSON is the interchange format for the whole ecosystem, so **backward compatibility is a hard requirement** — see `CODING_STANDARDS.md` §Serialization. `from_dict()` must tolerate HBJSON written by older versions that lack newer keys.

## Dependencies

Runtime deps are deliberately minimal: `honeybee-core`, `honeybee-energy`, and `PH-units` (unit parsing/conversion). No heavy scientific stack — the code has to load in Rhino.

## Grouping concepts: never overload a honeybee-core attribute

An HB `Room` carries **no intrinsic semantics** — it is a geometry container, and its
granularity is a modeling convenience. Every real grouping concept has its own explicit
attribute:

| Concept | Question it answers | Attribute | Owner |
|---|---|---|---|
| Dwelling | which rooms are one household? how many units? | `People.properties.ph.dwellings` (`PhDwellings`) | this repo |
| E+ Thermal Zone | which rooms share one air node + one HVAC? | `Room.zone` | **honeybee-energy** |
| Building Segment | which WUFI case / PHPP file? | `Room.properties.ph.ph_bldg_segment` | this repo |
| TFA Space | which PHPP room? | `Room.properties.ph.spaces` | this repo |

`honeybee_energy_ph/dwellings.py` is the single implementation of dwelling grouping,
consumed by both `honeybee_grasshopper_ph` and `PHX`. Rooms in one dwelling share a
`PhDwellings` **instance** (identity compared on `.identifier`); a Room holding several
dwellings uses `num_dwellings > 1`.

**Do not tag Honeybee-PH data onto honeybee-core attributes.** `Room.zone` was used as a
dwelling tag while it was inert; honeybee-energy later gave it real E+ meaning, silently
merging thermal zones and dropping HVAC systems. See
[decision 0002](decisions/0002-dwelling-identity-not-room-zone.md).

## Where the boundaries are

- Export/conversion logic → **PHX**, not here.
- Grasshopper components → **honeybee_grasshopper_ph**, not here.
- This repo stays a pure, IronPython-2.7-safe data-model library.
