import json

import pytest

from honeybee_ph.bldg_segment import BldgSegment
from honeybee_ph.properties.room import RoomPhProperties
from honeybee_ph.site import Site
from tests.test_honeybee_ph.test_site.epw_fixture import write_synthetic_epw


def test_site_from_epw_builds_complete_preliminary_monthly_climate(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "site.epw")

    site = Site.from_epw(str(epw_path))

    assert site.location.display_name == "Synthetic Test City"
    assert site.location.latitude == 42.25
    assert site.location.longitude == -73.35
    assert site.location.site_elevation == 321.0
    assert site.location.climate_zone is None
    assert site.location.hours_from_UTC == -5.0
    assert site.climate.display_name == "Synthetic Test City"
    assert site.climate.station_elevation == 321.0
    assert site.climate.monthly_temps.air_temps.values == pytest.approx(list(range(1, 13)))
    assert site.climate.monthly_temps.ground_temps.values == [10.0] * 12
    assert len(site.climate.monthly_radiation.north.values) == 12
    assert site.climate.peak_loads is None
    assert site.climate.provenance.source_type == "epw_derived"
    assert site.climate.provenance.is_certification_approved is False
    assert site.climate.is_monthly_demand_ready is True
    assert site.climate.is_peak_load_ready is False
    assert site.climate.peak_load_readiness_issues() == [
        "provenance.peak_load_data_available: approved or specialized peak-load climate data must be supplied separately."
    ]
    assert site.phpp_library_codes.country_code == ""
    assert site.phpp_library_codes.region_code == ""
    assert site.phpp_library_codes.dataset_name == ""
    assert "US0055c-New York" not in json.dumps(site.to_dict())


def test_site_from_epw_round_trip_and_duplicate_are_independent(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "round-trip.epw")
    first = Site.from_epw(str(epw_path))

    encoded = json.dumps(first.to_dict(), allow_nan=False)
    round_tripped = Site.from_dict(json.loads(encoded))
    duplicated = first.duplicate()
    second = Site.from_epw(str(epw_path))

    assert round_tripped.to_dict() == first.to_dict()
    assert duplicated.to_dict() == first.to_dict()
    assert second.climate.monthly_temps.air_temps.values == first.climate.monthly_temps.air_temps.values
    assert second.climate.monthly_radiation.north.values == first.climate.monthly_radiation.north.values
    assert second.climate.provenance.source_checksum == first.climate.provenance.source_checksum
    assert second.climate.provenance.conversion_method == first.climate.provenance.conversion_method
    for candidate in (round_tripped, duplicated, second):
        assert candidate is not first
        assert candidate.location is not first.location
        assert candidate.climate is not first.climate
        assert candidate.climate.monthly_temps is not first.climate.monthly_temps
        assert candidate.climate.monthly_temps.air_temps is not first.climate.monthly_temps.air_temps
        assert candidate.climate.monthly_radiation is not first.climate.monthly_radiation
        assert candidate.climate.monthly_radiation.north is not first.climate.monthly_radiation.north
        assert candidate.climate.ground is not first.climate.ground
        assert candidate.climate.provenance is not first.climate.provenance
        assert candidate.climate.provenance.assumptions is not first.climate.provenance.assumptions
        assert candidate.phpp_library_codes is not first.phpp_library_codes

    duplicated.climate.monthly_temps.air_temps.january = -99.0
    duplicated.climate.monthly_radiation.north.january = -99.0
    duplicated.climate.ground.ground_thermal_conductivity = -99.0
    duplicated.climate.provenance.assumptions["mutated"] = True
    assert first.climate.monthly_temps.air_temps.january == 1.0
    assert first.climate.monthly_radiation.north.january != -99.0
    assert first.climate.ground.ground_thermal_conductivity == 2
    assert "mutated" not in first.climate.provenance.assumptions


def test_site_from_epw_forwards_conversion_options(tmp_path):
    epw_path = write_synthetic_epw(
        tmp_path / "options.epw",
        ground_temperatures={0.5: [10.0] * 12, 2.0: [12.0] * 12},
    )

    site = Site.from_epw(
        str(epw_path),
        ground_temperature_depth=2.0,
        ground_reflectance=0.6,
        diffuse_model="anisotropic",
    )

    assert site.climate.monthly_temps.ground_temps.values == [12.0] * 12
    assert site.climate.provenance.assumptions["ground_temperature_depth_m"] == 2.0
    assert site.climate.provenance.assumptions["ground_reflectance"] == 0.6
    assert site.climate.provenance.assumptions["diffuse_model"] == "anisotropic"


def test_epw_site_survives_building_segment_and_room_property_paths(tmp_path):
    epw_path = write_synthetic_epw(tmp_path / "host-paths.epw")
    segment = BldgSegment()
    segment.site = Site.from_epw(str(epw_path))

    segment_round_trip = BldgSegment.from_dict(segment.to_dict())
    segment_duplicate = segment.duplicate()
    room_properties = RoomPhProperties(_host=None)
    room_properties.ph_bldg_segment = segment
    room_round_trip = RoomPhProperties.from_dict(room_properties.to_dict()["ph"], host=None)
    room_duplicate = room_properties.duplicate()

    for candidate in (
        segment_round_trip.site,
        segment_duplicate.site,
        room_round_trip.ph_bldg_segment.site,
        room_duplicate.ph_bldg_segment.site,
    ):
        assert candidate.to_dict() == segment.site.to_dict()
        assert candidate is not segment.site
        assert candidate.climate.provenance is not segment.site.climate.provenance


def test_site_from_epw_raises_one_error_with_accumulated_issues(tmp_path):
    epw_path = write_synthetic_epw(
        tmp_path / "invalid.epw",
        field_overrides={
            "dry_bulb_temperature": {0: 99.9},
            "wind_speed": {1: 999},
        },
    )

    with pytest.raises(ValueError) as error:
        Site.from_epw(str(epw_path))

    message = str(error.value)
    assert "EPW conversion failed" in message
    assert str(epw_path) in message
    assert "dry_bulb_temperature hour 1" in message
    assert "wind_speed hour 2" in message
