from honeybee_ph import site


def test_Climate_PeakLoadValueSet_to_from_dict_roundtrip():
    o = site.Climate_PeakLoadValueSet()
    d = o.to_dict()
    new_obj = site.Climate_PeakLoadValueSet.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_PeakLoadValueSet_to_from_dict_duplicate():
    o = site.Climate_PeakLoadValueSet()
    new_obj = o.duplicate()
    assert new_obj.to_dict() == o.to_dict()


def test_Climate_PeakLoadValueSet_to_from_dict_with_values():
    o = site.Climate_PeakLoadValueSet()

    o.temp = 1
    o.rad_north = 2
    o.rad_east = 3
    o.rad_south = 4
    o.rad_west = 5
    o.rad_global = 6

    d = o.to_dict()
    new_obj = site.Climate_PeakLoadValueSet.from_dict(d)

    assert new_obj.to_dict() == d


def test_Climate_PeakLoadValueSet_to_from_dict_with_values_duplicate():
    o = site.Climate_PeakLoadValueSet()

    o.temp = 1
    o.rad_north = 2
    o.rad_east = 3
    o.rad_south = 4
    o.rad_west = 5
    o.rad_global = 6

    new_obj = site.Climate_PeakLoadValueSet.from_dict(o.to_dict())

    assert new_obj.temp == 1
    assert new_obj.rad_north == 2
    assert new_obj.rad_east == 3
    assert new_obj.rad_south == 4
    assert new_obj.rad_west == 5
    assert new_obj.rad_global == 6
