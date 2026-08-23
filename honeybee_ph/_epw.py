# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Internal conversion of caller-supplied EPW weather data."""

import hashlib
import os

try:
    from typing import Any, Dict, List, Optional, Tuple
except ImportError:  # pragma: no cover - IronPython 2.7
    pass

from ladybug.epw import EPW
from ladybug.skymodel import calc_horizontal_infrared
from ladybug.wea import Wea

from honeybee_ph.site import Climate_MonthlyValueSet, ClimateProvenance
from honeybee_ph_utils.validation import is_finite_real as _is_finite_real


class EPWConversionResult(object):
    """Internal values and accumulated issues from an EPW conversion."""

    def __init__(self, file_path):
        # type: (str) -> None
        self.file_path = file_path
        self.location_name = None  # type: Optional[str]
        self.latitude = None  # type: Optional[float]
        self.longitude = None  # type: Optional[float]
        self.elevation = None  # type: Optional[float]
        self.utc_offset = None  # type: Optional[float]
        self.monthly_air_temperatures = None  # type: Optional[List[float]]
        self.monthly_dewpoint_temperatures = None  # type: Optional[List[float]]
        self.monthly_sky_temperatures = None  # type: Optional[List[float]]
        self.monthly_ground_temperatures = None  # type: Optional[List[float]]
        self.ground_temperature_depth = None  # type: Optional[float]
        self.monthly_north_radiation = None  # type: Optional[List[float]]
        self.monthly_east_radiation = None  # type: Optional[List[float]]
        self.monthly_south_radiation = None  # type: Optional[List[float]]
        self.monthly_west_radiation = None  # type: Optional[List[float]]
        self.monthly_global_radiation = None  # type: Optional[List[float]]
        self.average_wind_speed = None  # type: Optional[float]
        self.summer_daily_temperature_swing = None  # type: Optional[float]
        self.issues = []  # type: List[str]
        self.provenance = ClimateProvenance(
            source_type="epw_derived",
            source_uri=file_path,
            conversion_method="ladybug_epw_preliminary_monthly",
            conversion_method_version="1",
            is_certification_approved=False,
            monthly_data_available=False,
            peak_load_data_available=False,
            assumptions={
                "summer_daily_temperature_swing": (
                    "mean daily dry-bulb range over the warmest three consecutive calendar months"
                ),
                "sky_temperature": (
                    "ladybug EPW.sky_temperature with horizontal-infrared fallback from opaque sky cover"
                ),
            },
        )

    @property
    def source_checksum(self):
        # type: () -> Optional[str]
        """SHA-256 checksum for the exact EPW snapshot used by Ladybug."""
        return self.provenance.source_checksum


def _issue(file_path, field_name, message):
    # type: (str, str, str) -> str
    return "{}: {}: {}".format(file_path, field_name, message)


def _read_source(result):
    # type: (EPWConversionResult) -> Optional[str]
    try:
        with open(result.file_path, "rb") as epw_file:
            source = epw_file.read()
    except (IOError, OSError) as error:
        result.issues.append(_issue(result.file_path, "file", "unable to read EPW ({})".format(error)))
        return None

    result.provenance.source_checksum = hashlib.sha256(source).hexdigest()
    try:
        text = source.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        result.issues.append(_issue(result.file_path, "file", "EPW is not valid UTF-8 text ({})".format(error)))
        return None
    return text


def _header_float_issue(file_path, field_name, raw_value, minimum=None, maximum=None):
    # type: (str, str, str, Optional[float], Optional[float]) -> Tuple[Optional[float], Optional[str]]
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return None, _issue(file_path, field_name, "expected a finite number; observed {!r}.".format(raw_value))
    if not _is_finite_real(value):
        return None, _issue(file_path, field_name, "expected a finite number; observed {!r}.".format(raw_value))
    if (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        return None, _issue(
            file_path,
            field_name,
            "expected a value from {} through {}; observed {!r}.".format(minimum, maximum, raw_value),
        )
    return value, None


def _validate_header(result, lines):
    # type: (EPWConversionResult, List[str]) -> bool
    if len(lines) < 9:
        result.issues.append(
            _issue(
                result.file_path,
                "header",
                "expected at least 8 EPW header lines and hourly data; got {} total lines.".format(len(lines)),
            )
        )
        return False

    location_fields = lines[0].split(",")
    if len(location_fields) < 10 or location_fields[0].strip().upper() != "LOCATION":
        result.issues.append(_issue(result.file_path, "location", "expected a 10-field EPW LOCATION header."))
        return False

    location_values = (
        ("location.latitude", location_fields[6], -90.0, 90.0),
        ("location.longitude", location_fields[7], -180.0, 180.0),
        ("location.utc_offset", location_fields[8], -12.0, 14.0),
        ("location.elevation", location_fields[9], -1000.0, 10000.0),
    )
    issue_count = len(result.issues)
    for field_name, raw_value, minimum, maximum in location_values:
        _, issue = _header_float_issue(result.file_path, field_name, raw_value, minimum, maximum)
        if issue:
            result.issues.append(issue)
    if len(result.issues) != issue_count:
        return False

    leap_fields = lines[4].split(",")
    leap_value = leap_fields[1].strip() if len(leap_fields) > 1 else ""
    if leap_value not in ("Yes", "No"):
        result.issues.append(
            _issue(result.file_path, "header.is_leap_year", "expected 'Yes' or 'No'; observed {!r}.".format(leap_value))
        )
        return False
    expected_hours = 8784 if leap_value == "Yes" else 8760
    observed_hours = len([line for line in lines[8:] if line.strip()])
    if observed_hours != expected_hours:
        year_type = "leap" if leap_value == "Yes" else "non-leap"
        result.issues.append(
            _issue(
                result.file_path,
                "hourly_data",
                "expected {} hourly rows for a {} year; got {}.".format(expected_hours, year_type, observed_hours),
            )
        )
        return False
    return True


def _preflight_integer_fields(result, lines):
    # type: (EPWConversionResult, List[str]) -> bool
    issue_count = len(result.issues)
    integer_fields = (
        (12, "horizontal_infrared_radiation_intensity"),
        (13, "global_horizontal_radiation"),
        (14, "direct_normal_radiation"),
        (15, "diffuse_horizontal_radiation"),
    )
    for index, line in enumerate(lines[8:]):
        fields = line.split(",")
        for field_index, field_name in integer_fields:
            if len(fields) <= field_index:
                continue
            try:
                value = float(fields[field_index])
            except ValueError:
                continue
            if not _is_finite_real(value):
                result.issues.append(
                    _issue(
                        result.file_path,
                        "{} hour {}".format(field_name, index + 1),
                        "observed {!r}.".format(value),
                    )
                )
    return len(result.issues) == issue_count


def _validate_options(result, ground_temperature_depth, ground_reflectance, diffuse_model):
    # type: (EPWConversionResult, Optional[float], float, str) -> None
    if not _is_finite_real(ground_reflectance) or not 0 <= ground_reflectance <= 1:
        result.issues.append(
            _issue(
                result.file_path,
                "ground_reflectance",
                "expected a finite value from 0 through 1; observed {!r}.".format(ground_reflectance),
            )
        )
    else:
        result.provenance.assumptions["ground_reflectance"] = ground_reflectance
    if diffuse_model not in ("isotropic", "anisotropic"):
        result.issues.append(
            _issue(
                result.file_path,
                "diffuse_model",
                "expected 'isotropic' or 'anisotropic'; observed {!r}.".format(diffuse_model),
            )
        )
    else:
        result.provenance.assumptions["diffuse_model"] = diffuse_model
    if ground_temperature_depth is not None and (
        not _is_finite_real(ground_temperature_depth) or ground_temperature_depth < 0
    ):
        result.issues.append(
            _issue(
                result.file_path,
                "ground_temperature_depth",
                "expected None or a finite non-negative depth in meters; observed {!r}.".format(
                    ground_temperature_depth
                ),
            )
        )


def _validated_series(file_path, field_name, values, missing_value, minimum, maximum):
    # type: (str, str, List[float], float, float, float) -> Tuple[Optional[List[float]], List[str]]
    issues = []
    for index, value in enumerate(values):
        hour = index + 1
        if not _is_finite_real(value):
            issues.append(_issue(file_path, "{} hour {}".format(field_name, hour), "observed {!r}.".format(value)))
        elif value == missing_value:
            issues.append(
                _issue(
                    file_path,
                    "{} hour {}".format(field_name, hour),
                    "observed missing sentinel {!r}.".format(missing_value),
                )
            )
        elif value < minimum or value > maximum:
            issues.append(
                _issue(
                    file_path,
                    "{} hour {}".format(field_name, hour),
                    "expected {} through {}; observed {!r}.".format(minimum, maximum, value),
                )
            )
    return (None if issues else values), issues


def _monthly_sums_and_counts(collection):
    # type: (Any) -> Tuple[List[float], List[int]]
    monthly_sums = [0.0] * 12
    monthly_counts = [0] * 12
    for value, dt in zip(collection.values, collection.datetimes):
        month_index = dt.month - 1
        monthly_sums[month_index] += value
        monthly_counts[month_index] += 1
    return monthly_sums, monthly_counts


def _monthly_means(collection):
    # type: (Any) -> List[float]
    monthly_sums, monthly_counts = _monthly_sums_and_counts(collection)
    return [total / count for total, count in zip(monthly_sums, monthly_counts)]


def _monthly_totals_kwh(collection):
    # type: (Any) -> List[float]
    monthly_sums, _ = _monthly_sums_and_counts(collection)
    return [total / 1000.0 for total in monthly_sums]


def _summer_daily_swing(values, datetimes, monthly_means):
    # type: (List[float], List[Any], List[float]) -> Tuple[float, List[int]]
    start_month = max(
        range(12),
        key=lambda index: sum(monthly_means[(index + offset) % 12] for offset in range(3)),
    )
    warmest_months = [((start_month + offset) % 12) + 1 for offset in range(3)]
    daily_values = {}  # type: Dict[Tuple[int, int], List[float]]
    for value, dt in zip(values, datetimes):
        if dt.month in warmest_months:
            daily_values.setdefault((dt.month, dt.day), []).append(value)
    daily_ranges = [max(day_values) - min(day_values) for day_values in daily_values.values()]
    return sum(daily_ranges) / len(daily_ranges), warmest_months


def _resolved_horizontal_infrared(result, epw, dry_bulb, dewpoint):
    # type: (EPWConversionResult, EPW, Optional[List[float]], Optional[List[float]]) -> Optional[List[float]]
    horizontal_ir = list(epw.horizontal_infrared_radiation_intensity.values)
    opaque_sky = list(epw.opaque_sky_cover.values)
    resolved = []
    issues = []
    for index, value in enumerate(horizontal_ir):
        if value >= 9999:
            sky_cover = opaque_sky[index]
            if dry_bulb is None or dewpoint is None:
                continue
            if not _is_finite_real(sky_cover) or sky_cover < 0 or sky_cover > 10:
                issues.append(
                    _issue(
                        result.file_path,
                        "opaque_sky_cover hour {}".format(index + 1),
                        "required for horizontal-infrared fallback; observed {!r}.".format(sky_cover),
                    )
                )
            else:
                resolved.append(calc_horizontal_infrared(sky_cover, dry_bulb[index], dewpoint[index]))
        elif value < 0:
            issues.append(
                _issue(
                    result.file_path,
                    "horizontal_infrared_radiation_intensity hour {}".format(index + 1),
                    "expected a non-negative value; observed {!r}.".format(value),
                )
            )
        else:
            resolved.append(value)
    result.issues.extend(issues)
    return None if issues or len(resolved) != len(horizontal_ir) else resolved


def _select_ground_temperature(result, epw, requested_depth):
    # type: (EPWConversionResult, EPW, Optional[float]) -> None
    ground_series = epw.monthly_ground_temperature
    available_depths = sorted(ground_series.keys())
    if not available_depths:
        result.issues.append(
            _issue(result.file_path, "ground_temperature", "EPW header contains no monthly ground-temperature series.")
        )
        return
    if requested_depth is None:
        if len(available_depths) != 1:
            result.issues.append(
                _issue(
                    result.file_path,
                    "ground_temperature_depth",
                    "EPW header has multiple series; choose one of {} m.".format(available_depths),
                )
            )
            return
        selected_depth = available_depths[0]
    elif requested_depth not in ground_series:
        result.issues.append(
            _issue(
                result.file_path,
                "ground_temperature_depth",
                "requested {} m; available depths are {} m.".format(requested_depth, available_depths),
            )
        )
        return
    else:
        selected_depth = requested_depth

    values = list(ground_series[selected_depth].values)
    if len(values) != 12:
        result.issues.append(
            _issue(
                result.file_path,
                "ground_temperature depth {} m".format(selected_depth),
                "expected 12 monthly values; got {}.".format(len(values)),
            )
        )
        return
    ground_issues = []
    for month_name, value in zip(Climate_MonthlyValueSet.months, values):
        if not _is_finite_real(value) or value < -70 or value > 70:
            ground_issues.append(
                _issue(
                    result.file_path,
                    "ground_temperature depth {} m {}".format(selected_depth, month_name),
                    "expected a finite value from -70 through 70 C; observed {!r}.".format(value),
                )
            )
    result.issues.extend(ground_issues)
    if not ground_issues:
        result.ground_temperature_depth = selected_depth
        result.monthly_ground_temperatures = values
        result.provenance.assumptions["ground_temperature_depth_m"] = selected_depth


def _set_directional_radiation(result, epw, direct_normal, diffuse_horizontal, ground_reflectance, diffuse_model):
    # type: (EPWConversionResult, EPW, Optional[List[float]], Optional[List[float]], float, str) -> None
    if direct_normal is None or diffuse_horizontal is None:
        return
    wea = Wea(epw.location, epw.direct_normal_radiation, epw.diffuse_horizontal_radiation)
    isotropic = diffuse_model == "isotropic"
    orientations = (
        ("north", "monthly_north_radiation", 0),
        ("east", "monthly_east_radiation", 90),
        ("south", "monthly_south_radiation", 180),
        ("west", "monthly_west_radiation", 270),
    )
    for _, field_name, azimuth in orientations:
        total_irradiance = wea.directional_irradiance(
            altitude=0,
            azimuth=azimuth,
            ground_reflectance=ground_reflectance,
            isotropic=isotropic,
        )[0]
        setattr(result, field_name, _monthly_totals_kwh(total_irradiance))
    result.provenance.assumptions["vertical_plane_azimuths_degrees"] = {
        name: azimuth for name, _, azimuth in orientations
    }


def convert_epw(file_path, ground_temperature_depth=None, ground_reflectance=0.2, diffuse_model="isotropic"):
    # type: (str, Optional[float], float, str) -> EPWConversionResult
    """Convert EPW monthly-demand fields into an internal result."""
    path = os.path.abspath(str(file_path))
    result = EPWConversionResult(path)
    _validate_options(result, ground_temperature_depth, ground_reflectance, diffuse_model)
    if result.issues:
        return result
    source_text = _read_source(result)
    if source_text is None:
        return result
    lines = source_text.splitlines()
    if not _validate_header(result, lines):
        return result
    if not _preflight_integer_fields(result, lines):
        return result

    try:
        epw = EPW.from_file_string(source_text if source_text.endswith("\n") else source_text + "\n")
        location = epw.location
        dry_collection = epw.dry_bulb_temperature
        dewpoint_collection = epw.dew_point_temperature
        wind_collection = epw.wind_speed
        global_collection = epw.global_horizontal_radiation
        direct_collection = epw.direct_normal_radiation
        diffuse_collection = epw.diffuse_horizontal_radiation
    except Exception as error:
        result.issues.append(_issue(path, "epw", "Ladybug failed to parse the file ({})".format(error)))
        return result

    result.location_name = location.city
    result.latitude = location.latitude
    result.longitude = location.longitude
    result.elevation = location.elevation
    result.utc_offset = location.time_zone
    result.provenance.source_name = location.city

    dry_bulb, dry_issues = _validated_series(
        path, "dry_bulb_temperature", list(dry_collection.values), 99.9, -70.0, 70.0
    )
    dewpoint, dewpoint_issues = _validated_series(
        path, "dew_point_temperature", list(dewpoint_collection.values), 99.9, -70.0, 70.0
    )
    wind_speed, wind_issues = _validated_series(path, "wind_speed", list(wind_collection.values), 999, 0.0, 40.0)
    global_horizontal, global_issues = _validated_series(
        path, "global_horizontal_radiation", list(global_collection.values), 9999, 0.0, 9998.0
    )
    direct_normal, direct_issues = _validated_series(
        path, "direct_normal_radiation", list(direct_collection.values), 9999, 0.0, 9998.0
    )
    diffuse_horizontal, diffuse_issues = _validated_series(
        path, "diffuse_horizontal_radiation", list(diffuse_collection.values), 9999, 0.0, 9998.0
    )
    result.issues.extend(dry_issues)
    result.issues.extend(dewpoint_issues)
    result.issues.extend(wind_issues)
    result.issues.extend(global_issues)
    result.issues.extend(direct_issues)
    result.issues.extend(diffuse_issues)

    if dry_bulb is not None:
        result.monthly_air_temperatures = _monthly_means(dry_collection)
        result.summer_daily_temperature_swing, warmest_months = _summer_daily_swing(
            dry_bulb, list(dry_collection.datetimes), result.monthly_air_temperatures
        )
        result.provenance.assumptions["warmest_consecutive_months"] = warmest_months
    if dewpoint is not None:
        result.monthly_dewpoint_temperatures = _monthly_means(dewpoint_collection)
    if wind_speed is not None:
        result.average_wind_speed = wind_collection.average
    if global_horizontal is not None:
        result.monthly_global_radiation = _monthly_totals_kwh(global_collection)

    horizontal_ir = _resolved_horizontal_infrared(result, epw, dry_bulb, dewpoint)
    if horizontal_ir is not None:
        epw.horizontal_infrared_radiation_intensity.values = horizontal_ir
        result.monthly_sky_temperatures = _monthly_means(epw.sky_temperature)
    _set_directional_radiation(
        result,
        epw,
        direct_normal,
        diffuse_horizontal,
        ground_reflectance,
        diffuse_model,
    )
    _select_ground_temperature(result, epw, ground_temperature_depth)
    required_monthly_values = (
        result.monthly_air_temperatures,
        result.monthly_dewpoint_temperatures,
        result.monthly_sky_temperatures,
        result.monthly_ground_temperatures,
        result.monthly_north_radiation,
        result.monthly_east_radiation,
        result.monthly_south_radiation,
        result.monthly_west_radiation,
        result.monthly_global_radiation,
    )
    result.provenance.monthly_data_available = not result.issues and all(
        values is not None for values in required_monthly_values
    )
    return result
