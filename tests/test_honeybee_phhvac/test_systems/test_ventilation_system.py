from copy import copy

from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_phhvac import ventilation
from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment


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
    assert o1.supply_ducting_size_description == "0.160 Θ"


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
    assert o1.exhaust_ducting_size_description == "100.000 x 200.000"


# -- Transforms -------


def test_scale_system_with_no_ducts():
    o1 = ventilation.PhVentilationSystem()
    o1.scale(0.0254)
    assert o1.supply_ducting_total_length == 0
    assert o1.exhaust_ducting_total_length == 0


def test_scale_system_with_single_exhaust_duct():
    sys_1 = ventilation.PhVentilationSystem()

    # Build the geometry in INCHES
    pt_1 = Point3D(0, 0, 0)
    pt_2 = Point3D(0, 0, 144)
    line_seg_1 = LineSegment3D(pt_1, pt_2)
    duct_seg_1 = PhDuctSegment(line_seg_1, _width=12, _height=36)
    duct_ele_1 = PhDuctElement()
    duct_ele_1.add_segment(duct_seg_1)
    sys_1.add_exhaust_duct_element(duct_ele_1)

    assert sys_1.exhaust_ducting_total_length == 144
    assert sys_1.exhaust_ducting_size_description == "12.000 x 36.000"
    assert sys_1.supply_ducting_total_length == 0
    assert sys_1.supply_ducting_size_description == None

    sys_2 = sys_1.scale(0.0254)

    assert sys_1.exhaust_ducting_total_length == 144
    assert sys_1.exhaust_ducting_size_description == "12.000 x 36.000"
    assert sys_1.supply_ducting_total_length == 0
    assert sys_1.supply_ducting_size_description == None

    assert sys_2.exhaust_ducting_total_length == 3.6576
    assert sys_2.exhaust_ducting_size_description == "0.305 x 0.914"
    assert sys_2.supply_ducting_total_length == 0
    assert sys_2.supply_ducting_size_description == None


def test_scale_system_with_multiple_exhaust_ducts():
    sys_1 = ventilation.PhVentilationSystem()

    # Build the geometry in INCHES
    pt_1 = Point3D(0, 0, 0)
    pt_2 = Point3D(0, 0, 144)
    line_seg_1 = LineSegment3D(pt_1, pt_2)
    duct_seg_1 = PhDuctSegment(line_seg_1, _width=12, _height=36)
    duct_ele_1 = PhDuctElement()
    duct_ele_1.add_segment(duct_seg_1)
    sys_1.add_exhaust_duct_element(duct_ele_1)

    pt_3 = Point3D(0, 0, 0)
    pt_4 = Point3D(0, 0, 144)
    line_seg_2 = LineSegment3D(pt_3, pt_4)
    duct_seg_2 = PhDuctSegment(line_seg_2, _width=12, _height=36)
    duct_ele_2 = PhDuctElement()
    duct_ele_2.add_segment(duct_seg_2)
    sys_1.add_exhaust_duct_element(duct_ele_2)

    assert sys_1.exhaust_ducting_total_length == 288
    assert sys_1.exhaust_ducting_size_description == "12.000 x 36.000"
    assert sys_1.supply_ducting_total_length == 0
    assert sys_1.supply_ducting_size_description == None

    sys_2 = sys_1.scale(0.0254)

    assert sys_1.exhaust_ducting_total_length == 288
    assert sys_1.exhaust_ducting_size_description == "12.000 x 36.000"
    assert sys_1.supply_ducting_total_length == 0
    assert sys_1.supply_ducting_size_description == None

    assert sys_2.exhaust_ducting_total_length == 7.3152
    assert sys_2.exhaust_ducting_size_description == "0.305 x 0.914"
    assert sys_2.supply_ducting_total_length == 0
    assert sys_2.supply_ducting_size_description == None


def test_scale_system_with_single_supply_duct():
    sys_1 = ventilation.PhVentilationSystem()

    # Build the geometry in INCHES
    pt_1 = Point3D(0, 0, 0)
    pt_2 = Point3D(0, 0, 144)
    line_seg_1 = LineSegment3D(pt_1, pt_2)
    duct_seg_1 = PhDuctSegment(line_seg_1, _diameter=6)
    duct_ele_1 = PhDuctElement()
    duct_ele_1.add_segment(duct_seg_1)
    sys_1.add_supply_duct_element(duct_ele_1)

    assert sys_1.supply_ducting_total_length == 144
    assert sys_1.supply_ducting_size_description == "6.000 Θ"
    assert sys_1.exhaust_ducting_total_length == 0
    assert sys_1.exhaust_ducting_size_description == None

    sys_2 = sys_1.scale(0.0254)

    assert sys_1.supply_ducting_total_length == 144
    assert sys_1.supply_ducting_size_description == "6.000 Θ"
    assert sys_1.exhaust_ducting_total_length == 0
    assert sys_1.exhaust_ducting_size_description == None

    assert sys_2.supply_ducting_total_length == 3.6576
    assert sys_2.supply_ducting_size_description == "0.152 Θ"
    assert sys_2.exhaust_ducting_total_length == 0
    assert sys_2.exhaust_ducting_size_description == None


def test_scale_system_with_multiple_supply_ducts():
    sys_1 = ventilation.PhVentilationSystem()

    # Build the geometry in INCHES
    pt_1 = Point3D(0, 0, 0)
    pt_2 = Point3D(0, 0, 144)
    line_seg_1 = LineSegment3D(pt_1, pt_2)
    duct_seg_1 = PhDuctSegment(line_seg_1, _diameter=6)
    duct_ele_1 = PhDuctElement()
    duct_ele_1.add_segment(duct_seg_1)
    sys_1.add_supply_duct_element(duct_ele_1)

    pt_3 = Point3D(0, 0, 0)
    pt_4 = Point3D(0, 0, 144)
    line_seg_2 = LineSegment3D(pt_3, pt_4)
    duct_seg_2 = PhDuctSegment(line_seg_2, _diameter=6)
    duct_ele_2 = PhDuctElement()
    duct_ele_2.add_segment(duct_seg_2)
    sys_1.add_supply_duct_element(duct_ele_2)

    assert sys_1.supply_ducting_total_length == 288
    assert sys_1.supply_ducting_size_description == "6.000 Θ"
    assert sys_1.exhaust_ducting_total_length == 0
    assert sys_1.exhaust_ducting_size_description == None

    sys_2 = sys_1.scale(0.0254)

    assert sys_1.supply_ducting_total_length == 288
    assert sys_1.supply_ducting_size_description == "6.000 Θ"
    assert sys_1.exhaust_ducting_total_length == 0
    assert sys_1.exhaust_ducting_size_description == None

    assert sys_2.supply_ducting_total_length == 7.3152
    assert sys_2.supply_ducting_size_description == "0.152 Θ"
    assert sys_2.exhaust_ducting_total_length == 0
    assert sys_2.exhaust_ducting_size_description == None
