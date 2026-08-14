# 0004 — Do Not Bundle Licensed PHI/Phius Climate Data

**Date:** 2026-08-14
**Status:** DECIDED — bundled dataset library will not be implemented
**Decider:** Ed May
**Research:** [`planning/archive/climate-dataset-library/`](../../planning/archive/climate-dataset-library/README.md)
**Replacement:** [`planning/features/epw-derived-preliminary-climate/`](../../planning/features/epw-derived-preliminary-climate/README.md)

## Context

The ph-modeler POC showed that `Site()` carries a New York identity while its
monthly climate values are all zero. The first proposed remedy was to package
real PHPP climate datasets in honeybee-ph and expose
`Site.from_dataset("US0055c-New York")`.

That would copy certification datasets into a public GPL package. PHI provides
PHPP climate-data updates through licensed PHPP access and requires
PHI-approved climate datasets for certification. Phius climate datasets are
likewise supplied through membership/project access, with custom datasets sold
as a service. Purchase or authorized access does not itself grant public
redistribution rights.

EPW is an open weather-file format, but the data inside an EPW can come from
sources with different licenses. A safe library boundary is therefore to
process a file supplied by the caller, preserve its provenance, and never
bundle or automatically redistribute weather data.

PHI also distinguishes monthly temperature/radiation data used for energy
demand from the specialized heating/cooling load dataset. A simple EPW monthly
aggregation is not a substitute for PHI/Phius-approved load data.

## Decision

1. **Do not ship PHI/Phius climate datasets in honeybee-ph** unless the data
   owner supplies an explicit redistribution grant compatible with this public
   package.
2. Supersede the `climate-dataset-library` feature. Do not implement
   `available_datasets()` or a name-based resolver backed by copied PHI/Phius
   values.
3. Implement a separate, source-neutral converter for a **user-supplied EPW**.
   It may derive preliminary monthly demand climate data, but it must:
   - retain source/method/checksum provenance;
   - identify itself as `epw_derived` and not certification-approved;
   - avoid assigning a PHI/Phius dataset identifier;
   - leave peak-load data explicitly unavailable unless supplied through a
     separately authorized source and method;
   - perform no network download and bundle no EPW files.
4. Treat the EPW format separately from the source-data license. Callers are
   responsible for having the right to process their input file.

## Rationale

- Avoids redistributing paid or access-controlled certification IP.
- Keeps honeybee-ph a data-model/conversion library rather than an unofficial
  mirror of certification datasets.
- Provides a useful preliminary-design path for scripts and web applications
  without falsely claiming PHI/Phius equivalence.
- Makes missing peak-load data visible instead of converting absence to a
  plausible-looking zero.

## What would reopen this

- PHI or Phius publishes a dataset under explicit terms permitting public
  redistribution in this package.
- BLDGTYP obtains a written redistribution license covering named datasets and
  derived package distribution.

Either event would justify a new decision and feature packet. It would not
silently reactivate the archived proposal.

## References

- PHI PHPP licensing and access: https://shop.passivehouse.com/en/products/phpp-10-129/
- PHI certification climate criteria: https://passivehouse.com/downloads/03_building_criteria_en.pdf
- iPHA climate-data FAQ: https://www.passivehouse-international.org/index.php?page_id=290
- Phius climate data: https://www.phius.org/climate-data
- EnergyPlus weather-source documentation: https://energyplus.net/assets/nrel_custom/pdfs/pdfs_v24.1.0/AuxiliaryPrograms.pdf
