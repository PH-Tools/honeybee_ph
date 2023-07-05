import pytest
from honeybee_energy_ph.properties.construction import window
from honeybee_energy_ph.construction.window import PhWindowFrame, PhWindowGlazing


def test_default_window_construction_shade_properties_dict_round_trip():
    s1 = window.WindowConstructionPhProperties("test_shade_prop")
    d1 = s1.to_dict()
    s2 = window.WindowConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_custom_window_construction_shade_properties_dict_round_trip():
    s1 = window.WindowConstructionPhProperties("test_shade_prop")
    s1.ph_frame = PhWindowFrame("frame")
    s1.ph_glazing = PhWindowGlazing("glazing")

    d1 = s1.to_dict()
    s2 = window.WindowConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_default_window_construction_shade_properties_duplicate():
    s1 = window.WindowConstructionPhProperties("test_shade_prop")
    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_custom_window_construction_shade_properties_duplicate():
    s1 = window.WindowConstructionPhProperties("test_shade_prop")
    s1.ph_frame = PhWindowFrame("frame")
    s1.ph_glazing = PhWindowGlazing("glazing")
    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_default_window_construction_shade_properties_wrong_type_from_dict():
    wrong_dict = {
        "type": "not_allowed_type",
    }
    with pytest.raises(window.WindowConstructionPhProperties_FromDictError):
        s1 = window.WindowConstructionPhProperties.from_dict(wrong_dict, None)
