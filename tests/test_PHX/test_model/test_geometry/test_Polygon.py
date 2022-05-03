from typing import Dict
import pytest
from PHX.model import geometry


def test_blank_Polygon(reset_class_counters):
    p1 = geometry.PhxPolygon()
    assert p1.id_num == 1
    assert p1.normal_vector
    assert not p1.vertices
    assert not p1.child_polygon_ids
    assert not p1.vertices_id_numbers


def test_multiple_Polygon_id_numbers(reset_class_counters):
    p1 = geometry.PhxPolygon()
    p2 = geometry.PhxPolygon()
    p3 = geometry.PhxPolygon()

    assert p1.id_num == 1
    assert p2.id_num == 2
    assert p3.id_num == 3


def test_add_vertices_to_Polygon(reset_class_counters):
    p1 = geometry.PhxPolygon()

    v1 = geometry.PhxVertix(0, 0, 0)
    v2 = geometry.PhxVertix(0, 1, 0)
    v3 = geometry.PhxVertix(1, 1, 0)
    v4 = geometry.PhxVertix(1, 0, 0)

    p1.add_vertix(v1)
    p1.add_vertix(v2)
    p1.add_vertix(v3)
    p1.add_vertix(v4)

    assert len(p1.vertices) == 4
    assert v1 in p1.vertices
    assert v2 in p1.vertices
    assert v3 in p1.vertices
    assert v4 in p1.vertices

    assert len(p1.vertices_id_numbers) == 4
    assert v1.id_num in p1.vertices_id_numbers
    assert v2.id_num in p1.vertices_id_numbers
    assert v3.id_num in p1.vertices_id_numbers
    assert v4.id_num in p1.vertices_id_numbers


def test_add_child_poly_id(reset_class_counters, polygon_1x1x0, polygon_2x2x0):
    p1 = geometry.PhxPolygon()
    p1.add_vertix(geometry.PhxVertix(0, 0, 0))
    p1.add_vertix(geometry.PhxVertix(0, 1, 0))
    p1.add_vertix(geometry.PhxVertix(1, 1, 0))
    p1.add_vertix(geometry.PhxVertix(1, 0, 0))

    p2 = geometry.PhxPolygon()
    p2.add_vertix(geometry.PhxVertix(0, 0, 0))
    p2.add_vertix(geometry.PhxVertix(0, 2, 0))
    p2.add_vertix(geometry.PhxVertix(2, 2, 0))
    p2.add_vertix(geometry.PhxVertix(2, 0, 0))

    p1.add_child_poly_id(p2.id_num)
    assert len(p1.child_polygon_ids) == 1
    assert p2.id_num in p1.child_polygon_ids
    for v in p2.vertices:
        assert v not in p1.vertices


# -- Test Cube


def test_cube_polygons_cardinal_orientation_on_axis(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    assert phx_polygons['vertical']['north'].cardinal_orientation_angle == 0
    assert phx_polygons['vertical']['east'].cardinal_orientation_angle == 90
    assert phx_polygons['vertical']['south'].cardinal_orientation_angle == 180
    assert phx_polygons['vertical']['west'].cardinal_orientation_angle == 270

    assert phx_polygons['horizontal']['downward'].cardinal_orientation_angle == 0
    assert phx_polygons['horizontal']['upward'].cardinal_orientation_angle == 0


def test_cube_polygons_vertical_orientation_on_axis(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    assert phx_polygons['vertical']['north'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['north'].is_vertical == True
    assert phx_polygons['vertical']['north'].is_horizontal == False

    assert phx_polygons['vertical']['east'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['east'].is_vertical == True
    assert phx_polygons['vertical']['east'].is_horizontal == False

    assert phx_polygons['vertical']['south'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['south'].is_vertical == True
    assert phx_polygons['vertical']['south'].is_horizontal == False

    assert phx_polygons['vertical']['west'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['west'].is_vertical == True
    assert phx_polygons['vertical']['west'].is_horizontal == False

    assert phx_polygons['horizontal']['downward'].angle_from_horizontal == 180
    assert phx_polygons['horizontal']['downward'].is_vertical == False
    assert phx_polygons['horizontal']['downward'].is_horizontal == True

    assert phx_polygons['horizontal']['upward'].angle_from_horizontal == 0
    assert phx_polygons['horizontal']['upward'].is_vertical == False
    assert phx_polygons['horizontal']['upward'].is_horizontal == True


def test_cube_polygons_cardinal_orientation_rotated(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    vert_srfcs = phx_polygons['vertical']
    assert vert_srfcs['northeast'].cardinal_orientation_angle == pytest.approx(0 + 60)
    assert vert_srfcs['southeast'].cardinal_orientation_angle == pytest.approx(90 + 60)
    assert vert_srfcs['southwest'].cardinal_orientation_angle == pytest.approx(180 + 60)
    assert vert_srfcs['northwest'].cardinal_orientation_angle == pytest.approx(270 + 60)

    hor_srfcs = phx_polygons['horizontal']
    assert hor_srfcs['downward_rotated'].cardinal_orientation_angle == 0
    assert hor_srfcs['upward_rotated'].cardinal_orientation_angle == 0


def test_cube_polygons_vertical_orientation_rotated(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    assert phx_polygons['vertical']['northeast'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['northeast'].is_vertical == True
    assert phx_polygons['vertical']['northeast'].is_horizontal == False

    assert phx_polygons['vertical']['southeast'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['southeast'].is_vertical == True
    assert phx_polygons['vertical']['southeast'].is_horizontal == False

    assert phx_polygons['vertical']['southwest'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['southwest'].is_vertical == True
    assert phx_polygons['vertical']['southwest'].is_horizontal == False

    assert phx_polygons['vertical']['northwest'].angle_from_horizontal == 90
    assert phx_polygons['vertical']['northwest'].is_vertical == True
    assert phx_polygons['vertical']['northwest'].is_horizontal == False

    assert phx_polygons['horizontal']['downward_rotated'].angle_from_horizontal == 180
    assert phx_polygons['horizontal']['downward_rotated'].is_vertical == False
    assert phx_polygons['horizontal']['downward_rotated'].is_horizontal == True

    assert phx_polygons['horizontal']['upward_rotated'].angle_from_horizontal == 0
    assert phx_polygons['horizontal']['upward_rotated'].is_vertical == False
    assert phx_polygons['horizontal']['upward_rotated'].is_horizontal == True


# -- Test Square Pyramid


def test_sq_pyramid_polygons_vertical_orientation_on_axis(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    pyramid_srfcs = phx_polygons['sq_pyramid']
    assert pyramid_srfcs['north'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['north'].is_vertical == False
    assert pyramid_srfcs['north'].is_horizontal == False

    assert pyramid_srfcs['east'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['east'].is_vertical == False
    assert pyramid_srfcs['east'].is_horizontal == False

    assert pyramid_srfcs['south'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['south'].is_vertical == False
    assert pyramid_srfcs['south'].is_horizontal == False

    assert pyramid_srfcs['west'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['west'].is_vertical == False
    assert pyramid_srfcs['west'].is_horizontal == False

    assert pyramid_srfcs['downward'].angle_from_horizontal == 180
    assert pyramid_srfcs['downward'].is_vertical == False
    assert pyramid_srfcs['downward'].is_horizontal == True

    assert pyramid_srfcs['upward'].angle_from_horizontal == 0
    assert pyramid_srfcs['upward'].is_vertical == False
    assert pyramid_srfcs['upward'].is_horizontal == True


def test_sq_pyramid_polygons_cardinal_orientation_on_axis(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    pyramid_srfcs = phx_polygons['sq_pyramid']
    assert pyramid_srfcs['north'].cardinal_orientation_angle == 0
    assert pyramid_srfcs['east'].cardinal_orientation_angle == 90
    assert pyramid_srfcs['south'].cardinal_orientation_angle == 180
    assert pyramid_srfcs['west'].cardinal_orientation_angle == 270

    assert pyramid_srfcs['downward'].cardinal_orientation_angle == 0
    assert pyramid_srfcs['upward'].cardinal_orientation_angle == 0


def test_sq_pyramid_polygons_vertical_orientation_rotated(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    pyramid_srfcs = phx_polygons['sq_pyramid']
    assert pyramid_srfcs['northeast'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['northeast'].is_vertical == False
    assert pyramid_srfcs['northeast'].is_horizontal == False

    assert pyramid_srfcs['southeast'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['southeast'].is_vertical == False
    assert pyramid_srfcs['southeast'].is_horizontal == False

    assert pyramid_srfcs['southwest'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['southwest'].is_vertical == False
    assert pyramid_srfcs['southwest'].is_horizontal == False

    assert pyramid_srfcs['northwest'].angle_from_horizontal == pytest.approx(77.74803)
    assert pyramid_srfcs['northwest'].is_vertical == False
    assert pyramid_srfcs['northwest'].is_horizontal == False

    assert pyramid_srfcs['downward_rotated'].angle_from_horizontal == 180
    assert pyramid_srfcs['downward_rotated'].is_vertical == False
    assert pyramid_srfcs['downward_rotated'].is_horizontal == True

    assert pyramid_srfcs['upward_rotated'].angle_from_horizontal == 0
    assert pyramid_srfcs['upward_rotated'].is_vertical == False
    assert pyramid_srfcs['upward_rotated'].is_horizontal == True


def test_sq_pyramid_polygons_cardinal_orientation_rotated(reset_class_counters, phx_polygons: Dict[str, Dict[str, geometry.PhxPolygon]]):
    polys = phx_polygons['sq_pyramid']
    assert polys['northeast'].cardinal_orientation_angle == pytest.approx(0 + 60)
    assert polys['southeast'].cardinal_orientation_angle == pytest.approx(90 + 60)
    assert polys['southwest'].cardinal_orientation_angle == pytest.approx(180 + 60)
    assert polys['northwest'].cardinal_orientation_angle == pytest.approx(270 + 60)

    assert polys['downward_rotated'].cardinal_orientation_angle == 0
    assert polys['upward_rotated'].cardinal_orientation_angle == 0
