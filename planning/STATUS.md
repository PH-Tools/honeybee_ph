# Planning Status

Master index of active planning work in honeybee-ph. Update the table when a unit of work is added, changes status, or is folded back into `context/`.

_Last updated: 2026-08-12_

## Active / current work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| Default dwelling identity across HBJSON round-trips | Bug fix | **Requested** — reproduced in PHX; not implemented | [`refactor/dwelling-default-roundtrip.md`](refactor/dwelling-default-roundtrip.md) |
| Decouple "Dwelling" from `Room.zone` | Refactor (cross-repo, **primary**) | **Implemented** — awaiting release + install, then `PHX` | [`refactor/dwelling-zone-decoupling.md`](refactor/dwelling-zone-decoupling.md) → [decision 0002](../context/decisions/0002-dwelling-identity-not-room-zone.md) |
| Multiple ventilation systems per room | Refactor | Deferred — decided NOT to implement | [`refactor/multiple-ventilation-systems.md`](refactor/multiple-ventilation-systems.md) → [decision 0001](../context/decisions/0001-no-multiple-ventilation-systems-per-room.md) |

## Completed / archived work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| Aperture-level Psi-Install (Install Types) | Refactor (cross-repo, **primary**) | **Complete** — merged (PR #87) + released v1.33.33; archived; decision [0003](../context/decisions/0003-psi-install-is-aperture-instance-data.md) | [`archive/aperture-psi-install/`](archive/aperture-psi-install/aperture-psi-install-plan.md) |

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

## Update rule

When an item reaches `Complete`, fold its outcome into the relevant `context/` doc and, if it settled a design choice, add a `context/decisions/` record — then drop or archive the planning folder.
