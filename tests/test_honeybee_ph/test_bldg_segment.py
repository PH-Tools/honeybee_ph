from ladybug_geometry.geometry3d import Point3D, LineSegment3D
from honeybee_ph.bldg_segment import SetPoints, BldgSegment
from honeybee_energy_ph.construction.thermal_bridge import PhThermalBridge


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

    assert o2.to_dict() == d1


def test_bdg_segment_round_trip_w_tbs():
    o1 = BldgSegment()

    # -- Add a new TB
    tb_geom = LineSegment3D.from_end_points(Point3D(0, 0, 0), Point3D(10, 0, 0))
    tb1 = PhThermalBridge(_identifier="test", _geometry=tb_geom)
    o1.add_new_thermal_bridge(tb1)

    d1 = o1.to_dict()
    o2 = BldgSegment.from_dict(d1)

    assert o2.to_dict() == d1


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