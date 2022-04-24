from PHX.model import geometry


def test_blank_vertix(reset_class_counters):
    vert_1 = geometry.Vertix()
    assert vert_1
    assert vert_1.id_num == 1


def test_multiple_vertices_id_num(reset_class_counters):
    vert_1 = geometry.Vertix()
    vert_2 = geometry.Vertix()
    vert_3 = geometry.Vertix()
    assert vert_1.id_num == 1
    assert vert_2.id_num == 2
    assert vert_3.id_num == 3


def test_vertix_equality(reset_class_counters):
    vert_1 = geometry.Vertix(0, 0, 0)
    vert_2 = geometry.Vertix(0, 0, 0)
    assert vert_1 != vert_2
    assert vert_1.unique_key == vert_2.unique_key
    assert hash(vert_1) == hash(vert_2)


def test_vertix_not_equal(reset_class_counters):
    vert_1 = geometry.Vertix(1, 0, 0)
    vert_3 = geometry.Vertix(0, 0, 1)
    assert vert_1 != vert_3
    assert vert_1.unique_key != vert_3.unique_key
    assert hash(vert_1) != hash(vert_3)


def test_set_of_vertices(reset_class_counters):
    v1 = geometry.Vertix(0, 0, 0)
    v2 = geometry.Vertix(0, 0, 0)
    v3 = geometry.Vertix(0, 0, 1)
    v4 = geometry.Vertix(0, 1, 1)
    v5 = geometry.Vertix(1, 1, 1)

    s = set()
    s.add(v1)
    s.add(v2)
    s.add(v3)
    s.add(v4)
    s.add(v5)

    assert len(s) == 5
    assert v1 in s


def test_unique_key(reset_class_counters):
    v1 = geometry.Vertix(0, 0, 0)
    v2 = geometry.Vertix(0, 0, 0)  # <-- Same
    v3 = geometry.Vertix(0, 0, 1)
    v4 = geometry.Vertix(0, 1, 1)
    v5 = geometry.Vertix(1, 1, 1)

    d = {}
    d[v1.unique_key] = v1
    d[v2.unique_key] = v2
    d[v3.unique_key] = v3
    d[v4.unique_key] = v4
    d[v5.unique_key] = v5

    assert len(d) == 4  # <-- same should get excluded
