# Decision Records

Numbered, dated records of significant design/architecture decisions for
honeybee-ph — especially decisions **not** to do something, so future
investigations start from the prior research instead of from scratch.

Format: `NNNN-short-kebab-title.md` with Date / Status / Decider / Context /
Decision / Rationale / What-would-reopen-this. Link to any supporting
research (e.g. `planning/refactor/`).

| # | Decision | Status |
|---|---|---|
| [0001](0001-no-multiple-ventilation-systems-per-room.md) | Do NOT add multiple ventilation systems per room (WUFI-Passive supports only one ventilator per space) | Decided 2026-07-14 |
| [0002](0002-dwelling-identity-not-room-zone.md) | Dwelling identity lives on `PhDwellings`, NOT on `Room.zone` (which honeybee-energy reads as an E+ thermal-zone instruction) | Decided 2026-07-21 |
| [0003](0003-psi-install-is-aperture-instance-data.md) | Psi-install is aperture-instance data resolved from named Install Types — never a reason to duplicate a window construction | Decided 2026-08-12 |
