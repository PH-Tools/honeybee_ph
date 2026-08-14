# STATUS — epw-derived-preliminary-climate

**Status:** In progress · Phases 01–04 complete · Phase 05 release handoff · 2026-08-14

- Replaces the superseded bundled climate-dataset proposal.
- Product/IP boundary is decided in context decision 0004.
- Public shape, provenance fields, monthly conversion rules, peak-load
  exclusion, and validation expectations are specified in `PRD.md`.
- Prerequisite verified: PyPI publishes `honeybee-ph 1.33.39`, including the
  required `>=1.33.35` independent-site baseline.
- Phase 01 adds the provenance model, additive HBJSON contract, explicit null
  peak-load state, blank PHPP codes, and deterministic readiness diagnostics.
- Phase 02 adds the internal, snapshot-consistent Ladybug EPW converter with
  path/header/cardinality/value validation, location/scalars, monthly dry-bulb,
  dewpoint, and sky temperatures, warm-season swing, and SHA-256 provenance.
- Phase 03 adds global-horizontal and cardinal vertical-plane monthly
  radiation, explicit diffuse/reflectance assumptions, and deterministic EPW
  ground-temperature depth selection without inferred fallback values.
- Phase 04 adds the public `Site.from_epw()` factory, explicitly unknown
  ASHRAE climate zone, blank PHPP codes, null peak loads, JSON/HBJSON host
  round-trips, and recursive independence verification.
- No in-repo consumer outside `site.py` dereferences peak loads or requires
  nonblank PHPP climate codes; the identified PHX consumer is now guarded on
  its companion branch.
- Phase 05 local verification is complete: public docs/context are updated;
  built sdist/wheel contain no EPW or copied climate dataset; built-wheel
  conversion passes under CPython 3.10.
- PHX readiness is implemented on
  `codex/epw-derived-preliminary-climate-readiness` at `2e8864c`; 881 PHX tests
  pass against its locked dependency and focused integration passes against
  this feature checkout.
- OpenPH was located under `openph-workspace` and audited. It has no direct
  honeybee-ph climate ingestion; the canonical PHX boundary now rejects the
  monthly-only state before OpenPH construction.
- **Next step / release blocker:** merge and release expected
  `honeybee-ph==1.33.40`, verify the published artifact, raise/lock PHX to
  `honeybee-ph>=1.33.40`, verify/release PHX, then archive this packet.
- Do not add or copy any real PHI/Phius/EPW dataset into this repository while
  implementing or testing. Generate a minimal synthetic EPW fixture or use a
  license-compatible test fixture with its terms recorded.
