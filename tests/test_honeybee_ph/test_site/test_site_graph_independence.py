from copy import deepcopy
from inspect import signature
import json
import subprocess
import sys

import pytest

from honeybee.model import Model
from honeybee.room import Room
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
        (site.Climate_MonthlyValueSet, "_values"),
        (site.Climate_MonthlyTempCollection, "_air"),
        (site.Climate_MonthlyTempCollection, "_dewpoint"),
        (site.Climate_MonthlyTempCollection, "_sky"),
        (site.Climate_MonthlyTempCollection, "_ground"),
        (site.Climate_MonthlyRadiationCollection, "_north"),
        (site.Climate_MonthlyRadiationCollection, "_east"),
        (site.Climate_MonthlyRadiationCollection, "_south"),
        (site.Climate_MonthlyRadiationCollection, "_west"),
        (site.Climate_MonthlyRadiationCollection, "_glob"),
        (site.Climate_PeakLoadCollection, "_heat_load_1"),
        (site.Climate_PeakLoadCollection, "_heat_load_2"),
        (site.Climate_PeakLoadCollection, "_cooling_load_1"),
        (site.Climate_PeakLoadCollection, "_cooling_load_2"),
        (site.Climate, "_monthly_temps"),
        (site.Climate, "_monthly_radiation"),
        (site.Climate, "_peak_loads"),
        (site.Site, "_location"),
        (site.Site, "_climate"),
        (site.Site, "_phpp_library_codes"),
    ],
)
def test_mutable_constructor_parameters_default_to_none(constructor, parameter_name):
    assert signature(constructor).parameters[parameter_name].default is None


@pytest.mark.parametrize(
    "constructor, path",
    [
        (site.Climate_MonthlyTempCollection, "air_temps"),
        (site.Climate_MonthlyTempCollection, "dewpoints"),
        (site.Climate_MonthlyTempCollection, "sky_temps"),
        (site.Climate_MonthlyTempCollection, "ground_temps"),
        (site.Climate_MonthlyRadiationCollection, "north"),
        (site.Climate_MonthlyRadiationCollection, "east"),
        (site.Climate_MonthlyRadiationCollection, "south"),
        (site.Climate_MonthlyRadiationCollection, "west"),
        (site.Climate_MonthlyRadiationCollection, "glob"),
        (site.Climate_PeakLoadCollection, "heat_load_1"),
        (site.Climate_PeakLoadCollection, "heat_load_2"),
        (site.Climate_PeakLoadCollection, "cooling_load_1"),
        (site.Climate_PeakLoadCollection, "cooling_load_2"),
        (site.Climate, "ground"),
        (site.Climate, "monthly_temps"),
        (site.Climate, "monthly_temps.air_temps"),
        (site.Climate, "monthly_radiation"),
        (site.Climate, "monthly_radiation.north"),
        (site.Climate, "peak_loads"),
        (site.Climate, "peak_loads.heat_load_1"),
        (site.Site, "location"),
        (site.Site, "climate"),
        (site.Site, "climate.monthly_temps.air_temps"),
        (site.Site, "phpp_library_codes"),
        (BldgSegment, "site"),
        (BldgSegment, "site.location"),
        (BldgSegment, "site.climate"),
        (BldgSegment, "site.climate.monthly_radiation.north"),
        (BldgSegment, "site.phpp_library_codes"),
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
        (site.Climate_MonthlyTempCollection, "air_temps.january", 11.0),
        (site.Climate_MonthlyRadiationCollection, "north.january", 22.0),
        (site.Climate_PeakLoadCollection, "heat_load_1.temp", -12.0),
        (site.Climate, "monthly_temps.air_temps.january", 33.0),
        (site.Climate, "monthly_radiation.north.january", 44.0),
        (site.Climate, "peak_loads.heat_load_1.temp", -14.0),
        (site.Climate, "ground.ground_thermal_conductivity", 3.0),
        (site.Site, "location.latitude", 42.0),
        (site.Site, "climate.ground.ground_density", 1800),
        (site.Site, "climate.monthly_temps.air_temps.january", 55.0),
        (site.Site, "climate.monthly_radiation.north.january", 66.0),
        (site.Site, "climate.peak_loads.heat_load_1.temp", -16.0),
        (site.Site, "phpp_library_codes.region_code", "Massachusetts"),
        (BldgSegment, "site.location.latitude", 43.0),
        (BldgSegment, "site.climate.monthly_temps.air_temps.january", 77.0),
        (BldgSegment, "site.phpp_library_codes.region_code", "New Jersey"),
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
    climate.ground.ground_thermal_conductivity = 1.7
    climate.ground.ground_heat_capacity = 850
    climate.ground.ground_density = 1900
    climate.ground.depth_groundwater = 2.5
    climate.ground.flow_rate_groundwater = 0.02
    climate.user_data["source"] = "test"
    return climate


def test_climate_duplicate_is_recursively_independent():
    climate = _populated_climate()
    duplicate = climate.duplicate()

    assert duplicate.to_dict() == climate.to_dict()
    for path in CLIMATE_MUTABLE_PATHS:
        assert _resolve(duplicate, path) is not _resolve(climate, path)


def test_ground_duplicate_owns_user_data():
    ground = site.Climate_Ground()
    ground.user_data["source"] = "test"
    ground.ground_thermal_conductivity = 1.7
    ground.ground_heat_capacity = 850
    ground.ground_density = 1900
    ground.depth_groundwater = 2.5
    ground.flow_rate_groundwater = 0.02

    duplicate = ground.duplicate()

    assert duplicate.to_dict() == ground.to_dict()
    assert duplicate.user_data is not ground.user_data


@pytest.mark.parametrize("original", [_populated_climate(), site.Climate_Ground()])
def test_duplicate_preserves_dynamic_attributes(original):
    custom_value = {"downstream": []}
    original.custom_extension_value = custom_value

    duplicate = original.duplicate()

    assert duplicate.custom_extension_value is custom_value


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


def test_mutable_children_preserve_positional_order():
    temp_children = tuple(site.Climate_MonthlyValueSet([value] * 12) for value in range(1, 5))
    temperatures = site.Climate_MonthlyTempCollection(*temp_children)
    assert (
        temperatures.air_temps,
        temperatures.dewpoints,
        temperatures.sky_temps,
        temperatures.ground_temps,
    ) == temp_children

    radiation_children = tuple(site.Climate_MonthlyValueSet([value] * 12) for value in range(5, 10))
    radiation = site.Climate_MonthlyRadiationCollection(*radiation_children)
    assert (radiation.north, radiation.east, radiation.south, radiation.west, radiation.glob) == radiation_children

    peak_children = tuple(site.Climate_PeakLoadValueSet(_temp=value) for value in range(10, 14))
    peak_loads = site.Climate_PeakLoadCollection(*peak_children)
    assert (
        peak_loads.heat_load_1,
        peak_loads.heat_load_2,
        peak_loads.cooling_load_1,
        peak_loads.cooling_load_2,
    ) == peak_children

    climate = site.Climate("Test", 100.0, 7.0, 3.0, temperatures, radiation, peak_loads)
    assert climate.monthly_temps is temperatures
    assert climate.monthly_radiation is radiation
    assert climate.peak_loads is peak_loads

    location = site.Location()
    phpp_codes = site.PHPPCodes()
    site_obj = site.Site(location, climate, phpp_codes)
    assert site_obj.location is location
    assert site_obj.climate is climate
    assert site_obj.phpp_library_codes is phpp_codes


def _room_site(room):
    return room.properties.ph.ph_bldg_segment.site


def _room_with_populated_site():
    room = Room.from_box("source-room")
    room_site = _populated_site()
    room_site.user_data["scope"] = "site"
    room.properties.ph.ph_bldg_segment.site = room_site
    return room, room_site


def test_room_property_default_site_graphs_are_independent():
    left = Room.from_box("left-room")
    right = Room.from_box("right-room")

    for path in SITE_MUTABLE_PATHS:
        assert _resolve(_room_site(left), path) is not _resolve(_room_site(right), path)


def test_room_duplicate_owns_complete_site_graph():
    room, original_site = _room_with_populated_site()

    duplicate_site = _room_site(room.duplicate())

    assert duplicate_site.to_dict() == original_site.to_dict()
    for path in SITE_MUTABLE_PATHS:
        assert _resolve(duplicate_site, path) is not _resolve(original_site, path)


def test_model_hbjson_round_trip_owns_complete_site_graph():
    room, original_site = _room_with_populated_site()
    serialized = json.loads(json.dumps(Model("site-graph-model", [room]).to_dict()))

    left_model = Model.from_dict(deepcopy(serialized))
    right_model = Model.from_dict(deepcopy(serialized))
    left_site = _room_site(left_model.rooms[0])
    right_site = _room_site(right_model.rooms[0])

    assert json.loads(json.dumps(left_model.to_dict())) == serialized
    assert json.loads(json.dumps(right_model.to_dict())) == serialized
    assert left_site.to_dict() == original_site.to_dict()
    for path in SITE_MUTABLE_PATHS:
        assert _resolve(left_site, path) is not _resolve(original_site, path)
        assert _resolve(left_site, path) is not _resolve(right_site, path)

    left_site.climate.monthly_temps.air_temps.january = -5.0
    assert right_site.climate.monthly_temps.air_temps.january == 1
    assert original_site.climate.monthly_temps.air_temps.january == 1
