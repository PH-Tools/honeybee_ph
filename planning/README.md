# planning/

Working plans for honeybee-ph. See [`.instructions.md`](.instructions.md) for the rules and folder contract.

**Read order:** [`STATUS.md`](STATUS.md) first — it indexes all active work and points to the right folder.

## Layout

- `STATUS.md` — master index of active features/refactors.
- `features/` — plans for new capabilities.
- `refactor/` — cross-cutting refactor investigations.
- `archive/` — completed/superseded work, flat by slug, indexed in `archive/README.md`.

When an item is done, fold its outcome into `context/` (and `context/decisions/` where a choice was settled), then move its folder into `archive/<slug>/` and add a row to `archive/README.md`.
