# PRD — EPW-derived preliminary monthly climate

**Status:** Scoped · 2026-08-14
**Author:** Ed May + Codex
**Kind:** Feature / data-contract extension (this repo primary; downstream
readiness coordination required)

---

## Goal

Allow a Python or Grasshopper caller to turn a local EPW file into a complete
set of **preliminary monthly demand inputs** without redistributing PHI/Phius
climate data or misrepresenting EPW-derived values as certification data.

Target public entry point:

```python
from honeybee_ph.site import Site

site = Site.from_epw(
    "/path/to/weather.epw",
    ground_temperature_depth=0.5,
    ground_reflectance=0.2,
    diffuse_model="isotropic",
)
```

The method reads only the supplied local file. It performs no search, download,
dataset-name resolution, or caching outside the returned object.

## Non-negotiable boundary

- No PHI/Phius climate dataset is shipped, copied, scraped, or reconstructed.
- No EPW file is included in the source distribution or wheel.
- EPW denotes a format, not a blanket data license. The caller is responsible
  for the right to process the supplied file.
- Output is labeled `epw_derived`, `is_certification_approved=False`, and
  `peak_load_data_available=False`.
- The converter never assigns a PHI/Phius dataset identifier. The returned
  `Site.phpp_library_codes` uses a deliberately blank `PHPPCodes` record.
- EPW-derived monthly values are not advertised as PHPP/Phius-equivalent.

See decision
[`0004-no-bundled-licensed-climate-data`](../../../context/decisions/0004-no-bundled-licensed-climate-data.md).

## Model contract

Add an IronPython-safe `ClimateProvenance` model attached to `Climate` with:

- `source_type`: `legacy_unknown`, `phi_approved`, `phius_approved`,
  `epw_derived`, or `user_defined`;
- `source_name`, `source_uri`, and `source_version` (optional strings);
- `source_checksum` (SHA-256 for a file-backed source when available);
- `conversion_method` and `conversion_method_version`;
- `is_certification_approved` (`True`, `False`, or `None` when unknown);
- `monthly_data_available` (`True`, `False`, or `None`);
- `peak_load_data_available` (`True`, `False`, or `None`);
- `assumptions` (a small JSON-safe dict recording chosen algorithms/values).

Backward compatibility:

- `Climate.provenance` defaults to `None`; readiness treats `None` as legacy
  unknown state;
- old HBJSON without `provenance` loads with `provenance=None` and reserializes
  without adding a key;
- `to_dict()` writes `provenance` only when an explicit
  `ClimateProvenance` object is present, so existing `Climate()` serialized
  output remains unchanged;
- `Climate.peak_loads` remains populated for legacy/default construction, but
  may be `None` for a source that explicitly declares peak data unavailable;
- `to_dict()` writes `peak_loads: null` for that explicit state and
  `from_dict()` accepts missing, object, or null values;
- `duplicate()` recursively duplicates provenance and all available climate
  collections.

Provide local readiness checks that distinguish:

- monthly-demand-ready;
- peak-load-ready;
- incomplete/unknown.

No validator may infer availability from whether numeric values happen to be
zero; zero can be a real source value.

## EPW conversion contract

Use `ladybug.epw.EPW` and existing Ladybug data collections. No new runtime
dependency is required; this repo already imports `ladybug.epw` in
`honeybee_ph_utils/sky_matrix.py`.

### Location and scalar values

- latitude, longitude, elevation, UTC offset, and display name come from the
  EPW location header;
- station elevation comes from that same header;
- average wind speed is the annual arithmetic mean of valid EPW wind-speed
  values;
- summer daily temperature swing is the mean daily dry-bulb max-minus-min over
  the warmest three consecutive calendar months, determined from monthly mean
  dry-bulb values; record this method in provenance;
- invalid/missing source values produce a field-specific conversion issue,
  never a silent zero.

### Monthly temperatures

- air temperature = monthly mean EPW dry-bulb temperature;
- dewpoint = monthly mean EPW dewpoint temperature;
- sky temperature = monthly mean `EPW.sky_temperature`;
- ground temperature comes only from the EPW ground-temperature header:
  - no series: fail monthly readiness with a targeted issue;
  - one series and no requested depth: use it and record its depth;
  - multiple series and no requested depth: require the caller to choose;
  - requested unavailable depth: fail and list available depths.

No air-temperature proxy or zero-filled ground series is permitted.

### Monthly solar radiation

- global = monthly total EPW global horizontal radiation, converted from
  Wh/m2 to kWh/m2;
- north/east/south/west = monthly totals from
  `ladybug.wea.Wea.directional_irradiance()` for vertical unobstructed planes
  at azimuths 0/90/180/270 degrees;
- `ground_reflectance` and `diffuse_model` are explicit arguments, validated,
  and recorded in provenance;
- v1 supports Ladybug's isotropic and anisotropic directional modes only; no
  shading or site-obstruction model is implied.

### Peak-load data

EPW annual/design-condition values do not become PHI/Phius peak-load sets.
`Climate.peak_loads` is `None`, provenance states
`peak_load_data_available=False`, and peak-load readiness fails with a message
that approved/specialized load climate data must be supplied separately.

## Validation and errors

- Reject a missing/unreadable file, malformed EPW, non-annual/incomplete hourly
  series, missing required monthly fields, non-finite values, and impossible
  location/time-zone ranges.
- Accumulate independent data-quality issues where possible; do not make the
  user repair one field at a time.
- Errors name the EPW path, field, month/depth where applicable, and observed
  value/cardinality.
- Two conversions of the same EPW return independent object graphs and the
  same source checksum/method metadata.

## Non-goals

- Certification climate generation or approval.
- PHPP/Phius heating/cooling load dataset generation.
- Weather-file downloading, catalog search, or redistribution.
- Future-weather morphing, climate-change scenarios, or interpolation between
  stations.
- Replacing PHI/Phius climate identifiers with a synthetic look-alike.

## Acceptance criteria

- A user-supplied EPW produces location plus all required monthly temperature
  and N/E/S/W/global radiation values with documented units/methods.
- Provenance and availability survive duplicate and HBJSON round-trips.
- No PHI/Phius identifier is written and no weather file is packaged.
- Missing ground data and all peak-load requests fail explicitly.
- Monthly-demand readiness passes only when every required derived field is
  present and finite.
- Repeated conversions are independent.
- IronPython-safe syntax, focused coverage for the new behavior, docs/nav
  updates, and full pytest at or above the 75% repository coverage floor.
