---
title: Ventilation systems
---

# Explicit ventilation-system construction

Use `PhVentilationSystem.balanced_hrv()` when a selected HRV or ERV is known.
The factory validates the unit type, recovery/electric ranges, and duct
directions; preserves zero or many exterior duct elements; and returns an
independent system graph. It does not choose equipment, invent ducts, or attach
the system to a Room.

## Supported authoring states

| State | Honeybee-PH representation |
|---|---|
| No mechanical ventilation | Leave `room.properties.ph_hvac.ventilation_system` as `None`. |
| Summer window ventilation | Use the existing summer daytime/nighttime window ACH inputs; keep the mechanical system as `None`. These inputs do not imply PHPP K12=3 window-only primary ventilation. |
| Balanced HRV/ERV with no exterior ducts | Call `balanced_hrv()` with a selected `Ventilator` and omit both duct collections. |
| Balanced HRV/ERV with modeled exterior ducts | Pass explicit supply elements with `duct_type=1` and exhaust elements with `duct_type=2`. Each element may contain one or more caller-defined segments. |

Honeybee-PH does not currently author PHPP's primary “Only window
ventilation” mode. That state needs its own authoritative source model and must
not be inferred from summer-window ACH.

## Balanced system without exterior ducts

Set every unit field from the selected equipment and project data. The factory
requires sensible recovery greater than zero and no greater than one, latent
recovery from zero through one, and nonnegative electric efficiency. It does
not validate quantity, frost-control settings, or unit location.
The values below are illustrative selected/project inputs, not library
recommendations.

```python
from honeybee.room import Room

from honeybee_phhvac.ventilation import PhVentilationSystem, Ventilator

room = Room.from_box("Apartment")
unit = Ventilator()
unit.display_name = "Selected ERV"
unit.quantity = 1
unit.sensible_heat_recovery = 0.82
unit.latent_heat_recovery = 0.45
unit.electric_efficiency = 0.35
unit.frost_protection_reqd = True
unit.temperature_below_defrost_used = -5.0
unit.in_conditioned_space = True
unit.subsoil_heat_exchange_efficiency = None
unit.preheated_intake_temperature_c = None

system = PhVentilationSystem.balanced_hrv(
    unit,
    display_name="Apartment ERV",
)

# Attachment is an explicit caller action.
room.properties.ph_hvac.set_ventilation_system(system)
```

Omitting `supply_ducting` and `exhaust_ducting`, or passing empty collections,
means no exterior duct elements are modeled. It is not shorthand for unknown
ducts and does not create a default length.

## Balanced system with exterior ducts

Build segments from actual geometry and physical attributes, group them into
typed exterior duct elements, and pass those elements to the factory.

```python
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment
from honeybee_phhvac.ventilation import PhVentilationSystem, Ventilator

unit = Ventilator()
unit.display_name = "Selected ERV"
unit.quantity = 1
unit.sensible_heat_recovery = 0.82
unit.latent_heat_recovery = 0.45
unit.electric_efficiency = 0.35
unit.frost_protection_reqd = True
unit.temperature_below_defrost_used = -5.0
unit.in_conditioned_space = True
unit.subsoil_heat_exchange_efficiency = None
unit.preheated_intake_temperature_c = None

supply_geometry = LineSegment3D.from_end_points(
    Point3D(0, 0, 0), Point3D(2.4, 0, 0)
)
exhaust_geometry = LineSegment3D.from_end_points(
    Point3D(0, 1, 0), Point3D(1.8, 1, 0)
)

supply = PhDuctElement("Exterior supply", _duct_type=1)
supply.add_segment(PhDuctSegment(supply_geometry, _diameter=0.2))

exhaust = PhDuctElement("Exterior exhaust", _duct_type=2)
exhaust.add_segment(PhDuctSegment(exhaust_geometry, _diameter=0.2))

system = PhVentilationSystem.balanced_hrv(
    unit,
    supply_ducting=[supply],
    exhaust_ducting=[exhaust],
    display_name="Apartment ERV",
)
```

The returned system owns duplicates of the unit, elements, segments, geometry,
and nested `user_data`. Caller-owned inputs can therefore be reused or changed
without mutating the factory result.

## Migration from implicit defaults

Do not use a bare `Ventilator()` plus
`PhDuctElement.default_supply_duct()` / `default_exhaust_duct()` as a nominal
HRV. A bare unit has zero sensible recovery, while each default duct helper
creates a physical 1 m segment; together they encode specific, generally false
performance and geometry.

Instead:

1. Leave the Room ventilation system as `None` when no mechanical system is
   selected.
2. Populate a `Ventilator` from selected equipment data.
3. Call `balanced_hrv()` with empty duct collections when there truly are no
   exterior ducts, or pass elements built from known exterior duct geometry.

There is intentionally no `preliminary_balanced_hrv()` preset. Sensible and
latent recovery, fan power, frost protection, unit location, and exterior duct
assumptions require an accepted, cited assumption set before such a preset can
be added.
