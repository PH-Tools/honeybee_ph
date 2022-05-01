from PHX.model.enums import hvac
from PHX.model.hvac import cooling


def test_default_PhxCoolingDevice(reset_class_counters):
    dev_1 = cooling.PhxCoolingDevice()
    dev_2 = cooling.PhxCoolingDevice()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True


# -- Ventilation Cooling ------------------------------------------------------

def test_default_PhxCoolingVentilationParams(reset_class_counters):
    p1 = cooling.PhxCoolingVentilationParams()
    p2 = cooling.PhxCoolingVentilationParams()

    p3 = p1 + p2
    assert p3 == p2 == p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.single_speed == p1.single_speed
    assert p3.min_coil_temp == p1.min_coil_temp
    assert p3.capacity == p1.capacity
    assert p3.annual_COP == p1.annual_COP
    assert p3.total_system_perf_ratio == p1.total_system_perf_ratio


def test_mixed_PhxCoolingVentilationParams(reset_class_counters):
    p1 = cooling.PhxCoolingVentilationParams(
        single_speed=True,
        min_coil_temp=20,
        capacity=20,
        annual_COP=6,
    )
    p2 = cooling.PhxCoolingVentilationParams(
        single_speed=False,
        min_coil_temp=10,
        capacity=10,
        annual_COP=4,
    )

    p3 = p1 + p2
    assert p3 != p2 != p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.single_speed == True
    assert p3.min_coil_temp == 15
    assert p3.capacity == 15
    assert p3.annual_COP == 5
    assert p3.total_system_perf_ratio == 0.2


def test_default_PhxCoolingVentilation(reset_class_counters):
    dev_1 = cooling.PhxCoolingVentilation()
    dev_2 = cooling.PhxCoolingVentilation()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_2.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True


def test_add_default_PhxCoolingVentilation(reset_class_counters):
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


def test_add_mixed_PhxCoolingVentilation(reset_class_counters):
    dev_1 = cooling.PhxCoolingVentilation()
    dev_1.percent_coverage = 0.25
    dev_1.params = cooling.PhxCoolingVentilationParams(
        single_speed=True,
        min_coil_temp=20,
        capacity=20,
        annual_COP=20,
    )
    dev_2 = cooling.PhxCoolingVentilation()
    dev_2.percent_coverage = 0.5
    dev_2.params = cooling.PhxCoolingVentilationParams(
        single_speed=False,
        min_coil_temp=10,
        capacity=10,
        annual_COP=10,
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


# -- Recirculation Cooling ------------------------------------------------------


def test_default_PhxCoolingRecirculationParams(reset_class_counters):
    p1 = cooling.PhxCoolingRecirculationParams()
    p2 = cooling.PhxCoolingRecirculationParams()

    p3 = p1 + p2
    assert p3 == p2 == p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.single_speed == p1.single_speed
    assert p3.min_coil_temp == p1.min_coil_temp
    assert p3.capacity == p1.capacity
    assert p3.annual_COP == p1.annual_COP
    assert p3.total_system_perf_ratio == p1.total_system_perf_ratio
    assert p3.flow_rate_m3_hr == p1.flow_rate_m3_hr
    assert p3.flow_rate_variable == p1.flow_rate_variable


def test_mixed_PhxCoolingRecirculationParams(reset_class_counters):
    p1 = cooling.PhxCoolingRecirculationParams(
        single_speed=True,
        min_coil_temp=20,
        capacity=20,
        annual_COP=6,
        flow_rate_m3_hr=100,
        flow_rate_variable=True
    )
    p2 = cooling.PhxCoolingRecirculationParams(
        single_speed=False,
        min_coil_temp=10,
        capacity=10,
        annual_COP=4,
        flow_rate_m3_hr=50,
        flow_rate_variable=False
    )

    p3 = p1 + p2
    assert p3 != p2 != p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.single_speed == True
    assert p3.min_coil_temp == 15
    assert p3.capacity == 15
    assert p3.annual_COP == 5
    assert p3.total_system_perf_ratio == 0.2
    assert p3.flow_rate_m3_hr == 75
    assert p3.flow_rate_variable == True


def test_default_PhxCoolingRecirculation(reset_class_counters):
    dev_1 = cooling.PhxCoolingRecirculation()
    dev_2 = cooling.PhxCoolingRecirculation()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_2.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True


def test_add_default_PhxCoolingRecirculation(reset_class_counters):
    dev_1 = cooling.PhxCoolingRecirculation()
    dev_2 = cooling.PhxCoolingRecirculation()
    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.single_speed == dev_1.params.single_speed
    assert dev_3.params.min_coil_temp == dev_1.params.min_coil_temp
    assert dev_3.params.capacity == dev_1.params.capacity
    assert dev_3.params.annual_COP == dev_1.params.annual_COP
    assert dev_3.params.total_system_perf_ratio == dev_1.params.total_system_perf_ratio
    assert dev_3.params.flow_rate_m3_hr == dev_1.params.flow_rate_m3_hr
    assert dev_3.params.flow_rate_variable == dev_1.params.flow_rate_variable


def test_add_mixed_PhxCoolingRecirculation(reset_class_counters):
    dev_1 = cooling.PhxCoolingRecirculation()
    dev_1.params = cooling.PhxCoolingRecirculationParams(
        single_speed=True,
        min_coil_temp=20,
        capacity=20,
        annual_COP=6,
        flow_rate_m3_hr=100,
        flow_rate_variable=True
    )
    dev_2 = cooling.PhxCoolingRecirculation()
    dev_2.params = cooling.PhxCoolingRecirculationParams(
        single_speed=False,
        min_coil_temp=10,
        capacity=10,
        annual_COP=4,
        flow_rate_m3_hr=50,
        flow_rate_variable=False
    )

    dev_3 = dev_1 + dev_2

    # --Base Params
    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling

    # -- Class Specific Params
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.single_speed == True
    assert dev_3.params.min_coil_temp == 15
    assert dev_3.params.capacity == 15
    assert dev_3.params.annual_COP == 5
    assert dev_3.params.total_system_perf_ratio == 0.2
    assert dev_3.params.flow_rate_m3_hr == 75
    assert dev_3.params.flow_rate_variable == True


# -- Dehumidification ---------------------------------------------------------


def test_default_PhxCoolingDehumidificationParams(reset_class_counters):
    p1 = cooling.PhxCoolingDehumidificationParams()
    p2 = cooling.PhxCoolingDehumidificationParams()

    p3 = p1 + p2
    assert p3 == p2 == p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.annual_COP == p1.annual_COP
    assert p3.total_system_perf_ratio == p1.total_system_perf_ratio
    assert p3.useful_heat_loss == p1.useful_heat_loss


def test_mixed_PhxCoolingDehumidificationParams(reset_class_counters):
    p1 = cooling.PhxCoolingDehumidificationParams(
        annual_COP=6,
        useful_heat_loss=False
    )
    p2 = cooling.PhxCoolingDehumidificationParams(
        annual_COP=4,
        useful_heat_loss=True
    )

    p3 = p1 + p2
    assert p3 != p2 != p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.annual_COP == 5
    assert p3.total_system_perf_ratio == 0.2
    assert p3.useful_heat_loss == True


def test_default_PhxCoolingDehumidification(reset_class_counters):
    dev_1 = cooling.PhxCoolingDehumidification()
    dev_2 = cooling.PhxCoolingDehumidification()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_2.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True


def test_add_default_PhxCoolingDehumidification(reset_class_counters):
    dev_1 = cooling.PhxCoolingDehumidification()
    dev_2 = cooling.PhxCoolingDehumidification()
    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.annual_COP == dev_1.params.annual_COP
    assert dev_3.params.total_system_perf_ratio == dev_1.params.total_system_perf_ratio
    assert dev_3.params.useful_heat_loss == dev_1.params.useful_heat_loss


def test_add_mixed_PhxCoolingDehumidification(reset_class_counters):
    dev_1 = cooling.PhxCoolingDehumidification()
    dev_1.params = cooling.PhxCoolingDehumidificationParams(
        annual_COP=6,
        useful_heat_loss=False
    )

    dev_2 = cooling.PhxCoolingDehumidification()
    dev_2.params = cooling.PhxCoolingDehumidificationParams(
        annual_COP=4,
        useful_heat_loss=True
    )

    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling

    # -- Class-specific attrs
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.annual_COP == 5
    assert dev_3.params.total_system_perf_ratio == 0.2
    assert dev_3.params.useful_heat_loss == True


# -- Panel Cooling ------------------------------------------------------------


def test_default_PhxCoolingPanelParams(reset_class_counters):
    p1 = cooling.PhxCoolingPanelParams()
    p2 = cooling.PhxCoolingPanelParams()

    p3 = p1 + p2
    assert p3 == p2 == p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.annual_COP == p1.annual_COP
    assert p3.total_system_perf_ratio == p1.total_system_perf_ratio


def test_mixed_PhxCoolingPanelParams(reset_class_counters):
    p1 = cooling.PhxCoolingPanelParams(
        hp_type=hvac.HeatPumpType.ANNUAL,
        annual_COP=6,
    )
    p2 = cooling.PhxCoolingPanelParams(
        hp_type=hvac.HeatPumpType.ANNUAL,
        annual_COP=4,
    )

    p3 = p1 + p2
    assert p3 != p2 != p1

    # -- Base attrs
    assert p3.aux_energy == p1.aux_energy
    assert p3.aux_energy_dhw == p1.aux_energy_dhw
    assert p3.solar_fraction == p1.solar_fraction
    assert p3.in_conditioned_space == p1.in_conditioned_space

    # -- Class-specific attrs
    assert p3.hp_type == p1.hp_type
    assert p3.annual_COP == 5
    assert p3.total_system_perf_ratio == 0.2


def test_default_PhxCoolingPanel(reset_class_counters):
    dev_1 = cooling.PhxCoolingPanel()
    dev_2 = cooling.PhxCoolingPanel()

    assert dev_1.id_num == 1
    assert dev_2.id_num == 2
    assert dev_1.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_2.device_type == hvac.DeviceType.HEAT_PUMP
    assert dev_1.usage_profile.cooling == True
    assert dev_2.usage_profile.cooling == True


def test_add_default_PhxCoolingPanel(reset_class_counters):
    dev_1 = cooling.PhxCoolingPanel()
    dev_2 = cooling.PhxCoolingPanel()
    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.annual_COP == dev_1.params.annual_COP
    assert dev_3.params.total_system_perf_ratio == dev_1.params.total_system_perf_ratio


def test_add_mixed_PhxCoolingPanel(reset_class_counters):
    dev_1 = cooling.PhxCoolingPanel()
    dev_1.params = cooling.PhxCoolingPanelParams(
        hp_type=hvac.HeatPumpType.ANNUAL,
        annual_COP=6,
    )
    dev_2 = cooling.PhxCoolingPanel()
    dev_2.params = cooling.PhxCoolingPanelParams(
        hp_type=hvac.HeatPumpType.ANNUAL,
        annual_COP=4,
    )

    dev_3 = dev_1 + dev_2

    assert dev_3 != dev_2 != dev_1
    assert dev_3.device_type == dev_1.device_type
    assert dev_3.usage_profile.cooling == dev_1.usage_profile.cooling

    # -- Class-specific attrs
    assert dev_3.params.hp_type == dev_1.params.hp_type
    assert dev_3.params.annual_COP == 5
    assert dev_3.params.total_system_perf_ratio == 0.2
