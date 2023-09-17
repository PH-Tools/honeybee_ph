from honeybee_energy_ph.properties.hot_water.hw_system import SHWSystemPhProperties
from honeybee_energy_ph.hvac.hot_water import PhSHWTank, PhPipeElement


def test_basic_SHWSystemPhProperties_round_trip():
    obj = SHWSystemPhProperties(None)
    d = obj.to_dict()
    new_obj = SHWSystemPhProperties.from_dict(d["ph"], None)
    assert new_obj.to_dict() == d


def test_SHWSystemPhProperties_copy():
    system = SHWSystemPhProperties(None)
    system.id_num = 1
    system.tank_1 = PhSHWTank()
    system.tank_2 = PhSHWTank()
    system.tank_buffer = PhSHWTank()
    system.tank_solar = PhSHWTank()
    system._heaters = {}
    system._distribution_piping = {
        "branch_1": PhPipeElement(),
        "branch_2": PhPipeElement(),
    }
    system._recirc_piping = {"recirc_1": PhPipeElement(), "recirc_2": PhPipeElement()}
    system._number_tap_points = 2

    new_system = system.__copy__()

    assert new_system.id_num == system.id_num
    assert new_system.tank_1 == system.tank_1
    assert new_system.tank_2 == system.tank_2
    assert new_system.tank_buffer == system.tank_buffer
    assert new_system.tank_solar == system.tank_solar
    assert new_system._heaters == system._heaters
    assert new_system._distribution_piping == system._distribution_piping
    assert new_system._recirc_piping == system._recirc_piping
    assert new_system._number_tap_points == system._number_tap_points
    assert new_system.recirc_temp == system.recirc_temp
    assert new_system.recirc_hours == system.recirc_hours
