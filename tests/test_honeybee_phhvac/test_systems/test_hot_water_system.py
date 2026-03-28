from copy import copy

import pytest
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from ladybug_geometry.geometry3d.polyline import LineSegment3D

from honeybee_phhvac import hot_water_piping as hwp
from honeybee_phhvac import hot_water_system as hws
from honeybee_phhvac.hot_water_devices import PhHvacHotWaterHeaterElectric, PhHvacHotWaterTank


def test_basic_HotWaterSystem_round_trip():
    obj = hws.PhHotWaterSystem()
    assert str(obj)
    assert repr(obj)
    assert obj.ToString()
    assert not obj.tank_1
    assert not obj.tank_2
    assert not obj.tank_buffer
    assert not obj.tank_solar
    assert not obj.heaters
    assert not obj.distribution_piping
    assert not obj.recirc_piping
    assert obj.number_tap_points == 0

    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)

    assert str(obj)
    assert repr(obj)
    assert obj.ToString()
    assert new_obj.to_dict() == d
    assert not new_obj.tank_1
    assert not new_obj.tank_2
    assert not new_obj.tank_buffer
    assert not new_obj.tank_solar
    assert not new_obj.heaters
    assert not new_obj.distribution_piping
    assert not new_obj.recirc_piping
    assert new_obj.number_tap_points == 0


def test_from_dict_wrong_type_raises_PhHotWaterSystem_FromDictError():
    obj = hws.PhHotWaterSystem()
    d = obj.to_dict()
    d["type"] = "not_a_valid_system_type"  # type: ignore

    with pytest.raises(hws.PhHotWaterSystem_FromDictError):
        hws.PhHotWaterSystem.from_dict(d)


def test_HotWaterSystem_round_trip_with_one_tank():
    obj = hws.PhHotWaterSystem()
    obj.tank_1 = PhHvacHotWaterTank()
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_two_tanks():
    obj = hws.PhHotWaterSystem()
    obj.tank_1 = PhHvacHotWaterTank()
    obj.tank_2 = PhHvacHotWaterTank()
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_three_tanks():
    obj = hws.PhHotWaterSystem()
    obj.tank_1 = PhHvacHotWaterTank()
    obj.tank_2 = PhHvacHotWaterTank()
    obj.tank_buffer = PhHvacHotWaterTank()
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_four_tanks():
    obj = hws.PhHotWaterSystem()
    obj.tank_1 = PhHvacHotWaterTank()
    obj.tank_2 = PhHvacHotWaterTank()
    obj.tank_buffer = PhHvacHotWaterTank()
    obj.tank_solar = PhHvacHotWaterTank()
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_one_heater():
    obj = hws.PhHotWaterSystem()
    assert len(obj.heaters) == 0
    obj.add_heater(None)
    assert len(obj.heaters) == 0

    obj.add_heater(PhHvacHotWaterHeaterElectric())
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_two_heaters():
    obj = hws.PhHotWaterSystem()
    obj.add_heater(PhHvacHotWaterHeaterElectric())
    obj.add_heater(PhHvacHotWaterHeaterElectric())
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_one_distribution_Trunk():
    obj = hws.PhHotWaterSystem()
    obj.add_distribution_piping(hwp.PhHvacPipeTrunk())
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_one_distribution_Branch():
    obj = hws.PhHotWaterSystem()
    obj.add_distribution_piping(hwp.PhHvacPipeBranch())
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_one_distribution_Element():
    obj = hws.PhHotWaterSystem()
    obj.add_distribution_piping(hwp.PhHvacPipeElement())
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_round_trip_with_one_recirc_Element():
    obj = hws.PhHotWaterSystem()
    obj.add_recirc_piping(hwp.PhHvacPipeElement())
    d = obj.to_dict()
    new_obj = hws.PhHotWaterSystem.from_dict(d)
    assert new_obj.to_dict() == d


def test_HotWaterSystem_copy():
    system = hws.PhHotWaterSystem()
    new_system_a = copy(system)
    assert system == hws.PhHotWaterSystem.from_dict(new_system_a.to_dict())

    system.id_num = 1
    system.tank_1 = PhHvacHotWaterTank()
    system.tank_2 = PhHvacHotWaterTank()
    system.tank_buffer = PhHvacHotWaterTank()
    system.tank_solar = PhHvacHotWaterTank()
    system.add_heater(PhHvacHotWaterHeaterElectric())
    system.add_distribution_piping(hwp.PhHvacPipeTrunk())
    system.add_distribution_piping(hwp.PhHvacPipeBranch())
    system.add_recirc_piping(hwp.PhHvacPipeElement())
    system.number_tap_points = 2

    new_system_b = copy(system)
    assert system == hws.PhHotWaterSystem.from_dict(new_system_b.to_dict())

    new_system_c = system.duplicate()
    assert system == hws.PhHotWaterSystem.from_dict(new_system_c.to_dict())


def test_total_distribution_pipe_length():
    system = hws.PhHotWaterSystem()
    assert system.total_distribution_pipe_length == 0.0

    pt1 = Point3D(0, 0, 0)
    vec1 = Vector3D(0, 0, 1)

    pipe_1 = hwp.PhHvacPipeElement()
    pipe_1.add_segment(hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 30.0)))
    pipe_1.add_segment(hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 30.0)))
    system.add_distribution_piping(pipe_1)

    assert system.total_distribution_pipe_length == 60.0


def test_total_home_run_fixture_pipe_length():
    system = hws.PhHotWaterSystem()
    assert system.total_home_run_fixture_pipe_length == 0.0

    line_segment_1 = LineSegment3D.from_sdl(Point3D(0, 0, 0), Vector3D(0, 0, 1), 30.0)
    pipe_segment_1 = hwp.PhHvacPipeSegment(line_segment_1)
    pipe_element_1 = hwp.PhHvacPipeElement()
    pipe_element_1.add_segment(pipe_segment_1)

    fixture1 = hwp.PhHvacPipeElement()
    fixture1.add_segment(pipe_segment_1)
    assert fixture1.length == 30.0

    branch1 = hwp.PhHvacPipeBranch()
    branch1.pipe_element = pipe_element_1
    branch1.add_fixture(fixture1)
    assert branch1.length == 30.0
    assert branch1.total_length == 60.0
    assert branch1.total_home_run_fixture_length == 60.0

    trunk1 = hwp.PhHvacPipeTrunk()
    trunk1.pipe_element = pipe_element_1
    trunk1.add_branch(branch1)

    system.add_distribution_piping(trunk1)
    assert system.total_home_run_fixture_pipe_length == 90.0

    system.clear_distribution_piping()
    assert system.total_home_run_fixture_pipe_length == 0.0


def test_recirc_piping_total_length():
    system = hws.PhHotWaterSystem()
    assert system.total_recirc_pipe_length == 0.0

    pt1 = Point3D(0, 0, 0)
    vec1 = Vector3D(0, 0, 1)
    pipe_segment_1 = hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 30.0))
    pipe_segment_2 = hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 50.0))

    pipe_element_1 = hwp.PhHvacPipeElement()
    pipe_element_1.add_segment(pipe_segment_1)
    pipe_element_1.add_segment(pipe_segment_2)
    system.add_recirc_piping(pipe_element_1)

    assert system.total_recirc_pipe_length == 80.0


def test_recirc_default_temp_and_run_period():
    obj = hws.PhHotWaterSystem()
    assert obj.recirc_temp == 60.0
    assert obj.recirc_hours == 24


def test_recirc_custom_temp_and_run_period():
    system = hws.PhHotWaterSystem()
    assert system.recirc_temp == 60.0
    assert system.recirc_hours == 24

    pt1 = Point3D(0, 0, 0)
    vec1 = Vector3D(0, 0, 1)
    pipe_segment_1 = hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 30.0))
    pipe_segment_1.water_temp_c = 50.0
    pipe_segment_1.daily_period = 12
    pipe_segment_2 = hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 50.0))
    pipe_segment_2.water_temp_c = 100.0
    pipe_segment_1.daily_period = 6

    pipe_element_1 = hwp.PhHvacPipeElement()
    pipe_element_1.add_segment(pipe_segment_1)
    pipe_element_1.add_segment(pipe_segment_2)
    system.add_recirc_piping(pipe_element_1)

    assert system.recirc_temp == 81.25
    assert system.recirc_hours == 17


# -- Transforms ---


def test_scale_system_with_no_piping():
    system = hws.PhHotWaterSystem()
    system.scale(0.0254)
    assert system.total_distribution_pipe_length == 0
    assert system.total_recirc_pipe_length == 0


def test_scale_system_with_single_trunk():
    system1 = hws.PhHotWaterSystem()
    pt1 = Point3D(0, 0, 0)
    vec1 = Vector3D(0, 0, 1)
    pipe_segment_1 = hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 144.0))
    pipe_element_1 = hwp.PhHvacPipeElement()
    pipe_element_1.add_segment(pipe_segment_1)
    trunk1 = hwp.PhHvacPipeTrunk()
    trunk1.pipe_element = pipe_element_1
    system1.add_distribution_piping(trunk1)

    system2 = system1.scale(0.0254)
    assert system1.total_distribution_pipe_length == pytest.approx(144.0)
    assert system2.total_distribution_pipe_length == pytest.approx(3.6576)


def test_scale_system_with_single_recirc_element():
    system1 = hws.PhHotWaterSystem()
    pt1 = Point3D(0, 0, 0)
    vec1 = Vector3D(0, 0, 1)
    pipe_segment_1 = hwp.PhHvacPipeSegment(LineSegment3D.from_sdl(pt1, vec1, 144.0))
    pipe_element_1 = hwp.PhHvacPipeElement()
    pipe_element_1.add_segment(pipe_segment_1)
    system1.add_recirc_piping(pipe_element_1)

    system2 = system1.scale(0.0254)
    assert system1.total_recirc_pipe_length == pytest.approx(144.0)
    assert system2.total_recirc_pipe_length == pytest.approx(3.6576)
