from uuid import uuid4

from honeybee_energy_ph.construction import window


def test_default_PhWindowFrameElement():
    window_frame_element = window.PhWindowFrameElement(uuid4())
    assert window_frame_element.width == 0.1
    assert window_frame_element.u_factor == 1.0
    assert window_frame_element.psi_glazing == 0.04
    assert window_frame_element.psi_install == 0.04
    assert window_frame_element.chi_value == 0.0
    assert window_frame_element.solar_absorptance == 0.25
    assert window_frame_element.thermal_emissivity == 0.6

    assert window_frame_element


def test_default_PhWindowFrameElement_to_from_dict_roundtrip():
    window_frame_element = window.PhWindowFrameElement(str(uuid4()))
    window_frame_element.user_data["test_key"] = "test_value"
    d = window_frame_element.to_dict()
    new_window_frame_element = window.PhWindowFrameElement.from_dict(d)

    assert window_frame_element is not new_window_frame_element
    assert new_window_frame_element.to_dict() == d
    assert new_window_frame_element.width == 0.1
    assert new_window_frame_element.u_factor == 1.0
    assert new_window_frame_element.psi_glazing == 0.04
    assert new_window_frame_element.psi_install == 0.04
    assert new_window_frame_element.chi_value == 0.0
    assert new_window_frame_element.solar_absorptance == 0.25
    assert new_window_frame_element.thermal_emissivity == 0.6
    assert "test_key" in new_window_frame_element.user_data


def test_PhWindowFrameElement_radiation_props_roundtrip():
    window_frame_element = window.PhWindowFrameElement(str(uuid4()))
    window_frame_element.solar_absorptance = 0.85
    window_frame_element.thermal_emissivity = 0.92
    d = window_frame_element.to_dict()
    new_window_frame_element = window.PhWindowFrameElement.from_dict(d)

    assert new_window_frame_element.solar_absorptance == 0.85
    assert new_window_frame_element.thermal_emissivity == 0.92


def test_PhWindowFrameElement_from_legacy_dict_without_radiation_props():
    """Old HBJSON without the radiation keys should fall back to PHPP defaults."""
    window_frame_element = window.PhWindowFrameElement(str(uuid4()))
    d = window_frame_element.to_dict()
    del d["solar_absorptance"]
    del d["thermal_emissivity"]

    new_window_frame_element = window.PhWindowFrameElement.from_dict(d)
    assert new_window_frame_element.solar_absorptance == 0.25
    assert new_window_frame_element.thermal_emissivity == 0.6


def test_duplicate_PhWindowFrameElement():
    window_frame_element = window.PhWindowFrameElement(str(uuid4()))
    window_frame_element.width = 0.5
    window_frame_element.u_factor = 2.0
    window_frame_element.psi_glazing = 0.08
    window_frame_element.psi_install = 0.08
    window_frame_element.chi_value = 1.0
    window_frame_element.solar_absorptance = 0.7
    window_frame_element.thermal_emissivity = 0.9
    window_frame_element.user_data["test_key"] = "test_value"

    new_window_frame_element = window_frame_element.duplicate()

    assert new_window_frame_element.width == 0.5
    assert new_window_frame_element.u_factor == 2.0
    assert new_window_frame_element.psi_glazing == 0.08
    assert new_window_frame_element.psi_install == 0.08
    assert new_window_frame_element.chi_value == 1.0
    assert new_window_frame_element.solar_absorptance == 0.7
    assert new_window_frame_element.thermal_emissivity == 0.9

    assert window_frame_element is not new_window_frame_element
    assert window_frame_element.identifier == new_window_frame_element.identifier
    assert "test_key" in new_window_frame_element.user_data
