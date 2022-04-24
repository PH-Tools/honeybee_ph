from distutils.command.build import build
from PHX.model import building


def test_default_Building(reset_class_counters):
    b1 = building.Building()
    b2 = building.Building()

    assert id(b1) != id(b2)
    assert not b1
    assert not b2
    assert not b1.components
    assert not b2.components
    assert not b1.zones
    assert not b2.zones


def test_add_single_component(reset_class_counters):
    b = building.Building()
    c1 = building.Component()
    b.add_components(c1)

    assert b
    assert b.components
    assert len(b.components) == 1
    assert c1 in b.components


def test_add_multiple_components(reset_class_counters):
    b = building.Building()
    c1 = building.Component()
    c2 = building.Component()
    b.add_components([c1, c2])

    assert b
    assert b.components
    assert len(b.components) == 2
    assert c1 in b.components
    assert c2 in b.components


def test_add_single_zone(reset_class_counters):
    b = building.Building()
    z1 = building.Zone()
    b.add_zones(z1)

    assert b
    assert b.zones
    assert len(b.zones) == 1
    assert z1 in b.zones


def test_add_multiple_zones(reset_class_counters):
    b = building.Building()
    z1 = building.Zone()
    z2 = building.Zone()
    b.add_zones([z1, z2])

    assert b
    assert b.zones
    assert len(b.zones) == 2
    assert z1 in b.zones
    assert z2 in b.zones


def test_group_compos_by_assembly_with_single_compo(reset_class_counters):
    b = building.Building()
    c1 = building.Component()
    b.add_components(c1)
    b.merge_components_by_assembly()

    assert b
    assert b.components
    assert len(b.components) == 1
    assert c1 in b.components


def test_merge_compos_by_assembly_with_multiple_compos_same_assembly(reset_class_counters):
    b = building.Building()
    c1 = building.Component(assembly_type_id_num=1, polygon_ids={1, 2})
    c2 = building.Component(assembly_type_id_num=1, polygon_ids={3, 4, 5})
    c3 = building.Component(assembly_type_id_num=1, polygon_ids={6})
    b.add_components([c1, c2, c3])
    b.merge_components_by_assembly()

    assert b
    assert b.components
    assert len(b.components) == 1

    assert c1 not in b.components
    assert c2 not in b.components
    assert c3 not in b.components

    for i in c1.polygon_ids:
        assert i in b.polygon_ids
    for i in c2.polygon_ids:
        assert i in b.polygon_ids
    for i in c3.polygon_ids:
        assert i in b.polygon_ids


def test_merge_compos_by_assembly_with_multiple_compos_different_assembly(reset_class_counters):
    b = building.Building()
    c1 = building.Component(assembly_type_id_num=1, polygon_ids={1, 2})
    c2 = building.Component(assembly_type_id_num=1, polygon_ids={3, 4, 5})
    c3 = building.Component(assembly_type_id_num=2, polygon_ids={6})
    c4 = building.Component(assembly_type_id_num=2, polygon_ids={7, 8, 9})
    c5 = building.Component(assembly_type_id_num=3, polygon_ids={10, 11})
    b.add_components([c1, c2, c3, c4, c5])
    b.merge_components_by_assembly()

    assert b
    assert b.components
    assert len(b.components) == 3

    assert c1 not in b.components
    assert c2 not in b.components
    assert c3 not in b.components
    assert c4 not in b.components
    assert c5 in b.components

    for i in c1.polygon_ids:
        assert i in b.polygon_ids
    for i in c2.polygon_ids:
        assert i in b.polygon_ids
    for i in c3.polygon_ids:
        assert i in b.polygon_ids
    for i in c4.polygon_ids:
        assert i in b.polygon_ids
    for i in c5.polygon_ids:
        assert i in b.polygon_ids
