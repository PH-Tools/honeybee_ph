import honeybee_ph.site


def test_climate_location():
    loc = honeybee_ph.site.Location()

    assert loc


def test_climate_location_serialization():
    loc = honeybee_ph.site.Location()
    d = loc.to_dict()
    new_o = honeybee_ph.site.Location.from_dict(d)

    assert new_o.to_dict() == d
