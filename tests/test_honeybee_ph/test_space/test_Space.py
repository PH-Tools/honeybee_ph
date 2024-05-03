import pytest
from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D

from honeybee_ph import space


def test_Space_avg_clear_height_even_heights(floor_segment_geometry):
    sp = space.Space()

    # Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    sp.add_new_volumes([vol_1, vol_2])

    # ((100 * 2.5)+(100 * 2.5))/(100+100) -> (250+250)/200 -> 500/200 -> 2.5
    assert sp.avg_clear_height == 2.5
    assert sp.average_floor_weighting_factor == 1.0
    assert len(sp.floor_segment_surfaces) == 2


def test_Space_avg_clear_height_uneven_heights(floor_segment_geometry):
    sp = space.Space()

    # Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 1

    sp.add_new_volumes([vol_1, vol_2])

    # ((100 * 2)+(100 * 1))/(100+100) -> (200+100)/200 -> 300/200 -> 1.5
    assert sp.avg_clear_height == 1.5
    assert sp.average_floor_weighting_factor == 1.0
    assert len(sp.floor_segment_surfaces) == 2


# -- Transforms --


def test_Space_scale(floor_segment_geometry):
    # --  Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # -- Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # -- Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    # -- Build the Space
    sp = space.Space()
    sp.add_new_volumes([vol_1, vol_2])

    # -- Scale the Space and all the Volumes, all the floors
    sp2 = sp.scale(3.28084)  # M --> FOOT

    assert sp2.floor_area == pytest.approx(2_152.7822)
    assert sp2.weighted_floor_area == pytest.approx(2_152.7822)
    assert sp2.avg_clear_height == pytest.approx(8.2021)
    assert sp2.net_volume == pytest.approx(17_657.34)
    assert sp2.average_floor_weighting_factor == 1.0
    assert len(sp2.floor_segment_surfaces) == 2


def test_Space_rotate(floor_segment_geometry):
    # --  Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # -- Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # -- Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    # -- Build the Space
    sp = space.Space()
    sp.add_new_volumes([vol_1, vol_2])

    # -- Rotate the Space and all the Volumes, all the floors
    sp2 = sp.rotate(Vector3D(0, 0, 1), 90, Point3D(0, 0, 0))  # Rotate 90 degrees around Z axis

    assert sp2.floor_area == pytest.approx(200)
    assert sp2.weighted_floor_area == pytest.approx(200)
    assert sp2.avg_clear_height == pytest.approx(2.5)
    assert sp2.net_volume == pytest.approx(500)
    assert sp2.average_floor_weighting_factor == 1.0
    assert len(sp2.floor_segment_surfaces) == 2


def test_Space_move(floor_segment_geometry):
    # --  Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # -- Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # -- Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    # -- Build the Space
    sp = space.Space()
    sp.add_new_volumes([vol_1, vol_2])

    # -- Move the Space and all the Volumes, all the floors
    sp2 = sp.move(Vector3D(1, 0, 0))

    assert sp2.floor_area == pytest.approx(200)
    assert sp2.weighted_floor_area == pytest.approx(200)
    assert sp2.avg_clear_height == pytest.approx(2.5)
    assert sp2.net_volume == pytest.approx(500)
    assert sp2.average_floor_weighting_factor == 1.0
    assert len(sp2.floor_segment_surfaces) == 2


def test_Space_reflect(floor_segment_geometry):
    # --  Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # -- Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # -- Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    # -- Build the Space
    sp = space.Space()
    sp.add_new_volumes([vol_1, vol_2])

    # -- Reflect the Space and all the Volumes, all the floors
    sp2 = sp.reflect(Vector3D(1, 0, 0), Point3D(0, 0, 0))

    assert sp2.floor_area == pytest.approx(200)
    assert sp2.weighted_floor_area == pytest.approx(200)
    assert sp2.avg_clear_height == pytest.approx(2.5)
    assert sp2.net_volume == pytest.approx(500)
    assert sp2.average_floor_weighting_factor == 1.0
    assert len(sp2.floor_segment_surfaces) == 2


# -- Serialize --


def test_Space_serialize(floor_segment_geometry):
    # --  Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # -- Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # -- Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    # -- Build the Space
    sp = space.Space()
    sp.add_new_volumes([vol_1, vol_2])

    d1 = sp.to_dict()
    o = space.Space.from_dict(d1, sp.host)
    d2 = o.to_dict()

    assert d1 == d2

    # -- Add User Data
    sp.user_data["test_key"] = "test_value"
    d3 = sp.to_dict()
    o2 = space.Space.from_dict(d3, sp.host)
    d4 = o2.to_dict()
    assert d3 == d4


# -- Duplicate --


def test_Space_duplicate(floor_segment_geometry):
    # --  Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1
    flr_seg_1.weighting_factor = 1.0

    flr_seg_2 = space.SpaceFloorSegment()
    flr_seg_2.geometry = floor_segment_geometry.flr_segment_2
    flr_seg_2.weighting_factor = 1.0

    # -- Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    floor_2 = space.SpaceFloor()
    floor_2.add_floor_segment(flr_seg_2)
    floor_2.geometry = floor_segment_geometry.flr_segment_2

    # -- Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    vol_2 = space.SpaceVolume()
    vol_2.floor = floor_2
    vol_2.avg_ceiling_height = 2.5

    # -- Build the Space
    sp = space.Space()
    sp.add_new_volumes([vol_1, vol_2])

    # -- duplicate
    new_sp = sp.duplicate(sp.host)

    # --
    assert new_sp.to_dict() == sp.to_dict()
    assert new_sp.floor_area == sp.floor_area
    assert new_sp.avg_clear_height == sp.avg_clear_height
    assert new_sp.weighted_floor_area == sp.weighted_floor_area
    assert new_sp.floor_area == sp.floor_area
    assert len(new_sp.volumes) == len(sp.volumes)
    assert len(new_sp.floor_segment_surfaces) == len(sp.floor_segment_surfaces)
    assert new_sp.quantity == sp.quantity
    assert new_sp.wufi_type == sp.wufi_type
    assert new_sp.name == sp.name
    assert new_sp.number == sp.number
    assert new_sp.host == sp.host
