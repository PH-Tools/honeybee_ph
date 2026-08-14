# STATUS — ventilation-system-factories

**Status:** Scoped · 2026-08-14

- Filed from the ph-modeler POC architecture review; implementation not
  started.
- Review revised the request: the current bare unit has 0% sensible recovery
  and the current default ducts each create a physical 1 m segment. Their
  composition is not a neutral balanced-HRV default.
- Public `balanced_hrv()` signature, ownership, empty-duct, validation, and
  no-mechanical contracts are fixed in `PRD.md`.
- **Next step:** execute Phase 01 jointly against the PHX/OpenPH packets: derive
  and accept the system/device/duct state matrix before implementation.
- Cross-repo dependency: PHX/OpenPH must accept explicit no-device and
  no-exterior-duct states before those states can pass the full pipeline.
- Blocker: select/document the source of any shipped preliminary performance
  values. The explicit constructor taking a real `Ventilator` is not blocked.
- A preliminary preset is optional and must be omitted—not guessed—if its
  assumptions are not accepted.
