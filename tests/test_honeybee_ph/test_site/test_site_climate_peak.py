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


def test_collection_serialization_with_user_data():
    collection = site.Climate_PeakLoadCollection()
    collection.user_data["test_key"] = "test_value"
    d = collection.to_dict()
    new_obj = site.Climate_PeakLoadCollection.from_dict(d)

    assert "test_key" in new_obj.user_data
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


def test_peak_load_collection_deserialization_when_identifier_is_missing():
    """when deserializing from dict, if identifier is missing, (old hbjson files))"""
    obj_1 = site.Climate_PeakLoadCollection()
    d1 = obj_1.to_dict()
    d1.pop("identifier", None)
    obj_2 = site.Climate_PeakLoadCollection.from_dict(d1)

    assert obj_2.identifier != obj_1.identifier
    assert isinstance(obj_2, site.Climate_PeakLoadCollection)
    assert obj_1.to_dict() != obj_2.to_dict()
