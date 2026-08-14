# STATUS — independent-site-defaults

**Status:** Implemented · verified locally; release pending · 2026-08-14

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
- Phase 03 adds real Honeybee Room default/duplicate coverage, a JSON-normalized
  Model HBJSON round-trip loaded twice, public ownership docstrings, and the
  canonical mutable-constructor ownership rule.
- Phase 03 verification is complete: 98 focused graph/host/HBJSON tests and
  891 repository tests pass; Black and `git diff --check` are clean; the
  changed module parses with Python 2.7 grammar and compiles under the installed
  IronPython runtime.
- `dist/honeybee_ph-1.33.34-py3-none-any.whl` installs with declared
  dependencies in a fresh isolated environment and passes default, duplicate,
  mutation-isolation, and repeated-deserialization smoke checks.
- The configured repository-wide `fail_under = 100` coverage check reports
  79% across the existing codebase. Ed authorized that existing aggregate
  baseline for this feature on 2026-08-14; no unrelated coverage expansion was
  added. `honeybee_ph/site.py` reports 99%, with only pre-existing import
  fallback and invalid-length validation lines uncovered.
- **Next step:** merge this branch to `main`. GitHub Actions will run tests,
  create the version bump/tag, publish to PyPI, and create the GitHub release.
  Then record the actual released version, update the EPW minimum prerequisite,
  mark this packet Complete, and archive it.
- Blockers: none.
- Downstream: `../epw-derived-preliminary-climate/` is blocked on this feature's
  completion and release.

## Do-not-run boundary

- Do not publish or tag manually from this feature branch; release is owned by
  `.github/workflows/ci.yml` after merge to `main`.
- Do not unblock `epw-derived-preliminary-climate` or archive this packet until
  the published artifact is verified and its actual version is recorded.
