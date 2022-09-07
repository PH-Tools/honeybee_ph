from honeybee_ph import site


def test_peak_load_value_set_serialization():
    o = site.Climate_PeakLoadValueSet()
    d = o.to_dict()
    new_obj = site.Climate_PeakLoadValueSet.from_dict(d)

    assert new_obj.to_dict() == d


def test_collection_empty():
    collection = site.Climate_PeakLoadCollection()
    assert collection


def test_collection_serialization_empty():
    collection = site.Climate_PeakLoadCollection()
    d = collection.to_dict()
    new_obj = site.Climate_PeakLoadCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_collection_serialization_with_values():
    collection = site.Climate_PeakLoadCollection()

    collection.heat_load_1.temp = 1
    collection.heat_load_1.rad_north = 2
    collection.heat_load_1.rad_east = 3
    collection.heat_load_1.rad_south = 4
    collection.heat_load_1.rad_west = 5
    collection.heat_load_1.rad_global = 6

    d = collection.to_dict()
    new_obj = site.Climate_PeakLoadCollection.from_dict(d)

    assert new_obj.to_dict() == d
