from honeybee_energy_ph.load.phius_mf import PhiusNonResRoom, PhiusResidentialStory
from honeybee_ph import space


def test_phius_residential_story():
    phius_story = PhiusResidentialStory([], "M2")
    assert phius_story.story_number == "001"


# -----------------------------------------------------------------------------
# -- Test the class


def test_sort_phius_residential_stories():
    a = PhiusResidentialStory([], "M2")
    a.story_number = "001"

    b = PhiusResidentialStory([], "M2")
    b.story_number = "002"

    c = PhiusResidentialStory([], "M2")
    c.story_number = "003"

    d = PhiusResidentialStory([], "M2")
    d.story_number = "004"

    stories_sorted = sorted([d, b, c, a])
    assert stories_sorted == [a, b, c, d]


def test_phius_mf_non_res():
    a = PhiusNonResRoom()
    assert a is not None


def test_phius_mf_non_res_from_space(floor_segment_geometry):
    sp = space.Space()

    # Build the Floor Segments
    flr_seg_1 = space.SpaceFloorSegment()
    flr_seg_1.geometry = floor_segment_geometry.flr_segment_1

    # Build the Floors
    floor_1 = space.SpaceFloor()
    floor_1.add_floor_segment(flr_seg_1)
    floor_1.geometry = floor_segment_geometry.flr_segment_1

    # Build the Volumes
    vol_1 = space.SpaceVolume()
    vol_1.floor = floor_1
    vol_1.avg_ceiling_height = 2.5

    sp.add_new_volumes([vol_1])

    a = PhiusNonResRoom.from_ph_space(sp, "M2")
    assert a.reference_floor_area_ft2 == 1076.3899999999999
    assert a.reference_floor_area_m2 == 100
