from ladybug_geometry.geometry3d import LineSegment3D, Point3D

from honeybee_energy_ph.construction.thermal_bridge import PhThermalBridge
from honeybee_ph.bldg_segment import BldgSegment, PhVentilationSummerBypassMode, PhWindExposureType, SetPoints


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


def test_set_summer_bypass_mode_roundtrip():
    seg1 = BldgSegment()
    seg1.summer_hrv_bypass_mode = PhVentilationSummerBypassMode(2)

    d1 = seg1.to_dict()
    seg2 = BldgSegment.from_dict(d1)
    assert seg2.summer_hrv_bypass_mode == seg1.summer_hrv_bypass_mode


def test_set_summer_bypass_mode_duplicate():
    seg1 = BldgSegment()
    seg1.summer_hrv_bypass_mode = PhVentilationSummerBypassMode(2)

    seg2 = seg1.duplicate()
    assert seg2.summer_hrv_bypass_mode == seg1.summer_hrv_bypass_mode


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
