# 0006 — Use Explicit Ventilation-System States and Selected Equipment

**Date:** 2026-08-14
**Status:** DECIDED
**Decider:** Ed May
**Research:** [`planning/archive/default-ventilation-system-factory/`](../../planning/archive/default-ventilation-system-factory/README.md)

## Context

The ph-modeler POC composed a bare `Ventilator()` with one default 1 m supply
duct and one default 1 m exhaust duct to satisfy downstream conversion. That
graph looked like a balanced HRV but encoded zero sensible recovery plus
invented exterior duct geometry. Absence also crossed repository boundaries as
numeric ID `0`, which blurred no assignment with a real device reference.

Existing Honeybee-PH summer-window ACH inputs describe summer ventilation.
They are not an authoritative source representation for PHPP's primary K12=3
“Only window ventilation” mode.

## Decision

1. Represent no mechanical ventilation as `None` on Room HVAC properties. Do
   not create a placeholder system or device ID.
2. Construct balanced HRV/ERV systems with
   `PhVentilationSystem.balanced_hrv()` from a selected `Ventilator` whose
   recovery and electric-efficiency values are explicit and valid.
3. Treat zero exterior duct elements as a valid, lossless state. When exterior
   ducts exist, preserve every typed element and segment through HBJSON and PHX
   to the PHPP calculation boundary.
4. Keep summer-window ACH independent from the primary mechanical state. Do
   not infer PHPP K12=3 until an authoritative upstream source state is
   designed.
5. Keep absence as `None` in Honeybee-PH and PHX. Numeric `0` is permitted only
   in target-format adapters that require the legacy value and as temporary
   OpenPH input compatibility.
6. Do not add `preliminary_balanced_hrv()` without a separately accepted,
   cited assumption set for recovery, fan power, frost protection, unit
   location, exterior ducts, and provenance labeling.

## Rationale

- A constructor should validate known design intent, not disguise missing
  selections as plausible equipment.
- Empty exterior-duct collections are physically meaningful for a unit wholly
  within the thermal envelope.
- Multiple exterior duct elements contribute independently to the PHPP duct
  efficiency exponent and cannot be collapsed without losing information.
- Target-specific null aliases belong at serialization/export boundaries, not
  in the source domain model.

## What would reopen this

- A supported source model is accepted for primary window-only ventilation.
- Ed accepts a complete, cited preliminary HRV/ERV assumption set.
- A target format removes its numeric no-assignment convention, allowing the
  corresponding boundary adapter to drop `0`.
