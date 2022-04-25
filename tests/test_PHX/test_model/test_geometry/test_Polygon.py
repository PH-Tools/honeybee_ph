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
