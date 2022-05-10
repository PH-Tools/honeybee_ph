from PHX.model import components


def test_default_component_opaque(reset_class_counters):
    c1 = components.PhxComponentOpaque()
    c2 = components.PhxComponentOpaque()

    assert c1.id_num == 1
    assert c2.id_num == 2
    assert c1 != c2

    assert not c1.polygon_ids
    assert not c2.polygon_ids


def test_add_with_empty_poly_ids(reset_class_counters):
    c1 = components.PhxComponentOpaque()
    c2 = components.PhxComponentOpaque()

    c3 = c1 + c2
    assert c3 != c2 != c1
    assert not c1.polygon_ids
    assert not c2.polygon_ids
    assert not c3.polygon_ids


def test_add_polygons(reset_class_counters, polygon_1x1x0, polygon_2x2x0):
    c1 = components.PhxComponentOpaque()
    c1.add_polygons(polygon_1x1x0)
    c2 = components.PhxComponentOpaque()
    c2.add_polygons(polygon_2x2x0)

    c3 = c1 + c2
    assert c3 != c2 != c1
    assert len(c3.polygons) == 2
    assert polygon_1x1x0 in c3.polygons
    assert polygon_2x2x0 in c3.polygons
