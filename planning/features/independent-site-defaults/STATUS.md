# STATUS — independent-site-defaults

**Status:** In progress · Phase 01 complete · 2026-08-14

- Defect reproduced during the ph-modeler POC review: separate `Site()` calls
  share a nested `Climate` object.
- Static audit also identified constructed defaults throughout `site.py` and a
  shallow `Climate.__copy__()` implementation.
- Phase 01 pins the default `Site`/`Climate` serialization payload and covers
  every mutable constructor default, default-graph identity/mutation path,
  recursive duplicate path, legacy load, repeated load, and explicit-child
  ownership contract.
- The red baseline is recorded as 66 strict expected failures and 26 passing
  compatibility/ownership checks. `--runxfail` confirms all 66 defects fail
  before production code changes.
- **Next step:** execute Phase 02: replace constructed defaults, make copies
  recursive, and turn all 66 expected failures green.
- Blockers: none.
- Downstream: `../epw-derived-preliminary-climate/` is blocked on this feature's
  completion and release.
