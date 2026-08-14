# Ventilation state contract

**Status:** Accepted for implementation · 2026-08-14

This is the shared source contract for honeybee-ph, PHX, and OpenPH. It is
derived from the PHPP V10.6 `Ventilation` and `Addl vent` inputs documented in
OpenPH's completed `ventilation-input-semantics` packet. `None` means absence in
the Python domain models; a target exporter may translate that state to a
required numeric wire-format value, but `0` is not a device identifier or a
domain-model sentinel.

## Supported source states

| Source state | honeybee-ph | PHX | OpenPH / target result |
|---|---|---|---|
| No mechanical system | `Room.properties.ph_hvac.ventilation_system is None` | `PhxSpace.vent_unit_id_num is None`; no device | OpenPH `NONE`; no device lookup; PHPP K12 blank |
| Summer window ventilation | Existing summer daytime/nighttime window ACH data; no `PhVentilationSystem` | Existing summer-ventilation fields; no device assignment | Existing summer calculation; independent of PHPP K12 |
| Balanced HRV/ERV, no exterior ducts | `balanced_hrv(unit)` or empty duct collections | One real device; zero duct elements | `BALANCED_PH_WITH_HR`; duct coefficient `exp(0) = 1.0` |
| Balanced HRV/ERV, one/many duct elements | Explicit typed supply/exhaust collections | Preserve elements and their segments | Preserve elements to the PHPP boundary; sum coefficients in the exponent |
| Mechanical system missing a device | Invalid source | Conversion fails before adding rooms/devices | No placeholder or downstream lookup |
| Unresolved PHX device reference | Not constructible from a valid conversion | Invalid PHX variant | Aggregate diagnostic names Space and missing device ID |

The PHPP primary `3-Only window ventilation` / K12=3 state is not currently
authorable from honeybee-ph. `PhVentilationSystem` carries mechanical device
data, and existing window inputs describe summer ventilation only. K12=3 is
therefore explicitly deferred; it must not be inferred from summer ACH data or
encoded as an empty mechanical system.

## Mechanical-system rules

| PHPP K12 state | Device | Exterior ducts | Assignment |
|---|---|---|---|
| `1-Balanced PH ventilation with HR` | Required | 0..n supply and 0..n exhaust elements | Every mechanically served Space resolves to the real device |
| `2-Extract air unit` | Required | 0..n elements, normally exhaust | Every mechanically served Space resolves to the real device |
| `3-Only window ventilation` | Forbidden | None | No device assignment; source authoring deferred |
| Blank / no selection | Forbidden | None | No device assignment |

`balanced_hrv()` implements only the first row. It requires an explicit
`Ventilator`, duplicates all accepted children, sets `sys_type=1`, creates no
ducts implicitly, and does not attach itself to a Room.

## Duct preservation and PHPP aggregation

PHX preserves every `PhxDuctElement` and its constituent segments. The
canonical formulas and cell evidence live in OpenPH's archived
`ventilation-input-semantics/STATE_TABLE.md`, under “Exterior Duct Rows.” The
source-model consequences are:

- zero rows produce `EXP(0) = 1.0`, so no exterior duct loss is a valid state;
- multiple elements remain distinct until the target applies its documented
  aggregation;
- a zero-length or zero-airflow row contributes zero;
- no 1 m duct may be manufactured as a cardinality fallback.

## PHX boundary rules

- `PhxSpace.vent_unit_id_num` is `Optional[int]` with a default of `None`.
- honeybee-ph conversion creates a PHX device only from a real source
  `Ventilator`; an incomplete mechanical source fails with a targeted message.
- variant validation reports all unresolved Space/device and duct/device
  references before target output starts.
- WUFI XML and METr JSON emit numeric `0` under the accepted legacy writer
  convention; WUFI import normalizes blank/`0` back to `None`. This is target
  adaptation, not PHX domain state or a claim about the external schemas.
- PHPP skips assignment/device lookup for `None`.
- OpenPH consumes `None` directly and temporarily continues accepting legacy
  PHX `0` input as a compatibility alias.

## Factory and preset decision

The explicit `balanced_hrv(ventilator, ...)` constructor is approved. A
`preliminary_balanced_hrv()` preset remains deferred: no complete, accepted
source currently fixes sensible/latent recovery, specific electric power,
frost protection, location, and duct assumptions. The feature will ship
without guessed performance values unless those assumptions are separately
accepted.
