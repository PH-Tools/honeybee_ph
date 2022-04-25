from PHX.model.hvac import _base, enums


def test_PhxUsageProfile_add(reset_class_counters):
    use_1 = _base.PhxUsageProfile(False, False, False, True, True, False)
    use_2 = _base.PhxUsageProfile(False, False, True, True, False, False)

    use_3 = use_1 + use_2
    assert use_3 != use_2 != use_1
    assert use_3.space_heating == False
    assert use_3.dhw_heating == False
    assert use_3.cooling == True
    assert use_3.ventilation == True
    assert use_3.humidification == True
    assert use_3.dehumidification == False


def test_add_default_PhxMechEquipmentParams(reset_class_counters):
    p1 = _base.PhxMechanicalEquipmentParams()
    p2 = _base.PhxMechanicalEquipmentParams()

    p3 = p1 + p2
    assert p3.aux_energy == None
    assert p3.aux_energy_dhw == None
    assert p3.solar_fraction == None
    assert p3.in_conditioned_space == True


def test_r_add_default_PhxMechEquipmentParams(reset_class_counters):
    p1 = _base.PhxMechanicalEquipmentParams()
    p2 = _base.PhxMechanicalEquipmentParams()

    p3 = p1.__radd__(p2)
    assert p3.aux_energy == None
    assert p3.aux_energy_dhw == None
    assert p3.solar_fraction == None
    assert p3.in_conditioned_space == True

    p4 = p2.__radd__(p1)
    assert p4.aux_energy == None
    assert p4.aux_energy_dhw == None
    assert p4.solar_fraction == None
    assert p4.in_conditioned_space == True


def test_sum_default_PhxMechEquipmentParams(reset_class_counters):
    p1 = _base.PhxMechanicalEquipmentParams()
    p2 = _base.PhxMechanicalEquipmentParams()

    p3: _base.PhxMechanicalEquipmentParams = sum([p1, p2])
    assert p3.aux_energy == None
    assert p3.aux_energy_dhw == None
    assert p3.solar_fraction == None
    assert p3.in_conditioned_space == True


def test_add_mixed_PhxMechEquipmentParams(reset_class_counters):
    p1 = _base.PhxMechanicalEquipmentParams(
        aux_energy=12,
        aux_energy_dhw=0.4,
        solar_fraction=None,
        in_conditioned_space=False,
    )
    p2 = _base.PhxMechanicalEquipmentParams(
        aux_energy=None,
        aux_energy_dhw=0.4,
        solar_fraction=13,
        in_conditioned_space=True,
    )

    p3 = p1 + p2
    assert p3.aux_energy == 12
    assert p3.aux_energy_dhw == 0.8
    assert p3.solar_fraction == 13
    assert p3.in_conditioned_space == True


def test_PhxMechanicalEquipment(reset_class_counters):
    mech_equip_1 = _base.PhxMechanicalEquipment()
    mech_equip_2 = _base.PhxMechanicalEquipment()

    assert mech_equip_1 != mech_equip_2
    assert mech_equip_1.id_num == 1
    assert mech_equip_2.id_num == 2


def test_add_default_PhxMechanicalEquipment(reset_class_counters):
    mech_equip_1 = _base.PhxMechanicalEquipment()
    mech_equip_2 = _base.PhxMechanicalEquipment()

    mech_equip_3 = mech_equip_1 + mech_equip_2
    assert mech_equip_3 != mech_equip_1 != mech_equip_2

    mech_equip_4 = sum([mech_equip_1, mech_equip_2])
    assert mech_equip_4 != mech_equip_1 != mech_equip_2


def test_r_add_default_PhxMechanicalEquipment(reset_class_counters):
    mech_equip_1 = _base.PhxMechanicalEquipment()
    mech_equip_2 = _base.PhxMechanicalEquipment()

    mech_equip_3 = mech_equip_1.__radd__(mech_equip_2)
    assert mech_equip_3 != mech_equip_1 != mech_equip_2


def test_add_mixed_PhxMechanicalEquipment(reset_class_counters):
    mech_equip_1 = _base.PhxMechanicalEquipment(
        quantity=1,
        unit=0.5,
        percent_coverage=0.25,
        usage_profile=_base.PhxUsageProfile(False, False, False, True, False, False),
    )
    mech_equip_2 = _base.PhxMechanicalEquipment(
        quantity=9,
        unit=0.25,
        percent_coverage=0.75,
        usage_profile=_base.PhxUsageProfile(True, False, False, False, False, True),
    )

    mech_equip_3 = mech_equip_1 + mech_equip_2
    assert mech_equip_3 != mech_equip_1 != mech_equip_2
    assert mech_equip_3.quantity == 10
    assert mech_equip_3.unit == 0.75
    assert mech_equip_3.percent_coverage == 1.0
    assert mech_equip_3.usage_profile.space_heating == True
    assert mech_equip_3.usage_profile.dhw_heating == False
    assert mech_equip_3.usage_profile.cooling == False
    assert mech_equip_3.usage_profile.ventilation == True
    assert mech_equip_3.usage_profile.humidification == False
    assert mech_equip_3.usage_profile.dehumidification == True

    mech_equip_4: _base.PhxMechanicalEquipment = sum([mech_equip_1, mech_equip_2])
    assert mech_equip_4 != mech_equip_1 != mech_equip_2
    assert mech_equip_4.quantity == 10
    assert mech_equip_4.unit == 0.75
    assert mech_equip_4.percent_coverage == 1.0
    assert mech_equip_4.usage_profile.space_heating == True
    assert mech_equip_4.usage_profile.dhw_heating == False
    assert mech_equip_4.usage_profile.cooling == False
    assert mech_equip_4.usage_profile.ventilation == True
    assert mech_equip_4.usage_profile.humidification == False
    assert mech_equip_4.usage_profile.dehumidification == True


def test_default_PhxMechanicalSubSystem(reset_class_counters):
    sys_1 = _base.PhxMechanicalSubSystem()
    sys_2 = _base.PhxMechanicalSubSystem()

    assert sys_1 != sys_2
    assert sys_1.id_num == 1
    assert sys_1.system_type == enums.DeviceType.ELECTRIC
    assert str(sys_1)
    assert repr(sys_1)

    assert sys_2.id_num == 2
    assert sys_2.system_type == enums.DeviceType.ELECTRIC
    assert str(sys_2)
    assert repr(sys_2)


def test_set_PhxMechanicalSubSystem_identifier(reset_class_counters):
    sys_1 = _base.PhxMechanicalSubSystem()

    sys_1.identifier = 'this is a test'
    assert sys_1.identifier == 'this is a test'

    sys_1.identifier = 12
    assert sys_1.identifier == '12'

    sys_1.identifier = None
    assert sys_1.identifier == '12'
