import honeybee_ph.site


def test_climate_location():
    loc = honeybee_ph.site.Location()

    assert loc


def test_climate_location_serialization():
    loc = honeybee_ph.site.Location()
    d = loc.to_dict()
    new_o = honeybee_ph.site.Location.from_dict(d)

    assert new_o.to_dict() == d


def test_climate_location_serialization_with_user_data():
    loc = honeybee_ph.site.Location()
    loc.user_data["test_key"] = "test_value"
    d = loc.to_dict()
    new_o = honeybee_ph.site.Location.from_dict(d)

    assert "test_key" in new_o.user_data
    assert new_o.to_dict() == d


def test_location_deserialization_when_identifier_is_missing():
    """when deserializing from dict, if identifier is missing, (old hbjson files))"""
    obj_1 = honeybee_ph.site.Location()
    d1 = obj_1.to_dict()
    d1.pop("identifier", None)
    obj_2 = honeybee_ph.site.Location.from_dict(d1)

    assert obj_2.identifier != obj_1.identifier
    assert isinstance(obj_2, honeybee_ph.site.Location)
    assert obj_1.to_dict() != obj_2.to_dict()
