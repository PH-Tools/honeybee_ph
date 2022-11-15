import pytest
from honeybee_ph import space

def test_volume(floor_segment_geometry):
    # -- Seg
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.weighting_factor = 1.0

    # -- Floor
    flr1 = space.SpaceFloor()
    flr1.add_floor_segment(seg1)
    flr1.geometry = floor_segment_geometry.flr_segment_1

    # -- Volume
    vol1 = space.SpaceVolume()
    vol1.floor = flr1

    assert vol1.floor_area == 100
    assert vol1.weighted_floor_area == 100

# -- Serialization --

def test_volume_serialize(floor_segment_geometry):
    # -- Seg
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.weighting_factor = 1.0

    # -- Floor
    flr1 = space.SpaceFloor()
    flr1.add_floor_segment(seg1)
    flr1.geometry = floor_segment_geometry.flr_segment_1

    # -- Volume
    vol1 = space.SpaceVolume()
    vol1.floor = flr1

    d1 = vol1.to_dict()
    o = space.SpaceVolume.from_dict(d1)
    d2 = o.to_dict()
    
    assert d1 == d2

# -- Scale -- 

def test_volume_scale(floor_segment_geometry):
    # -- Seg
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.weighting_factor = 1.0

    # -- Floor
    flr1 = space.SpaceFloor()
    flr1.add_floor_segment(seg1)
    flr1.geometry = floor_segment_geometry.flr_segment_1

    # -- Volume
    vol1 = space.SpaceVolume()
    vol1.floor = flr1

    assert vol1.floor_area == 100
    assert vol1.weighted_floor_area == 100
    assert vol1.avg_ceiling_height == 2.5
    assert vol1.net_volume == 250

    vol1.scale(3.28084) # M --> FOOT

    assert vol1.floor_area == pytest.approx(1_076.39111056)
    assert vol1.weighted_floor_area == pytest.approx(1_076.39111056)
    assert vol1.avg_ceiling_height == pytest.approx(8.2021)
    assert vol1.net_volume == pytest.approx(8_828.67)

# -- Duplication -- 

def test_volume_duplicate(floor_segment_geometry):
    # -- Seg
    seg1 = space.SpaceFloorSegment()
    seg1.geometry = floor_segment_geometry.flr_segment_1
    seg1.weighting_factor = 1.0

    # -- Floor
    flr1 = space.SpaceFloor()
    flr1.add_floor_segment(seg1)
    flr1.geometry = floor_segment_geometry.flr_segment_1

    # -- Volume
    vol1 = space.SpaceVolume()
    vol1.floor = flr1

    new_vol = vol1.duplicate()

    assert new_vol.avg_ceiling_height == vol1.avg_ceiling_height
    assert new_vol.floor_area == vol1.floor_area
    assert new_vol.weighted_floor_area == vol1.weighted_floor_area
    assert new_vol.net_volume == vol1.net_volume
    assert len(new_vol.floor_segment_surfaces) == len(vol1.floor_segment_surfaces)