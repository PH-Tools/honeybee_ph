# STATUS — independent-site-defaults

**Status:** Complete · archived · release target `v1.33.35` · 2026-08-14

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
- The implementation packet is complete and archived. Merge to `main` is the
  release handoff: GitHub Actions will run tests, create `v1.33.35`, publish to
  PyPI, and create the GitHub release.
- **Final release check:** verify the `v1.33.35` tag, GitHub release, and PyPI
  artifact before beginning the EPW-derived climate packet.
- Blockers: none.
- Downstream: [`epw-derived-preliminary-climate`](../../features/epw-derived-preliminary-climate/README.md)
  remains blocked until the `honeybee-ph>=1.33.35` artifact is published and
  verified.

## Do-not-run boundary

- Do not publish or tag manually from this feature branch; release is owned by
  `.github/workflows/ci.yml` after merge to `main`.
- Do not begin `epw-derived-preliminary-climate` until the published
  `honeybee-ph>=1.33.35` artifact is verified.
