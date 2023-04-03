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
