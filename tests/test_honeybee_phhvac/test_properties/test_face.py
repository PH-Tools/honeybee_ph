from honeybee_phhvac.properties.face import FacePhHvacProperties


def test_abridged_dict_round_trip():
    p1 = FacePhHvacProperties(_host=None)
    d1 = p1.to_dict(abridged=True)
    assert d1["ph_hvac"]["type"] == "FacePhHvacPropertiesAbridged"
    p2 = FacePhHvacProperties.from_dict(d1["ph_hvac"], p1.host)
    assert p2.to_dict(abridged=True) == d1


def test_unabridged_dict_round_trip():
    p1 = FacePhHvacProperties(_host=None)
    d1 = p1.to_dict(abridged=False)
    assert d1["ph_hvac"]["type"] == "FacePhHvacProperties"
    p2 = FacePhHvacProperties.from_dict(d1["ph_hvac"], p1.host)
    assert p2.to_dict(abridged=False) == d1


def test_duplicate_properties():
    p1 = FacePhHvacProperties(_host=None)
    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()
