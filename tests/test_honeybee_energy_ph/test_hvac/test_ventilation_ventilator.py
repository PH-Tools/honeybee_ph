from honeybee_energy_ph.hvac import ventilation


def test_default_ventilator():
    o1 = ventilation.Ventilator()
    assert o1.ToString()

    d = o1.to_dict()
    o2 = ventilation.Ventilator.from_dict(d)
    assert o2.to_dict() == d


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
    assert o2.to_dict() == d
