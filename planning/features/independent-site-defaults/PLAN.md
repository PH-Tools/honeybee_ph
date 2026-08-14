# PLAN — independent-site-defaults

Implement in order. Tests that reproduce the shared-state defect precede all
constructor changes.

| Phase | Objective | Gate | Status |
|---:|---|---|---|
| 01 | Pin compatibility and reproduce every shared-identity path | No code changes before failures exist | **Complete** — 66 red / 26 green contract checks |
| 02 | Replace constructed defaults and implement recursive duplication | Phase 01 regression matrix complete | **Complete** — 95 focused cases green |
| 03 | Verify HBJSON, host-object behavior, docs, full suite, and release | Phase 02 focused tests green | **Implemented** — local verification complete; release/archive pending merge |

Phase documents:

1. [`phase-01-regression-and-compatibility-contract.md`](phases/phase-01-regression-and-compatibility-contract.md)
2. [`phase-02-constructors-and-deep-duplication.md`](phases/phase-02-constructors-and-deep-duplication.md)
3. [`phase-03-integration-docs-and-release.md`](phases/phase-03-integration-docs-and-release.md)

## Required downstream sequence

```text
independent-site-defaults
    -> release
    -> epw-derived-preliminary-climate
```
