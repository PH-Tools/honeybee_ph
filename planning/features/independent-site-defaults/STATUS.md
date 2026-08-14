# STATUS — independent-site-defaults

**Status:** In progress · Phases 01–02 complete · 2026-08-14

- Defect reproduced during the ph-modeler POC review: separate `Site()` calls
  share a nested `Climate` object.
- Static audit also identified constructed defaults throughout `site.py` and a
  shallow `Climate.__copy__()` implementation.
- Phase 01 pins the default `Site`/`Climate` serialization payload and covers
  every mutable constructor default, default-graph identity/mutation path,
  recursive duplicate path, legacy load, repeated load, and explicit-child
  ownership contract.
- The Phase 01 red baseline recorded 66 strict expected failures and 26 passing
  compatibility/ownership checks. `--runxfail` confirmed all 66 defects failed
  before production code changes.
- Phase 02 replaces all 20 constructed defaults, makes modeled `Climate` and
  `Climate_Ground` duplication independent while preserving caller-added
  attributes, and copies deserialized `user_data` dictionaries.
- The focused graph contract now passes all 95 cases, including explicit and
  positional child ownership plus every ground scalar.
- **Next step:** execute Phase 03 host-object/HBJSON, artifact, documentation,
  full-suite, and compatibility verification.
- Blockers: none.
- Downstream: `../epw-derived-preliminary-climate/` is blocked on this feature's
  completion and release.
