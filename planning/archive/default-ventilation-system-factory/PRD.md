# PRD — Explicit `PhVentilationSystem` factories

**Status:** Complete · honeybee-ph v1.33.42 / PHX v1.56.79 · 2026-08-14
**Author:** Ed May + Codex
**Kind:** Feature (this repo, `honeybee_phhvac`) with downstream PHX/OpenPH coordination

---

## WHAT

Add explicit, physically honest constructors for common ventilation-system
states. Do **not** make the POC's hand-built `Ventilator()` plus two default 1 m
ducts the unnamed production default.

Required public shape:

```python
system = PhVentilationSystem.balanced_hrv(
    ventilator=my_verified_unit,
    supply_ducting=[],
    exhaust_ducting=[],
)
```

The separately named preliminary-model preset is deferred from this feature:

```python
system = PhVentilationSystem.preliminary_balanced_hrv()
```

The word `preliminary`/`placeholder` is load-bearing: callers must be able to
distinguish assumed performance from selected equipment in code, docs, and
serialized user data.

### Behavior contract

1. **Balanced constructor.** Creates `sys_type=1` and requires or receives a
   `Ventilator` whose sensible recovery, electric efficiency, frost protection,
   and other relevant values are explicit. It accepts zero, one, or multiple
   supply/exhaust `PhDuctElement`s; an empty collection means no modeled
   exterior duct segments, not “please invent a 1 m duct.”
   The factory duplicates caller-supplied ventilator and duct objects so it
   does not rename or otherwise mutate caller-owned equipment; each factory
   result owns an independent graph.
2. **No contradictory defaults.** A `sys_type=1` balanced heat-recovery system
   must not silently pair with the current bare `Ventilator()` value of
   `sensible_heat_recovery = 0.0` unless the caller set that value deliberately
   or invoked a clearly named non-HR constructor.
3. **Preliminary preset (deferred follow-up).** Its complete physical assumptions are
   documented and tested: sensible/latent recovery, specific electric power,
   frost protection, unit location, and duct representation. Values must come
   from a stated standard/library convention or be clearly marked BLDGTYP
   preliminary assumptions—not selected-equipment data.
4. **No-mechanical state.** No mechanical system is represented by leaving
   `RoomPhHvacProperties.ventilation_system` unset (`None`). No factory returns
   a dummy `PhVentilationSystem` for this state. Natural/window ventilation is
   not a `PhVentilationSystem`; document and coordinate its existing source
   representation after the cross-repo state matrix is accepted. Do not
   simulate either state with device ID `0` or an empty balanced system.
5. **Validation.** Factories validate recovery/fan-power ranges, duct direction,
   and contradictory combinations. Errors name the physical field, not only a
   downstream serialization failure.
6. **Round-trip.** All factory results preserve their values and semantic state
   through `to_dict()`/`from_dict()`, Honeybee duplication, and HBJSON.
7. **No implicit attachment.** Factories return a system. Attaching it to a Room
   remains an explicit caller operation.

### Existing defaults

`PhDuctElement.default_supply_duct()` and `.default_exhaust_duct()` currently
create a 1 m segment. `Ventilator()` currently has zero sensible/latent recovery.
These may remain for backward compatibility, but new public documentation must
not present their composition as a physically neutral balanced-HRV default.
Any deprecation or value change requires a separate compatibility decision.

### Constraints

- IronPython 2.7-compatible syntax and comment-style type hints.
- No new dependencies.
- Preserve backward-compatible HBJSON deserialization.
- Tests cover each named factory, contradictory inputs, fresh independent
  objects, duplication/round-trip, and downstream PHX conversion.
- OpenPH end-to-end behavior is verified in the coordinated downstream feature,
  not used to justify dummy honeybee-ph inputs.

## WHY

The POC had to assemble a ventilation unit and two 1 m ducts because downstream
conversion rejected their absence. That made the pipeline run, but those values
are not neutral: heat-recovery efficiency and exterior duct length materially
change heating demand.

The original writeup described the four-call block as “not a decision.” The
review showed the opposite. A zero-recovery `Ventilator()` attached to a system
named “Balanced PH ventilation with HR,” plus fabricated ducts, embeds several
physical decisions while making them look like boilerplate.

The library should still make valid programmatic construction easy, but ease
must come from explicit named states and validated composition—not hidden
assumptions. This also gives PHX and OpenPH a clean source contract for
distinguishing no mechanical system, a balanced system without exterior duct
loss, and an incomplete model.

## Acceptance criteria

- One obvious constructor builds a valid balanced system from explicit equipment
  and duct inputs.
- Empty duct collections remain empty and semantically meaningful.
- No named HRV preset silently has 0% sensible recovery.
- No preliminary preset ships without a separately accepted complete set of
  physical assumptions.
- Missing/no-mechanical ventilation is not encoded as an accidental device ID.
- Factory objects are independent and round-trip through HBJSON.
- PHX converts each supported state without inventing new physical inputs.

### Required factory signature

```python
PhVentilationSystem.balanced_hrv(
    ventilator,
    supply_ducting=None,
    exhaust_ducting=None,
    display_name=None,
)
```

`None` and an empty collection both mean no modeled exterior duct elements;
they never trigger default duct creation. The factory validates all inputs,
duplicates accepted children, sets `sys_type=1`, and returns the unattached
system. `ventilator.sensible_heat_recovery` must be finite and greater than
zero through 1.0; latent recovery must be finite from 0.0 through 1.0;
electric efficiency must be finite and nonnegative. Duct elements in the
supply/exhaust inputs must carry the matching direction.
