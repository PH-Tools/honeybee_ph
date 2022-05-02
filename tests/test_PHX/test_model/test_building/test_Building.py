from distutils.command.build import build
from PHX.model import building


def test_default_Building(reset_class_counters):
    b1 = building.PhxBuilding()
    b2 = building.PhxBuilding()

    assert id(b1) != id(b2)
    assert not b1
    assert not b2
    assert not b1.components
    assert not b2.components
    assert not b1.zones
    assert not b2.zones


def test_add_single_component(reset_class_counters):
    b = building.PhxBuilding()
    c1 = building.PhxComponent()
    b.add_components(c1)

    assert b
    assert b.components
    assert len(b.components) == 1
    assert c1 in b.components


def test_add_multiple_components(reset_class_counters):
    b = building.PhxBuilding()
    c1 = building.PhxComponent()
    c2 = building.PhxComponent()
    b.add_components([c1, c2])

    assert b
    assert b.components
    assert len(b.components) == 2
    assert c1 in b.components
    assert c2 in b.components


def test_add_single_zone(reset_class_counters):
    b = building.PhxBuilding()
    z1 = building.PhxZone()
    b.add_zones(z1)

    assert b
    assert b.zones
    assert len(b.zones) == 1
    assert z1 in b.zones


def test_add_multiple_zones(reset_class_counters):
    b = building.PhxBuilding()
    z1 = building.PhxZone()
    z2 = building.PhxZone()
    b.add_zones([z1, z2])

    assert b
    assert b.zones
    assert len(b.zones) == 2
    assert z1 in b.zones
    assert z2 in b.zones


def test_group_compos_by_assembly_with_single_compo(reset_class_counters):
    b = building.PhxBuilding()
    c1 = building.PhxComponent()
    b.add_components(c1)
    b.merge_components_by_assembly()

    assert b
    assert b.components
    assert len(b.components) == 1
    assert c1 in b.components
