---
title: EPW preliminary climate
---

# EPW-derived preliminary climate

`Site.from_epw()` converts a caller-supplied annual EPW file into preliminary
monthly-demand climate inputs. It reads only the supplied local file; it does
not search for, download, cache, or redistribute weather data.

```python
from honeybee_ph.site import Site

site = Site.from_epw(
    "/path/to/weather.epw",
    ground_temperature_depth=0.5,
    ground_reflectance=0.2,
    diffuse_model="isotropic",
)
```

EPW-derived values are not PHI- or Phius-approved certification climate data.
The returned `Site` therefore has blank PHPP library codes, no peak-load
climate sets, `is_certification_approved=False`, and
`peak_load_data_available=False`. Supply approved or specialized peak-load
climate data separately when a downstream workflow requires it.

PHX conversion currently rejects this monthly-only Site before building an
export model. Its `ValueError` includes the climate-readiness issue stating
that approved or specialized peak-load climate data must be supplied
separately. Adding that data is a deliberate downstream enrichment step; the
EPW factory never fills peak inputs with zeros.

## Derived fields and units

| Output | Source / method | Unit |
|---|---|---|
| Latitude / longitude | EPW location header | decimal degrees |
| Site and station elevation | EPW location header | m |
| UTC offset | EPW location header | h |
| Air temperature | Monthly mean dry-bulb | °C |
| Dewpoint | Monthly mean dewpoint | °C |
| Sky temperature | Monthly mean Ladybug `EPW.sky_temperature` | °C |
| Ground temperature | Selected EPW monthly ground series | °C |
| Global radiation | Monthly global-horizontal total | kWh/m² |
| N/E/S/W radiation | Monthly vertical-plane total | kWh/m² |
| Average wind speed | Annual arithmetic mean | m/s |
| Summer daily swing | Mean daily dry-bulb range over the warmest three consecutive months | K |

Cardinal radiation uses unobstructed vertical planes at Ladybug azimuths
0°/90°/180°/270° for north/east/south/west. `ground_reflectance` must be from
0 through 1. `diffuse_model` is either `"isotropic"` or `"anisotropic"`.
These choices and the azimuth mapping are retained in climate provenance. No
shading or site-obstruction model is implied.

## Ground-temperature selection

Ground temperature comes only from the EPW ground-temperature header. When the
file contains one series, omitting `ground_temperature_depth` selects it. When
the file contains multiple series, pass an available depth in meters. A file
with no ground series, or a requested depth that is unavailable, raises a
targeted `ValueError`; air temperature and zero are never substituted.

## Readiness and provenance

A successful conversion sets `monthly_data_available=True`, and
`site.climate.is_monthly_demand_ready` is true only when every required scalar
and all 12 monthly values are finite. Peak-load readiness remains false.

`site.climate.provenance` records the absolute source path, SHA-256 checksum,
conversion method/version, selected ground depth, radiation assumptions, and
availability flags. Provenance survives JSON/HBJSON round-trips and
duplication. The caller remains responsible for the right to process the EPW.
