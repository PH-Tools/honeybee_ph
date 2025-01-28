from pytest import approx

from honeybee_energy_ph.load.phius_mf import PhiusResidentialStory


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
