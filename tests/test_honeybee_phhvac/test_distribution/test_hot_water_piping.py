from math import radians

import pytest
from ladybug_geometry.geometry3d.line import LineSegment3D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D

from honeybee_phhvac import hot_water_piping

# -- Segment


def test_PhPipeSegment_dict_round_trip():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    pipe1 = hot_water_piping.PhHvacPipeSegment(geom)
    d_1 = pipe1.to_dict()
    pipe2 = hot_water_piping.PhHvacPipeSegment.from_dict(d_1)

    assert pipe2.to_dict() == pipe1.to_dict()

    # -- Add user-data
    pipe2.user_data["test_key"] = "test_vale"
    assert "test_key" in pipe2.user_data
    assert "test_key" not in pipe1.user_data
    assert pipe2.to_dict() != pipe1.to_dict()


def test_scale_PhPipeSegment():
    p1, p2 = Point3D(0, 0, 0), Vector3D(0, 0, 10)
    geom = LineSegment3D(p1, p2)
    pipe1 = hot_water_piping.PhHvacPipeSegment(geom, _insul_thickness=1.0)
    assert pipe1.length == 10
    assert pipe1.insulation_thickness == 1.0

    pipe2 = pipe1.scale(2.0)

    assert pipe1.length == 10
    assert pipe1.insulation_thickness == 1.0

    assert pipe2.length == 20
    assert pipe2.insulation_thickness == 2.0


# -- Element


def test_PhPipeElement_dict_round_trip():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    d1 = ele1.to_dict()

    ele2 = hot_water_piping.PhHvacPipeElement.from_dict(d1)

    assert ele1.to_dict() == ele2.to_dict()

    # -- Add user-data
    ele2.user_data["test_key"] = "test_vale"
    assert "test_key" in ele2.user_data
    assert "test_key" not in ele1.user_data
    assert ele2.to_dict() != ele1.to_dict()


def test_PhPipeElement_segment_names():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    seg1.display_name = "segment_0"
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    assert ele1.segment_names == ["segment_0"]


def test_PhPipeElement_with_no_segments_material_name():
    ele1 = hot_water_piping.PhHvacPipeElement()
    assert ele1.material_name == "1-COPPER_M"


def test_PhPipeElement_with_one_segments_material_name():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _material=3)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    assert ele1.material_name == "3-COPPER_K"


def test_PhPipeElement_with_two_same_segments_material_name():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _material=3)
    seg2 = hot_water_piping.PhHvacPipeSegment(geom, _material=3)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    ele1.add_segment(seg2)

    assert ele1.material_name == "3-COPPER_K"


def test_PhPipeElement_with_two_different_segments_material_name():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _material=3)
    seg2 = hot_water_piping.PhHvacPipeSegment(geom, _material=4)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    ele1.add_segment(seg2)

    with pytest.raises(ValueError):
        assert ele1.material_name == "3-COPPER_K"


def test_PhPipeElement_with_no_segments_diameter_name():
    ele1 = hot_water_piping.PhHvacPipeElement()
    assert ele1.diameter_name == "1-3/8in"


def test_PhPipeElement_with_one_segments_diameter_name():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _diameter=2)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    assert ele1.diameter_name == "2-1/2IN"


def test_PhPipeElement_with_two_same_segments_diameter_name():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _diameter=2)
    seg2 = hot_water_piping.PhHvacPipeSegment(geom, _diameter=2)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    ele1.add_segment(seg2)

    assert ele1.diameter_name == "2-1/2IN"


def test_PhPipeElement_with_two_different_segments_diameter_name():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _diameter=2)
    seg2 = hot_water_piping.PhHvacPipeSegment(geom, _diameter=3)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    ele1.add_segment(seg2)

    with pytest.raises(ValueError):
        assert ele1.diameter_name == "2-1/2IN"


def test_scale_PhPipeElement_with_multiple_segments():
    p1, p2 = Point3D(0, 0, 0), Vector3D(0, 0, 10)
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _insul_thickness=1.0)
    seg2 = hot_water_piping.PhHvacPipeSegment(geom, _insul_thickness=2.0)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    ele1.add_segment(seg2)

    assert ele1.length == 20

    ele2 = ele1.scale(2.0)

    assert ele1.length == 20
    assert ele2.length == 40


def test_rotate_xy_PhPipeElement_with_multiple_segments():
    p1, p2 = Point3D(0, 0, 0), Vector3D(10, 0, 0)
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom, _insul_thickness=1.0)
    seg2 = hot_water_piping.PhHvacPipeSegment(geom, _insul_thickness=2.0)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)
    ele1.add_segment(seg2)

    assert ele1.length == 20.0
    assert ele1.segments[0].geometry.p2.x == pytest.approx(10.0)

    # +90 means a 90 degree COUNTER-clockwise rotation
    ele2 = ele1.rotate_xy(90, Point3D(0, 0, 0))

    assert ele1.length == pytest.approx(20.0)
    assert ele2.length == pytest.approx(20.0)
    assert ele2.segments[0].geometry.p2.x == pytest.approx(0.0)
    assert ele2.segments[0].geometry.p2.y == pytest.approx(10.0)
    assert ele2.segments[0].geometry.p2.z == pytest.approx(0.0)

    # +180 means a 189 degree COUNTER-clockwise rotation
    ele3 = ele1.rotate_xy(180, Point3D(0, 0, 0))

    assert ele1.length == pytest.approx(20.0)
    assert ele3.length == pytest.approx(20.0)
    assert ele3.segments[0].geometry.p2.x == pytest.approx(-10.0)
    assert ele3.segments[0].geometry.p2.y == pytest.approx(0.0)
    assert ele3.segments[0].geometry.p2.z == pytest.approx(0.0)

    # +180 means a 189 degree COUNTER-clockwise rotation
    ele4 = ele1.rotate_xy(270, Point3D(0, 0, 0))

    assert ele1.length == pytest.approx(20.0)
    assert ele4.length == pytest.approx(20.0)
    assert ele4.segments[0].geometry.p2.x == pytest.approx(0.0)
    assert ele4.segments[0].geometry.p2.y == pytest.approx(-10.0)
    assert ele4.segments[0].geometry.p2.z == pytest.approx(0.0)


# --- Branch


def test_PhPipeBranch_dict_round_trip():
    # -- Build the Pipe Element
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    # -- Build the Branch
    branch1 = hot_water_piping.PhHvacPipeBranch()
    branch1.pipe_element = ele1
    branch1.add_fixture(ele1)
    d1 = branch1.to_dict()

    # --
    branch2 = hot_water_piping.PhHvacPipeBranch.from_dict(d1)

    assert branch1.to_dict() == branch2.to_dict()

    # -- Add user-data
    branch2.user_data["test_key"] = "test_vale"
    assert "test_key" in branch2.user_data
    assert "test_key" not in branch1.user_data
    assert branch2.to_dict() != branch1.to_dict()


def test_scale_PhPipeBranch_with_element_but_no_fixtures():
    # -- Build the geometry
    p1, p2 = Point3D(0, 0, 0), Vector3D(0, 0, 10)
    geom = LineSegment3D(p1, p2)

    ## -- Set the Branch's Geometry
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    # -- Build the Branch
    branch1 = hot_water_piping.PhHvacPipeBranch()
    branch1.pipe_element = ele1

    assert len(branch1.fixtures) == 0
    assert branch1.length == 10
    assert branch1.total_length == 10

    branch2 = branch1.scale(2.0)

    assert len(branch2.fixtures) == 0
    assert branch2.length == 20
    assert branch2.total_length == 20


def test_scale_PhPipeBranch_with_multiple_fixtures():
    # -- Build the geometry
    p1, p2 = Point3D(0, 0, 0), Vector3D(0, 0, 10)
    geom = LineSegment3D(p1, p2)

    ## -- Set the Branch's Geometry
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    # -- Build the Branch
    branch1 = hot_water_piping.PhHvacPipeBranch()
    branch1.pipe_element = ele1

    # -- Build and add fixtures
    seg2 = hot_water_piping.PhHvacPipeSegment(geom)
    ele2 = hot_water_piping.PhHvacPipeElement()
    ele2.add_segment(seg2)
    branch1.add_fixture(ele2)

    seg3 = hot_water_piping.PhHvacPipeSegment(geom)
    ele3 = hot_water_piping.PhHvacPipeElement()
    ele3.add_segment(seg3)
    branch1.add_fixture(ele3)

    assert len(branch1.fixtures) == 2
    assert branch1.total_length == 30

    branch2 = branch1.scale(2.0)

    assert len(branch2.fixtures) == 2
    assert branch2.total_length == 60


def test_rotate_xy_PhPipeBranch_with_multiple_fixtures():
    # -- Build the geometry
    p1, p2 = Point3D(0, 0, 0), Vector3D(10, 0, 0)
    geom = LineSegment3D(p1, p2)

    ## -- Set the Branch's Geometry
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    # -- Build the Branch
    branch1 = hot_water_piping.PhHvacPipeBranch()
    branch1.pipe_element = ele1

    # -- Build and add fixtures
    seg2 = hot_water_piping.PhHvacPipeSegment(geom)
    ele2 = hot_water_piping.PhHvacPipeElement()
    ele2.add_segment(seg2)
    branch1.add_fixture(ele2)

    seg3 = hot_water_piping.PhHvacPipeSegment(geom)
    ele3 = hot_water_piping.PhHvacPipeElement()
    ele3.add_segment(seg3)
    branch1.add_fixture(ele3)

    assert len(branch1.fixtures) == 2
    assert branch1.total_length == 30

    # +90 means a 90 degree COUNTER-clockwise rotation
    branch2 = branch1.rotate_xy(90, Point3D(0, 0, 0))

    assert len(branch2.fixtures) == 2
    assert branch2.total_length == pytest.approx(30.0)
    assert branch2.fixtures[0].segments[0].geometry.p2.x == pytest.approx(0.0)
    assert branch2.fixtures[0].segments[0].geometry.p2.y == pytest.approx(10.0)
    assert branch2.fixtures[0].segments[0].geometry.p2.z == pytest.approx(0.0)

    # +180 means a 189 degree COUNTER-clockwise rotation
    branch3 = branch1.rotate_xy(180, Point3D(0, 0, 0))

    assert len(branch3.fixtures) == 2
    assert branch3.total_length == pytest.approx(30.0)
    assert branch3.fixtures[0].segments[0].geometry.p2.x == pytest.approx(-10.0)
    assert branch3.fixtures[0].segments[0].geometry.p


# -- Trunk


def test_PhPipeTrunk_dict_round_trip():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    # -- Build the Branch
    branch1 = hot_water_piping.PhHvacPipeBranch()
    branch1.pipe_element = ele1

    # -- Build the Trunk
    trunk1 = hot_water_piping.PhHvacPipeTrunk()
    trunk1.pipe_element = ele1
    trunk1.add_branch(branch1)
    d1 = trunk1.to_dict()

    trunk2 = hot_water_piping.PhHvacPipeTrunk.from_dict(d1)

    assert trunk1.to_dict() == trunk2.to_dict()

    # -- Add user-data
    trunk2.user_data["test_key"] = "test_vale"
    assert "test_key" in trunk2.user_data
    assert "test_key" not in trunk1.user_data
    assert trunk2.to_dict() != trunk1.to_dict()


def test_rotate_xy_PhPipeTrunk_with_multiple_branches():
    # -- Build the geometry
    p1, p2 = Point3D(0, 0, 0), Vector3D(10, 0, 0)
    geom = LineSegment3D(p1, p2)

    ## -- Set the Branch's Geometry
    seg1 = hot_water_piping.PhHvacPipeSegment(geom)
    ele1 = hot_water_piping.PhHvacPipeElement()
    ele1.add_segment(seg1)

    # -- Build the Branch
    branch1 = hot_water_piping.PhHvacPipeBranch()
    branch1.pipe_element = ele1

    # -- Build and add fixtures
    seg2 = hot_water_piping.PhHvacPipeSegment(geom)
    ele2 = hot_water_piping.PhHvacPipeElement()
    ele2.add_segment(seg2)
    branch1.add_fixture(ele2)

    seg3 = hot_water_piping.PhHvacPipeSegment(geom)
    ele3 = hot_water_piping.PhHvacPipeElement()
    ele3.add_segment(seg3)
    branch1.add_fixture(ele3)

    # -- Build the Trunk
    trunk1 = hot_water_piping.PhHvacPipeTrunk()
    trunk1.pipe_element = ele1
    trunk1.add_branch(branch1)

    assert len(trunk1.branches) == 1
    assert trunk1.total_length == 40

    # +90 means a 90 degree COUNTER-clockwise rotation
    trunk2 = trunk1.rotate_xy(90, Point3D(0, 0, 0))

    assert len(trunk2.branches) == 1
    assert trunk2.total_length == pytest.approx(40.0)
    assert trunk2.branches[0].fixtures[0].segments[0].geometry.p2.x == pytest.approx(0.0)
    assert trunk2.branches[0].fixtures[0].segments[0].geometry.p2.y == pytest.approx(10.0)
    assert trunk2.branches[0].fixtures[0].segments[0].geometry.p2.z == pytest.approx(0.0)

    # +180 means a 189 degree COUNTER-clockwise rotation
    trunk3 = trunk1.rotate_xy(180, Point3D(0, 0, 0))

    assert len(trunk3.branches) == 1
