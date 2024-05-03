import pytest
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_ph import space

TOL = 0.00001


def test_basic_floor_segment(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    assert seg.floor_area == 100


def test_basic_floor_segment_floor_area_weighting(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    assert seg.floor_area == 100
    assert seg.weighted_floor_area == 100

    seg.weighting_factor = 0.5
    assert seg.floor_area == 100
    assert seg.weighted_floor_area == 50

    seg.weighting_factor = 0.734
    assert seg.floor_area == 100
    assert seg.weighted_floor_area == 73.4


def test_floor_segment_no_geometry():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 1.0
    assert seg.floor_area == 0
    assert seg.weighted_floor_area == 0


# -- Serialization --


def test_flr_seg_serialization_without_geom():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 0.74

    d1 = seg.to_dict()
    o = space.SpaceFloorSegment.from_dict(d1)
    d2 = o.to_dict()
    assert d1 == d2


def test_flr_seg_serialization_with_geom(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 0.74

    d1 = seg.to_dict()
    o = space.SpaceFloorSegment.from_dict(d1)
    d2 = o.to_dict()
    assert d1 == d2


def test_flr_seg_serialization_with_geom_and_mesh(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 0.74

    d1 = seg.to_dict(include_mesh=True)
    o = space.SpaceFloorSegment.from_dict(d1)
    d2 = o.to_dict(include_mesh=True)
    assert d1 == d2


# -- Duplication --


def test_flr_seg_duplication_no_geom():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 0.856

    seg2 = seg.duplicate()
    assert seg.geometry == seg2.geometry
    assert seg.weighting_factor == seg2.weighting_factor
    assert seg.reference_point == seg2.reference_point
    assert seg.weighted_floor_area == seg2.weighted_floor_area


def test_flr_seg_duplication_with_geom(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 0.856

    seg2 = seg.duplicate()
    assert seg.geometry == seg2.geometry
    assert seg.weighting_factor == seg2.weighting_factor
    assert seg.reference_point == seg2.reference_point
    assert seg.weighted_floor_area == seg2.weighted_floor_area


def test_flr_seg_duplication_with_reference_point_at_0_0_0(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 0.856
    seg.reference_point = Point3D(0, 0, 0)

    seg2 = seg.duplicate()
    assert seg.geometry == seg2.geometry
    assert seg.weighting_factor == seg2.weighting_factor
    assert seg.reference_point == seg2.reference_point
    assert seg.weighted_floor_area == seg2.weighted_floor_area


def test_flr_seg_duplication_with_reference_point(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 0.856
    seg.reference_point = Point3D(1, 2, 3)

    seg2 = seg.duplicate()
    assert seg.geometry == seg2.geometry
    assert seg.weighting_factor == seg2.weighting_factor
    assert seg.reference_point == seg2.reference_point
    assert seg.weighted_floor_area == seg2.weighted_floor_area


def test_flr_seg_duplication_geom_only_without_geom():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 0.856

    with pytest.raises(AttributeError):
        seg.duplicate_geometry()


def test_flr_seg_duplication_geom_only_with_geom(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 0.856

    new_geom = seg.duplicate_geometry()
    assert seg.geometry == new_geom


# -- Transform With Geometry --


def test_floor_segment_scale_M_to_FOOT(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    assert seg.floor_area == 100

    seg2 = seg.scale(3.28084)  # M --> FOOT
    assert seg.floor_area == 100
    assert seg2.floor_area == pytest.approx(1_076.39111056)


def test_floor_segment_scale_M_to_INCH(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    assert seg.floor_area == 100

    seg2 = seg.scale(39.37007874)  # M --> INCH
    assert seg.floor_area == 100
    assert seg2.floor_area == pytest.approx(155_000.31)


def test_floor_segment_scale_M_to_CM(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    assert seg.floor_area == 100

    seg2 = seg.scale(100)  # M --> CM
    assert seg.floor_area == 100
    assert seg2.floor_area == pytest.approx(1_000_000)


def test_floor_segment_scale_M_to_MM(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    assert seg.floor_area == 100

    seg2 = seg.scale(1_000)  # M --> MM
    assert seg.floor_area == 100
    assert seg2.floor_area == pytest.approx(100_000_000)


def test_floor_segment_move(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    seg.reference_point = Point3D(5, 5, 0)
    assert seg.floor_area == 100
    assert seg.reference_point is not None
    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)

    seg2 = seg.move(Vector3D(1, 0, 0))
    assert seg.floor_area == 100
    assert seg2.floor_area == 100

    assert seg.reference_point == Point3D(5, 5, 0)
    assert seg2.reference_point == Point3D(6, 5, 0)


def test_floor_segment_rotate(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    seg.reference_point = Point3D(5, 5, 0)
    assert seg.floor_area == 100
    assert seg.reference_point is not None
    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)

    seg2 = seg.rotate(Vector3D(0, 0, 1), 90, Point3D(0, 0, 0))
    assert seg.floor_area == 100
    assert seg2.floor_area == 100

    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)
    assert seg2.reference_point is not None
    assert seg2.reference_point.is_equivalent(Point3D(-5, 5, 0), TOL)


def test_floor_segment_rotate_xy(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    seg.reference_point = Point3D(5, 5, 0)
    assert seg.floor_area == 100
    assert seg.reference_point is not None
    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)

    seg2 = seg.rotate_xy(90, Point3D(0, 0, 0))
    assert seg.floor_area == 100
    assert seg2.floor_area == 100

    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)
    assert seg2.reference_point is not None
    assert seg2.reference_point.is_equivalent(Point3D(-5, 5, 0), TOL)


def test_floor_segment_reflect(floor_segment_geometry):
    seg = space.SpaceFloorSegment()
    seg.geometry = floor_segment_geometry.flr_segment_1
    seg.weighting_factor = 1.0
    seg.reference_point = Point3D(5, 5, 0)
    assert seg.floor_area == 100
    assert seg.reference_point is not None
    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)

    seg2 = seg.reflect(Vector3D(0, 1, 0), Point3D(0, 0, 0))
    assert seg.floor_area == 100
    assert seg2.floor_area == 100

    assert seg.reference_point.is_equivalent(Point3D(5, 5, 0), TOL)
    assert seg2.reference_point is not None
    assert seg2.reference_point.is_equivalent(Point3D(5, -5, 0), TOL)


# -- Transform Without Geometry --


def test_floor_segment_scale_no_geometry():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 1.0
    assert seg.floor_area == 0

    seg2 = seg.scale(1_000)  # M --> MM
    assert seg.floor_area == 0
    assert seg2.floor_area == 0


def test_floor_segment_move_no_geometry():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 1.0
    assert seg.floor_area == 0

    seg2 = seg.move(Vector3D(1, 0, 0))
    assert seg.floor_area == 0
    assert seg2.floor_area == 0


def test_floor_segment_rotate_no_geometry():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 1.0
    assert seg.floor_area == 0

    seg2 = seg.rotate(Vector3D(0, 0, 1), 90, Point3D(0, 0, 0))
    assert seg.floor_area == 0
    assert seg2.floor_area == 0


def test_floor_segment_rotate_xy_no_geometry():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 1.0
    assert seg.floor_area == 0

    seg2 = seg.rotate_xy(90, Point3D(0, 0, 0))
    assert seg.floor_area == 0
    assert seg2.floor_area == 0


def test_floor_segment_reflect_no_geometry():
    seg = space.SpaceFloorSegment()
    seg.weighting_factor = 1.0
    assert seg.floor_area == 0

    seg2 = seg.reflect(Vector3D(0, 1, 0), Point3D(0, 0, 0))
    assert seg.floor_area == 0
    assert seg2.floor_area == 0
