# Planning Status

Master index of active planning work in honeybee-ph. Update the table when a unit of work is added, changes status, or is folded back into `context/`.

_Last updated: 2026-08-14_

## Active / current work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| EPW-derived preliminary monthly climate + provenance/readiness | Feature (cross-repo readiness, **primary**) | **Scoped** — replaces bundled dataset proposal; blocked until `honeybee-ph>=1.33.35` is published and verified | [`features/epw-derived-preliminary-climate/`](features/epw-derived-preliminary-climate/README.md) → [decision 0004](../context/decisions/0004-no-bundled-licensed-climate-data.md) |
| `Space.from_room()` default-space factory (upstream from GH) | Feature (cross-repo, **primary**) | **Implementing** — Phase 03 complete; Phase 04 release/GH handoff next | [`features/space-from-room-factory/`](features/space-from-room-factory/README.md) |
| Explicit `PhVentilationSystem` factories | Feature (cross-repo) | **Scoped** — local API fixed; Phase 01 state matrix required before code | [`features/default-ventilation-system-factory/`](features/default-ventilation-system-factory/README.md) |
| Default dwelling identity across HBJSON round-trips | Bug fix | **Requested** — reproduced in PHX; not implemented | [`refactor/dwelling-default-roundtrip.md`](refactor/dwelling-default-roundtrip.md) |
| Decouple "Dwelling" from `Room.zone` | Refactor (cross-repo, **primary**) | **Released** in v1.33.30 — downstream install/PHX status remains in companion docs | [`refactor/dwelling-zone-decoupling.md`](refactor/dwelling-zone-decoupling.md) → [decision 0002](../context/decisions/0002-dwelling-identity-not-room-zone.md) |
| Multiple ventilation systems per room | Refactor | Deferred — decided NOT to implement | [`refactor/multiple-ventilation-systems.md`](refactor/multiple-ventilation-systems.md) → [decision 0001](../context/decisions/0001-no-multiple-ventilation-systems-per-room.md) |

## Recommended execution order

For one implementation stream:

1. `space-from-room-factory` — isolated, fully scoped primary implementation.
2. `epw-derived-preliminary-climate` — depends on published
   `honeybee-ph>=1.33.35` and adds the broader
   provenance/readiness contract.
3. `default-ventilation-system-factory` — complete only with coordinated
   PHX/OpenPH state semantics.

Hard dependencies are narrower than the linear queue:

```text
honeybee-ph>=1.33.35 -> epw-derived-preliminary-climate
space-from-room-factory -> honeybee-ph release -> GH wrapper re-point
ventilation state matrix -> PHX/OpenPH semantics -> ventilation closeout
```

## Completed / archived work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| Independent `Site`/`Climate` defaults and duplication | Feature / defect repair | **Complete** — archived; 98 focused + 891 full tests pass; release target `v1.33.35` via merge CI | [`archive/independent-site-defaults/`](archive/independent-site-defaults/README.md) |
| Aperture-level Psi-Install (Install Types) | Refactor (cross-repo, **primary**) | **Complete** — merged (PR #87) + released v1.33.33; archived; decision [0003](../context/decisions/0003-psi-install-is-aperture-instance-data.md) | [`archive/aperture-psi-install/`](archive/aperture-psi-install/aperture-psi-install-plan.md) |
| Bundled PHI/Phius climate dataset library | Feature | **Superseded** — licensed datasets will not be redistributed; replaced by user-supplied EPW conversion; decision [0004](../context/decisions/0004-no-bundled-licensed-climate-data.md) | [`archive/climate-dataset-library/`](archive/climate-dataset-library/README.md) |

## Cross-repo work

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
| `honeybee_ph` | [`features/space-from-room-factory/`](features/space-from-room-factory/PRD.md) | Primary — factory + tests |
| `honeybee_grasshopper_ph` | `planning/refactor/space-from-room-factory.md` | Wrapper re-point; shrinks `make_spaces/` — blocked on primary release |

`epw-derived-preliminary-climate` is owned here and will be implemented here,
with downstream readiness coordination. This repo owns EPW conversion, provenance,
availability, and HBJSON; PHX/OpenPH must reject unavailable peak-load data
precisely rather than manufacturing zeros.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`features/epw-derived-preliminary-climate/`](features/epw-derived-preliminary-climate/README.md) | Primary — user-supplied EPW conversion + provenance/readiness |
| `PHX` | follow-up to be filed during Phase 01 | Preserve monthly-only/unavailable-load state |
| `openph-workspace` | follow-up to be filed during Phase 01 | Targeted readiness diagnostic; no zero fallback |

`default-ventilation-system-factory` shares one state contract with PHX and
OpenPH. The target-derived state matrix is Phase 01; no repo may independently
invent a `None`, ID `0`, or duct fallback.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`features/default-ventilation-system-factory/`](features/default-ventilation-system-factory/README.md) | Authoring-side factories + validation |
| `PHX` | `planning/features/ventilation-assignment-semantics/` | Explicit target-neutral assignment/device representation |
| `openph-workspace` | `planning/features/ventilation-input-semantics/` | PHPP-derived device/duct state rules + readiness |

## Update rule

When an item reaches `Complete`, fold its outcome into the relevant `context/` doc and, if it settled a design choice, add a `context/decisions/` record — then drop or archive the planning folder.
