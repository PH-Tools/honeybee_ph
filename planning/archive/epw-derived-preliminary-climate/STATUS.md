# STATUS — epw-derived-preliminary-climate

**Status:** Complete · released and downstream-verified · 2026-08-14

- Replaces the superseded bundled climate-dataset proposal.
- Product/IP boundary is decided in context decision 0004.
- Public shape, provenance fields, monthly conversion rules, peak-load
  exclusion, and validation expectations are specified in `PRD.md`.
- Prerequisite verified: PyPI published `honeybee-ph 1.33.39`, including the
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
- Honeybee-ph PR #93 merged at `8917fd6`; GitHub Actions published v1.33.40.
  A fresh Python 3.14 venv installed the PyPI wheel and verified EPW monthly
  readiness, explicit peak-load unavailability, null peak loads, and
  `epw_derived` provenance.
- PHX readiness merged in PR #81 at `4a76a4a`; its dependency floor and lock
  require `honeybee-ph>=1.33.40`. The Python 3.10 gate passed with 881 tests,
  3 skipped, and 1 deselected before GitHub Actions published PHX v1.56.76.
- A fresh Python 3.10 venv installed PHX v1.56.76 plus honeybee-ph v1.33.40,
  derived a real synthetic EPW climate, and verified the targeted PHX
  peak-load-readiness rejection before values were copied.
- OpenPH was located under `openph-workspace` and audited. It has no direct
  honeybee-ph climate ingestion; the canonical PHX boundary now rejects the
  monthly-only state before OpenPH construction.
- All implementation, packaging, release, downstream, and archive gates are
  complete. No follow-up release blocker remains for this packet.
- Do not add or copy any real PHI/Phius/EPW dataset into this repository while
  implementing or testing. Generate a minimal synthetic EPW fixture or use a
  license-compatible test fixture with its terms recorded.
