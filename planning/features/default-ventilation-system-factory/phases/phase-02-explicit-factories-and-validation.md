# Phase 02 — Explicit factories and validation

## Objective

Implement physically honest local construction for an explicit balanced
HRV/ERV without changing legacy constructors or inventing ducts.

## Tests first

- Required ventilator and exact `sys_type=1`.
- `None`, empty, one, and multiple supply/exhaust duct collections.
- Fresh/independent result graph and non-mutation of caller-owned children.
- Recovery, electric-efficiency, finite-number, collection/type, and duct
  direction validation with physical field names in errors.
- No implicit Room attachment.
- No call to `default_supply_duct()` or `default_exhaust_duct()`.

## Implementation

1. Add the PRD's IronPython-safe `balanced_hrv()` classmethod.
2. Validate all inputs before constructing/returning a system.
3. Duplicate the ventilator and every duct element into the returned system.
4. Set display name deterministically without mutating an unnamed source
   ventilator; apply the final system name to the duplicated child only where
   existing display behavior requires it.
5. Keep `PhVentilationSystem()` and current duct default helpers unchanged for
   backward compatibility; stop presenting their composition as neutral.
6. Add no-mechanical documentation/helper only if Phase 01 requires an API;
   default outcome is documentation that Room assignment `None` is the state.

## Exit checks

- Focused factory tests pass at 100% coverage.
- Existing constructor/duct tests remain unchanged and pass.
- No preliminary performance preset is added in this phase.

