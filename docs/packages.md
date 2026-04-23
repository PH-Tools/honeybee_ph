---
title: Packages
card_title: Packages
card_description: "The five Python packages included in Honeybee-PH and what each one does."
---

# Packages

Honeybee-PH is distributed as a single PyPI package (`honeybee-ph`) containing five
sub-packages. Each extends a different part of the Ladybug Tools ecosystem with
Passive House data.

## honeybee_ph

The core Passive House data model. Adds PH-specific elements to Honeybee including:

- **Spaces** — interior floor areas with iCFA/TFA weighting factors
- **Building segments** — PH certification boundaries and climate data
- **Certification** — PHI and Phius certification thresholds and settings
- **Site** — location, climate, and shading data

[PyPI](https://pypi.org/project/honeybee-ph/) |
[Source](https://github.com/PH-Tools/honeybee_ph/tree/main/honeybee_ph)

## honeybee_phhvac

PH-specific HVAC systems and devices:

- Ventilation (ERV/HRV units, ductwork, exhaust devices)
- Heating (boilers, district heat, direct electric)
- Heat pumps (air-source, ground-source, combined)
- Domestic hot water (tanks, heat pumps, solar thermal, piping)
- Renewable energy devices (PV)
- Supportive devices (circulation pumps, frost protection)

[Source](https://github.com/PH-Tools/honeybee_ph/tree/main/honeybee_phhvac)

## honeybee_energy_ph

Extensions to Honeybee-Energy for PH-style constructions, materials, and window frames.

> **Note:** Most HVAC functionality has migrated to `honeybee_phhvac`. This package
> is maintained for construction and material extensions.

[Source](https://github.com/PH-Tools/honeybee_ph/tree/main/honeybee_energy_ph)

## honeybee_ph_standards

Reference datasets shipped as JSON files:

- Climate data for PHI and Phius locations
- Standard construction assemblies
- Program and occupancy defaults

[Source](https://github.com/PH-Tools/honeybee_ph/tree/main/honeybee_ph_standards)

## honeybee_ph_utils

Shared utilities used by the other packages:

- Unit conversion helpers (IP / SI)
- Color maps for visualization
- Input validation

[Source](https://github.com/PH-Tools/honeybee_ph/tree/main/honeybee_ph_utils)
