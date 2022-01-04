import honeybee_ph.climate


def test_climate():
    cli = honeybee_ph.climate.Climate()
    assert cli


def test_climate_serialization():
    cli = honeybee_ph.climate.Climate()
    d = cli.to_dict()
    new_o = honeybee_ph.climate.Climate.from_dict(d)

    assert new_o.to_dict() == d
