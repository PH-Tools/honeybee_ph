from PHX.model.hvac import ventilation


def test_add_default_PhxVentilatorParams(reset_class_counters):
    p1 = ventilation.PhxDeviceVentilatorParams()
    p2 = ventilation.PhxDeviceVentilatorParams()

    p3 = p1 + p2

    assert p3.sensible_heat_recovery == p1.sensible_heat_recovery
    assert p3.latent_heat_recovery == p1.latent_heat_recovery
    assert p3.quantity == 2
    assert p3.electric_efficiency == p1.electric_efficiency
    assert p3.frost_protection_reqd == p1.frost_protection_reqd
    assert p3.temperature_below_defrost_used == p1.temperature_below_defrost_used


def test_add_mixed_PhxVentilatorParams(reset_class_counters):
    p1 = ventilation.PhxDeviceVentilatorParams(
        sensible_heat_recovery=10,
        latent_heat_recovery=10,
        quantity=2,
        electric_efficiency=4,
        frost_protection_reqd=True,
        temperature_below_defrost_used=-5.0,
    )
    p2 = ventilation.PhxDeviceVentilatorParams(
        sensible_heat_recovery=20,
        latent_heat_recovery=20,
        quantity=3,
        electric_efficiency=2,
        frost_protection_reqd=False,
        temperature_below_defrost_used=5.0,
    )
    p3 = p1 + p2
    assert p1 != p2 != p3
    assert p3.sensible_heat_recovery == 15
    assert p3.latent_heat_recovery == 15
    assert p3.quantity == 5
    assert p3.electric_efficiency == 3
    assert p3.frost_protection_reqd == True
    assert p3.temperature_below_defrost_used == 0.0


def test_default_PhxVentilator(reset_class_counters):
    p1 = ventilation.PhxDeviceVentilator()
    p2 = ventilation.PhxDeviceVentilator()

    assert p1.id_num == 1
    assert p2.id_num == 2


def test__PhxVentilator_params(reset_class_counters):
    d1 = ventilation.PhxDeviceVentilator()
    d1.params.quantity = 1
    d2 = ventilation.PhxDeviceVentilator()
    d2.params.quantity = 12

    assert d1.params != d2.params
    assert d1.params.quantity != d2.params.quantity


def test_add_default_PhxVentilator(reset_class_counters):
    p1 = ventilation.PhxDeviceVentilator()
    p2 = ventilation.PhxDeviceVentilator()

    p3 = p1 + p2

    assert p1 != p2 != p3


def test_add_mixed_PhxVentilator(reset_class_counters):
    d1 = ventilation.PhxDeviceVentilator()
    d1.params = ventilation.PhxDeviceVentilatorParams(
        sensible_heat_recovery=10,
        latent_heat_recovery=10,
        quantity=2,
        electric_efficiency=4,
        frost_protection_reqd=True,
        temperature_below_defrost_used=-5.0,
    )
    d2 = ventilation.PhxDeviceVentilator()
    d2.params = ventilation.PhxDeviceVentilatorParams(
        sensible_heat_recovery=20,
        latent_heat_recovery=20,
        quantity=3,
        electric_efficiency=2,
        frost_protection_reqd=False,
        temperature_below_defrost_used=5.0,
    )

    d3 = d1 + d2

    assert d1 != d2 != d3
    assert d3.params.sensible_heat_recovery == 15
    assert d3.params.latent_heat_recovery == 15
    assert d3.params.quantity == 5
    assert d3.params.electric_efficiency == 3
    assert d3.params.frost_protection_reqd == True
    assert d3.params.temperature_below_defrost_used == 0.0
