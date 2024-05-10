from uuid import uuid4
from honeybee_energy_ph.construction import window


def test_default_PhWindowFrameElement():
    window_frame_element = window.PhWindowFrameElement(uuid4())
    assert window_frame_element.width == 0.1
    assert window_frame_element.u_factor == 1.0
    assert window_frame_element.psi_glazing == 0.04
    assert window_frame_element.psi_install == 0.04
    assert window_frame_element.chi_value == 0.0

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
    assert "test_key" in new_window_frame_element.user_data


def test_duplicate_PhWindowFrameElement():
    window_frame_element = window.PhWindowFrameElement(str(uuid4()))
    window_frame_element.width = 0.5
    window_frame_element.u_factor = 2.0
    window_frame_element.psi_glazing = 0.08
    window_frame_element.psi_install = 0.08
    window_frame_element.chi_value = 1.0
    window_frame_element.user_data["test_key"] = "test_value"

    new_window_frame_element = window_frame_element.duplicate()

    assert new_window_frame_element.width == 0.5
    assert new_window_frame_element.u_factor == 2.0
    assert new_window_frame_element.psi_glazing == 0.08
    assert new_window_frame_element.psi_install == 0.08
    assert new_window_frame_element.chi_value == 1.0

    assert window_frame_element is not new_window_frame_element
    assert window_frame_element.identifier == new_window_frame_element.identifier
    assert "test_key" in new_window_frame_element.user_data
