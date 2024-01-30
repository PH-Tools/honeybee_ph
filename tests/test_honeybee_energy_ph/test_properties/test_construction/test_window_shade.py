import pytest

from honeybee_energy_ph.construction.window import (
    PhWindowFrame,
    PhWindowFrameElement,
    PhWindowGlazing,
)
from honeybee_energy_ph.properties.construction import windowshade


def test_window_construction_shade_properties_dict_round_trip():
    s1 = windowshade.WindowConstructionShadePhProperties("test_shade_prop")
    d1 = s1.to_dict()
    s2 = windowshade.WindowConstructionShadePhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_window_construction_shade_properties_with_ph_frame_and_glazing_dict_round_trip():
    s1 = windowshade.WindowConstructionShadePhProperties("test_shade_prop")

    # -- Build a test frame with random data
    s1.ph_frame = PhWindowFrame("id-1")
    s1.ph_frame.top = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.235
    s1.ph_frame.top.u_factor = 0.456
    s1.ph_frame.top.psi_glazing = 0.234
    s1.ph_frame.top.psi_install = 0.8989
    s1.ph_frame.top.chi_value = 0.43
    s1.ph_frame.right = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.45
    s1.ph_frame.top.u_factor = 0.235
    s1.ph_frame.top.psi_glazing = 0.736
    s1.ph_frame.top.psi_install = 0.6345
    s1.ph_frame.top.chi_value = 0.967
    s1.ph_frame.bottom = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.14
    s1.ph_frame.top.u_factor = 352
    s1.ph_frame.top.psi_glazing = 0.7457
    s1.ph_frame.top.psi_install = 0.463
    s1.ph_frame.top.chi_value = 0.413243
    s1.ph_frame.left = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.787
    s1.ph_frame.top.u_factor = 0.999
    s1.ph_frame.top.psi_glazing = 0.232344
    s1.ph_frame.top.psi_install = 0.234
    s1.ph_frame.top.chi_value = 0.634

    s1.ph_glazing = PhWindowGlazing("id-2")
    s1.ph_glazing.u_factor = 0.123
    s1.ph_glazing.g_value = 0.456

    d1 = s1.to_dict()
    s2 = windowshade.WindowConstructionShadePhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_window_construction_shade_properties_duplicate():
    s1 = windowshade.WindowConstructionShadePhProperties("test_shade_prop")
    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_window_construction_shade_properties_with_ph_frame_and_glazing_duplicate():
    s1 = windowshade.WindowConstructionShadePhProperties("test_shade_prop")

    # -- Build a test frame with random data
    s1.ph_frame = PhWindowFrame("id-1")
    s1.ph_frame.top = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.235
    s1.ph_frame.top.u_factor = 0.456
    s1.ph_frame.top.psi_glazing = 0.234
    s1.ph_frame.top.psi_install = 0.8989
    s1.ph_frame.top.chi_value = 0.43
    s1.ph_frame.right = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.45
    s1.ph_frame.top.u_factor = 0.235
    s1.ph_frame.top.psi_glazing = 0.736
    s1.ph_frame.top.psi_install = 0.6345
    s1.ph_frame.top.chi_value = 0.967
    s1.ph_frame.bottom = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.14
    s1.ph_frame.top.u_factor = 352
    s1.ph_frame.top.psi_glazing = 0.7457
    s1.ph_frame.top.psi_install = 0.463
    s1.ph_frame.top.chi_value = 0.413243
    s1.ph_frame.left = PhWindowFrameElement("PhWindowFrameElement")
    s1.ph_frame.top.width = 0.787
    s1.ph_frame.top.u_factor = 0.999
    s1.ph_frame.top.psi_glazing = 0.232344
    s1.ph_frame.top.psi_install = 0.234
    s1.ph_frame.top.chi_value = 0.634

    s1.ph_glazing = PhWindowGlazing("id-2")
    s1.ph_glazing.u_factor = 0.123
    s1.ph_glazing.g_value = 0.456

    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_window_construction_shade_properties_wrong_type_from_dict():
    wrong_dict = {
        "type": "not_allowed_type",
    }
    with pytest.raises(windowshade.WindowConstructionShadePhProperties_FromDictError):
        s1 = windowshade.WindowConstructionShadePhProperties.from_dict(wrong_dict, None)
