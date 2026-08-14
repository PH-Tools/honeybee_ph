# PLAN — epw-derived-preliminary-climate

Implement in order. A phase may start only after the prior phase's exit checks
are satisfied. Keep the feature docs-only until implementation is explicitly
requested.

| Phase | Objective | Gate |
|---:|---|---|
| 01 ✅ | Freeze provenance, completeness, serialization, and downstream contracts | Complete; PyPI `1.33.39` prerequisite and focused contract tests verified |
| 02 ✅ | Implement EPW parsing, source validation, location, scalars, and monthly temperatures | Complete; synthetic EPW suite has 100% branch coverage for the converter |
| 03 ✅ | Implement directional monthly radiation and explicit ground-temperature selection | Complete; 36 focused synthetic EPW tests verified |
| 04 ✅ | Add `Site.from_epw()`, readiness checks, duplication, and HBJSON integration | Complete; 52 focused converter/integration/readiness tests verified |
| 05 | Verify packaging, IronPython compatibility, docs, downstream diagnostics, and release | Focused and full tests green |

Phase documents:

1. [`phase-01-provenance-and-completeness-contract.md`](phases/phase-01-provenance-and-completeness-contract.md)
2. [`phase-02-epw-location-and-temperature-conversion.md`](phases/phase-02-epw-location-and-temperature-conversion.md)
3. [`phase-03-radiation-and-ground-conversion.md`](phases/phase-03-radiation-and-ground-conversion.md)
4. [`phase-04-site-integration-and-readiness.md`](phases/phase-04-site-integration-and-readiness.md)
5. [`phase-05-docs-downstream-and-release.md`](phases/phase-05-docs-downstream-and-release.md)

## Required sequence with adjacent work

```text
published honeybee-ph>=1.33.35
    -> EPW Phase 01 provenance/completeness
    -> EPW conversion phases
    -> PHX/OpenPH readiness verification
```

`space-from-room-factory` is independent and may proceed before or alongside
this packet after the shared-site fix is complete.
