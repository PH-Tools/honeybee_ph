# Phase 05 — Preset decision, docs, and release

## Objective

Decide the optional preliminary preset, document every supported state, run
full gates, and release the coordinated contract.

## Preliminary preset gate

Add `preliminary_balanced_hrv()` only if Ed accepts a complete, cited assumption
set covering:

- sensible and latent recovery;
- electric efficiency/specific fan power;
- frost-protection behavior and threshold;
- conditioned/unconditioned unit location;
- supply/exhaust exterior duct representation;
- display/provenance label identifying assumed—not selected—equipment.

If any value remains unresolved, record the preset as Deferred and complete the
feature without it. Never fill gaps from current defaults.

## Docs and verification

1. Update docstrings and `docs/nav.yml` for public factories.
2. Document no-mechanical (`None`), natural/window, balanced with zero exterior
   ducts, and balanced with duct elements.
3. Add migration guidance away from composing bare `Ventilator()` with default
   ducts as a nominal HRV.
4. Run Black, `git diff --check`, IronPython compatibility, and full pytest at
   100% coverage.
5. Record downstream suite/reference evidence, release versions, and minimum
   compatible pins.
6. Fold the stable ventilation-state contract into `context/`, update all
   packets/statuses, and archive only after cross-repo releases are verified.

## Exit checks

- Every documented constructor state passes the end-to-end matrix.
- Optional preset is either fully specified/tested or explicitly deferred.
- No public example contains dummy ID `0`, zero-recovery HRV, or invented duct.
- Released versions and downstream compatibility requirements are recorded.

