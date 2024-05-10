from uuid import uuid4

from honeybee_energy_ph.construction import window


def test_default_PhWindowFrame():
    window_frame = window.PhWindowFrame(uuid4())

    assert window_frame.top.width == 0.1
    assert window_frame.top.u_factor == 1.0
    assert window_frame.top.psi_glazing == 0.04
    assert window_frame.top.psi_install == 0.04
    assert window_frame.top.chi_value == 0.0


def test_PhWindowFrame_to_from_dict_roundtrip():
    window_frame = window.PhWindowFrame(str(uuid4()))
    window_frame.top.user_data["test_key"] = "test_value"
    window_frame.top.width = 0.24
    window_frame.top.u_factor = 1.2
    window_frame.top.psi_glazing = 0.064
    window_frame.top.psi_install = 0.065
    window_frame.top.chi_value = 0.123

    window_frame.user_data["test_key"] = "test_value"

    d = window_frame.to_dict()
    new_window_frame = window.PhWindowFrame.from_dict(d)

    assert window_frame is not new_window_frame
    assert new_window_frame.to_dict() == d
    assert new_window_frame.top.width == 0.24
    assert new_window_frame.top.u_factor == 1.2
    assert new_window_frame.top.psi_glazing == 0.064
    assert new_window_frame.top.psi_install == 0.065
    assert new_window_frame.top.chi_value == 0.123
    assert "test_key" in new_window_frame.top.user_data
    assert "test_key" in new_window_frame.user_data


def test_PhWindowFrame_duplicate():
    window_frame = window.PhWindowFrame(str(uuid4()))
    window_frame.top.width = 0.24
    window_frame.top.u_factor = 1.2
    window_frame.top.psi_glazing = 0.064
    window_frame.top.psi_install = 0.065
    window_frame.top.chi_value = 0.123
    window_frame.top.user_data["test_key"] = "test_value"

    window_frame.user_data["test_key"] = "test_value"

    new_window_frame = window_frame.duplicate()

    assert new_window_frame.top.width == 0.24
    assert new_window_frame.top.u_factor == 1.2
    assert new_window_frame.top.psi_glazing == 0.064
    assert new_window_frame.top.psi_install == 0.065
    assert new_window_frame.top.chi_value == 0.123
    assert "test_key" in new_window_frame.top.user_data
    assert "test_key" in new_window_frame.user_data

    assert window_frame is not new_window_frame
    assert window_frame.identifier == new_window_frame.identifier
    assert window_frame.top.identifier == new_window_frame.top.identifier
    assert "test_key" in new_window_frame.top.user_data
    assert "test_key" in new_window_frame.user_data
