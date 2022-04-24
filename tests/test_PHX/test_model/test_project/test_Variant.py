from PHX.model import project


def test_blank_variant(reset_class_counters):
    assert project.Variant._count == 0
    var = project.Variant()

    assert str(var)
    assert not var.graphics3D
    assert not var.building
    assert not var.mech_systems.subsystems
    assert not var.mech_systems.cooling_subsystems
    assert var.id_num == 1
    assert project.Variant._count == 1
