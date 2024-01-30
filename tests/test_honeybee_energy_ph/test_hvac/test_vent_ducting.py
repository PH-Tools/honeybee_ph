from typing import List

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_energy_ph.hvac.ducting import PhDuctElement, PhDuctSegment

# -- PhDuctSegment ---


def test_default_segment():
    o1 = PhDuctSegment.default()
    assert o1


def test_default_segment_round_trip():
    o1 = PhDuctSegment.default()
    d1 = o1.to_dict()

    o2 = PhDuctSegment.from_dict(d1)
    assert o2.to_dict() == d1


def test_custom_segment_length():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)

    assert o1.length == 12


def test_custom_segment_round_trip():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)
    d1 = o1.to_dict()

    o2 = PhDuctSegment.from_dict(d1)
    assert o2.to_dict() == d1

    # -- With user-data
    o2.user_data["test_key"] = "test_value"
    assert "test_key" in o2.user_data
    assert "test_key" not in o1.user_data
    assert o2.to_dict() != o1.to_dict()


def test_custom_segment_duplicate():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)
    o2 = o1.duplicate()

    assert o2.to_dict() == o1.to_dict()


# -- PhDuctElement ---


def test_default_supply_element():
    o1 = PhDuctElement.default_supply_duct()
    assert o1


def test_default_exhaust_element():
    o1 = PhDuctElement.default_exhaust_duct()
    assert o1


def test_default_element_round_trip():
    o1 = PhDuctElement.default_supply_duct()
    d1 = o1.to_dict()

    o2 = PhDuctElement.from_dict(d1)
    assert o2.to_dict() == d1

    # -- With user-data
    o2.user_data["test_key"] = "test_value"
    assert "test_key" in o2.user_data
    assert "test_key" not in o1.user_data
    assert o2.to_dict() != o1.to_dict()


def test_custom_element_round_trip():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())

    d1 = ele1.to_dict()

    o2 = PhDuctElement.from_dict(d1)
    assert o2.to_dict() == d1


def test_custom_element_duplicate():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())

    ele2 = ele1.duplicate()

    assert ele1.to_dict() == ele2.to_dict()
