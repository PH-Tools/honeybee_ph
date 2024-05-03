import pytest
from honeybee.units import conversion_factor_to_meters
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_phhvac.ducting import PhDuctElement, PhDuctSegment

INCH_TO_METER_FACTOR = conversion_factor_to_meters("Inches")


# -- Scale individual Duct Segments --------


def test_segment_with_diam_scale_from_inches():
    seg_1 = PhDuctSegment(
        _geom=LineSegment3D(Point3D(0, 0, 0), Vector3D(39.3701, 0, 0)),
        _insul_thickness=1.0,
        _diameter=6.0,
    )

    assert seg_1.length == pytest.approx(39.3701)
    assert seg_1.insulation_thickness == pytest.approx(1.0)
    assert seg_1.diameter == pytest.approx(6.0)
    assert seg_1.width is None
    assert seg_1.height is None

    seg_2 = seg_1.scale(INCH_TO_METER_FACTOR)

    assert seg_1.length == pytest.approx(39.3701)
    assert seg_1.insulation_thickness == pytest.approx(1.0)
    assert seg_1.diameter == pytest.approx(6.0)
    assert seg_1.width is None
    assert seg_1.height is None

    assert seg_2.length == pytest.approx(1.0)
    assert seg_2.insulation_thickness == pytest.approx(0.0254)
    assert seg_2.diameter == pytest.approx(0.1524)
    assert seg_2.width is None
    assert seg_2.height is None


def test_segment_with_height_and_width_scale_from_inches():
    seg_1 = PhDuctSegment(
        _geom=LineSegment3D(Point3D(0, 0, 0), Vector3D(39.3701, 0, 0)),
        _insul_thickness=1.0,
        _width=12.0,
        _height=6.0,
    )

    assert seg_1.length == pytest.approx(39.3701)
    assert seg_1.insulation_thickness == pytest.approx(1.0)
    assert seg_1.diameter == pytest.approx(0.16)
    assert seg_1.width == pytest.approx(12.0)
    assert seg_1.height == pytest.approx(6.0)

    seg_2 = seg_1.scale(INCH_TO_METER_FACTOR)

    assert seg_1.length == pytest.approx(39.3701)
    assert seg_1.insulation_thickness == pytest.approx(1.0)
    assert seg_1.diameter == pytest.approx(0.16)
    assert seg_1.width == pytest.approx(12.0)
    assert seg_1.height == pytest.approx(6.0)

    assert seg_2.length == pytest.approx(1.0)
    assert seg_2.insulation_thickness == pytest.approx(0.0254)
    assert seg_2.diameter == pytest.approx(0.004064)
    assert seg_2.width == pytest.approx(0.3048)
    assert seg_2.height == pytest.approx(0.1524)


# -- Scale Duct Elements --------


def test_scale_duct_element_with_single_segment():
    seg_1 = PhDuctSegment(
        _geom=LineSegment3D(Point3D(0, 0, 0), Vector3D(39.3701, 0, 0)),
        _insul_thickness=1.0,
        _diameter=6.0,
    )
    duct = PhDuctElement()
    duct.add_segment(seg_1)
    duct_2 = duct.scale(INCH_TO_METER_FACTOR)
    assert duct.length == pytest.approx(39.3701)
    assert duct_2.length == pytest.approx(1.0)


def test_scale_duct_element_with_multiple_segments():
    seg_1 = PhDuctSegment(
        _geom=LineSegment3D(Point3D(0, 0, 0), Vector3D(39.3701, 0, 0)),
        _insul_thickness=1.0,
        _diameter=6.0,
    )
    seg_2 = PhDuctSegment(
        _geom=LineSegment3D(Point3D(39.3701, 0, 0), Vector3D(39.3701, 0, 0)),
        _insul_thickness=1.0,
        _diameter=6.0,
    )
    duct = PhDuctElement()
    duct.add_segment(seg_1)
    duct.add_segment(seg_2)
    duct_2 = duct.scale(INCH_TO_METER_FACTOR)
    assert duct.length == pytest.approx(78.7402)
    assert duct_2.length == pytest.approx(2.0)
