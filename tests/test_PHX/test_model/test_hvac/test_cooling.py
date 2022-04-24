from PHX.model.hvac import cooling, enums

def test_default_PhxCoolingDevice(reset_class_counters):
    dev_1 = cooling.PhxCoolingDevice()
    dev_2 = cooling.PhxCoolingDevice()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True

def test_default_PhxCooingVentilation(reset_class_counters):
    dev_1 = cooling.PhxCoolingVentilation()
    dev_2 = cooling.PhxCoolingVentilation()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.device_type == enums.DeviceType.HEAT_PUMP
    assert dev_2.device_type == enums.DeviceType.HEAT_PUMP
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True

def test_add_default_PhxCooingVentilation(reset_class_counters):
    dev_1 = cooling.PhxCoolingVentilation()
    dev_2 = cooling.PhxCoolingVentilation()
    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.single_speed == dev_1.params.single_speed
    assert dev_3.params.min_coil_temp == dev_1.params.min_coil_temp
    assert dev_3.params.capacity == dev_1.params.capacity
    assert dev_3.params.annual_COP == dev_1.params.annual_COP

def test_add_mixed_PhxCooingVentilation(reset_class_counters):
    dev_1 = cooling.PhxCoolingVentilation()
    dev_1.percent_coverage = 0.25
    dev_1.params = cooling.PhxCoolingVentilationParams(
        hp_type = enums.HeatPumpType.ANNUAL,
        single_speed = True,
        min_coil_temp = 20,
        capacity = 20,
        annual_COP = 20,
    )
    dev_2 = cooling.PhxCoolingVentilation()
    dev_2.percent_coverage = 0.5
    dev_2.params = cooling.PhxCoolingVentilationParams(
        hp_type = enums.HeatPumpType.ANNUAL,
        single_speed = False,
        min_coil_temp = 10,
        capacity = 10,
        annual_COP = 10,
    )

    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.percent_coverage == 0.75
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == True
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.single_speed == True
    assert dev_3.params.min_coil_temp == 15
    assert dev_3.params.capacity == 15
    assert dev_3.params.annual_COP == 15