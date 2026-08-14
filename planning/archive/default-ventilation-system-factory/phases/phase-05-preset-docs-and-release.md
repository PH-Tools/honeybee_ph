# Phase 05 — Deferred preset, docs, and release

**Status:** Complete · released and archived · 2026-08-14

## Objective

Record the preliminary preset as a deferred follow-up, document every supported
state, run full gates, and release the coordinated contract.

## Deferred preliminary preset

This feature ships without `preliminary_balanced_hrv()`. A future packet may
propose it only with Ed's acceptance of a complete, cited assumption set
covering:

- sensible and latent recovery;
- electric efficiency/specific fan power;
- frost-protection behavior and threshold;
- conditioned/unconditioned unit location;
- supply/exhaust exterior duct representation;
- display/provenance label identifying assumed—not selected—equipment.

Never fill gaps from current defaults.

## Docs and verification

1. Update docstrings and `docs/nav.yml` for public factories.
2. Document no-mechanical (`None`), natural/window, balanced with zero exterior
   ducts, and balanced with duct elements.
3. Add migration guidance away from composing bare `Ventilator()` with default
   ducts as a nominal HRV.
4. Run Black, `git diff --check`, IronPython compatibility, and full pytest at
   or above the 75% repository coverage floor.
5. Record downstream suite/reference evidence, release versions, and minimum
   compatible pins.
6. Fold the stable ventilation-state contract into `context/`, update all
   packets/statuses, and archive only after cross-repo releases are verified.

## Exit checks

- Every documented constructor state passes the end-to-end matrix.
- Preliminary preset is explicitly deferred to a separately accepted packet.
- No public example contains dummy ID `0`, zero-recovery HRV, or invented duct.
- Released versions and downstream compatibility requirements are recorded.

## Outcome

`docs/ventilation-systems.md` documents every supported authoring state and
migration away from bare equipment plus default 1 m ducts. Both Python examples
execute independently and explicitly set all ventilator fields that flow
downstream; their values are labeled illustrative, not recommended defaults.
Decision 0006 preserves the stable state/absence/deferred-preset contract.

The preliminary preset remains deferred. All simplify reuse, quality, and
efficiency findings are resolved; the decision-record research link follows
this archived packet. Black, Python 2 grammar parsing, `git diff --check`, and
the exact public examples pass. The full suite passes 1,016 tests with 80%
aggregate coverage.

honeybee-ph v1.33.42 and PHX v1.56.79 are published. PHX declares and locks
`honeybee-ph>=1.33.42`; both artifacts pass clean-install smoke tests. The
published matrix with OpenPH 0.5.1 and openph-demand 0.5.0 installs and converts
the no-mechanical, zero-duct, and multi-duct states successfully. All three
implementation releases were verified before the planning packets were
archived.
