from PHX.model.hvac import heating, enums


def test_PhxHeatingDevice(reset_class_counters):
    d1 = heating.PhxHeatingDevice()
    d2 = heating.PhxHeatingDevice()

    assert d1.id_num == 1
    assert d2.id_num == 2


# -----------------------------------------------------------------------------
# Electric

def test_default_PhxHeaterElectric(reset_class_counters):
    d1 = heating.PhxHeaterElectric()
    d2 = heating.PhxHeaterElectric()

    assert d1.id_num == 1
    assert d2.id_num == 2


# -----------------------------------------------------------------------------
# Boilers

def test_default_PhxHeaterBoilerFossil(reset_class_counters):
    d1 = heating.PhxHeaterBoilerFossil()
    d2 = heating.PhxHeaterBoilerFossil()

    assert d1.id_num == 1
    assert d2.id_num == 2


def test_PhxHeaterBoilerFossil_set_fuel(reset_class_counters):
    d1 = heating.PhxHeaterBoilerFossil()
    d1.params.fuel = 1
    d2 = heating.PhxHeaterBoilerFossil()
    d2.params.fuel = 2

    assert d1.params.fuel == enums.FuelType.GAS
    assert d2.params.fuel == enums.FuelType.OIL


def test_default_PhxHeaterBoilerWood(reset_class_counters):
    d1 = heating.PhxHeaterBoilerWood()
    d2 = heating.PhxHeaterBoilerWood()

    assert d1.id_num == 1
    assert d2.id_num == 2


def test_PhxHeaterBoilerWood_set_fuel(reset_class_counters):
    d1 = heating.PhxHeaterBoilerWood()
    d1.params.fuel = 3
    d2 = heating.PhxHeaterBoilerWood()
    d2.params.fuel = 4

    assert d1.params.fuel == enums.FuelType.WOOD_LOG
    assert d2.params.fuel == enums.FuelType.WOOD_PELLET

# -----------------------------------------------------------------------------
# District Heat


def test_default_PhxHeaterDistrictHeat(reset_class_counters):
    d1 = heating.PhxHeaterDistrictHeat()
    d2 = heating.PhxHeaterDistrictHeat()

    assert d1.id_num == 1
    assert d2.id_num == 2

# -----------------------------------------------------------------------------
# Heat Pumps


def test_default_PhxHeaterHeatPumpAnnual(reset_class_counters):
    d1 = heating.PhxHeaterHeatPumpAnnual()
    d2 = heating.PhxHeaterHeatPumpAnnual()

    assert d1.id_num == 1
    assert d2.id_num == 2


def test_default_PhxHeaterHeatPumpMonthly(reset_class_counters):
    d1 = heating.PhxHeaterHeatPumpMonthly()
    d2 = heating.PhxHeaterHeatPumpMonthly()

    assert d1.id_num == 1
    assert d2.id_num == 2


def test_default_PhxHeaterHeatPumpMonthlyParams_set_monthly_COPs(reset_class_counters):
    p1 = heating.PhxHeaterHeatPumpMonthlyParams()
    p2 = heating.PhxHeaterHeatPumpMonthlyParams()

    p1.monthly_COPS = []
    assert p1.COP_1 == None
    assert p1.COP_2 == None
    assert p1.monthly_COPS == None
    assert p2.COP_1 == None
    assert p2.COP_2 == None
    assert p2.monthly_COPS == None

    p1.monthly_COPS = [1, 2]
    assert p1.COP_1 == 1
    assert p1.COP_2 == 2
    assert p1.monthly_COPS == None
    assert p2.COP_1 == None
    assert p2.COP_2 == None
    assert p2.monthly_COPS == None

    p2.monthly_COPS = [12]
    assert p1.COP_1 == 1
    assert p1.COP_2 == 2
    assert p1.monthly_COPS == None
    assert p2.COP_1 == 12
    assert p2.COP_2 == 12
    assert p2.monthly_COPS == None

    p1.monthly_COPS = [6, 5, 4]
    assert p1.COP_1 == 6
    assert p1.COP_2 == 5
    assert p1.monthly_COPS == None
    assert p2.COP_1 == 12
    assert p2.COP_2 == 12
    assert p2.monthly_COPS == None


def test_default_PhxHeaterHeatPumpMonthlyParams_set_monthly_temps(reset_class_counters):
    p1 = heating.PhxHeaterHeatPumpMonthlyParams()
    p2 = heating.PhxHeaterHeatPumpMonthlyParams()

    p1.monthly_temps = []
    assert p1.ambient_temp_1 == None
    assert p1.ambient_temp_2 == None
    assert p1.monthly_temps == None
    assert p2.ambient_temp_1 == None
    assert p2.ambient_temp_2 == None
    assert p2.monthly_temps == None

    p1.monthly_temps = [1, 2]
    assert p1.ambient_temp_1 == 1
    assert p1.ambient_temp_2 == 2
    assert p1.monthly_temps == None
    assert p2.ambient_temp_1 == None
    assert p2.ambient_temp_2 == None
    assert p2.monthly_temps == None

    p2.monthly_temps = [12]
    assert p1.ambient_temp_1 == 1
    assert p1.ambient_temp_2 == 2
    assert p1.monthly_temps == None
    assert p2.ambient_temp_1 == 12
    assert p2.ambient_temp_2 == 12
    assert p2.monthly_temps == None

    p1.monthly_temps = [6, 5, 4]
    assert p1.ambient_temp_1 == 6
    assert p1.ambient_temp_2 == 5
    assert p1.monthly_temps == None
    assert p2.ambient_temp_1 == 12
    assert p2.ambient_temp_2 == 12
    assert p2.monthly_temps == None


def test_default_PhxHeaterHeatPumpHotWater(reset_class_counters):
    d1 = heating.PhxHeaterHeatPumpHotWater()
    d2 = heating.PhxHeaterHeatPumpHotWater()

    assert d1.id_num == 1
    assert d2.id_num == 2


def test_default_PhxHeaterHeatPumpCombined(reset_class_counters):
    d1 = heating.PhxHeaterHeatPumpCombined()
    d2 = heating.PhxHeaterHeatPumpCombined()

    assert d1.id_num == 1
    assert d2.id_num == 2
