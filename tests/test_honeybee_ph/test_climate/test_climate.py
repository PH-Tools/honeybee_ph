import honeybee_ph.location


def test_climate():
    cli = honeybee_ph.location.Climate()
    assert cli


def test_climate_serialization():
    cli = honeybee_ph.location.Climate()
    d = cli.to_dict()
    new_o = honeybee_ph.location.Climate.from_dict(d)

    assert new_o.to_dict() == d
