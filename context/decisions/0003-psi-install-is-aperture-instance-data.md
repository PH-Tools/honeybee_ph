# 0003 — Psi-Install Is Aperture-Instance Data, Resolved From Named Install Types

**Date:** 2026-08-12
**Status:** DECIDED — implemented
**Decider:** Ed May
**Research:** [`planning/refactor/aperture-psi-install.md`](../../planning/refactor/aperture-psi-install.md)
**Companion repos:** `PHX/planning/refactor/aperture-psi-install.md`,
`honeybee_grasshopper_ph/planning/refactor/aperture-psi-install.md`,
`ph-navigator-v2/planning/features_v1.1/aperture-psi-install/upstream-alignment.md`
**Resolves:** honeybee_ph [#51](https://github.com/PH-Tools/honeybee_ph/issues/51);
honeybee_grasshopper_ph [#59](https://github.com/PH-Tools/honeybee_grasshopper_ph/issues/59)

## Context

`psi_install` lived only on `PhWindowFrameElement` — the shared window construction. Giving
one window a different install condition required a whole duplicate construction. The GH
component that automated this minted uuid-suffixed constructions per aperture: 939 window
constructions where 79 existed (project 2310, bug #59). The install condition is a property
of *where a window sits* (mid-wall, buried jamb, party wall), not of the window type.

## Decision

1. **Install conditions are their own named type** — `PhApertureInstallType` (Ψ value +
   source note), mirroring PH-Navigator v2's Install Type library. Not a bare float, so
   assignments stay QA-legible and round-trip PHN's `apit_*` identifiers.
2. **Assignment is per-aperture, per-edge** — four optional slots on `AperturePhProperties`
   (`install_types`, top/right/bottom/left). `None` = inherit the construction frame
   element's value, which keeps its meaning as the type default.
3. **One resolver** — `honeybee_ph_utils/aperture_psi_install.py` is the only way any
   consumer (ISO 10077-1, PHX, reports) obtains effective values. No hidden defaults.
4. **No boolean on/off flag** (what issue #51 originally proposed) — a zero-Ψ Install Type
   *is* the off state. One mechanism, not two.
5. **Exporters absorb target limitations, not the data model** — PHPP accepts per-window-row
   Ψ-install natively; WUFI/METr carry it only on the WindowType, so the PHX exporter
   synthesizes minimal content-keyed window-type variants at export time. Construction
   duplication is confined to the last mile, never in the HBJSON.
6. **No "mulled"/neighbor language in honeybee-ph** — edge adjacency is PH-Navigator's
   responsibility; a mulled edge arrives here as an explicit zero-Ψ assignment.

## Why this, not the alternatives

- **Boolean flags (#51 as filed):** covers on/off but not per-instance *values* — the actual
  pain. Subsumed by zero-Ψ types.
- **Content-keyed construction dedup in GH (bug-#59 doc):** treats the symptom; instance
  data faked with per-instance types keeps the whole bug class alive.
- **Bare per-edge floats on the aperture:** loses provenance and makes PHN round-trips lossy.

## Invariant to protect

Identical inputs ⇒ identical, stable identifiers; object count grows with distinct
content, never with instance count. Encoded in the test suites of all three repos.
