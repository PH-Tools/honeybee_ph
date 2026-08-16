# Planning Status

Master index of active planning work in honeybee-ph. Update the table when a unit of work is added, changes status, or is folded back into `context/`.

_Last updated: 2026-08-15_

## Active / current work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| Decouple "Dwelling" from `Room.zone` | Refactor (cross-repo, **primary**) | **Released** in v1.33.30 — downstream install/PHX status remains in companion docs | [`refactor/dwelling-zone-decoupling.md`](refactor/dwelling-zone-decoupling.md) → [decision 0002](../context/decisions/0002-dwelling-identity-not-room-zone.md) |
| Multiple ventilation systems per room | Refactor | Deferred — decided NOT to implement | [`refactor/multiple-ventilation-systems.md`](refactor/multiple-ventilation-systems.md) → [decision 0001](../context/decisions/0001-no-multiple-ventilation-systems-per-room.md) |

## Recommended execution order

Two cross-repo items were filed from PHX/OpenPH on 2026-08-15 with honeybee-ph as
**primary** (see *Cross-repo work*): the `SetPoints.mechanical_cooling` flag is a
one-field change and can go first; the PHPP-10 foundation-shape fields are the larger
one and gate PHX's `Ground` writer and OpenPH's foundation objects.

## Completed / archived work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| Default dwelling identity across HBJSON round-trips | Bug fix | **Complete** — count-based assignment restored; 1,020 tests pass at 80% coverage; release pending | [`archive/dwelling-default-roundtrip/`](archive/dwelling-default-roundtrip/README.md) |
| Explicit `PhVentilationSystem` factories | Feature (cross-repo, **primary**) | **Complete** — honeybee-ph v1.33.42 and PHX v1.56.79 released; published four-package matrix verified | [`archive/default-ventilation-system-factory/`](archive/default-ventilation-system-factory/README.md) → [decision 0006](../context/decisions/0006-explicit-ventilation-system-states.md) |
| EPW-derived preliminary monthly climate + provenance/readiness | Feature (cross-repo readiness, **primary**) | **Complete** — honeybee-ph v1.33.40 and PHX v1.56.76 released; both published artifacts pass EPW/readiness smoke checks | [`archive/epw-derived-preliminary-climate/`](archive/epw-derived-preliminary-climate/README.md) → [decision 0004](../context/decisions/0004-no-bundled-licensed-climate-data.md) |
| `Space.from_room()` default-space factory (upstream from GH) | Feature (cross-repo, **primary**) | **Complete** — factory released v1.33.36; GH wrapper released v1.28.1 with generated pin; meter, foot, multi-floor, host, and round-trip canvas checks pass | [`archive/space-from-room-factory/`](archive/space-from-room-factory/README.md) |
| Independent `Site`/`Climate` defaults and duplication | Feature / defect repair | **Complete** — archived; 98 focused + 891 full tests pass; release target `v1.33.35` via merge CI | [`archive/independent-site-defaults/`](archive/independent-site-defaults/README.md) |
| Aperture-level Psi-Install (Install Types) | Refactor (cross-repo, **primary**) | **Complete** — merged (PR #87) + released v1.33.33; archived; decision [0003](../context/decisions/0003-psi-install-is-aperture-instance-data.md) | [`archive/aperture-psi-install/`](archive/aperture-psi-install/aperture-psi-install-plan.md) |
| Bundled PHI/Phius climate dataset library | Feature | **Superseded** — licensed datasets will not be redistributed; replaced by user-supplied EPW conversion; decision [0004](../context/decisions/0004-no-bundled-licensed-climate-data.md) | [`archive/climate-dataset-library/`](archive/climate-dataset-library/README.md) |

## Cross-repo work

**Filed 2026-08-15 from PHX (honeybee-ph primary; not yet started here):** — on
completion of each, the PHX packet writes a hand-off doc into the OpenPH feature folder
(`openph-workspace/planning/features/ground-degree-hours-alignment/upstream/`); the
honeybee-ph half should hand PHX the released version and the exact attribute/JSON names.

| Item | Change here | Pointer |
|------|-------------|---------|
| Mechanical cooling flag (`Verification!N30`) | `bldg_segment.py::SetPoints.mechanical_cooling: bool = False` (+ `to_dict`/`from_dict`/`duplicate`/`__eq__`), GH input on the setpoints component, `honeybee-ph-schema` field. PHX then writes `Verification!N30`; OpenPH reads it instead of a hardcoded `True` | `PHX/planning/bug-fix/phpp-writer-input-gaps/06-verification-mechanical-cooling.md` |
| Foundation shape for PHPP 10.x `Ground` | `foundations.py`: `interior_wall_to_heated_area_m2` / `_u_value` (slab, unheated basement, crawl space — or hoisted to `PhFoundation`), `PhVentedCrawlspace.wind_shield_factor = 0.05`; fix crawlspace perimeter default (2.5 → 0.0); decide slab perimeter-insulation defaults (recommend "none"); optional naming cleanups. Schema + GH inputs follow | `PHX/planning/features/foundation-phpp10-shape/PRD.md` §4, §6 |


`aperture-psi-install` spans four repos. This repo is the **primary** — it owns the new
`PhApertureInstallType` object, the per-edge aperture slots, and the resolver; it ships first.
Resolves issue #51 here and bug #59 in `honeybee_grasshopper_ph`.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`archive/aperture-psi-install/`](archive/aperture-psi-install/aperture-psi-install-plan.md) | Primary — data model + resolver + tests — **complete, archived** |
| `PHX` | `planning/archive/aperture-psi-install/` | PHPP per-row write; WUFI/METr variant synthesis — **complete, archived** |
| `honeybee_grasshopper_ph` | `planning/refactor/aperture-psi-install.md` | Components; deletes the bug-#59 mechanism |
| `ph-navigator-v2` | `planning/features_v1.1/aperture-psi-install/upstream-alignment.md` | Phase-07 GH-client mapping |

`dwelling-zone-decoupling` spans three repos. This repo is the **primary** — it owns the
shared `honeybee_energy_ph/dwellings.py` helper and ships first; the others are blocked on it.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`refactor/dwelling-zone-decoupling.md`](refactor/dwelling-zone-decoupling.md) | Primary — shared helper + tests |
| `honeybee_grasshopper_ph` | `planning/dwelling-zone-decoupling.md` | Root cause — the two `Room.zone` references |
| `PHX` | `planning/refactor/dwelling-zone-decoupling.md` | Downstream consumer — clearance + dedup |

`space-from-room-factory` spans two repos. This repo is the **primary** — it gains the
SDK-level default-space factory (pure ladybug-geometry) and ships first; the GH repo then
re-points its component at it and retires the Rhino-side duplicate.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`archive/space-from-room-factory/`](archive/space-from-room-factory/PRD.md) | Primary — **complete, archived; released v1.33.36** |
| `honeybee_grasshopper_ph` | `planning/archive/space-from-room-factory/` | Wrapper **complete, archived; released v1.28.1** with generated `honeybee-ph>=1.33.36` pin |

`epw-derived-preliminary-climate` is owned here and complete, with downstream
readiness coordination. This repo owns EPW conversion, provenance,
availability, and HBJSON; PHX rejects unavailable peak-load data precisely
rather than manufacturing zeros. OpenPH requires no direct change because its
canonical path consumes the already-validated PHX variant.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`archive/epw-derived-preliminary-climate/`](archive/epw-derived-preliminary-climate/README.md) | Primary — **complete, archived; released v1.33.40** |
| `PHX` | PR #81 | **Complete; released v1.56.76** with `honeybee-ph>=1.33.40` and pre-copy readiness rejection |
| `openph-workspace` | audit only | No direct honeybee-ph climate ingestion; canonical PHX boundary is sufficient |

`default-ventilation-system-factory` shares one state contract with PHX and
OpenPH. The target-derived state matrix is Phase 01; no repo may independently
invent a `None`, ID `0`, or duct fallback.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`archive/default-ventilation-system-factory/`](archive/default-ventilation-system-factory/README.md) | **Complete, archived; released v1.33.42** |
| `PHX` | `planning/archive/ventilation-assignment-semantics/` | **Complete, archived; released v1.56.79; requires honeybee-ph>=1.33.42** |
| `openph-workspace` | `planning/archive/dated/2026-08-14/ventilation-input-semantics/` | **Complete, archived; released OpenPH v0.5.1** |

## Update rule

When an item reaches `Complete`, fold its outcome into the relevant `context/` doc and, if it settled a design choice, add a `context/decisions/` record — then drop or archive the planning folder.
