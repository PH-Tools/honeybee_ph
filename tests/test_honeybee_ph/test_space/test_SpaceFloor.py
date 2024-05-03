import pytest
from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D

from honeybee_ph import space


def test_floor(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)

    assert seg1 in floor.floor_segments

    seg2 = space.SpaceFloorSegment()
    seg2.geometry = floor_segment_geometry.flr_segment_2

    floor.add_floor_segment(seg2)

    assert seg1 in floor.floor_segments
    assert seg2 in floor.floor_segments


# -- Serialize ---


def test_floor_serialize_without_segments():
    floor = space.SpaceFloor()

    d1 = floor.to_dict()
    o = space.SpaceFloor.from_dict(d1)
    d2 = o.to_dict()

    assert d1 == d2


def test_floor_serialize_with_segments(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    d1 = floor.to_dict()
    o = space.SpaceFloor.from_dict(d1)
    d2 = o.to_dict()

    assert d1 == d2


def test_floor_serialize_with_segments_and_mesh(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    d1 = floor.to_dict(include_mesh=True)
    o = space.SpaceFloor.from_dict(d1)
    d2 = o.to_dict(include_mesh=True)

    assert d1 == d2


# -- Duplicate ---


def test_duplicate_floor(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1

    seg2 = space.SpaceFloorSegment()
    seg2.weighting_factor = 1.0
    seg2.geometry = floor_segment_geometry.flr_segment_2

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.add_floor_segment(seg2)

    dup_floor = floor.duplicate()

    assert floor.geometry == dup_floor.geometry
    assert len(floor.floor_segments) == len(dup_floor.floor_segments)
    assert floor.floor_area == dup_floor.floor_area
    assert floor.weighted_floor_area == dup_floor.weighted_floor_area


def test_duplicate_floor_geometry_success(floor_segment_geometry):
    floor = space.SpaceFloor()
    floor.geometry = floor_segment_geometry.flr_segment_1

    dup_floor_geom = floor.duplicate_geometry()

    assert floor.geometry == dup_floor_geom


def test_duplicate_floor_geometry_fail():
    floor = space.SpaceFloor()
    with pytest.raises(Exception):
        floor.duplicate_geometry()


# -- Transforms ---


def test_scale_floor_single_segment(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    floor2 = floor.scale(3.28084)  # M --> FOOT
    assert floor2.floor_area == pytest.approx(1_076.39111056)
    assert floor2.weighted_floor_area == pytest.approx(1_076.39111056)
    assert floor2.geometry is not None
    assert floor2.geometry.area == pytest.approx(1_076.39111056)


def test_scale_floor_multiple_segments(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1

    seg2 = space.SpaceFloorSegment()
    seg2.weighting_factor = 1.0
    seg2.geometry = floor_segment_geometry.flr_segment_2

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.add_floor_segment(seg2)

    assert floor.floor_area == 200
    assert floor.weighted_floor_area == 200

    floor2 = floor.scale(3.28084)  # M --> FOOT
    assert floor.floor_area == 200
    assert floor.weighted_floor_area == 200
    assert floor2.floor_area == pytest.approx(2_152.7822)
    assert floor2.weighted_floor_area == pytest.approx(2_152.7822)

    floor3 = floor2.scale(0.305)  # FOOT --> M
    assert floor.floor_area == 200
    assert floor.weighted_floor_area == 200
    assert floor2.floor_area == pytest.approx(2_152.7822)
    assert floor2.weighted_floor_area == pytest.approx(2_152.7822)
    assert floor3.floor_area == pytest.approx(200.262566119688)
    assert floor3.weighted_floor_area == pytest.approx(200.262566119688)


def test_move_floor_single_segment(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.reference_point = Point3D(5, 5, 0)

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    floor2 = floor.move(Vector3D(1, 0, 0))
    assert floor2.floor_area == pytest.approx(100)
    assert floor2.reference_points[0] == Point3D(6, 5, 0)


def test_rotate_floor_single_segment(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.reference_point = Point3D(5, 5, 0)

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    floor2 = floor.rotate(Vector3D(0, 0, 1), 90, Point3D(0, 0, 0))
    assert floor2.floor_area == pytest.approx(100)
    assert floor2.reference_points[0] == Point3D(-5, 5, 0)


def test_rotate_xy_floor_single_segment(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.reference_point = Point3D(5, 5, 0)

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    floor2 = floor.rotate_xy(90, Point3D(0, 0, 0))
    assert floor2.floor_area == pytest.approx(100)
    assert floor2.reference_points[0] == Point3D(-5, 5, 0)


def test_reflect_floor_single_segment(floor_segment_geometry):
    seg1 = space.SpaceFloorSegment()
    seg1.weighting_factor = 1.0
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.reference_point = Point3D(5, 5, 0)

    floor = space.SpaceFloor()
    floor.add_floor_segment(seg1)
    floor.geometry = floor_segment_geometry.flr_segment_1

    floor2 = floor.reflect(Vector3D(1, 0, 0), Point3D(0, 0, 0))
    assert floor2.floor_area == pytest.approx(100)
    assert floor2.reference_points[0] == Point3D(-5, 5, 0)
