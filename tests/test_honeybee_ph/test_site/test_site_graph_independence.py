from copy import deepcopy
from inspect import signature
import json
import subprocess
import sys

import pytest

from honeybee_ph import site
from honeybee_ph.bldg_segment import BldgSegment


MONTHS = (
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
)

CLIMATE_MUTABLE_PATHS = (
    "user_data",
    "ground",
    "ground.user_data",
    "monthly_temps",
    "monthly_temps.user_data",
    "monthly_temps.air_temps",
    "monthly_temps.air_temps.user_data",
    "monthly_temps.dewpoints",
    "monthly_temps.dewpoints.user_data",
    "monthly_temps.sky_temps",
    "monthly_temps.sky_temps.user_data",
    "monthly_temps.ground_temps",
    "monthly_temps.ground_temps.user_data",
    "monthly_radiation",
    "monthly_radiation.user_data",
    "monthly_radiation.north",
    "monthly_radiation.north.user_data",
    "monthly_radiation.east",
    "monthly_radiation.east.user_data",
    "monthly_radiation.south",
    "monthly_radiation.south.user_data",
    "monthly_radiation.west",
    "monthly_radiation.west.user_data",
    "monthly_radiation.glob",
    "monthly_radiation.glob.user_data",
    "peak_loads",
    "peak_loads.user_data",
    "peak_loads.heat_load_1",
    "peak_loads.heat_load_1.user_data",
    "peak_loads.heat_load_2",
    "peak_loads.heat_load_2.user_data",
    "peak_loads.cooling_load_1",
    "peak_loads.cooling_load_1.user_data",
    "peak_loads.cooling_load_2",
    "peak_loads.cooling_load_2.user_data",
)

SITE_MUTABLE_PATHS = (
    "user_data",
    "location",
    "location.user_data",
    "climate",
    "phpp_library_codes",
    "phpp_library_codes.user_data",
) + tuple("climate.{}".format(path) for path in CLIMATE_MUTABLE_PATHS)


def _xfail(*values):
    return pytest.param(*values, marks=pytest.mark.xfail(strict=True, reason="shared mutable constructor default"))


def _resolve(obj, path):
    for attribute in path.split("."):
        obj = getattr(obj, attribute)
    return obj


def _canonicalize_generated_base_attributes(value):
    if not isinstance(value, dict):
        return value

    canonical = {}
    identifier = value.get("identifier")
    for key, child in value.items():
        if key == "identifier":
            canonical[key] = "<generated>"
        elif key == "display_name" and child == identifier:
            canonical[key] = "<generated>"
        else:
            canonical[key] = _canonicalize_generated_base_attributes(child)
    return canonical


def _default_base(display_name="<generated>"):
    return {"display_name": display_name, "identifier": "<generated>", "user_data": {}}


def _default_monthly_values():
    expected = _default_base()
    expected.update(dict((month, 0.0) for month in MONTHS))
    return expected


def _default_monthly_temperatures():
    expected = _default_base()
    expected.update(
        {
            "air_temps": _default_monthly_values(),
            "dewpoints": _default_monthly_values(),
            "sky_temps": _default_monthly_values(),
            "ground_temps": _default_monthly_values(),
        }
    )
    return expected


def _default_monthly_radiation():
    expected = _default_base()
    expected.update(
        dict((orientation, _default_monthly_values()) for orientation in ("north", "east", "south", "west", "glob"))
    )
    return expected


def _default_peak_load_values():
    expected = _default_base()
    expected.update(
        {
            "temp": 0.0,
            "rad_north": 0.0,
            "rad_east": 0.0,
            "rad_south": 0.0,
            "rad_west": 0.0,
            "rad_global": 0.0,
            "dewpoint": None,
            "sky_temp": None,
            "ground_temp": None,
        }
    )
    return expected


def _default_peak_loads():
    expected = _default_base()
    expected.update(
        dict(
            (load_name, _default_peak_load_values())
            for load_name in ("heat_load_1", "heat_load_2", "cooling_load_1", "cooling_load_2")
        )
    )
    return expected


def _default_ground():
    expected = _default_base()
    expected.update(
        {
            "ground_thermal_conductivity": 2,
            "ground_heat_capacity": 1000,
            "ground_density": 2000,
            "depth_groundwater": 3,
            "flow_rate_groundwater": 0.05,
        }
    )
    return expected


def _default_climate():
    expected = _default_base("New York")
    expected.update(
        {
            "station_elevation": 0.0,
            "summer_daily_temperature_swing": 8.0,
            "average_wind_speed": 4.0,
            "ground": _default_ground(),
            "monthly_temps": _default_monthly_temperatures(),
            "monthly_radiation": _default_monthly_radiation(),
            "peak_loads": _default_peak_loads(),
        }
    )
    return expected


def _default_site():
    location = _default_base()
    location.update(
        {"latitude": 40.6, "longitude": -73.8, "site_elevation": None, "climate_zone": 1, "hours_from_UTC": -4}
    )
    phpp_codes = _default_base("US0055c-New York")
    phpp_codes.update(
        {
            "country_code": "US-United States of America",
            "region_code": "New York",
            "dataset_name": "US0055c-New York",
        }
    )
    expected = _default_base()
    expected.update({"location": location, "climate": _default_climate(), "phpp_library_codes": phpp_codes})
    return expected


@pytest.mark.parametrize(
    "constructor, parameter_name",
    [
        _xfail(site.Climate_MonthlyValueSet, "_values"),
        _xfail(site.Climate_MonthlyTempCollection, "_air"),
        _xfail(site.Climate_MonthlyTempCollection, "_dewpoint"),
        _xfail(site.Climate_MonthlyTempCollection, "_sky"),
        _xfail(site.Climate_MonthlyTempCollection, "_ground"),
        _xfail(site.Climate_MonthlyRadiationCollection, "_north"),
        _xfail(site.Climate_MonthlyRadiationCollection, "_east"),
        _xfail(site.Climate_MonthlyRadiationCollection, "_south"),
        _xfail(site.Climate_MonthlyRadiationCollection, "_west"),
        _xfail(site.Climate_MonthlyRadiationCollection, "_glob"),
        _xfail(site.Climate_PeakLoadCollection, "_heat_load_1"),
        _xfail(site.Climate_PeakLoadCollection, "_heat_load_2"),
        _xfail(site.Climate_PeakLoadCollection, "_cooling_load_1"),
        _xfail(site.Climate_PeakLoadCollection, "_cooling_load_2"),
        _xfail(site.Climate, "_monthly_temps"),
        _xfail(site.Climate, "_monthly_radiation"),
        _xfail(site.Climate, "_peak_loads"),
        _xfail(site.Site, "_location"),
        _xfail(site.Site, "_climate"),
        _xfail(site.Site, "_phpp_library_codes"),
    ],
)
def test_mutable_constructor_parameters_default_to_none(constructor, parameter_name):
    assert signature(constructor).parameters[parameter_name].default is None


@pytest.mark.parametrize(
    "constructor, path",
    [
        _xfail(site.Climate_MonthlyTempCollection, "air_temps"),
        _xfail(site.Climate_MonthlyTempCollection, "dewpoints"),
        _xfail(site.Climate_MonthlyTempCollection, "sky_temps"),
        _xfail(site.Climate_MonthlyTempCollection, "ground_temps"),
        _xfail(site.Climate_MonthlyRadiationCollection, "north"),
        _xfail(site.Climate_MonthlyRadiationCollection, "east"),
        _xfail(site.Climate_MonthlyRadiationCollection, "south"),
        _xfail(site.Climate_MonthlyRadiationCollection, "west"),
        _xfail(site.Climate_MonthlyRadiationCollection, "glob"),
        _xfail(site.Climate_PeakLoadCollection, "heat_load_1"),
        _xfail(site.Climate_PeakLoadCollection, "heat_load_2"),
        _xfail(site.Climate_PeakLoadCollection, "cooling_load_1"),
        _xfail(site.Climate_PeakLoadCollection, "cooling_load_2"),
        (site.Climate, "ground"),
        _xfail(site.Climate, "monthly_temps"),
        _xfail(site.Climate, "monthly_temps.air_temps"),
        _xfail(site.Climate, "monthly_radiation"),
        _xfail(site.Climate, "monthly_radiation.north"),
        _xfail(site.Climate, "peak_loads"),
        _xfail(site.Climate, "peak_loads.heat_load_1"),
        _xfail(site.Site, "location"),
        _xfail(site.Site, "climate"),
        _xfail(site.Site, "climate.monthly_temps.air_temps"),
        _xfail(site.Site, "phpp_library_codes"),
        (BldgSegment, "site"),
        _xfail(BldgSegment, "site.location"),
        _xfail(BldgSegment, "site.climate"),
        _xfail(BldgSegment, "site.climate.monthly_radiation.north"),
        _xfail(BldgSegment, "site.phpp_library_codes"),
    ],
)
def test_default_nested_objects_are_independent(constructor, path):
    left = constructor()
    right = constructor()

    assert _resolve(left, path) is not _resolve(right, path)


@pytest.mark.parametrize(
    "constructor, path, changed_value",
    [
        (site.Climate_MonthlyValueSet, "january", 99.0),
        _xfail(site.Climate_MonthlyTempCollection, "air_temps.january", 11.0),
        _xfail(site.Climate_MonthlyRadiationCollection, "north.january", 22.0),
        _xfail(site.Climate_PeakLoadCollection, "heat_load_1.temp", -12.0),
        _xfail(site.Climate, "monthly_temps.air_temps.january", 33.0),
        _xfail(site.Climate, "monthly_radiation.north.january", 44.0),
        _xfail(site.Climate, "peak_loads.heat_load_1.temp", -14.0),
        (site.Climate, "ground.ground_thermal_conductivity", 3.0),
        _xfail(site.Site, "location.latitude", 42.0),
        _xfail(site.Site, "climate.ground.ground_density", 1800),
        _xfail(site.Site, "climate.monthly_temps.air_temps.january", 55.0),
        _xfail(site.Site, "climate.monthly_radiation.north.january", 66.0),
        _xfail(site.Site, "climate.peak_loads.heat_load_1.temp", -16.0),
        _xfail(site.Site, "phpp_library_codes.region_code", "Massachusetts"),
        _xfail(BldgSegment, "site.location.latitude", 43.0),
        _xfail(BldgSegment, "site.climate.monthly_temps.air_temps.january", 77.0),
        _xfail(BldgSegment, "site.phpp_library_codes.region_code", "New Jersey"),
    ],
)
def test_mutating_default_graph_does_not_change_peer(constructor, path, changed_value):
    left = constructor()
    right = constructor()
    if "." in path:
        parent_path, attribute = path.rsplit(".", 1)
        left_parent = _resolve(left, parent_path)
        right_parent = _resolve(right, parent_path)
    else:
        attribute = path
        left_parent = left
        right_parent = right
    original_value = getattr(right_parent, attribute)

    try:
        setattr(left_parent, attribute, changed_value)
        assert getattr(right_parent, attribute) == original_value
    finally:
        setattr(left_parent, attribute, original_value)


def test_default_serialization_contract():
    script = (
        "import json\n"
        "from honeybee_ph import site\n"
        "print(json.dumps({'climate': site.Climate().to_dict(), 'site': site.Site().to_dict()}))\n"
    )
    serialized = json.loads(subprocess.check_output([sys.executable, "-c", script]))

    assert _canonicalize_generated_base_attributes(serialized["climate"]) == _default_climate()
    assert _canonicalize_generated_base_attributes(serialized["site"]) == _default_site()


def _populated_climate():
    climate = site.Climate(
        _display_name="Berkshires",
        _station_elevation=300.0,
        _daily_temp_swing=9.0,
        _average_wind_speed=3.5,
        _monthly_temps=site.Climate_MonthlyTempCollection(
            _air=site.Climate_MonthlyValueSet(range(1, 13)),
            _dewpoint=site.Climate_MonthlyValueSet(range(2, 14)),
            _sky=site.Climate_MonthlyValueSet(range(3, 15)),
            _ground=site.Climate_MonthlyValueSet(range(4, 16)),
        ),
        _monthly_radiation=site.Climate_MonthlyRadiationCollection(
            _north=site.Climate_MonthlyValueSet(range(5, 17)),
            _east=site.Climate_MonthlyValueSet(range(6, 18)),
            _south=site.Climate_MonthlyValueSet(range(7, 19)),
            _west=site.Climate_MonthlyValueSet(range(8, 20)),
            _glob=site.Climate_MonthlyValueSet(range(9, 21)),
        ),
        _peak_loads=site.Climate_PeakLoadCollection(
            _heat_load_1=site.Climate_PeakLoadValueSet(_temp=-15.0),
            _heat_load_2=site.Climate_PeakLoadValueSet(_temp=-12.0),
            _cooling_load_1=site.Climate_PeakLoadValueSet(_temp=32.0),
            _cooling_load_2=site.Climate_PeakLoadValueSet(_temp=35.0),
        ),
    )
    climate.ground.ground_density = 1900
    climate.user_data["source"] = "test"
    return climate


@pytest.mark.xfail(strict=True, reason="Climate duplicate is shallow")
def test_climate_duplicate_is_recursively_independent():
    climate = _populated_climate()
    duplicate = climate.duplicate()

    assert duplicate.to_dict() == climate.to_dict()
    for path in CLIMATE_MUTABLE_PATHS:
        assert _resolve(duplicate, path) is not _resolve(climate, path)


@pytest.mark.xfail(strict=True, reason="Climate_Ground duplicate reuses user_data")
def test_ground_duplicate_owns_user_data():
    ground = site.Climate_Ground()
    ground.user_data["source"] = "test"

    duplicate = ground.duplicate()

    assert duplicate.to_dict() == ground.to_dict()
    assert duplicate.user_data is not ground.user_data


def _populated_site():
    return site.Site(
        _location=site.Location(latitude=42.3, longitude=-73.4),
        _climate=_populated_climate(),
        _phpp_library_codes=site.PHPPCodes("US", "Massachusetts", "Test Dataset"),
    )


def test_site_duplicate_preserves_values_and_owns_nested_objects():
    original = _populated_site()
    duplicate = original.duplicate()

    assert duplicate.to_dict() == original.to_dict()
    for path in ("location", "climate", "phpp_library_codes"):
        assert _resolve(duplicate, path) is not _resolve(original, path)


@pytest.mark.xfail(strict=True, reason="Site duplicate contains a shallow Climate duplicate")
def test_site_duplicate_owns_complete_climate_graph():
    original = _populated_site()
    duplicate = original.duplicate()

    for path in SITE_MUTABLE_PATHS:
        assert _resolve(duplicate, path) is not _resolve(original, path)


def _without_base_attributes(value):
    if isinstance(value, dict):
        return dict(
            (key, _without_base_attributes(child))
            for key, child in value.items()
            if key not in ("identifier", "display_name", "user_data")
        )
    return value


def test_legacy_site_dict_without_base_attributes_loads_independently():
    legacy = _without_base_attributes(site.Site().to_dict())
    original_january = legacy["climate"]["monthly_temps"]["air_temps"]["january"]

    left = site.Site.from_dict(deepcopy(legacy))
    right = site.Site.from_dict(deepcopy(legacy))
    left.climate.monthly_temps.air_temps.january = 10.0

    assert _without_base_attributes(right.to_dict()) == legacy
    assert right.climate.monthly_temps.air_temps.january == original_january
    for path in SITE_MUTABLE_PATHS:
        assert _resolve(left, path) is not _resolve(right, path)


@pytest.mark.xfail(strict=True, reason="from_dict reuses input user_data dictionaries")
def test_repeated_site_deserialization_owns_user_data():
    serialized = site.Site().to_dict()
    serialized["user_data"]["scope"] = "site"
    serialized["climate"]["user_data"]["scope"] = "climate"
    serialized["climate"]["ground"]["user_data"]["scope"] = "ground"

    left = site.Site.from_dict(serialized)
    right = site.Site.from_dict(serialized)

    assert left.to_dict() == serialized
    assert right.to_dict() == serialized
    for path in SITE_MUTABLE_PATHS:
        assert _resolve(left, path) is not _resolve(right, path)


@pytest.mark.parametrize(
    "constructor, parameter, attribute, child_factory",
    [
        (site.Climate_MonthlyTempCollection, "_air", "air_temps", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyTempCollection, "_dewpoint", "dewpoints", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyTempCollection, "_sky", "sky_temps", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyTempCollection, "_ground", "ground_temps", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyRadiationCollection, "_north", "north", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyRadiationCollection, "_east", "east", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyRadiationCollection, "_south", "south", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyRadiationCollection, "_west", "west", site.Climate_MonthlyValueSet),
        (site.Climate_MonthlyRadiationCollection, "_glob", "glob", site.Climate_MonthlyValueSet),
        (site.Climate_PeakLoadCollection, "_heat_load_1", "heat_load_1", site.Climate_PeakLoadValueSet),
        (site.Climate_PeakLoadCollection, "_heat_load_2", "heat_load_2", site.Climate_PeakLoadValueSet),
        (site.Climate_PeakLoadCollection, "_cooling_load_1", "cooling_load_1", site.Climate_PeakLoadValueSet),
        (site.Climate_PeakLoadCollection, "_cooling_load_2", "cooling_load_2", site.Climate_PeakLoadValueSet),
        (site.Climate, "_monthly_temps", "monthly_temps", site.Climate_MonthlyTempCollection),
        (site.Climate, "_monthly_radiation", "monthly_radiation", site.Climate_MonthlyRadiationCollection),
        (site.Climate, "_peak_loads", "peak_loads", site.Climate_PeakLoadCollection),
        (site.Site, "_location", "location", site.Location),
        (site.Site, "_climate", "climate", site.Climate),
        (site.Site, "_phpp_library_codes", "phpp_library_codes", site.PHPPCodes),
    ],
)
def test_constructor_preserves_explicit_child_ownership(constructor, parameter, attribute, child_factory):
    child = child_factory()

    obj = constructor(**{parameter: child})

    assert getattr(obj, attribute) is child
