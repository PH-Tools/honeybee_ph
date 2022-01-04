import honeybee_ph.climate


def test_collection_empty():
    collection = honeybee_ph.climate.Climate_PeakLoadCollection()
    assert collection


def test_collection_serialization_empty():
    collection = honeybee_ph.climate.Climate_PeakLoadCollection()
    d = collection.to_dict()
    new_obj = honeybee_ph.climate.Climate_PeakLoadCollection.from_dict(d)

    assert new_obj.to_dict() == d


def test_collection_serialization_with_values():
    collection = honeybee_ph.climate.Climate_PeakLoadCollection()

    collection.temp = 1
    collection.rad_north = 2
    collection.rad_east = 3
    collection.rad_south = 4
    collection.rad_west = 5
    collection.rad_global = 6

    d = collection.to_dict()
    new_obj = honeybee_ph.climate.Climate_PeakLoadCollection.from_dict(d)

    assert new_obj.to_dict() == d
