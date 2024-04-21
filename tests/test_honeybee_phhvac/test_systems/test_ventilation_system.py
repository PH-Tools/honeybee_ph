from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_phhvac import ventilation
from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment
from copy import copy


def test_default_vent_system():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.PhVentilationSystem.from_dict(d)
    assert o2.to_dict() == d


def test_copy_default_vent_system():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ToString()

    o2 = copy(o1)
    assert o2.to_dict() == o1.to_dict()


def test_sort_systems_by_identifier():
    o1 = ventilation.PhVentilationSystem()
    o1.identifier = 1

    o2 = ventilation.PhVentilationSystem()
    o2.identifier = 2

    assert o1 < o2
    assert o2 > o1


def test_duplicate_default_vent_system():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ToString()

    o2 = o1.duplicate()
    assert o2.to_dict() == o1.to_dict()


def test_vent_system_with_ventilator():
    o1 = ventilation.PhVentilationSystem()
    v1 = ventilation.Ventilator()
    o1.ventilation_unit = v1
    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.PhVentilationSystem.from_dict(d)
    assert o2.to_dict() == d


def test_duplicate_vent_system_with_ventilator():
    o1 = ventilation.PhVentilationSystem()
    v1 = ventilation.Ventilator()
    o1.ventilation_unit = v1
    assert o1.ToString()

    o2 = o1.duplicate()
    assert o2.to_dict() == o1.to_dict()


def test_add_none_ventilator():
    o1 = ventilation.PhVentilationSystem()
    assert o1.ventilation_unit == None

    o1.ventilation_unit = None
    assert o1.ventilation_unit == None


def test_supply_ducting_total_length():
    o1 = ventilation.PhVentilationSystem()
    assert o1.supply_ducting_total_length == 0

    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    d1 = PhDuctSegment(geom)
    e1 = PhDuctElement()
    e1.add_segment(d1)

    o1.add_supply_duct_element(e1)
    assert o1.supply_ducting_total_length == 12


def test_exhaust_ducting_total_length():
    o1 = ventilation.PhVentilationSystem()
    assert o1.exhaust_ducting_total_length == 0

    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    d1 = PhDuctSegment(geom)
    e1 = PhDuctElement()
    e1.add_segment(d1)

    o1.add_exhaust_duct_element(e1)
    assert o1.exhaust_ducting_total_length == 12


def test_supply_round_ducting_size_description():
    o1 = ventilation.PhVentilationSystem()
    assert o1.supply_ducting_size_description == None

    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    d1 = PhDuctSegment(geom)
    e1 = PhDuctElement()
    e1.add_segment(d1)

    o1.add_supply_duct_element(e1)
    assert o1.supply_ducting_size_description == "160.00mm Θ"


def test_exhaust_rectangular_ducting_size_description():
    o1 = ventilation.PhVentilationSystem()
    assert o1.exhaust_ducting_size_description == None

    p1 = Point3D(0, 0, 0)
    p2 = Point3D(0, 0, 12)
    geom = LineSegment3D(p1, p2)
    d1 = PhDuctSegment(geom, _width=100, _height=200)
    e1 = PhDuctElement()
    e1.add_segment(d1)

    o1.add_exhaust_duct_element(e1)
    assert o1.exhaust_ducting_size_description == "100mm x 200mm"
