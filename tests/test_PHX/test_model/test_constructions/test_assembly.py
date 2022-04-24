from PHX.model import constructions


def test_default_assembly(reset_class_counters):
    a1 = constructions.Assembly()
    assert a1.id_num == 1
    a2 = constructions.Assembly()
    assert a2.id_num == 2

    assert a1 != a2
    assert not a1.layers
    assert not a2.layers
