from honeybee_phhvac import ventilation


def test_default_ventilator():
    o1 = ventilation.Ventilator()
    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.Ventilator.from_dict(d)
    assert o2.to_dict() == o1.to_dict()


def test_dict_round_trip_default_ventilator():
    o1 = ventilation.Ventilator()
    d1 = o1.to_dict()
    o2 = ventilation.Ventilator.from_dict(d1)

    assert o1.to_dict() == o2.to_dict()

    # -- user_data
    o2.user_data["test_key"] = "test_value"
    d2 = o2.to_dict()
    o3 = ventilation.Ventilator.from_dict(d2)
    assert o2.to_dict() == o3.to_dict()


def test_duplicate_default_ventilator():
    o1 = ventilation.Ventilator()
    assert o1.ToString()

    o2 = o1.duplicate()
    assert o2.to_dict() == o1.to_dict()

    # -- user_data
    o2.user_data["test_key"] = "test_value"
    assert "test_key" not in o1.user_data
    assert "test_key" in o2.user_data


def test_custom_ventilator():
    o1 = ventilation.Ventilator()
    o1.display_name = "Another"
    o1.id_num = 12
    o1.quantity = 2
    o1.sensible_heat_recovery = 0.74
    o1.latent_heat_recovery = 0.67
    o1.electric_efficiency = 0.6788
    o1.frost_protection_reqd = False
    o1.temperature_below_defrost_used = -12
    o1.in_conditioned_space = False

    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.Ventilator.from_dict(d)
    assert o2.to_dict() == o1.to_dict()
