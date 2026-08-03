from honeybee_ph.properties import aperture


def test_default_aperture_prop():
    a1 = aperture.AperturePhProperties(_host=None)
    assert a1


def test_default_aperture_prop_round_trip():
    a1 = aperture.AperturePhProperties(_host=None)
    d1 = a1.to_dict()

    a2 = aperture.AperturePhProperties.from_dict(d1["ph"], a1.host)
    assert a2.to_dict() == d1


def test_from_legacy_dict_uses_default_install_depth():
    a1 = aperture.AperturePhProperties(_host=None)
    aperture_dict = a1.to_dict()["ph"]
    del aperture_dict["install_depth"]

    a2 = aperture.AperturePhProperties.from_dict(aperture_dict, a1.host)

    assert a2.install_depth == 0.1016


def test_duplicate_empty_prop_dict():
    a1 = aperture.AperturePhProperties(_host=None)
    a2 = a1.duplicate()
    assert a2.to_dict() == a1.to_dict()


# TODO: Test with spaces, scale, ...
