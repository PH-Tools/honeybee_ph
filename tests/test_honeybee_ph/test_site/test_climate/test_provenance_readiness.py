from copy import deepcopy

import pytest

from honeybee_ph import site


def _available_provenance(**overrides):
    values = {
        "source_type": "user_defined",
        "source_name": "Test climate",
        "monthly_data_available": True,
        "peak_load_data_available": True,
        "assumptions": {"method": {"name": "controlled-values"}},
    }
    values.update(overrides)
    return site.ClimateProvenance(**values)


def test_climate_provenance_round_trip_preserves_unknown_flags():
    provenance = site.ClimateProvenance(
        source_type="legacy_unknown",
        source_uri=None,
        is_certification_approved=None,
        monthly_data_available=None,
        peak_load_data_available=None,
        assumptions={"note": "availability not supplied"},
    )

    restored = site.ClimateProvenance.from_dict(provenance.to_dict())

    assert restored.to_dict() == provenance.to_dict()
    assert restored.is_certification_approved is None
    assert restored.monthly_data_available is None
    assert restored.peak_load_data_available is None


def test_climate_provenance_rejects_unknown_source_type():
    with pytest.raises(ValueError, match="source_type"):
        site.ClimateProvenance(source_type="weather-ish")


def test_default_climate_serialization_remains_legacy_compatible():
    serialized = site.Climate().to_dict()

    assert "provenance" not in serialized
    assert isinstance(serialized["peak_loads"], dict)

    restored = site.Climate.from_dict(deepcopy(serialized))
    assert restored.provenance is None
    assert restored.to_dict() == serialized


def test_missing_peak_loads_keeps_legacy_default_but_null_round_trips():
    legacy = site.Climate().to_dict()
    legacy.pop("peak_loads")

    legacy_restored = site.Climate.from_dict(legacy)
    assert isinstance(legacy_restored.peak_loads, site.Climate_PeakLoadCollection)

    unavailable = site.Climate(
        _peak_loads=None,
        _provenance=_available_provenance(peak_load_data_available=False),
    )
    serialized = unavailable.to_dict()
    restored = site.Climate.from_dict(serialized)

    assert serialized["peak_loads"] is None
    assert restored.peak_loads is None
    assert restored.to_dict() == serialized


def test_climate_duplicate_recursively_copies_provenance_and_children():
    original = site.Climate(_provenance=_available_provenance())
    duplicate = original.duplicate()

    assert duplicate.to_dict() == original.to_dict()
    assert duplicate.provenance is not original.provenance
    assert duplicate.provenance.assumptions is not original.provenance.assumptions
    assert duplicate.provenance.assumptions["method"] is not original.provenance.assumptions["method"]
    assert duplicate.monthly_temps is not original.monthly_temps
    assert duplicate.monthly_radiation is not original.monthly_radiation
    assert duplicate.peak_loads is not original.peak_loads


def test_monthly_readiness_uses_availability_not_numeric_truthiness():
    climate = site.Climate(_provenance=_available_provenance())

    assert climate.monthly_demand_readiness_issues() == []
    assert climate.is_monthly_demand_ready is True

    climate.monthly_temps.ground_temps.march = None
    assert climate.monthly_demand_readiness_issues() == [
        "monthly_temps.ground_temps.march: expected a finite numeric value; got None."
    ]
    assert climate.is_monthly_demand_ready is False


def test_monthly_readiness_accumulates_non_real_values_as_issues():
    climate = site.Climate(_provenance=_available_provenance())
    climate.station_elevation = complex(1, 2)
    climate.monthly_temps.air_temps.january = float("nan")

    assert climate.monthly_demand_readiness_issues() == [
        "station_elevation: expected a finite numeric value; got (1+2j).",
        "monthly_temps.air_temps.january: expected a finite numeric value; got nan.",
    ]


def test_legacy_and_unavailable_monthly_readiness_are_distinct():
    legacy = site.Climate()
    unavailable = site.Climate(
        _provenance=_available_provenance(monthly_data_available=False),
    )

    assert legacy.monthly_demand_readiness_issues() == [
        "provenance: monthly climate data availability is unknown for this legacy climate."
    ]
    assert unavailable.monthly_demand_readiness_issues() == [
        "provenance.monthly_data_available: monthly climate data is explicitly unavailable."
    ]


def test_peak_readiness_reports_specialized_data_requirement():
    climate = site.Climate(
        _peak_loads=None,
        _provenance=_available_provenance(peak_load_data_available=False),
    )

    assert climate.peak_load_readiness_issues() == [
        "provenance.peak_load_data_available: approved or specialized peak-load climate data must be supplied separately."
    ]
    assert climate.is_peak_load_ready is False


def test_peak_readiness_accepts_explicit_zero_values():
    climate = site.Climate(_provenance=_available_provenance())

    assert climate.peak_load_readiness_issues() == []
    assert climate.is_peak_load_ready is True


def test_blank_phpp_codes_serialize_without_library_identity():
    codes = site.PHPPCodes.blank()

    assert codes.country_code == ""
    assert codes.region_code == ""
    assert codes.dataset_name == ""
    assert codes.to_dict()["display_name"] == ""
    assert site.PHPPCodes.from_dict(codes.to_dict()).to_dict() == codes.to_dict()
