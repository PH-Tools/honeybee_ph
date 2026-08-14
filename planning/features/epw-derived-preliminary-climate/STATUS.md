# STATUS — epw-derived-preliminary-climate

**Status:** Scoped · 2026-08-14

- Replaces the superseded bundled climate-dataset proposal.
- Product/IP boundary is decided in context decision 0004.
- Public shape, provenance fields, monthly conversion rules, peak-load
  exclusion, and validation expectations are specified in `PRD.md`.
- Prerequisite: `independent-site-defaults` is complete and archived; verify
  the published `honeybee-ph>=1.33.35` artifact before implementation begins.
- **Next step:** execute Phase 01 and freeze additive HBJSON/provenance and
  nullable peak-load compatibility before writing conversion code.
- Blockers: publication and verification of `honeybee-ph>=1.33.35`; downstream
  PHX/OpenPH readiness behavior must also be verified before release.
- Do not add or copy any real PHI/Phius/EPW dataset into this repository while
  implementing or testing. Generate a minimal synthetic EPW fixture or use a
  license-compatible test fixture with its terms recorded.
