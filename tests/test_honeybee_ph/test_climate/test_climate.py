import honeybee_ph.site


def test_climate():
    cli = honeybee_ph.site.Climate()
    assert cli


def test_climate_serialization():
    cli = honeybee_ph.site.Climate()
    d = cli.to_dict()
    new_o = honeybee_ph.site.Climate.from_dict(d)

    assert new_o.to_dict() == d
