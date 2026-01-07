from pytest import approx

from honeybee_energy_ph.construction import window
from honeybee_ph_utils.iso_10077_1 import ISO100771Data


def test_default_frame_and_glass():
    ph_frame = window.PhWindowFrame("ph_frame")
    for frame_element in ph_frame.elements:
        assert frame_element.width == 0.1
        assert frame_element.u_factor == 1.0
        assert frame_element.psi_glazing == 0.04
        assert frame_element.psi_install == 0.04
        assert frame_element.chi_value == 0.0

    ph_glazing = window.PhWindowGlazing("ph_glazing")
    assert ph_glazing.u_factor == 1.0
    assert ph_glazing.g_value == 0.4

    # -- Create the new ISO Data Object
    d = ISO100771Data(_win_width=1.5, _win_height=2.5, _frame=ph_frame, _glazing=ph_glazing)

    # -- Check the attributes
    assert d.area_window == approx(3.75)
    assert d.area_glazing == approx(2.99)
    assert d.area_frame == approx(0.76)

    assert d.side_exterior_length("top") == approx(1.5)
    assert d.side_exterior_length("bottom") == approx(1.5)
    assert d.side_exterior_length("left") == approx(2.5)
    assert d.side_exterior_length("right") == approx(2.5)

    assert d.side_interior_length("top") == approx(1.3)
    assert d.side_interior_length("bottom") == approx(1.3)
    assert d.side_interior_length("left") == approx(2.3)
    assert d.side_interior_length("right") == approx(2.3)

    assert d.corner_area("top") == approx(0.01)
    assert d.corner_area("bottom") == approx(0.01)
    assert d.corner_area("left") == approx(0.01)
    assert d.corner_area("right") == approx(0.01)

    assert d.side_area("top") == approx(0.14)
    assert d.side_area("bottom") == approx(0.14)
    assert d.side_area("left") == approx(0.24)
    assert d.side_area("right") == approx(0.24)

    assert d.side_frame_heat_loss("top") == approx(0.14)
    assert d.side_frame_heat_loss("bottom") == approx(0.14)
    assert d.side_frame_heat_loss("left") == approx(0.24)
    assert d.side_frame_heat_loss("right") == approx(0.24)

    assert d.side_psi_glazing_heat_lost("top") == approx(0.052)
    assert d.side_psi_glazing_heat_lost("bottom") == approx(0.052)
    assert d.side_psi_glazing_heat_lost("left") == approx(0.092)
    assert d.side_psi_glazing_heat_lost("right") == approx(0.092)

    assert d.side_psi_install_heat_lost("top") == approx(0.06)
    assert d.side_psi_install_heat_lost("bottom") == approx(0.06)
    assert d.side_psi_install_heat_lost("left") == approx(0.10)
    assert d.side_psi_install_heat_lost("right") == approx(0.10)

    assert d.uw == approx(1.162133)


def test_custom_frame_and_glass():
    ph_frame = window.PhWindowFrame("ph_frame")
    ph_frame.left.width = 0.1334
    ph_frame.left.u_factor = 1.1357
    ph_frame.left.psi_glazing = 0.019
    ph_frame.left.psi_install = 0

    ph_frame.right.width = 0.1334
    ph_frame.right.u_factor = 1.1357
    ph_frame.right.psi_glazing = 0.019
    ph_frame.right.psi_install = 0

    ph_frame.top.width = 0.1715
    ph_frame.top.u_factor = 1.1924
    ph_frame.top.psi_glazing = 0.019
    ph_frame.top.psi_install = 0

    ph_frame.bottom.width = 0.1334
    ph_frame.bottom.u_factor = 1.1357
    ph_frame.bottom.psi_glazing = 0.019
    ph_frame.bottom.psi_install = 0

    ph_glazing = window.PhWindowGlazing("ph_glazing")
    ph_glazing.u_factor = 0.666

    # -- Create the new ISO Data Object
    d = ISO100771Data(_win_width=0.8509, _win_height=1.88595, _frame=ph_frame, _glazing=ph_glazing)
    assert d.uw == approx(0.9210185120393359)


def test_wufi_method():
    ph_frame = window.PhWindowFrame("ph_frame")
    ph_frame.left.width = 0.1334
    ph_frame.left.u_factor = 1.1357
    ph_frame.left.psi_glazing = 0.019
    ph_frame.left.psi_install = 0

    ph_frame.right.width = 0.1334
    ph_frame.right.u_factor = 1.1357
    ph_frame.right.psi_glazing = 0.019
    ph_frame.right.psi_install = 0

    ph_frame.top.width = 0.1715
    ph_frame.top.u_factor = 1.1924
    ph_frame.top.psi_glazing = 0.019
    ph_frame.top.psi_install = 0

    ph_frame.bottom.width = 0.1334
    ph_frame.bottom.u_factor = 1.1357
    ph_frame.bottom.psi_glazing = 0.019
    ph_frame.bottom.psi_install = 0

    ph_glazing = window.PhWindowGlazing("ph_glazing")
    ph_glazing.u_factor = 0.666

    # -- Create the new ISO Data Object
    d = ISO100771Data(_win_width=0.8509, _win_height=1.88595, _frame=ph_frame, _glazing=ph_glazing)
    assert d.wufi_passive_uw == approx(0.9218268524945511)
