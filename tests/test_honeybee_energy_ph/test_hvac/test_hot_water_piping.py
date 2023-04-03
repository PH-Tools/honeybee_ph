
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.line import LineSegment3D

from honeybee_energy_ph.hvac import hot_water


def test_PhPipeSegment_dict_round_trip():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    pipe1 = hot_water.PhPipeSegment(geom)
    d1 = pipe1.to_dict()
    pipe2 = hot_water.PhPipeSegment.from_dict(d1)

    assert pipe2.to_dict() == pipe1.to_dict()

    # -- Add user-data
    pipe2.user_data["test_key"] = "test_vale"
    assert "test_key" in pipe2.user_data
    assert "test_key" not in pipe1.user_data
    assert pipe2.to_dict() != pipe1.to_dict()

def test_PhPipeElement_dict_round_trip():
    p1, p2 = Point3D(), Point3D()
    geom = LineSegment3D(p1, p2)
    seg1 = hot_water.PhPipeSegment(geom)
    ele1 = hot_water.PhPipeElement()
    ele1.add_segment(seg1)
    d1 = ele1.to_dict()

    ele2 = hot_water.PhPipeElement.from_dict(d1)

    assert ele1.to_dict() == ele2.to_dict()

    # -- Add user-data
    ele2.user_data["test_key"] = "test_vale"
    assert "test_key" in ele2.user_data
    assert "test_key" not in ele1.user_data
    assert ele2.to_dict() != ele1.to_dict()