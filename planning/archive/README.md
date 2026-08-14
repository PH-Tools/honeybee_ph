# planning/archive/ — completed & superseded work

Finished feature/refactor folders that have been folded back into `context/`, kept for history. Move a folder here (unchanged) when its work is `Complete` or `Superseded`; keep the flat `<slug>/` name so it stays findable by name.

This README is the index — scan or grep it instead of guessing dates. Add a row when you archive something.

| Item | Kind | Completed | Summary | Folder |
|------|------|-----------|---------|--------|
| EPW-derived preliminary monthly climate + provenance/readiness | Feature (cross-repo readiness, primary) | 2026-08-14 | Added user-supplied EPW conversion without bundled data; honeybee-ph v1.33.40 and PHX v1.56.76 published-artifact smokes pass. | [`epw-derived-preliminary-climate/`](epw-derived-preliminary-climate/README.md) |
| `Space.from_room()` default-space factory | Feature (cross-repo, primary) | 2026-08-14 | Added the pure-Ladybug Room factory; released v1.33.36; GH wrapper released v1.28.1; meter, foot, multi-floor, host, and HBJSON round-trip canvas checks pass. | [`space-from-room-factory/`](space-from-room-factory/README.md) |
| Independent `Site`/`Climate` defaults and duplication | Feature / defect repair | 2026-08-14 | Removed 20 constructed mutable defaults; made duplicate/load graphs recursively independent; verified Room, Model HBJSON, Python 2.7 grammar, and wheel behavior. Release target `v1.33.35`. | [`independent-site-defaults/`](independent-site-defaults/README.md) |
| Aperture-level Psi-Install (Install Types) | Refactor (cross-repo, primary) | 2026-08-12 | PhApertureInstallType + per-edge aperture slots + single resolver; ISO 10077-1 override-aware; resolves #51. Decision 0003. | [`aperture-psi-install/`](aperture-psi-install/aperture-psi-install-plan.md) |
| Bundled PHI/Phius climate dataset library | Feature | 2026-08-14 | Superseded before implementation: do not redistribute licensed/access-controlled certification data. Replaced by user-supplied EPW preliminary conversion. Decision 0004. | [`climate-dataset-library/`](climate-dataset-library/README.md) |

## Conventions

- **Flat by slug:** `planning/archive/<slug>/`. Do not nest by date.
- **Index here:** every archived item gets one row above (with the completed date as a column — that is where the chronology lives).
- **If this ever gets long** (dozens+), bucket by year — `planning/archive/2026/<slug>/` — never by day.
- The canonical outcome lives in `context/` (and `context/decisions/` if a choice was settled); this folder is history, not source of truth.
