import honeybee_ph.location


def test_climate_ground():
    grnd = honeybee_ph.location.Climate_Ground()

    assert grnd


def test_climate_Ground_serialization():
    grnd = honeybee_ph.location.Climate_Ground()
    d = grnd.to_dict()
    new_o = honeybee_ph.location.Climate_Ground.from_dict(d)

    assert new_o.to_dict() == d
