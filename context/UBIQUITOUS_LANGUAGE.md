---
DATE: 2026-08-25
STATUS: CANONICAL
---

# Ubiquitous Language — honeybee-ph

The vocabulary this repo uses for Passive House concepts attached to Honeybee objects.
Derived from [`PRD.md`](PRD.md), [`ARCHITECTURE.md`](ARCHITECTURE.md), [`decisions/`](decisions/), and the
class-level docstrings in the five sub-packages.

Rule of thumb: **a Honeybee object is a host, a honeybee-ph object is a meaning.** Where
the two vocabularies collide (Room, Zone, Construction, Equipment), the entries below
say which word wins in this repo.

---

## Hosting and attachment

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **Host** | The base Honeybee or Honeybee-Energy object (`Model`, `Room`, `Face`, `Aperture`, `Shade`, a load, a construction) that a PH property set hangs off. | parent, owner, container |
| **Property Set** | The PH data object reached at `.properties.ph` or `.properties.phhvac` on a host, which owns that host's `to_dict()` / `from_dict()`. | props, extension, plugin data |
| **Extension** | The registration performed by an `_extend_*.py` module on import, which makes a property set exist on its host type. | patch, monkey-patch, hook |
| **HBJSON** | The serialized Honeybee model file, and the only interchange format this repo produces or consumes. | JSON, model file, export |
| **Round-trip** | Writing a model to HBJSON and reading it back with no loss of PH data, including HBJSON written by older versions. | serialize/deserialize cycle, save-load |

---

## Grouping concepts

Four distinct groupings, each with its own explicit attribute. None of them is inferred
from how the modeler chose to split Rooms. See [decision 0002](decisions/0002-dwelling-identity-not-room-zone.md).

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **Room** | A Honeybee geometry container with no intrinsic Passive House meaning. | zone, space, room-block, thermal block |
| **Space** | The Passive House room whose floor area feeds TFA/iCFA, carried on `Room.properties.ph.spaces`. | room, PHPP room, TFA zone |
| **Building Segment** | The set of Rooms belonging to one PHPP file or one WUFI case, carried on `Room.properties.ph.ph_bldg_segment`. | variant, case, building, model |
| **Dwelling** | A household grouping, carried as a shared `PhDwellings` instance on `People.properties.ph.dwellings` and compared on `.identifier`. | unit, apartment, `Room.zone` tag |
| **Thermal Zone** | The EnergyPlus air-node grouping expressed by `Room.zone`, owned by honeybee-energy and never used to carry PH data. | zone, HVAC zone, E+ zone (in PH context) |
| **Additional Zone** | An adjacent unconditioned volume represented as a boundary condition (`PhAdditionalZone`) with a temperature reduction factor. | buffer zone, attached zone, thermal zone |

---

## Space geometry and area

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **Floor Segment** | One contiguous floor polygon inside a Space, carrying its own weighting factor and net-area factor. | floor piece, sub-floor, region |
| **Space Floor** | The set of Floor Segments that make up one horizontal level of a Space. | floor plate, level |
| **Space Volume** | A Space Floor plus its ceiling height, from which net volume is derived. | air volume, room volume |
| **Weighting Factor** | The multiplier applied to a Floor Segment's raw area to produce its TFA/iCFA contribution. | reduction factor, TFA factor, discount |
| **Net Area Factor** | The multiplier applied to a Floor Segment's raw area to produce net usable area, independent of the weighting factor. | usable factor, deduction |
| **TFA** | Treated Floor Area, the PHI reference area. | treated area, conditioned area |
| **iCFA** | Interior Conditioned Floor Area, the Phius reference area. | ICFA, CFA, floor area |
| **Reference Point** | The point on a Floor Segment used to test whether it is hosted inside a given Room. | centroid, center point |

---

## Site and climate

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **Site** | The Building Segment's location plus its climate data. | project location, weather |
| **Location** | Latitude, longitude, elevation, and time-zone data for a Site. | site, address, coordinates |
| **Climate** | The monthly and peak-load design data set used by the PH calculation. | weather, EPW, climate file |
| **Monthly Value Set** | Twelve values, one per calendar month, for one climate quantity. | monthly data, series |
| **Peak Load Set** | The design-condition values (temperature and per-orientation radiation) for one peak heating or cooling case. | design day, peak condition |
| **Provenance** | The optional record on a Climate of where its values came from, how they were derived, and whether they are certification-approved. | source, metadata, origin |
| **Readiness** | Whether a Climate holds enough data for a given downstream calculation, reported as issues rather than inferred from zeros. | validity, completeness, is_valid |
| **Source Energy Factor** | The multiplier converting delivered energy of a given fuel to source (primary) energy. | PE factor, PER factor, conversion factor |
| **CO2e Factor** | The multiplier converting delivered energy of a given fuel to CO2-equivalent emissions. | carbon factor, emissions rate |

---

## Envelope and openings

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **Construction** | The Honeybee-Energy layered build-up that a PH property set decorates. | assembly, build-up, detail |
| **Assembly** | Reference (library) construction data shipped in `honeybee_ph_standards`. | construction (when referring to library data), template |
| **Window Frame** | The four-sided frame of a window construction, composed of four Frame Elements. | sash, frame profile |
| **Frame Element** | One side (top, right, bottom, left) of a Window Frame with its own width, U-value, psi-glazing, chi, absorptance, and emissivity. | frame side, member, profile |
| **Glazing** | The center-of-glass U-value and g-value of a window construction. | glass, IGU, pane |
| **g-value** | The solar-energy transmittance of the glazing. | SHGC (in this repo's code), solar factor |
| **Install Type** | A named window-installation condition (`PhApertureInstallType`) carrying a psi-install value and a source note. | install condition, install detail, psi type |
| **Psi-Install** | The linear thermal transmittance of the window-to-wall installation, assigned per aperture per edge and inheriting the Frame Element default when unassigned. | install psi, perimeter psi, install bridge |
| **Thermal Bridge** | A linear heat-loss path with 3D geometry, a psi-value, an fRsi value, and a group type. | TB, junction, detail |
| **Psi-value** | Linear thermal transmittance, W/mK. | psi, linear U-value |
| **Chi-value** | Point thermal transmittance, W/K. | chi, point bridge |
| **fRsi** | The temperature factor at the interior surface, used for the hygiene/condensation check. | f-factor, surface factor, temp factor |
| **Foundation** | The ground-contact configuration of a Building Segment, one of heated basement, unheated basement, slab-on-grade, vented crawlspace, or none. | ground, slab, basement |

---

## Mechanical systems

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **Ventilation System** | The fresh-air system as a whole: one Ventilator plus its supply and exhaust duct elements. | HRV, ERV, vent system, ventilation unit |
| **Ventilator** | The heat- or energy-recovery unit itself, with explicit sensible recovery, latent recovery, and electric efficiency. | HRV, ERV, ventilation unit, AHU |
| **Duct Element** | One named exterior duct run belonging to a Ventilation System, made of one or more Duct Segments. | duct, run |
| **Exhaust Ventilator** | A local extract device (dryer, kitchen hood, user-defined) that is not part of the fresh-air Ventilation System. | exhaust fan, extract system |
| **Heating System** | A PH heat-generation system that is not a heat pump (direct electric, fossil boiler, wood boiler, district). | heater, heat source |
| **Heat Pump System** | A PH heat pump, specified either annual, rated-monthly, or combined, with its own cooling parameter sets. | ASHP, minisplit, HP |
| **Cooling Params** | The per-mode cooling specification on a Heat Pump System: ventilation air, recirculation, dehumidification, or panel. | cooling system, cooling mode |
| **Hot Water System** | The domestic hot water system: heaters, tanks, and the recirculation and branch piping. | DHW, SHW, service water |
| **Pipe Trunk / Branch / Fixture** | The three-level hierarchy of hot water piping, each level composed of Pipe Segments. | main, riser, run |
| **Renewable Device** | An on-site generation device, currently photovoltaic. | PV, solar, generator |
| **Supportive Device** | An auxiliary electrical device (pumps and similar) whose energy is counted separately from appliances. | aux equipment, parasitic load |
| **Setpoints** | The Building Segment's winter and summer indoor design temperatures. | thermostat, design temps |
| **Summer Bypass Mode** | The control mode for bypassing the Ventilator's heat exchanger in summer. | summer bypass, HRV bypass |

---

## Loads, appliances, and occupancy

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **PH Equipment** | A single appliance or plug-load item with a PH-defined energy demand and reference quantity. | device, MEL, load, machine |
| **Equipment Collection** | The set of PH Equipment items attached to a Room's electric-equipment load. | appliance list, equipment set |
| **MEL** | Miscellaneous Electric Load, the Phius category for non-appliance plug loads. | plug load, misc load |
| **Non-Res Program** | A Phius non-residential space-use program assigned to a Phius Non-Res Room. | program type, use type, occupancy type |
| **Residential Story** | A Phius per-story residential grouping used for lighting and MEL allocation. | floor, level |

---

## Certification

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **PHI Certification** | The Building Segment's PHI settings, expressed as a versioned PHPP settings object. | Passive House cert, PHPP settings (loosely) |
| **Phius Certification** | The Building Segment's Phius settings and performance targets. | Phius cert data, WUFI settings |
| **Certification Program** | Which Phius program a building is pursuing. | cert type, standard |
| **Certification Class** | Which PHI level a building is pursuing (Classic, Plus, Premium). | cert level, tier, program |
| **Building Use Type** | The occupancy classification driving certification criteria (residential, school, office, and so on). | occupancy, program, category |
| **Building Type** | Whether the project is new construction, retrofit, or mixed. | project type, scope |
| **Building Status** | Whether the project is in planning, construction, or complete. | phase, stage |

---

## Downstream and boundaries

| Term | Definition | Aliases to avoid |
| ---- | ---------- | ---------------- |
| **PHX** | The separate library that converts honeybee-ph models to and from PHPP and WUFI-Passive. | exporter, converter (unqualified) |
| **PHPP** | PHI's Excel workbook and the only accepted PHI certification tool. | Passive House spreadsheet, the Excel |
| **WUFI-Passive** | The Phius desktop certification tool, which reads and writes XML. | WUFI (unqualified), Phius tool |
| **METr** | Phius's browser-based successor to WUFI-Passive, with JSON model files. | Metr, C3rro, the new WUFI |
| **Boundary Adapter** | Export-side code in PHX that absorbs a target format's limitations so the data model does not have to. | exporter hack, workaround, shim |

---

## Relationships

- A **Room** hosts zero or more **Spaces**, exactly one **Building Segment** reference, and at most one **Ventilation System**.
- A **Space** contains one or more **Space Volumes**; each Space Volume has one **Space Floor**; each Space Floor has one or more **Floor Segments**.
- A **Building Segment** has exactly one **Site**, one **PHI Certification**, one **Phius Certification**, one **Setpoints**, and zero or more **Thermal Bridges**.
- A **Site** has exactly one **Location** and one **Climate**; a **Climate** has zero or one **Provenance**.
- A **Ventilation System** has exactly one **Ventilator** and zero or more **Duct Elements**; a Room may not have more than one Ventilation System ([decision 0001](decisions/0001-no-multiple-ventilation-systems-per-room.md)).
- A **Dwelling** is shared by one or more **Rooms**; a single Room may represent several dwellings via `num_dwellings > 1`.
- An **Aperture** has one **Construction** (carrying one **Window Frame** and one **Glazing**) and zero to four per-edge **Install Types**.
- A **Window Frame** has exactly four **Frame Elements**.
- **Absence is `None`**, never `0`. Numeric zero as a no-assignment marker is permitted only inside a **Boundary Adapter** ([decision 0006](decisions/0006-explicit-ventilation-system-states.md)).

---

## Example dialogue

> **Dev:** "Six Rooms are one apartment. Do I set the same **Thermal Zone** on all six?"

> **Domain expert:** "No. Six Rooms being one household is a **Dwelling**, and Dwelling identity lives on `PhDwellings` reached through the People load. `Room.zone` is the E+ **Thermal Zone** and belongs to honeybee-energy. Tag six Rooms with a shared zone and E+ merges them into one air node and drops five HVAC systems."

> **Dev:** "So what makes those six Rooms one PHPP file?"

> **Domain expert:** "The **Building Segment**. Different question, different attribute. Dwelling answers 'which Rooms are one household', Building Segment answers 'which WUFI case or PHPP file'. And the **Space** answers 'which PHPP room', which is a fourth grouping again. An HB **Room** answers none of them, it is only geometry."

> **Dev:** "The bathroom **Space** has a 0.5 **Weighting Factor**. Is that the same thing as the **Net Area Factor**?"

> **Domain expert:** "No. The Weighting Factor produces the **TFA**/**iCFA** contribution, the Net Area Factor produces net usable area. They multiply independently, so a Floor Segment can be discounted for one and not the other."

> **Dev:** "This Room has no mechanical ventilation. Do I give it a bare **Ventilator** so PHX has something to read?"

> **Domain expert:** "Never. Absence is `None`. A bare Ventilator reads downstream as a balanced HRV with zero recovery and invented ducts, which is worse than nothing. If there is a real unit, build the **Ventilation System** with `balanced_hrv()` from a selected Ventilator whose recovery and electric efficiency are explicit. If PHX's target format needs a numeric `0`, that substitution happens in the **Boundary Adapter**, not here."

> **Dev:** "This window sits in a buried jamb, so its **Psi-Install** differs. New **Construction**?"

> **Domain expert:** "No, that is what minted 939 constructions where 79 existed. Install condition is a property of where the window sits, so assign a named **Install Type** per edge on the Aperture. `None` on an edge means inherit the **Frame Element** default. A zero-psi Install Type is the off state, there is no separate flag."

---

## Flagged ambiguities

**"Zone" carries four unrelated meanings.** In this codebase it can mean the E+ **Thermal Zone** (`Room.zone`), an **Additional Zone** boundary condition, a **Building Segment** (PHI documentation calls these thermal zones), or, historically, a **Dwelling** tag. Recommendation: use "Zone" bare only for the EnergyPlus thermal zone. Everything else takes its full name. `PhAdditionalZone` is the one place the word survives for a non-E+ concept, and it should be read as "adjacent unconditioned volume", never as a grouping of Rooms.

**"Room" means one thing in Honeybee and another in Passive House.** A Honeybee `Room` is a geometry container; a PHPP "room" is what this repo calls a **Space**. `PhiusNonResRoom` uses the PH sense inside a class name, which reads backwards against the rest of the codebase. Recommendation: in prose always qualify as "HB Room" or "PH Space", never bare "room".

**Dwelling count is carried in two places.** `BldgSegment.num_dwelling_units` and `PhDwellings.num_dwellings` both answer "how many units". Recommendation: treat `PhDwellings` as the authority per [decision 0002](decisions/0002-dwelling-identity-not-room-zone.md) and read `BldgSegment.num_dwelling_units` as a segment-level reporting value only. Anything that needs true dwelling identity must go through `honeybee_energy_ph/dwellings.py`.

**"Ventilation unit" is used for both the system and the device.** The attribute is `PhVentilationSystem._ventilation_unit` but the class is `Ventilator`. Recommendation: **Ventilator** for the box, **Ventilation System** for the box plus its ducts. Retire "ventilation unit" in new prose and docstrings. Likewise, "HRV" and "ERV" name recovery behavior, not object types, so neither is a substitute for either term.

**"Equipment" and "device" are used interchangeably across packages.** `PhEquipment` means appliances and plug loads in `honeybee_energy_ph`, while `honeybee_phhvac` calls heat pumps, ventilators, and exhaust units "devices". Recommendation: **PH Equipment** for appliances and plug loads only; **device** for HVAC hardware. Never call a dishwasher a device or a heat pump equipment.

**"Construction" versus "Assembly".** Passive House practitioners say "assembly", Honeybee says "Construction", and this repo ships library data under `honeybee_ph_standards/constructions/`. Recommendation: **Construction** for the Honeybee object a PH property set decorates, **Assembly** for the reference library data. Do not use "assembly" for a live model object.

**Absence is expressed inconsistently across the ecosystem boundary.** `None`, numeric `0`, and empty collections have all been used to mean "no assignment". [Decision 0006](decisions/0006-explicit-ventilation-system-states.md) settles it: `None` means no assignment, an empty exterior-duct collection is a valid physical state (a unit wholly inside the envelope), and numeric `0` is a target-format convention that belongs only in a **Boundary Adapter**.

**"Mulled" and neighbor-edge language do not belong here.** Edge adjacency between apertures is PH-Navigator's concern. A mulled edge reaches honeybee-ph as an explicit zero-psi **Install Type**, and no honeybee-ph term should imply knowledge of a neighboring aperture ([decision 0003](decisions/0003-psi-install-is-aperture-instance-data.md)).

**"Identifier" versus "id_num".** `identifier` is the stable string (often a UUID) used for identity and round-tripping; `id_num` is a sequential integer minted for export ordering. Recommendation: identity comparisons always use `identifier`. `id_num` is export bookkeeping and carries no meaning inside the data model, which is exactly why numeric `0` must not be read as absence.
