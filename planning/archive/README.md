# planning/archive/ — completed & superseded work

Finished feature/refactor folders that have been folded back into `context/`, kept for history. Move a folder here (unchanged) when its work is `Complete` or `Superseded`; keep the flat `<slug>/` name so it stays findable by name.

This README is the index — scan or grep it instead of guessing dates. Add a row when you archive something.

| Item | Kind | Completed | Summary | Folder |
|------|------|-----------|---------|--------|
| `PhEquipment.__init__` reference_quantity defaults | Bug fix (data model) | 2026-08-25 | Every subclass declares its own `DEFAULT_REFERENCE_QUANTITY` instead of inheriting a base `2` that suited only one type; a drift test pins the class constants to `ph_default_equip` and a structural test fails when a new subclass forgets. Elevators moved 2 → 5. Decision 0007. | [`ph-equipment-reference-quantity-defaults/`](ph-equipment-reference-quantity-defaults/README.md) |
| Phius MF custom MEL/Lighting `reference_quantity` | Bug fix (cross-repo) | 2026-08-25 | Six Phius-MF MEL and lighting builders kept the `PhEquipment` base `reference_quantity = 2` instead of the standards value `5` ("User defined"), on every Phius MF export in both WUFI XML and METr JSON. Fixed downstream by constructing from `ph_default_equip[...]["PHIUS"]`; merged in honeybee_grasshopper_ph#69. | [`phius-mf-custom-load-reference-quantity/`](phius-mf-custom-load-reference-quantity/README.md) |
| Default dwelling identity across HBJSON round-trips | Bug fix | 2026-08-14 | Replaced process-local default UUID classification with the serialized `num_dwellings` assignment contract; 1,020 tests pass at 80% coverage; release pending. | [`dwelling-default-roundtrip/`](dwelling-default-roundtrip/README.md) |
| Explicit `PhVentilationSystem` factories | Feature (cross-repo, primary) | 2026-08-14 | Added selected-equipment `balanced_hrv()` without invented ducts; honeybee-ph v1.33.42, PHX v1.56.79, and OpenPH v0.5.1 released; published matrix passes. Decision 0006. | [`default-ventilation-system-factory/`](default-ventilation-system-factory/README.md) |
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
