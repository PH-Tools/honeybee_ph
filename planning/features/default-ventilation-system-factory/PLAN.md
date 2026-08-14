# PLAN — default-ventilation-system-factory

The local constructor is small; the feature is not complete until its states
survive PHX/OpenPH without dummy devices or ducts. Implement in this order.

| Phase | Objective | Gate |
|---:|---|---|
| 01 | Freeze cross-repo system/device/duct state matrix and reconcile packets | **Complete** — `STATE_TABLE.md` accepted |
| 02 | Implement explicit local factories and validation | **Complete** — focused factory/adjacent suites green |
| 03 | Prove ownership, duplication, Room attachment, and HBJSON | Phase 02 focused tests green |
| 04 | Implement/verify PHX and OpenPH semantics for every accepted state | PHX representation and OpenPH rules coordinated |
| 05 | Record deferred preset, finish docs/full gates, release, and hand off | End-to-end state matrix green |

Phase documents:

1. [`phase-01-cross-repo-state-contract.md`](phases/phase-01-cross-repo-state-contract.md)
2. [`phase-02-explicit-factories-and-validation.md`](phases/phase-02-explicit-factories-and-validation.md)
3. [`phase-03-serialization-and-room-integration.md`](phases/phase-03-serialization-and-room-integration.md)
4. [`phase-04-phx-openph-integration.md`](phases/phase-04-phx-openph-integration.md)
5. [`phase-05-preset-docs-and-release.md`](phases/phase-05-preset-docs-and-release.md)

## Required cross-repo sequence

```text
PHPP/WUFI state-table research [complete]
    -> accepted honeybee-ph source states
    -> PHX explicit assignment representation
    -> OpenPH no-device/zero-duct/multi-duct behavior
    -> end-to-end verification and release
```

The explicit `balanced_hrv()` implementation may land after Phase 01 while
downstream work continues, but this packet cannot reach Complete before Phase
04.
