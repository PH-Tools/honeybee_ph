# PRD — Climate dataset library + `Site.from_dataset()`

**Status:** Superseded · 2026-08-14
**Author:** Ed May + Claude
**Kind:** Feature (this repo only; no cross-repo dependencies)

> **Superseded:** This proposal will not be implemented. PHI/Phius climate
> datasets are licensed or access-controlled certification data and must not be
> copied into this public package without an explicit redistribution grant.
> Replacement: [`epw-derived-preliminary-climate`](../epw-derived-preliminary-climate/README.md).

---

## WHAT

Add a small library of real PHPP climate datasets to honeybee-ph, plus a
one-line constructor that produces a fully-populated `Site`:

```python
from honeybee_ph import site

nyc = site.Site.from_dataset("US0055c-New York")
room.properties.ph.ph_bldg_segment.site = nyc
```

Behavior contract:

1. **A dataset carries its data.** `from_dataset(name)` returns a `Site` whose
   `Climate` has real values for ALL of: 12-month air / dewpoint / sky /
   ground temperatures, 12-month radiation for N/E/S/W/global, all four
   peak-load sets (temp, sky temp, dewpoint, ground temp, radiation by
   orientation), station elevation, daily temperature swing, average wind
   speed — AND a matching `Location` (lat/lon/elevation/UTC offset) and
   `PHPPCodes` (country/region/dataset strings). Every required field is
   explicitly present; a literal zero is accepted only when zero is the
   source dataset's actual value, never as a missing-data fallback.
2. **Unknown name = loud error** listing the available dataset names — never a
   silently empty Site.
3. **Data lives as data**, not code: one JSON (or similar) file per dataset,
   packaged with the library (`honeybee_ph/_climate_data/` or similar,
   included in the wheel). Adding a dataset = adding a file, no code change.
4. **Seed contents:** start with the datasets BLDGTYP actually uses — at
   minimum `US0055c-New York`. Structure so more (other NY-metro, CO,
   MA/Berkshires) can be added trivially. A
   `site.available_datasets() -> list[str]` helper accompanies it.
5. **Existing default unchanged (for now).** `Site()` with no args keeps its
   current behavior (NYC-labeled, zero data) to avoid breaking serialization
   round-trips and existing tests. The *documented* path for programmatic
   model building becomes `from_dataset`. (A follow-up may revisit the bare
   default; out of scope here.)
6. **Dataset provenance is part of the record.** Each packaged dataset names
   its source, source/version date, PHPP dataset identifier, extraction or
   transcription method, and any known licensing/distribution constraint.
   Do not copy a licensed PHPP dataset into the public wheel without confirming
   redistribution rights.
7. **Version and validate the data schema.** Dataset files carry a small schema
   version. Loading validates required keys, 12-value monthly axes, numeric
   finite values, latitude/longitude/time-zone ranges, and consistency between
   the requested name and `PHPPCodes.dataset_name`. Invalid packaged data fails
   loudly with the file and field identified.
8. **Fresh objects on every call.** Two calls for the same dataset return
   independent `Site`, `Location`, `Climate`, monthly, peak-load, ground, and
   `PHPPCodes` objects. Mutation of one result cannot affect another.

### Reference values

A ready-made NYC dataset used by the POC exists at
`~/Desktop/ph-modeler/backend/app/fixtures/nyc_climate.json` (values lifted
from the openph-workspace `US0055c-New York` fixtures and exercised against
OpenPH results). Treat it as a seed/shape reference, then verify provenance,
redistribution rights, and values against the authoritative source before
shipping it in the public package. The
honeybee-ph-internal format may differ, but must cover the same fields.

### Constraints

- Match repo style: IronPython 2.7-compatible syntax, comment-style type
  hints, `_base._Base` conventions — this module is imported inside
  Rhino/Grasshopper. Data loading must work under both IronPython and
  CPython (plain `json` + `os.path`; no `importlib.resources` niceties that
  IronPython lacks — verify).
- No new dependencies.
- pytest coverage: dataset loads, every field non-degenerate (e.g. radiation
  monthly lists length 12, finite/range checks), unknown-name error, malformed
  packaged-data error, independent repeated loads, and round-trip
  `to_dict`/`from_dict` of a dataset-built Site.

## WHY

honeybee-ph's default `Site` is **NYC in identity only**: `Location` defaults
to (40.6, -73.8) and `PHPPCodes` to `"US0055c-New York"`, but every
`Climate_MonthlyValueSet` defaults to 0.0 (`honeybee_ph/site.py`). Nothing
downstream rescues this: PHX copies the numbers verbatim
(`PHX/from_HBJSON/create_variant.py:406`) and OpenPH consumes the numbers
directly — it never resolves the dataset code against a climate library
(only the PHPP Excel workbook itself does that, via its built-in climate
database). Result: a model that *looks* like it has a NYC climate computes
garbage — zero radiation, 0 °C flat — with no error anywhere.

In Grasshopper this rarely bites because climate data arrives through GH
components. But the moment a model is built **programmatically** (the
ph-modeler web-app POC, PH-Navigator, scripts, tests), every consumer must
hand-roll the same fix: the POC needed a bespoke JSON fixture plus ~40 lines
of attribute-by-attribute plumbing (`ph-modeler/backend/app/calculation.py`,
`_build_nyc_site()`) just to make a default shoebox solvable. That cost will
be paid again by every future non-Rhino front-end unless the library carries
its own data.

Secondary benefit: a real dataset library turns the zero-data trap into a
solved problem at its source — the natural way to build a Site becomes one
that cannot be silently empty.
