import warnings

from ladybug_geometry.geometry3d import LineSegment3D, Point3D

from honeybee_energy_ph.construction.thermal_bridge import PhThermalBridge
from honeybee_ph.bldg_segment import (
    BldgSegment,
    PhVentilationSummerBypassMode,
    PhWindExposureType,
    SetPoints,
    SummerVentilation,
)

# -- SetPoints -----------------------------------------------------------------


def test_set_points_round_trip():
    # -- default attrs
    o1 = SetPoints()
    d1 = o1.to_dict()
    o2 = SetPoints.from_dict(d1)

    assert o2.to_dict() == d1

    # -- customize attrs
    o1.winter = 22.3
    o1.summer = 134.8
    d3 = o1.to_dict()
    o3 = SetPoints.from_dict(d3)

    assert o3.to_dict() == d3


def test_set_points_duplicate():
    o1 = SetPoints()
    o2 = o1.duplicate()

    assert o1.to_dict() == o2.to_dict()


# -- SummerVentilation ---------------------------------------------------------


def test_summer_ventilation_default():
    sv = SummerVentilation()
    assert sv.summer_bypass_mode.value == "4-ALWAYS"
    assert sv.ventilation_system_ach is None
    assert sv.daytime_extract_system_ach == 0.0
    assert sv.daytime_extract_system_fan_power_wh_m3 == 0.0
    assert sv.daytime_window_ach == 0.0
    assert sv.nighttime_extract_system_ach == 0.0
    assert sv.nighttime_extract_system_fan_power_wh_m3 == 0.0
    assert sv.nighttime_extract_system_heat_fraction == 0.0
    assert sv.nighttime_extract_system_control == 0.0
    assert sv.nighttime_window_ach == 0.0
    assert sv.nighttime_minimum_indoor_temp_C == 0.0


def test_summer_ventilation_init_with_args():
    sv = SummerVentilation(
        _ventilation_system_ach=1.5,
        _ventilation_system_summer_bypass_mode=2,
        _daytime_extract_system_ach=0.3,
        _daytime_extract_system_fan_power_wh_m3=0.45,
        _daytime_window_ach=0.5,
        _nighttime_extract_system_ach=0.6,
        _nighttime_extract_system_fan_power_wh_m3=0.55,
        _nighttime_extract_system_heat_fraction=0.7,
        _nighttime_extract_system_control=0.8,
        _nighttime_window_ach=0.9,
        _nighttime_minimum_indoor_temp_C=18.0,
    )
    assert sv.ventilation_system_ach == 1.5
    assert sv.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"
    assert sv.daytime_extract_system_ach == 0.3
    assert sv.daytime_extract_system_fan_power_wh_m3 == 0.45
    assert sv.daytime_window_ach == 0.5
    assert sv.nighttime_extract_system_ach == 0.6
    assert sv.nighttime_extract_system_fan_power_wh_m3 == 0.55
    assert sv.nighttime_extract_system_heat_fraction == 0.7
    assert sv.nighttime_extract_system_control == 0.8
    assert sv.nighttime_window_ach == 0.9
    assert sv.nighttime_minimum_indoor_temp_C == 18.0


def test_summer_ventilation_round_trip():
    sv1 = SummerVentilation()
    d1 = sv1.to_dict()
    sv2 = SummerVentilation.from_dict(d1)

    assert sv2.to_dict() == d1
    assert sv2.summer_bypass_mode.value == sv1.summer_bypass_mode.value


def test_summer_ventilation_round_trip_custom():
    sv1 = SummerVentilation()
    sv1.summer_bypass_mode = PhVentilationSummerBypassMode(2)
    sv1.ventilation_system_ach = 2.5
    sv1.daytime_extract_system_ach = 0.4
    sv1.daytime_extract_system_fan_power_wh_m3 = 0.55
    sv1.daytime_window_ach = 0.6
    sv1.nighttime_extract_system_ach = 0.7
    sv1.nighttime_extract_system_fan_power_wh_m3 = 0.65
    sv1.nighttime_extract_system_heat_fraction = 0.8
    sv1.nighttime_extract_system_control = 0.9
    sv1.nighttime_window_ach = 1.0
    sv1.nighttime_minimum_indoor_temp_C = 16.0

    d1 = sv1.to_dict()
    sv2 = SummerVentilation.from_dict(d1)

    assert sv2.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"
    assert sv2.ventilation_system_ach == 2.5
    assert sv2.daytime_extract_system_ach == 0.4
    assert sv2.daytime_extract_system_fan_power_wh_m3 == 0.55
    assert sv2.daytime_window_ach == 0.6
    assert sv2.nighttime_extract_system_ach == 0.7
    assert sv2.nighttime_extract_system_fan_power_wh_m3 == 0.65
    assert sv2.nighttime_extract_system_heat_fraction == 0.8
    assert sv2.nighttime_extract_system_control == 0.9
    assert sv2.nighttime_window_ach == 1.0
    assert sv2.nighttime_minimum_indoor_temp_C == 16.0
    assert sv2.to_dict() == d1


def test_summer_ventilation_duplicate():
    sv1 = SummerVentilation()
    sv1.summer_bypass_mode = PhVentilationSummerBypassMode(3)
    sv1.ventilation_system_ach = 1.2
    sv1.daytime_extract_system_ach = 0.3
    sv1.daytime_extract_system_fan_power_wh_m3 = 0.4
    sv1.daytime_window_ach = 0.5
    sv1.nighttime_extract_system_ach = 0.6
    sv1.nighttime_extract_system_fan_power_wh_m3 = 0.7
    sv1.nighttime_extract_system_heat_fraction = 0.8
    sv1.nighttime_extract_system_control = 0.9
    sv1.nighttime_window_ach = 1.0
    sv1.nighttime_minimum_indoor_temp_C = 15.0

    sv2 = sv1.duplicate()

    assert sv2.summer_bypass_mode.value == sv1.summer_bypass_mode.value
    assert sv2.ventilation_system_ach == sv1.ventilation_system_ach
    assert sv2.nighttime_minimum_indoor_temp_C == sv1.nighttime_minimum_indoor_temp_C
    assert sv2.to_dict() == sv1.to_dict()
    # Verify it's a true copy, not a reference
    assert sv2 is not sv1
    assert sv2.summer_bypass_mode is not sv1.summer_bypass_mode


# -- BldgSegment ---------------------------------------------------------------


def test_default_bdg_segment_round_trip():
    o1 = BldgSegment()
    d1 = o1.to_dict()
    o2 = BldgSegment.from_dict(d1)

    assert o2.to_dict() == o1.to_dict()


def test_bdg_segment_round_trip_w_tbs():
    o1 = BldgSegment()

    # -- Add a new TB
    tb_geom = LineSegment3D.from_end_points(Point3D(0, 0, 0), Point3D(10, 0, 0))
    tb1 = PhThermalBridge(_identifier="test", _geometry=tb_geom)
    o1.add_new_thermal_bridge(tb1)

    d1 = o1.to_dict()
    o2 = BldgSegment.from_dict(d1)

    assert o2.to_dict() == o1.to_dict()


def test_bdg_segment_round_trip_w_user_data():
    o1 = BldgSegment()

    # -- Add user-data
    o1.user_data["test_key"] = "test_value"

    d1 = o1.to_dict()
    o2 = BldgSegment.from_dict(d1)

    assert "test_key" in o2.user_data
    assert o2.to_dict() == o1.to_dict()


def test_default_bdg_segment_duplicate():
    o1 = BldgSegment()
    o2 = o1.duplicate()

    assert o1.to_dict() == o2.to_dict()


def test_bdg_segment_w_tbs_duplicate():
    o1 = BldgSegment()

    # -- Add a new TB
    tb_geom = LineSegment3D.from_end_points(Point3D(0, 0, 0), Point3D(10, 0, 0))
    tb1 = PhThermalBridge(_identifier="test", _geometry=tb_geom)
    o1.add_new_thermal_bridge(tb1)

    o2 = o1.duplicate()

    assert o1.to_dict() == o2.to_dict()


def test_bdg_segment_w_user_data_duplicate():
    o1 = BldgSegment()

    # -- Add a new TB
    o1.user_data["test_key"] = "test_value"

    o2 = o1.duplicate()

    assert "test_key" in o2.user_data
    assert o1.to_dict() == o2.to_dict()


# -- Deprecated summer_hrv_bypass_mode property --------------------------------


def test_deprecated_summer_hrv_bypass_mode_getter():
    seg = BldgSegment()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        _ = seg.summer_hrv_bypass_mode
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
        assert "summer_ventilation" in str(w[0].message)


def test_deprecated_summer_hrv_bypass_mode_setter():
    seg = BldgSegment()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        seg.summer_hrv_bypass_mode = PhVentilationSummerBypassMode(2)
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
    # Verify value was set through to the underlying object
    assert seg.summer_ventilation.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"


def test_deprecated_summer_hrv_bypass_mode_setter_with_int():
    seg = BldgSegment()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        seg.summer_hrv_bypass_mode = 3
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
    assert seg.summer_ventilation.summer_bypass_mode.value == "3-ENTHALPY CONTROLLED"


def test_deprecated_summer_hrv_bypass_mode_setter_with_string():
    seg = BldgSegment()
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        seg.summer_hrv_bypass_mode = "2-Temperature Controlled"
        assert len(w) == 1
        assert issubclass(w[0].category, DeprecationWarning)
    assert seg.summer_ventilation.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"


def test_set_summer_bypass_mode_roundtrip_via_deprecated():
    """Round-trip through the deprecated property still works."""
    seg1 = BldgSegment()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        seg1.summer_hrv_bypass_mode = PhVentilationSummerBypassMode(2)

    d1 = seg1.to_dict()
    seg2 = BldgSegment.from_dict(d1)

    assert seg2.summer_ventilation.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"


def test_set_summer_bypass_mode_roundtrip_via_new_api():
    """Round-trip through the new summer_ventilation API."""
    seg1 = BldgSegment()
    seg1.summer_ventilation.summer_bypass_mode = PhVentilationSummerBypassMode(2)

    d1 = seg1.to_dict()
    seg2 = BldgSegment.from_dict(d1)

    assert seg2.summer_ventilation.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"
    assert seg2.to_dict() == d1


def test_set_summer_bypass_mode_duplicate_via_deprecated():
    seg1 = BldgSegment()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        seg1.summer_hrv_bypass_mode = PhVentilationSummerBypassMode(2)

    seg2 = seg1.duplicate()

    assert seg2.summer_ventilation.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"
    assert seg2.to_dict() == seg1.to_dict()


# -- Old serialization format backwards compat ---------------------------------


def test_from_dict_with_old_format():
    """Old JSON files have 'summer_hrv_bypass_mode' at the top level, not 'summer_ventilation'."""
    seg1 = BldgSegment()
    d1 = seg1.to_dict()

    # Simulate an old-format dict: replace 'summer_ventilation' with flat 'summer_hrv_bypass_mode'
    summer_vent_dict = d1.pop("summer_ventilation")
    d1["summer_hrv_bypass_mode"] = summer_vent_dict["summer_bypass_mode"]

    seg2 = BldgSegment.from_dict(d1)

    # The bypass mode value should survive the old-format round-trip
    assert seg2.summer_ventilation.summer_bypass_mode.value == "4-ALWAYS"


def test_from_dict_with_old_format_custom_value():
    """Old JSON with a non-default bypass mode deserializes correctly."""
    seg1 = BldgSegment()
    d1 = seg1.to_dict()

    # Simulate old format with custom value
    d1.pop("summer_ventilation")
    d1["summer_hrv_bypass_mode"] = {"value": "2-TEMPERATURE CONTROLLED"}

    seg2 = BldgSegment.from_dict(d1)

    assert seg2.summer_ventilation.summer_bypass_mode.value == "2-TEMPERATURE CONTROLLED"


def test_from_dict_new_format_takes_precedence():
    """If both keys exist (shouldn't happen normally), new format wins."""
    seg1 = BldgSegment()
    d1 = seg1.to_dict()

    # Add an old key alongside the new one — new key should win
    d1["summer_hrv_bypass_mode"] = {"value": "1-NONE"}

    seg2 = BldgSegment.from_dict(d1)

    # New format (4-ALWAYS default) takes precedence over old key (1-NONE)
    assert seg2.summer_ventilation.summer_bypass_mode.value == "4-ALWAYS"


def test_to_dict_uses_new_format():
    """to_dict should serialize under 'summer_ventilation', not 'summer_hrv_bypass_mode'."""
    seg = BldgSegment()
    d = seg.to_dict()

    assert "summer_ventilation" in d
    assert "summer_hrv_bypass_mode" not in d
    sv_dict = d["summer_ventilation"]
    assert "summer_bypass_mode" in sv_dict
    assert "ventilation_system_ach" in sv_dict
    assert "daytime_extract_system_ach" in sv_dict
    assert "daytime_extract_system_fan_power_wh_m3" in sv_dict
    assert "daytime_window_ach" in sv_dict
    assert "nighttime_extract_system_ach" in sv_dict
    assert "nighttime_extract_system_fan_power_wh_m3" in sv_dict
    assert "nighttime_extract_system_heat_fraction" in sv_dict
    assert "nighttime_extract_system_control" in sv_dict
    assert "nighttime_window_ach" in sv_dict
    assert "nighttime_minimum_indoor_temp_C" in sv_dict


def test_default_summer_bypass_mode_preserved():
    """The default bypass mode should be '4-Always' to match the old behavior."""
    seg = BldgSegment()
    assert seg.summer_ventilation.summer_bypass_mode.value == "4-ALWAYS"


# -- Wind exposure type --------------------------------------------------------


def test_set_wind_exposure_type_roundtrip():
    seg1 = BldgSegment()
    seg1.wind_exposure_type = PhWindExposureType(2)

    d1 = seg1.to_dict()
    seg2 = BldgSegment.from_dict(d1)
    assert seg2.wind_exposure_type.number == 2
    assert seg2.wind_exposure_type == seg1.wind_exposure_type


def test_set_wind_exposure_type_duplicate():
    seg1 = BldgSegment()
    seg1.wind_exposure_type = PhWindExposureType(2)

    seg2 = seg1.duplicate()
    assert seg2.wind_exposure_type.number == 2
    assert seg2.wind_exposure_type == seg1.wind_exposure_type
