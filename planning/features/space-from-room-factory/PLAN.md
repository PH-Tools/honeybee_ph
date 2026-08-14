# PLAN — space-from-room-factory

Implement in order. This repo owns the factory and release; the GH wrapper
changes only after the released minimum version is available.

| Phase | Objective | Gate |
|---:|---|---|
| 01 | Freeze API, unit, floor-selection, geometry, naming, and host contracts in tests | No production implementation yet |
| 02 | Implement the pure-Ladybug `Space.from_room()` assembly | Phase 01 failures reproduce missing capability |
| 03 | Prove attachment, duplication, HBJSON, docs, and full-suite compatibility | Phase 02 focused tests green |
| 04 | Release primary, re-point GH wrapper, compare behavior, and retire duplicate code | Released minimum version installed in GH environment |

Phase documents:

1. [`phase-01-contract-and-geometry-tests.md`](phases/phase-01-contract-and-geometry-tests.md)
2. [`phase-02-pure-space-factory.md`](phases/phase-02-pure-space-factory.md)
3. [`phase-03-integration-docs-and-verification.md`](phases/phase-03-integration-docs-and-verification.md)
4. [`phase-04-release-and-gh-handoff.md`](phases/phase-04-release-and-gh-handoff.md)

## Required cross-repo sequence

```text
honeybee_ph factory + tests
    -> honeybee_ph release
    -> honeybee_grasshopper_ph pin bump + wrapper re-point
    -> Rhino/Grasshopper parity smoke
```

