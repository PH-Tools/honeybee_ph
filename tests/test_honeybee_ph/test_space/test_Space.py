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
