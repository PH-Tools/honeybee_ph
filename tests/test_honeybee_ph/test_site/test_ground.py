import honeybee_ph.site


def test_climate_ground():
    grnd = honeybee_ph.site.Climate_Ground()

    assert grnd


def test_climate_Ground_serialization():
    grnd = honeybee_ph.site.Climate_Ground()
    d = grnd.to_dict()
    new_o = honeybee_ph.site.Climate_Ground.from_dict(d)

    assert new_o.to_dict() == d


def test_climate_Ground_serialization_with_user_data():
    grnd = honeybee_ph.site.Climate_Ground()
    grnd.user_data["test_key"] = "test_value"
    d = grnd.to_dict()
    new_o = honeybee_ph.site.Climate_Ground.from_dict(d)

    assert "test_key" in new_o.user_data
    assert new_o.to_dict() == d


def test_climate_Ground_deserialization_when_identifier_is_missing():
    """when deserializing from dict, if identifier is missing, (old hbjson files))"""
    ground_1 = honeybee_ph.site.Climate_Ground()
    d1 = ground_1.to_dict()
    d1.pop("identifier", None)
    ground_2 = honeybee_ph.site.Climate_Ground.from_dict(d1)

    assert ground_2.identifier != ground_1.identifier
    assert isinstance(ground_2, honeybee_ph.site.Climate_Ground)
    assert ground_1.to_dict() != ground_2.to_dict()


def test_duplicate_climate_Ground():
    grnd = honeybee_ph.site.Climate_Ground()
    grnd.user_data["test_key"] = "test_value"
    new_grnd = grnd.duplicate()

    assert new_grnd.user_data == grnd.user_data
    assert new_grnd.to_dict() == grnd.to_dict()
    assert new_grnd.identifier == grnd.identifier
    assert isinstance(new_grnd, honeybee_ph.site.Climate_Ground)
    assert isinstance(new_grnd, honeybee_ph.site._base._Base)
    assert "test_key" in new_grnd.user_data
