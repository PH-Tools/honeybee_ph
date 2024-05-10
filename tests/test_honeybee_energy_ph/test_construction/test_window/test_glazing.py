from uuid import uuid4

from honeybee_energy_ph.construction import window


def test_default_PhWindowGlazing():
    window_glazing = window.PhWindowGlazing(uuid4())
    assert window_glazing.u_factor == 1.0
    assert window_glazing.g_value == 0.4
    assert window_glazing


def test_PhWindowGlazing_to_from_dict_roundtrip():
    window_glazing = window.PhWindowGlazing(str(uuid4()))
    window_glazing.user_data["test_key"] = "test_value"
    window_glazing.u_factor = 1.2
    window_glazing.g_value = 0.5
    d = window_glazing.to_dict()
    new_window_glazing = window.PhWindowGlazing.from_dict(d)

    assert window_glazing is not new_window_glazing
    assert new_window_glazing.to_dict() == d
    assert new_window_glazing.u_factor == 1.2
    assert new_window_glazing.g_value == 0.5
    assert "test_key" in new_window_glazing.user_data


def test_PhWindowGlazing_duplicate():
    window_glazing = window.PhWindowGlazing(str(uuid4()))
    window_glazing.u_factor = 1.2
    window_glazing.g_value = 0.5
    window_glazing.user_data["test_key"] = "test_value"

    new_window_glazing = window_glazing.duplicate()

    assert new_window_glazing.u_factor == 1.2
    assert new_window_glazing.g_value == 0.5

    assert window_glazing is not new_window_glazing
    assert window_glazing.identifier == new_window_glazing.identifier
    assert "test_key" in new_window_glazing.user_data
