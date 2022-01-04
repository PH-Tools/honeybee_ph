import honeybee_ph.climate


def test_climate_location():
    loc = honeybee_ph.climate.Climate_Location()

    assert loc


def test_climate_location_serialization():
    loc = honeybee_ph.climate.Climate_Location()
    d = loc.to_dict()
    new_o = honeybee_ph.climate.Climate_Location.from_dict(d)

    assert new_o.to_dict() == d
