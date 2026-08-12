# planning/archive/ — completed & superseded work

Finished feature/refactor folders that have been folded back into `context/`, kept for history. Move a folder here (unchanged) when its work is `Complete` or `Superseded`; keep the flat `<slug>/` name so it stays findable by name.

This README is the index — scan or grep it instead of guessing dates. Add a row when you archive something.

| Item | Kind | Completed | Summary | Folder |
|------|------|-----------|---------|--------|
| Aperture-level Psi-Install (Install Types) | Refactor (cross-repo, primary) | 2026-08-12 | PhApertureInstallType + per-edge aperture slots + single resolver; ISO 10077-1 override-aware; resolves #51. Decision 0003. | [`aperture-psi-install/`](aperture-psi-install/aperture-psi-install-plan.md) |

## Conventions

- **Flat by slug:** `planning/archive/<slug>/`. Do not nest by date.
- **Index here:** every archived item gets one row above (with the completed date as a column — that is where the chronology lives).
- **If this ever gets long** (dozens+), bucket by year — `planning/archive/2026/<slug>/` — never by day.
- The canonical outcome lives in `context/` (and `context/decisions/` if a choice was settled); this folder is history, not source of truth.
