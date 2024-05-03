import pytest
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment

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
    assert id(o1) != id(o2)


def test_round_segment_shape_type():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)

    assert o1.shape_type == 1


def test_is_round():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)

    assert o1.is_round_duct == True


def test_rectangular_segment_shape_type():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)
    o1.width = 100
    o1.height = 200

    assert o1.shape_type == 2


def test_is_not_round():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)
    o1.width = 100
    o1.height = 200

    assert o1.is_round_duct == False


def test_shape_type_description_round():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)

    assert o1.shape_type_description == "0.160 Θ"


def test_shape_type_description_rectangular():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)
    o1.width = 100
    o1.height = 200

    assert o1.shape_type_description == "100.000 x 200.000"


def test_PhDuctSegment_duplicate():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    o1 = PhDuctSegment(geom)
    o2 = o1.duplicate()

    assert o1.to_dict() == o2.to_dict()
    assert id(o1) != id(o2)


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
    assert id(ele1) != id(ele2)


def test_element_is_round():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())

    assert ele1.is_round_duct == True


def test_single_round_element_shape_type_description():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())

    assert ele1.shape_type_description == "0.160 Θ"


def test_multiple_round_element_shape_type_description():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())
    ele1.add_segment(PhDuctSegment.default())

    assert ele1.shape_type_description == "0.160 Θ"


def test_multiple_round_elements_with_different_shape_type_description_raises_error():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment(_geom=geom, _diameter=160))
    ele1.add_segment(PhDuctSegment(_geom=geom, _diameter=150))

    with pytest.raises(ValueError):
        assert ele1.shape_type_description == "160.00mm Θ"


def test_element_is_not_round():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())
    ele1.segments[0].width = 100
    ele1.segments[0].height = 200

    assert ele1.is_round_duct == False


def test_single_rectangular_element_shape_type_description():
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment.default())
    ele1.segments[0].width = 100
    ele1.segments[0].height = 200

    assert ele1.shape_type_description == "100.000 x 200.000"


def test_multiple_rectangular_with_same_shape_shape_type_description():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment(geom, _width=100, _height=200))
    ele1.add_segment(PhDuctSegment(geom, _width=100, _height=200))

    assert ele1.shape_type_description == "100.000 x 200.000"


def test_multiple_rectangular_with_different_shape_shape_type_description_raises_error():
    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    ele1 = PhDuctElement()
    ele1.add_segment(PhDuctSegment(geom, _width=100, _height=200))
    ele1.add_segment(PhDuctSegment(geom, _width=150, _height=200))

    with pytest.raises(ValueError):
        assert ele1.shape_type_description == "100mm x 200mm"
