from honeybee_phhvac.hot_water_piping import PhHvacPipeElement, PhHvacPipeTrunk
from honeybee_phhvac.hot_water_devices import PhHvacHotWaterTank
from honeybee_phhvac.hot_water_system import HotWaterSystem


def test_basic_HotWaterSystem_round_trip():
    obj = HotWaterSystem(None)
    d = obj.to_dict()
    new_obj = HotWaterSystem.from_dict(d["ph"], None)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_copy():
    system = HotWaterSystem(None)
    system.id_num = 1
    system.tank_1 = PhHvacHotWaterTank()
    system.tank_2 = PhHvacHotWaterTank()
    system.tank_buffer = PhHvacHotWaterTank()
    system.tank_solar = PhHvacHotWaterTank()
    system._heaters = {}
    system._distribution_piping = {
        "trunk_1": PhHvacPipeTrunk(),
        "trunk_2": PhHvacPipeTrunk(),
    }
    system._recirc_piping = {"recirc_1": PhHvacPipeElement(), "recirc_2": PhHvacPipeElement()}
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
