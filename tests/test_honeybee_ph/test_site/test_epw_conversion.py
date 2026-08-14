import hashlib

import pytest
from ladybug.skymodel import calc_horizontal_infrared, calc_sky_temperature

from honeybee_ph._epw import convert_epw
from tests.test_honeybee_ph.test_site.epw_fixture import write_synthetic_epw


def test_epw_location_temperature_scalars_and_provenance(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "controlled.epw")

    result = convert_epw(str(epw_path))

    assert result.issues == []
    assert result.location_name == "Synthetic Test City"
    assert result.latitude == 42.25
    assert result.longitude == -73.35
    assert result.elevation == 321.0
    assert result.utc_offset == -5.0
    assert result.monthly_air_temperatures == pytest.approx(list(range(1, 13)))
    assert result.monthly_dewpoint_temperatures == pytest.approx(list(range(-4, 8)))
    assert result.monthly_sky_temperatures == pytest.approx([calc_sky_temperature(300.0)] * 12)
    assert result.average_wind_speed == pytest.approx(3.0)
    assert result.summer_daily_temperature_swing == pytest.approx(4.0)
    assert result.source_checksum == hashlib.sha256(epw_path.read_bytes()).hexdigest()
    assert result.provenance.source_checksum == result.source_checksum
    assert result.provenance.source_type == "epw_derived"
    assert result.provenance.source_uri == str(epw_path)
    assert result.provenance.conversion_method == "ladybug_epw_preliminary_monthly"
    assert result.provenance.conversion_method_version == "1"
    assert result.provenance.is_certification_approved is False
    assert result.provenance.assumptions["summer_daily_temperature_swing"] == (
        "mean daily dry-bulb range over the warmest three consecutive calendar months"
    )


def test_southern_warm_season_wraps_across_year_end(tmp_path):
    monthly_means = [30.0, 29.0, 5.0, 4.0, 3.0, 2.0, 1.0, 2.0, 3.0, 4.0, 5.0, 28.0]
    daily_ranges = [2.0, 4.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 12.0]
    epw_path = write_synthetic_epw(
        tmp_path / "southern.epw",
        monthly_means=monthly_means,
        daily_ranges=daily_ranges,
    )

    result = convert_epw(str(epw_path))

    expected = ((31 * 2.0) + (28 * 4.0) + (31 * 12.0)) / 90.0
    assert result.issues == []
    assert result.summer_daily_temperature_swing == pytest.approx(expected)
    assert result.provenance.assumptions["warmest_consecutive_months"] == [12, 1, 2]


def test_leap_year_is_accepted_as_complete_annual_series(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "leap.epw", is_leap_year=True)

    result = convert_epw(str(epw_path))

    assert result.issues == []
    assert len(result.monthly_air_temperatures) == 12


def test_partial_year_reports_hourly_cardinality(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "partial.epw")
    lines = epw_path.read_text().splitlines()
    epw_path.write_text("\n".join(lines[:-1]) + "\n")

    result = convert_epw(str(epw_path))

    assert result.issues == [
        "{}: hourly_data: expected 8760 hourly rows for a non-leap year; got 8759.".format(epw_path)
    ]


def test_malformed_epw_and_missing_path_return_targeted_issues(tmp_path):
    malformed = tmp_path / "malformed.epw"
    malformed.write_text("not an EPW\n")
    missing = tmp_path / "missing.epw"

    malformed_result = convert_epw(str(malformed))
    missing_result = convert_epw(str(missing))

    assert malformed_result.issues == [
        "{}: header: expected at least 8 EPW header lines and hourly data; got 1 total lines.".format(malformed)
    ]
    assert missing_result.issues[0].startswith("{}: file: unable to read EPW".format(missing))


def test_non_utf8_epw_returns_targeted_issue(tmp_path):
    epw_path = tmp_path / "binary.epw"
    epw_path.write_bytes(b"\xff\xfe\x00\x80")

    result = convert_epw(str(epw_path))

    assert result.issues[0].startswith("{}: file: EPW is not valid UTF-8 text".format(epw_path))


def test_invalid_location_header_and_leap_flag_are_targeted(tmp_path):
    bad_location = write_synthetic_epw(tmp_path / "bad-location-header.epw")
    lines = bad_location.read_text().splitlines()
    lines[0] = "NOT-LOCATION"
    bad_location.write_text("\n".join(lines) + "\n")

    bad_leap = write_synthetic_epw(tmp_path / "bad-leap.epw")
    lines = bad_leap.read_text().splitlines()
    leap_header = lines[4].split(",")
    leap_header[1] = "Maybe"
    lines[4] = ",".join(leap_header)
    bad_leap.write_text("\n".join(lines) + "\n")

    assert convert_epw(str(bad_location)).issues == [
        "{}: location: expected a 10-field EPW LOCATION header.".format(bad_location)
    ]
    assert convert_epw(str(bad_leap)).issues == [
        "{}: header.is_leap_year: expected 'Yes' or 'No'; observed 'Maybe'.".format(bad_leap)
    ]


def test_non_numeric_location_value_is_targeted(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "non-numeric-location.epw")
    lines = epw_path.read_text().splitlines()
    location = lines[0].split(",")
    location[6] = "north"
    lines[0] = ",".join(location)
    epw_path.write_text("\n".join(lines) + "\n")

    result = convert_epw(str(epw_path))

    assert result.issues == ["{}: location.latitude: expected a finite number; observed 'north'.".format(epw_path)]


def test_missing_and_non_finite_fields_accumulate_without_zero_fallback(tmp_path):
    epw_path = write_synthetic_epw(
        tmp_path / "invalid-values.epw",
        field_overrides={
            "dry_bulb_temperature": {0: 99.9},
            "dew_point_temperature": {1: float("nan")},
            "wind_speed": {2: float("inf")},
        },
    )

    result = convert_epw(str(epw_path))

    assert len(result.issues) == 3
    assert "dry_bulb_temperature hour 1" in result.issues[0]
    assert "missing sentinel 99.9" in result.issues[0]
    assert "dew_point_temperature hour 2" in result.issues[1]
    assert "observed nan" in result.issues[1]
    assert "wind_speed hour 3" in result.issues[2]
    assert "observed inf" in result.issues[2]
    assert result.monthly_air_temperatures is None
    assert result.monthly_dewpoint_temperatures is None
    assert result.average_wind_speed is None


def test_bad_location_fields_accumulate_before_ladybug_parse(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "bad-location.epw")
    lines = epw_path.read_text().splitlines()
    location = lines[0].split(",")
    location[6:10] = ["91", "181", "15", "nan"]
    lines[0] = ",".join(location)
    epw_path.write_text("\n".join(lines) + "\n")

    result = convert_epw(str(epw_path))

    assert len(result.issues) == 4
    assert "location.latitude" in result.issues[0]
    assert "location.longitude" in result.issues[1]
    assert "location.utc_offset" in result.issues[2]
    assert "location.elevation" in result.issues[3]


def test_out_of_range_hourly_values_accumulate(tmp_path):
    epw_path = write_synthetic_epw(
        tmp_path / "out-of-range.epw",
        field_overrides={
            "dry_bulb_temperature": {0: -71.0},
            "dew_point_temperature": {1: 71.0},
            "wind_speed": {2: 41.0},
        },
    )

    result = convert_epw(str(epw_path))

    assert len(result.issues) == 3
    assert "expected -70.0 through 70.0; observed -71.0" in result.issues[0]
    assert "expected -70.0 through 70.0; observed 71.0" in result.issues[1]
    assert "expected 0.0 through 40.0; observed 41.0" in result.issues[2]


@pytest.mark.parametrize(
    "horizontal_ir, opaque_sky, expected_field",
    [
        (float("nan"), 5, "horizontal_infrared_radiation_intensity"),
        (float("inf"), 5, "horizontal_infrared_radiation_intensity"),
        (-1.0, 5, "horizontal_infrared_radiation_intensity"),
        (None, 99, "opaque_sky_cover"),
    ],
)
def test_invalid_sky_source_values_are_targeted(tmp_path, horizontal_ir, opaque_sky, expected_field):
    epw_path = write_synthetic_epw(
        tmp_path / "invalid-sky.epw",
        horizontal_infrared=horizontal_ir,
        opaque_sky_cover=opaque_sky,
    )

    result = convert_epw(str(epw_path))

    assert result.monthly_sky_temperatures is None
    assert expected_field in result.issues[0]


def test_missing_horizontal_ir_cannot_fallback_from_invalid_temperature(tmp_path):
    epw_path = write_synthetic_epw(
        tmp_path / "fallback-missing-source.epw",
        horizontal_infrared=None,
        field_overrides={"dry_bulb_temperature": {0: 99.9}},
    )

    result = convert_epw(str(epw_path))

    assert len(result.issues) == 1
    assert "dry_bulb_temperature hour 1" in result.issues[0]
    assert result.monthly_sky_temperatures is None


def test_ladybug_parse_error_is_returned_as_issue(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "parse-error.epw")
    lines = epw_path.read_text().splitlines()
    first_hour = lines[8].split(",")
    first_hour[6] = "not-a-temperature"
    lines[8] = ",".join(first_hour)
    epw_path.write_text("\n".join(lines) + "\n")

    result = convert_epw(str(epw_path))

    assert len(result.issues) == 1
    assert "epw: Ladybug failed to parse the file" in result.issues[0]


@pytest.mark.parametrize("first_hour", ["too,few,fields", None])
def test_horizontal_ir_preflight_defers_structural_errors_to_ladybug(tmp_path, first_hour):
    epw_path = write_synthetic_epw(tmp_path / "structural-error.epw")
    lines = epw_path.read_text().splitlines()
    if first_hour is None:
        fields = lines[8].split(",")
        fields[12] = "not-infrared"
        lines[8] = ",".join(fields)
    else:
        lines[8] = first_hour
    epw_path.write_text("\n".join(lines) + "\n")

    result = convert_epw(str(epw_path))

    assert len(result.issues) == 1
    assert "epw: Ladybug failed to parse the file" in result.issues[0]


def test_sky_temperature_uses_ladybug_horizontal_infrared_fallback(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "sky-fallback.epw", horizontal_infrared=None)

    result = convert_epw(str(epw_path))

    cold_sky = calc_sky_temperature(calc_horizontal_infrared(5, -1.0, -6.0))
    warm_sky = calc_sky_temperature(calc_horizontal_infrared(5, 3.0, -2.0))
    expected_sky = (cold_sky + warm_sky) / 2.0
    assert result.issues == []
    assert result.monthly_sky_temperatures[0] == pytest.approx(expected_sky)
    assert result.provenance.assumptions["sky_temperature"] == (
        "ladybug EPW.sky_temperature with horizontal-infrared fallback from opaque sky cover"
    )


def test_checksum_and_conversion_metadata_are_deterministic(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "deterministic.epw")

    first = convert_epw(str(epw_path))
    second = convert_epw(str(epw_path))

    assert first.source_checksum == second.source_checksum
    assert first.provenance.conversion_method == second.provenance.conversion_method
    assert first.provenance.conversion_method_version == second.provenance.conversion_method_version
    assert first.monthly_air_temperatures == second.monthly_air_temperatures
