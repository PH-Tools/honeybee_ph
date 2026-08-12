import pytest

from honeybee_energy_ph.construction.window import PhApertureInstallType
from honeybee_ph.properties import aperture


def _install_type(_name, _psi):
    install_type = PhApertureInstallType(_name)
    install_type.display_name = _name
    install_type.psi_install = _psi
    return install_type


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


# -----------------------------------------------------------------------------
# -- AperturePsiInstalls


def test_default_AperturePsiInstalls():
    installs = aperture.AperturePsiInstalls()
    assert installs.any_assigned is False
    for side in aperture.AperturePsiInstalls.SIDES:
        assert installs.get_side(side) is None
    assert installs.to_dict() == {}
    assert repr(installs) == str(installs)
    assert installs.ToString() == str(installs)


def test_AperturePsiInstalls_get_side_invalid_raises():
    installs = aperture.AperturePsiInstalls()
    with pytest.raises(ValueError):
        installs.get_side("middle")


def test_AperturePsiInstalls_partial_assignment_roundtrip():
    installs = aperture.AperturePsiInstalls()
    installs.left = _install_type("Party Wall", 0.0)
    installs.top = _install_type("Buried Head", 0.052)
    assert installs.any_assigned is True

    d = installs.to_dict()
    assert set(d.keys()) == {"left", "top"}

    new_installs = aperture.AperturePsiInstalls.from_dict(d)
    assert new_installs.left is not None
    assert new_installs.left.psi_install == 0.0
    assert new_installs.left.display_name == "Party Wall"
    assert new_installs.top is not None
    assert new_installs.top.psi_install == 0.052
    assert new_installs.right is None
    assert new_installs.bottom is None
    assert new_installs.to_dict() == d


def test_AperturePsiInstalls_duplicate_is_deep():
    installs = aperture.AperturePsiInstalls()
    installs.right = _install_type("Mid-Wall", 0.04)

    new_installs = installs.duplicate()
    assert new_installs.right is not None
    assert new_installs.right is not installs.right
    assert new_installs.right.psi_install == 0.04
    assert new_installs.to_dict() == installs.to_dict()


# -----------------------------------------------------------------------------
# -- AperturePhProperties w/ install_types


def test_aperture_prop_with_install_types_round_trip():
    a1 = aperture.AperturePhProperties(_host=None)
    a1.install_types.bottom = _install_type("Sill Angle", 0.061)
    d1 = a1.to_dict()
    assert "install_types" in d1["ph"]

    a2 = aperture.AperturePhProperties.from_dict(d1["ph"], a1.host)
    assert a2.install_types.bottom is not None
    assert a2.install_types.bottom.psi_install == 0.061
    assert a2.install_types.top is None
    assert a2.to_dict() == d1


def test_aperture_prop_without_install_types_writes_no_key():
    """No assignments -> no 'install_types' key -> old-HBJSON output unchanged."""
    a1 = aperture.AperturePhProperties(_host=None)
    assert "install_types" not in a1.to_dict()["ph"]


def test_aperture_prop_from_legacy_dict_without_install_types():
    """Old HBJSON without the install_types key loads with all sides None."""
    a1 = aperture.AperturePhProperties(_host=None)
    aperture_dict = a1.to_dict()["ph"]
    assert "install_types" not in aperture_dict

    a2 = aperture.AperturePhProperties.from_dict(aperture_dict, a1.host)
    assert a2.install_types.any_assigned is False


def test_duplicate_aperture_prop_with_install_types():
    a1 = aperture.AperturePhProperties(_host=None)
    a1.install_types.left = _install_type("Party Wall", 0.0)

    a2 = a1.duplicate()
    assert a2.install_types.left is not None
    assert a2.install_types.left is not a1.install_types.left
    assert a2.to_dict() == a1.to_dict()


def test_apply_properties_from_dict_with_install_types():
    a1 = aperture.AperturePhProperties(_host=None)
    a1.install_types.right = _install_type("Jamb @ Masonry", 0.085)
    aperture_dict = a1.to_dict()["ph"]

    a2 = aperture.AperturePhProperties(_host=None)
    a2.apply_properties_from_dict(aperture_dict)
    assert a2.install_types.right is not None
    assert a2.install_types.right.psi_install == 0.085
    assert a2.install_types.right.display_name == "Jamb @ Masonry"


def test_apply_properties_from_dict_without_install_types():
    a1 = aperture.AperturePhProperties(_host=None)
    aperture_dict = a1.to_dict()["ph"]

    a2 = aperture.AperturePhProperties(_host=None)
    a2.apply_properties_from_dict(aperture_dict)
    assert a2.install_types.any_assigned is False


def test_hb_aperture_duplicate_carries_install_types():
    """The registered properties-plugin path: Aperture.duplicate() -> properties.ph.duplicate()."""
    from honeybee.aperture import Aperture
    from ladybug_geometry.geometry3d.face import Face3D
    from ladybug_geometry.geometry3d.pointvector import Point3D

    hb_aperture = Aperture(
        "test_aperture",
        Face3D([Point3D(0, 0, 0), Point3D(1, 0, 0), Point3D(1, 0, 1), Point3D(0, 0, 1)]),
    )
    hb_aperture.properties.ph.install_types.top = _install_type("Buried Head", 0.0)

    new_aperture = hb_aperture.duplicate()
    new_installs = new_aperture.properties.ph.install_types
    assert new_installs.top is not None
    assert new_installs.top is not hb_aperture.properties.ph.install_types.top
    assert new_installs.top.psi_install == 0.0
    assert new_installs.any_assigned is True


# TODO: Test with spaces, scale, ...
