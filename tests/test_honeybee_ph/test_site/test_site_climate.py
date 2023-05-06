import honeybee_ph.site


def test_climate():
    cli = honeybee_ph.site.Climate()
    assert cli


def test_climate_serialization():
    cli = honeybee_ph.site.Climate()
    d = cli.to_dict()
    new_o = honeybee_ph.site.Climate.from_dict(d)

    assert new_o.to_dict() == d


def test_climate_serialization_with_user_data():
    cli = honeybee_ph.site.Climate()
    cli.user_data["test_key"] = "test_value"
    d = cli.to_dict()
    new_o = honeybee_ph.site.Climate.from_dict(d)

    assert "test_key" in new_o.user_data
    assert new_o.to_dict() == d


def test_climate_deserialization_when_identifier_is_missing():
    """when deserializing from dict, if identifier is missing, (old hbjson files))"""
    obj_1 = honeybee_ph.site.Climate()
    d1 = obj_1.to_dict()
    d1.pop("identifier", None)
    obj_2 = honeybee_ph.site.Climate.from_dict(d1)

    assert obj_2.identifier != obj_1.identifier
    assert isinstance(obj_2, honeybee_ph.site.Climate)
    assert obj_1.to_dict() != obj_2.to_dict()
