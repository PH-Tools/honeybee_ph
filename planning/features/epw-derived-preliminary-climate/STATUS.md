# STATUS — epw-derived-preliminary-climate

**Status:** In progress · Phase 01 complete · 2026-08-14

- Replaces the superseded bundled climate-dataset proposal.
- Product/IP boundary is decided in context decision 0004.
- Public shape, provenance fields, monthly conversion rules, peak-load
  exclusion, and validation expectations are specified in `PRD.md`.
- Prerequisite verified: PyPI publishes `honeybee-ph 1.33.39`, including the
  required `>=1.33.35` independent-site baseline.
- Phase 01 adds the provenance model, additive HBJSON contract, explicit null
  peak-load state, blank PHPP codes, and deterministic readiness diagnostics.
- **Next step:** execute Phase 02: validated EPW location, scalar, and monthly
  temperature conversion without adding the public `Site.from_epw()` entry point.
- Release blocker: downstream PHX readiness behavior must be implemented and
  verified; no adjacent OpenPH checkout was available for a direct audit.
- Do not add or copy any real PHI/Phius/EPW dataset into this repository while
  implementing or testing. Generate a minimal synthetic EPW fixture or use a
  license-compatible test fixture with its terms recorded.
