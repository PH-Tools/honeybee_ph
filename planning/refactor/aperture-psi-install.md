# Refactor: Aperture-level Psi-Install (Install Types)

**Status:** Planned — design agreed 2026-08-12; not implemented
**Date:** 2026-08-12
**Author:** Ed May + Claude
**Kind:** Cross-repo refactor. This repo (`honeybee_ph`) is the **primary** — it owns the
new data model, the resolver, and the tests. Ships first; everything else is blocked on it.
**Resolves:** [honeybee_ph #51](https://github.com/PH-Tools/honeybee_ph/issues/51) (by a
different mechanism than the issue proposes — see §8) and, via the `honeybee_grasshopper_ph`
companion, [honeybee_grasshopper_ph #59](https://github.com/PH-Tools/honeybee_grasshopper_ph/issues/59).

**Companion docs (same slug in each repo):**
- `PHX/planning/refactor/aperture-psi-install.md` — resolved values on the aperture element; PHPP per-row write; WUFI/METr window-type variant synthesis
- `honeybee_grasshopper_ph/planning/refactor/aperture-psi-install.md` — new/reworked components; deletes the construction-duplication mechanism (bug #59)
- `ph-navigator-v2/planning/features_v1.1/aperture-psi-install/upstream-alignment.md` — phase-07 GH-client mapping

---

## 1. Problem statement

`psi_install` lives only on `PhWindowFrameElement` (`honeybee_energy_ph/construction/window.py:36`)
— i.e. on the shared window **construction**. Two windows of type `A1` with identical frames,
glass, and spacer but different install conditions require two whole constructions. The GH
workaround (`win_set_psi_install_values.py`) duplicates the construction per aperture with
uuid-suffixed identifiers, producing 939 constructions where 79 exist (bug #59, project 2310).

The install condition is not window-type data. It is a property of *where a window sits*
(mid-wall vs. buried jamb vs. party wall), often patterned by context ("all `A1` in wall-type
`B` share one value; all `A1` in wall-type `C` another"). It deserves its own type.

## 2. Design summary (cross-repo)

1. **`PhApertureInstallType`** — a new, small named object: display name + Ψ-install value
   (+ optional source note). The "type" for install conditions, orthogonal to the window
   construction. Mirrors PH-Navigator v2's Install Type library (`apit_*` rows, doc schema v10).
2. **Per-edge assignment on the aperture instance.** `AperturePhProperties` gains four optional
   per-edge slots (top/right/bottom/left, matching `PhWindowFrame` element order). `None` =
   inherit from the construction's frame element. The construction's `psi_install` keeps its
   current meaning as the **type default**.
3. **One resolver.** A single documented helper returns the effective four Ψ-install values for
   an aperture. Every consumer — ISO 10077-1 U_w, PHX conversion, reports — goes through it.
   No hidden defaults: aperture slot if set, else construction value. Full stop.
4. **Exporters diverge by target capability** (in PHX):
   - **PHPP** natively supports per-instance Ψ-install (four per-row Windows-worksheet columns,
     already written by PHX today) → per-row resolved values, zero extra types.
   - **WUFI/METr** carry Ψ-install only on the WindowType → the PHX exporter synthesizes the
     *minimal* set of deterministic, content-keyed window-type variants at export time.
     Duplication is confined to the last mile, invisible in the HBJSON.
5. **The GH per-aperture component stops duplicating constructions entirely** — the bug-#59
   mechanism is deleted, not patched.

"Mulled"/neighbor detection is **out of scope** for honeybee-ph. PH-Navigator owns edge
adjacency; a mulled edge arrives here as an explicit zero-Ψ install type. honeybee-ph gains no
language of "mulled".

## 3. Changes in this repo

### 3.1 `PhApertureInstallType` (new class)

Location: `honeybee_energy_ph/construction/window.py`, sibling of `PhWindowFrameElement` /
`PhWindowGlazing`. Subclass of `_base._Base` (identifier, display_name, user_data).

| Attribute | Type | Default | Notes |
|---|---|---|---|
| `psi_install` | float | 0.0 | W/mK |
| `source` | str | `""` | free-text provenance ("Phius mid-wall", "Flixo calc 2026-08-01", …) |

- `to_dict` / `from_dict` / `duplicate` / `__copy__` per repo serialization rules
  (hard rule 2: new fields default in `__init__`, `.get(key, default)` in `from_dict`).
- IronPython 2.7 compatible (hard rule 1).
- A zero-Ψ instance **is** the "install off" state — there is no separate boolean flag (§8).

### 3.2 `AperturePhProperties` per-edge slots

Location: `honeybee_ph/properties/aperture.py`. Follow the `ShadingDimensions` precedent:
a small container class (working name `AperturePsiInstalls`) with `.top` / `.right` /
`.bottom` / `.left`, each `Optional[PhApertureInstallType]`, default `None`.

- Serialize **inline, full objects** per edge (no model-level registry). Identifiers are
  preserved, so downstream consumers can dedupe/report by identifier. Tradeoff accepted:
  N apertures referencing one install type write N small copies in HBJSON; this is bounded
  (4 tiny dicts/aperture, only where overrides exist) and avoids new cross-referencing
  machinery in `ModelPhProperties`.
- Import direction is fine: `honeybee_ph/bldg_segment.py` already imports
  `PhThermalBridge` from `honeybee_energy_ph` — same pattern.
- Round-trips through `to_dict` / `from_dict` / `duplicate` / `apply_properties_from_dict`
  (the model-load path at `honeybee_ph/properties/model.py:210` already visits apertures).
- Backward compatibility: absent key ⇒ all `None` ⇒ identical results to today.

Edge naming/order matches `PhWindowFrame.elements` (top, right, bottom, left) everywhere.

### 3.3 The resolver (single source of truth)

Location: new module `honeybee_ph_utils/aperture_psi_install.py`.

```
resolve_psi_install_values(_hb_aperture)  # -> {"top": float, "right": ..., "bottom": ..., "left": ...}
resolve_effective_frame(_hb_aperture)     # -> PhWindowFrame (transient duplicate, psi_install overridden)
```

- Precedence per edge: aperture slot's `psi_install` if the slot is not `None`, else the
  construction frame element's `psi_install`. Handles `WindowConstructionShade` by reaching
  the nested `WindowConstruction` (same pattern as the GH components).
- `resolve_effective_frame` exists so ISO 10077-1 needs no internal changes: it feeds the calc
  a transient in-memory frame; nothing new is serialized.
- Pure functions, no Grasshopper imports — testable here (the bug-#59 lesson: GH-hosted logic
  can't be tested; this repo owns the worker suite).

### 3.4 ISO 10077-1 integration

`honeybee_ph_utils/iso_10077_1.py` — `calculate_hb_aperture_uw()` (`:388`) and any other
aperture-entry points route through `resolve_effective_frame()`. The frame/glazing-entry
functions (`calculate_window_uw`, `calculate_standard_window_uw`) are unchanged — they operate
on explicit frames and stay override-unaware by design. An edge resolved to a zero-Ψ install
type contributes zero install heat loss to U_w,installed.

### 3.5 Explicitly NOT changing

- `PhWindowFrameElement.psi_install` semantics and its 0.04 default (type-level default stays).
- No `psi_install_enabled` boolean anywhere (§8).
- No model-level install-type library/registry (inline serialization, §3.2).
- No neighbor/mull detection.

## 4. Tests (the "never again" invariants)

Bug #59 happened because per-instance data was faked with per-instance *types*. The invariant
that prevents the class of bug: **identical inputs ⇒ identical, stable output; object count
grows with distinct content, never with instance count.** Encode it:

- [ ] `PhApertureInstallType` round-trips `to_dict`/`from_dict`/`duplicate`; `.get` back-compat.
- [ ] `AperturePsiInstalls` round-trips, including through full-model HBJSON load
      (`apply_properties_from_dict`) and `Aperture.duplicate()`.
- [ ] Resolver precedence: slot set → slot value; slot `None` → construction value; mixed edges.
- [ ] Zero-Ψ install type ⇒ that edge contributes 0 to `heat_loss_psi_install` in the
      aperture U_w; other edges unchanged.
- [ ] Two apertures sharing **one** construction resolve to **different** values with zero new
      constructions in the model (`len(model.properties.energy.constructions)` unchanged).
- [ ] Old HBJSON (no `install_types` key) loads and produces byte-identical resolved values.
- [ ] `python3 -m pytest` at 100% coverage (hard rule 4); `docs/nav.yml` updated (hard rule 3).

## 5. Sequencing (cross-repo)

1. **This repo**: model + resolver + tests → release to PyPI.
2. **PHX**: consume resolver at `from_HBJSON`; PHPP per-row write; WUFI/METr variant synthesis.
3. **honeybee_grasshopper_ph**: new Create-Install-Type component; rewrite Set-Aperture-Psi-Installs;
   delete `duplicate_aperture_construction`. Closes #59.
4. **ph-navigator-v2**: phase-07 GH client maps its `installs` export block 1:1 onto the new model.

## 6. Implementation decisions (settled)

- **Names confirmed (Ed, 2026-08-12):** `PhApertureInstallType`, `AperturePsiInstalls`,
  serialized dict key `install_types`. Keep PHN's "Install Type" language in all user-facing copy.
- **WUFI variant `u_value_window`: recompute** (Ed, 2026-08-12) — see PHX companion doc §3.2.
- **No #59 interim patch** (Ed, 2026-08-12) — straight to full implementation.
- GH "set" component auto-wraps bare numeric inputs into anonymous content-keyed install
  types (recommended in GH companion doc §2.2; confirm ergonomics on the canvas at
  implementation).

## 7. Implementation phases (this repo)

Branch: `refactor/aperture-psi-install`. One phase at a time; each phase ends green
(`python3 -m pytest`, coverage 100%) with a simplify pass before moving on.

| Phase | Scope | Verification | State |
|---|---|---|---|
| 1 | `PhApertureInstallType` in `honeybee_energy_ph/construction/window.py` (§3.1) | Round-trip + duplicate tests in `tests/test_honeybee_energy_ph/`; IPy2.7-safe | ✅ 2026-08-12 |
| 2 | `AperturePsiInstalls` container + `AperturePhProperties.install_types` (§3.2), incl. `to_dict`/`from_dict`/`duplicate`/`apply_properties_from_dict` | Property round-trip tests; full-model HBJSON round-trip; old-HBJSON back-compat (`.get`) | ☐ |
| 3 | Resolver module `honeybee_ph_utils/aperture_psi_install.py` (§3.3) | Precedence tests (slot/inherit/mixed/shade-construction); shared-construction no-duplication test | ☐ |
| 4 | ISO 10077-1 integration (§3.4): aperture entry points use `resolve_effective_frame` | Zero-Ψ edge ⇒ zero install heat loss; unresolved paths byte-identical | ☐ |
| 5 | Closeout: `docs/nav.yml` (hard rule 3), full-suite 100% coverage, §4 checklist swept | All §4 boxes checked | ☐ |

## 8. Relationship to issue #51

Issue #51 asks for per-window, per-edge install **on/off** (PHPP's 0|1 columns) via a
`psi_install_enabled` flag on the frame element plus four `Optional[bool]` aperture overrides.
This refactor supersedes that mechanism while fully covering its intent:

| #51 acceptance criterion | How this design satisfies it |
|---|---|
| Frame-element `psi_install_enabled` flag | **Not implemented** — deliberately. A zero-Ψ value (type default or install type) expresses "no install psi"; one mechanism, not two. A frame type that "never gets install psi on an edge" sets that element's `psi_install = 0.0`. |
| Four `Optional[bool]` per-edge aperture overrides | Four `Optional[PhApertureInstallType]` per-edge slots — strictly more expressive: off (Ψ=0), *and* different values per instance, with named provenance. |
| Single documented resolver, aperture wins, `None` inherits | §3.3, identical semantics. |
| ISO 10077-1 uses resolved value; off-edge contributes zero | §3.4. |
| Backward compatibility via `.get` | §3.2 / §4. |
| Two rooms' apertures, one construction, different install conditions, no duplicates | The headline test in §4. |
| 100% pytest coverage | §4. |
| Companion issues on PHX + honeybee_grasshopper_ph | The companion planning docs (and the existing #59). |

When implemented, close #51 with a note that the boolean-flag design was replaced by
Install Types, criteria mapped as above.
