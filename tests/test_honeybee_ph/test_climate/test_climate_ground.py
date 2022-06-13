import honeybee_ph.site


def test_climate_ground():
    grnd = honeybee_ph.site.Climate_Ground()

    assert grnd


def test_climate_Ground_serialization():
    grnd = honeybee_ph.site.Climate_Ground()
    d = grnd.to_dict()
    new_o = honeybee_ph.site.Climate_Ground.from_dict(d)

    assert new_o.to_dict() == d
