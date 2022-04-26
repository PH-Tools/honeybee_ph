from PHX.model import constructions


def test_default_assembly(reset_class_counters):
    a1 = constructions.PhxConstructionOpaque()
    assert a1.id_num == 1
    a2 = constructions.PhxConstructionOpaque()
    assert a2.id_num == 2

    assert a1 != a2
    assert a1.identifier != a2.identifier
    assert not a1.layers
    assert not a2.layers


def test_set_assembly_identifier(reset_class_counters):
    a1 = constructions.PhxConstructionOpaque()
    a2 = constructions.PhxConstructionOpaque()

    a1.identifier = 'a_test'
    assert a1.identifier == 'a_test'
    assert a1.identifier != a2.identifier

    a1.identifier = None
    assert a1.identifier == 'a_test'
    assert a1.identifier != a2.identifier
