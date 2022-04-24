from PHX.model import building


def test_default_building(reset_class_counters):
    c1 = building.Component()
    c2 = building.Component()

    assert c1.id_num == 1
    assert c2.id_num == 2
    assert c1 != c2

    assert not c1.polygon_ids
    assert not c2.polygon_ids


def test_add_with_empty_poly_ids(reset_class_counters):
    c1 = building.Component()
    c2 = building.Component()

    c3 = c1 + c2
    assert c3 != c2 != c1
    assert not c1.polygon_ids
    assert not c2.polygon_ids
    assert not c3.polygon_ids


def test_add_with_poly_ids(reset_class_counters, polygon_1x1x0, polygon_2x2x0):
    c1 = building.Component()
    c1.add_polygon_id(polygon_1x1x0.id_num)
    c2 = building.Component()
    c2.add_polygon_id(polygon_2x2x0.id_num)

    c3 = c1 + c2
    assert c3 != c2 != c1
    assert len(c3.polygon_ids) == 2
    assert polygon_1x1x0.id_num in c3.polygon_ids
    assert polygon_2x2x0.id_num in c3.polygon_ids
