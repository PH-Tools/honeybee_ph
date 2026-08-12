import pytest
from honeybee.aperture import Aperture
from honeybee_energy.construction.window import WindowConstruction
from honeybee_energy.material.glazing import EnergyWindowMaterialSimpleGlazSys
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Point3D

from honeybee_energy_ph.construction import window
from honeybee_ph_utils import aperture_psi_install


def _build_hb_aperture(_with_ph_frame=True, _psi_install=0.04):
    """Build an HB-Aperture with a WindowConstruction (optionally carrying a PH frame)."""
    glazing_material = EnergyWindowMaterialSimpleGlazSys("test_mat", u_factor=1.0, shgc=0.4)
    construction = WindowConstruction("test_construction", [glazing_material])

    if _with_ph_frame:
        ph_frame = window.PhWindowFrame("test_frame")
        for frame_element in ph_frame.elements:
            frame_element.psi_install = _psi_install
        construction.properties.ph.ph_frame = ph_frame

        ph_glazing = window.PhWindowGlazing("test_glazing")
        construction.properties.ph.ph_glazing = ph_glazing

    hb_aperture = Aperture(
        "test_aperture",
        Face3D([Point3D(0, 0, 0), Point3D(2, 0, 0), Point3D(2, 0, 1), Point3D(0, 0, 1)]),
    )
    hb_aperture.properties.energy.construction = construction
    return hb_aperture


def _install_type(_name, _psi):
    install_type = window.PhApertureInstallType(_name)
    install_type.display_name = _name
    install_type.psi_install = _psi
    return install_type


# -----------------------------------------------------------------------------
# -- get_ph_frame


def test_get_ph_frame():
    hb_aperture = _build_hb_aperture()
    ph_frame = aperture_psi_install.get_ph_frame(hb_aperture)
    assert ph_frame is not None
    assert ph_frame.top.psi_install == 0.04


def test_get_ph_frame_no_ph_frame_returns_None():
    hb_aperture = _build_hb_aperture(_with_ph_frame=False)
    assert aperture_psi_install.get_ph_frame(hb_aperture) is None


def test_get_ph_frame_through_shade_construction():
    """WindowConstructionShade wraps the real WindowConstruction: reach through it."""
    from honeybee_energy.construction.windowshade import WindowConstructionShade
    from honeybee_energy.material.shade import EnergyWindowMaterialShade

    hb_aperture = _build_hb_aperture()
    window_construction = hb_aperture.properties.energy.construction
    shade_construction = WindowConstructionShade(
        "test_shade_construction", window_construction, EnergyWindowMaterialShade("test_shade")
    )
    hb_aperture.properties.energy.construction = shade_construction

    ph_frame = aperture_psi_install.get_ph_frame(hb_aperture)
    assert ph_frame is not None
    assert ph_frame.top.psi_install == 0.04


# -----------------------------------------------------------------------------
# -- resolve_psi_install_values


def test_resolve_all_inherited_from_frame():
    hb_aperture = _build_hb_aperture(_psi_install=0.04)
    values = aperture_psi_install.resolve_psi_install_values(hb_aperture)
    assert values == {"top": 0.04, "right": 0.04, "bottom": 0.04, "left": 0.04}


def test_resolve_with_mixed_assignments():
    hb_aperture = _build_hb_aperture(_psi_install=0.04)
    hb_aperture.properties.ph.install_types.left = _install_type("Party Wall", 0.0)
    hb_aperture.properties.ph.install_types.top = _install_type("Buried Head", 0.085)

    values = aperture_psi_install.resolve_psi_install_values(hb_aperture)
    assert values == {"top": 0.085, "right": 0.04, "bottom": 0.04, "left": 0.0}


def test_resolve_all_assigned_needs_no_frame():
    hb_aperture = _build_hb_aperture(_with_ph_frame=False)
    for side in ("top", "right", "bottom", "left"):
        setattr(hb_aperture.properties.ph.install_types, side, _install_type("Mid-Wall", 0.052))

    values = aperture_psi_install.resolve_psi_install_values(hb_aperture)
    assert values == {"top": 0.052, "right": 0.052, "bottom": 0.052, "left": 0.052}


def test_resolve_unassigned_side_without_frame_raises():
    hb_aperture = _build_hb_aperture(_with_ph_frame=False)
    hb_aperture.properties.ph.install_types.top = _install_type("Mid-Wall", 0.052)

    with pytest.raises(ValueError):
        aperture_psi_install.resolve_psi_install_values(hb_aperture)


def test_resolve_two_apertures_share_one_construction_no_duplication():
    """The headline invariant: different install conditions, same (single) construction."""
    hb_aperture_1 = _build_hb_aperture(_psi_install=0.04)
    construction = hb_aperture_1.properties.energy.construction

    hb_aperture_2 = Aperture(
        "test_aperture_2",
        Face3D([Point3D(0, 0, 0), Point3D(2, 0, 0), Point3D(2, 0, 1), Point3D(0, 0, 1)]),
    )
    hb_aperture_2.properties.energy.construction = construction
    hb_aperture_2.properties.ph.install_types.left = _install_type("Party Wall", 0.0)

    values_1 = aperture_psi_install.resolve_psi_install_values(hb_aperture_1)
    values_2 = aperture_psi_install.resolve_psi_install_values(hb_aperture_2)

    # -- Different effective values ...
    assert values_1["left"] == 0.04
    assert values_2["left"] == 0.0
    # -- ... same single shared construction object, never mutated
    assert hb_aperture_1.properties.energy.construction is hb_aperture_2.properties.energy.construction
    assert construction.properties.ph.ph_frame.left.psi_install == 0.04


# -----------------------------------------------------------------------------
# -- resolve_effective_frame


def test_effective_frame_with_no_assignments_matches_construction_frame():
    hb_aperture = _build_hb_aperture(_psi_install=0.04)
    ph_frame = aperture_psi_install.get_ph_frame(hb_aperture)
    effective_frame = aperture_psi_install.resolve_effective_frame(hb_aperture)

    assert effective_frame is not ph_frame
    for side in ("top", "right", "bottom", "left"):
        assert getattr(effective_frame, side).psi_install == getattr(ph_frame, side).psi_install


def test_effective_frame_applies_overrides_without_mutating_source():
    hb_aperture = _build_hb_aperture(_psi_install=0.04)
    hb_aperture.properties.ph.install_types.bottom = _install_type("Sill @ Slab", 0.0)

    effective_frame = aperture_psi_install.resolve_effective_frame(hb_aperture)
    assert effective_frame.bottom.psi_install == 0.0
    assert effective_frame.top.psi_install == 0.04

    # -- the construction's own frame is untouched
    ph_frame = aperture_psi_install.get_ph_frame(hb_aperture)
    assert ph_frame.bottom.psi_install == 0.04


def test_effective_frame_without_ph_frame_raises():
    hb_aperture = _build_hb_aperture(_with_ph_frame=False)
    with pytest.raises(ValueError):
        aperture_psi_install.resolve_effective_frame(hb_aperture)


# -----------------------------------------------------------------------------
# -- ISO 10077-1 integration


def test_hb_aperture_uw_unchanged_without_assignments():
    """No Install Types assigned -> identical U-w to the construction-frame calculation."""
    from honeybee_ph_utils import iso_10077_1

    hb_aperture = _build_hb_aperture(_psi_install=0.04)
    ph_frame = aperture_psi_install.get_ph_frame(hb_aperture)
    ph_glazing = aperture_psi_install.get_ph_glazing(hb_aperture)

    uw_via_aperture = iso_10077_1.calculate_hb_aperture_uw(hb_aperture)
    iso_data = iso_10077_1.ISO100771Data(2.0, 1.0, ph_frame, ph_glazing)
    assert uw_via_aperture == pytest.approx(iso_data.uw)


def test_hb_aperture_uw_zero_psi_edge_contributes_zero_install_loss():
    """An edge assigned a zero-psi Install Type contributes zero install heat loss."""
    from honeybee_ph_utils import iso_10077_1

    hb_aperture = _build_hb_aperture(_psi_install=0.04)
    uw_before = iso_10077_1.calculate_hb_aperture_uw(hb_aperture)

    hb_aperture.properties.ph.install_types.left = _install_type("Party Wall", 0.0)
    uw_after = iso_10077_1.calculate_hb_aperture_uw(hb_aperture)

    # -- the 'left' edge is the window height (1.0m); area is 2.0 m2
    expected_reduction = (0.04 * 1.0) / 2.0
    assert uw_before - uw_after == pytest.approx(expected_reduction)

    # -- the shared construction frame is not mutated by the calculation
    assert aperture_psi_install.get_ph_frame(hb_aperture).left.psi_install == 0.04


def test_hb_aperture_uw_without_ph_glazing_raises():
    from honeybee_ph_utils import iso_10077_1

    hb_aperture = _build_hb_aperture()
    hb_aperture.properties.energy.construction.properties.ph.ph_glazing = None

    with pytest.raises(Exception):
        iso_10077_1.calculate_hb_aperture_uw(hb_aperture)
