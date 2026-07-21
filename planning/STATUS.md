# Planning Status

Master index of active planning work in honeybee-ph. Update the table when a unit of work is added, changes status, or is folded back into `context/`.

_Last updated: 2026-07-21_

## Active / current work

| Item | Kind | Status | Pointer |
|------|------|--------|---------|
| Decouple "Dwelling" from `Room.zone` | Refactor (cross-repo, **primary**) | **Implemented** — awaiting release + install, then `PHX` | [`refactor/dwelling-zone-decoupling.md`](refactor/dwelling-zone-decoupling.md) → [decision 0002](../context/decisions/0002-dwelling-identity-not-room-zone.md) |
| Multiple ventilation systems per room | Refactor | Deferred — decided NOT to implement | [`refactor/multiple-ventilation-systems.md`](refactor/multiple-ventilation-systems.md) → [decision 0001](../context/decisions/0001-no-multiple-ventilation-systems-per-room.md) |

## Cross-repo work

`dwelling-zone-decoupling` spans three repos. This repo is the **primary** — it owns the
shared `honeybee_energy_ph/dwellings.py` helper and ships first; the others are blocked on it.

| Repo | Doc | Role |
|------|-----|------|
| `honeybee_ph` | [`refactor/dwelling-zone-decoupling.md`](refactor/dwelling-zone-decoupling.md) | Primary — shared helper + tests |
| `honeybee_grasshopper_ph` | `planning/dwelling-zone-decoupling.md` | Root cause — the two `Room.zone` references |
| `PHX` | `planning/refactor/dwelling-zone-decoupling.md` | Downstream consumer — clearance + dedup |

## Update rule

When an item reaches `Complete`, fold its outcome into the relevant `context/` doc and, if it settled a design choice, add a `context/decisions/` record — then drop or archive the planning folder.
