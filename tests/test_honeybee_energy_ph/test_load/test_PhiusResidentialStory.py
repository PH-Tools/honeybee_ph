from honeybee_energy_ph.load.phius_mf import PhiusResidentialStory
from pytest import approx


def test_phius_residential_story():
    phius_story = PhiusResidentialStory([])
    assert phius_story.story_number == "001"


# -----------------------------------------------------------------------------
# -- Test the class


def test_sort_phius_residential_stories():
    a = PhiusResidentialStory([])
    a.story_number = "001"

    b = PhiusResidentialStory([])
    b.story_number = "002"

    c = PhiusResidentialStory([])
    c.story_number = "003"

    d = PhiusResidentialStory([])
    d.story_number = "004"

    stories_sorted = sorted([d, b, c, a])
    assert stories_sorted == [a, b, c, d]


# -----------------------------------------------------------------------------
# -- Test the calculation methods


def test_phius_residential_story_calc_mel():
    phius_story = PhiusResidentialStory([])
    assert phius_story.calc_mel() == 0.0

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 278.7091  # 3000 ft2
    phius_story.total_number_dwellings = 3
    phius_story.total_number_bedrooms = 6
    assert phius_story.calc_mel() == approx(3_506.39, rel=1e-5)

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 2_229.673  # 24_000 ft2
    phius_story.total_number_dwellings = 30
    phius_story.total_number_bedrooms = 60
    assert phius_story.calc_mel() == approx(30_695.98, rel=1e-6)


def test_phius_residential_story_calc_int_lighting():
    phius_story = PhiusResidentialStory([])
    assert phius_story.calc_lighting_int() == 0.0

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 278.7091  # 3000 ft2
    phius_story.total_number_dwellings = 3
    phius_story.total_number_bedrooms = 6
    assert phius_story.calc_lighting_int() == approx(1_253.64, rel=1e-5)

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 2_229.673  # 24_000 ft2
    phius_story.total_number_dwellings = 30
    phius_story.total_number_bedrooms = 60
    assert phius_story.calc_lighting_int() == approx(10_938.16, rel=1e-6)


def test_phius_residential_story_calc_ext_lighting():
    phius_story = PhiusResidentialStory([])
    assert phius_story.calc_lighting_ext() == 0.0

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 278.7091  # 3000 ft2
    phius_story.total_number_dwellings = 3
    phius_story.total_number_bedrooms = 6
    assert phius_story.calc_lighting_ext() == approx(90.00, rel=1e-5)

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 2_229.673  # 24_000 ft2
    phius_story.total_number_dwellings = 30
    phius_story.total_number_bedrooms = 60
    assert phius_story.calc_lighting_ext() == approx(840.00, rel=1e-6)


def test_phius_residential_story_calc_garage_lighting():
    phius_story = PhiusResidentialStory([])
    assert phius_story.calc_lighting_garage() == 0.0

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 278.7091  # 3000 ft2
    phius_story.total_number_dwellings = 3
    phius_story.total_number_bedrooms = 6
    assert phius_story.calc_lighting_garage() == approx(60.00, rel=1e-5)

    # -- Set the fake data
    phius_story.total_floor_area_m2 = 2_229.673  # 24_000 ft2
    phius_story.total_number_dwellings = 30
    phius_story.total_number_bedrooms = 60
    assert phius_story.calc_lighting_garage() == approx(600.00, rel=1e-6)
