# Phase 02 — EPW location and temperature conversion

**Status:** Complete · 2026-08-14

## Objective

Parse and validate a local EPW and derive location, scalar climate properties,
and monthly temperature collections with no silent fallback values.

## Preconditions

- Phase 01 serialization/readiness contract is accepted and tested.
- A synthetic or explicitly redistributable EPW test fixture is selected and
  its provenance is documented in the test directory.

## Implementation

1. Add a narrow IronPython-safe EPW conversion module; use
   `ladybug.epw.EPW`, not a new parser or dependency.
2. Validate path/readability, annual series completeness, finite source values,
   and location/time-zone ranges before aggregation.
3. Map location name, latitude, longitude, elevation, and UTC offset.
4. Produce monthly means for dry-bulb, dewpoint, and Ladybug sky temperature.
5. Calculate annual mean wind speed.
6. Calculate summer daily swing as the mean daily range over the warmest three
   consecutive calendar months and record the method/version in provenance.
7. Compute and store the source file's SHA-256 without copying the file.
8. Return an internal conversion result carrying values plus accumulated
   issues; public `Site.from_epw()` waits for Phase 04.

## Tests

- Known synthetic hourly values produce exact monthly means and daily swing.
- Southern-hemisphere/warm-season ordering works through year-end.
- Leap-year, partial-year, malformed, missing-value, NaN/Inf, and bad-location
  cases fail with field-specific issues.
- Sky temperature uses Ladybug's EPW behavior, including its documented
  horizontal-infrared fallback.
- Source checksum and conversion method are deterministic.

## Exit checks

- Location and all non-radiation monthly temperature outputs are complete.
- No source missing value was converted to zero.
- Focused tests maintain 100% branch coverage for the new module.

## Completion evidence

- `honeybee_ph._epw.convert_epw()` reads one immutable file snapshot for
  SHA-256, validation, and `EPW.from_file_string()` conversion.
- The generated test EPW contains only controlled synthetic values; no weather
  observation or certification dataset is stored in the repository.
- Focused suite: `21 passed`; `honeybee_ph/_epw.py` has 100% statement and
  branch coverage.
- Full coverage gate: `946 passed`, `80%` aggregate coverage; Black,
  `git diff --check`, and Python 2.7 grammar parsing pass.
- Leap/non-leap cardinality, malformed input, independent invalid values,
  impossible location fields, southern warm-season wrap, deterministic method
  metadata, and horizontal-infrared sky fallback are pinned.
- The public `Site.from_epw()` entry point remains absent pending Phase 04.
