"""Synthetic EPW generation for tests.

The fixture contains no copied weather observations or certification climate
data. Every hourly value is generated from controlled constants and calendar
month/day/hour indices within the test run.
"""

from ladybug.epw import EPW
from ladybug.location import Location


def write_synthetic_epw(
    file_path,
    monthly_means=None,
    daily_ranges=None,
    wind_speed=3.0,
    horizontal_infrared=300.0,
    opaque_sky_cover=5,
    is_leap_year=False,
    field_overrides=None,
):
    monthly_means = [float(month) for month in range(1, 13)] if monthly_means is None else monthly_means
    daily_ranges = [4.0] * 12 if daily_ranges is None else daily_ranges
    field_overrides = {} if field_overrides is None else field_overrides

    epw = EPW.from_missing_values(is_leap_year=is_leap_year)
    epw.location = Location(
        city="Synthetic Test City",
        state="TS",
        country="Synthetic",
        latitude=42.25,
        longitude=-73.35,
        time_zone=-5.0,
        elevation=321.0,
        station_id="SYNTHETIC-001",
        source="Generated test data",
    )

    dry_bulb = []
    dewpoint = []
    for dt in epw.dry_bulb_temperature.datetimes:
        mean = monthly_means[dt.month - 1]
        half_range = daily_ranges[dt.month - 1] / 2.0
        offset = -half_range if dt.hour < 12 else half_range
        dry_bulb.append(mean + offset)
        dewpoint.append(mean - 5.0 + offset)

    length = len(dry_bulb)
    epw.dry_bulb_temperature.values = dry_bulb
    epw.dew_point_temperature.values = dewpoint
    epw.wind_speed.values = [wind_speed] * length
    epw.horizontal_infrared_radiation_intensity.values = [
        9999 if horizontal_infrared is None else horizontal_infrared
    ] * length
    epw.opaque_sky_cover.values = [opaque_sky_cover] * length
    epw.global_horizontal_radiation.values = [100.0] * length
    epw.direct_normal_radiation.values = [50.0] * length
    epw.diffuse_horizontal_radiation.values = [50.0] * length

    fields = {
        "dry_bulb_temperature": epw.dry_bulb_temperature,
        "dew_point_temperature": epw.dew_point_temperature,
        "wind_speed": epw.wind_speed,
        "horizontal_infrared_radiation_intensity": epw.horizontal_infrared_radiation_intensity,
        "opaque_sky_cover": epw.opaque_sky_cover,
        "global_horizontal_radiation": epw.global_horizontal_radiation,
        "direct_normal_radiation": epw.direct_normal_radiation,
        "diffuse_horizontal_radiation": epw.diffuse_horizontal_radiation,
    }
    for field_name, overrides in field_overrides.items():
        values = list(fields[field_name].values)
        for index, value in overrides.items():
            values[index] = value
        fields[field_name].values = values

    epw.write(str(file_path))
    return file_path
