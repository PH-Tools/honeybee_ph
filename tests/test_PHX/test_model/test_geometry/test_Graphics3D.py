from re import L
from PHX.model import geometry


def test_empty_Graphics3D(reset_class_counters):
    g3d = geometry.Graphics3D()
    assert not g3d
    assert not g3d.polygons
    assert not g3d.vertices


def test_add_single_polygon(reset_class_counters, polygon_1x1x0):
    g3d = geometry.Graphics3D()
    g3d.add_polygons(polygon_1x1x0)

    assert g3d
    assert len(g3d.polygons) == 1
    assert polygon_1x1x0 in g3d.polygons
    for v in polygon_1x1x0.vertices:
        assert v in g3d.vertices


def test_add_two_polygon(reset_class_counters, polygon_1x1x0, polygon_2x2x0):
    g3d = geometry.Graphics3D()
    g3d.add_polygons([polygon_1x1x0, polygon_2x2x0])

    assert g3d
    assert len(g3d.polygons) == 2
    assert polygon_1x1x0 in g3d.polygons
    assert polygon_2x2x0 in g3d.polygons
    for v in polygon_1x1x0.vertices:
        assert v in g3d.vertices
    for v in polygon_2x2x0.vertices:
        assert v in g3d.vertices
