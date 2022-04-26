from PHX.model import certification, ground


def test_default_PH_Building(reset_class_counters):
    obj_1 = certification.PhxPHBuilding()
    assert obj_1.id_num == 1
    obj_2 = certification.PhxPHBuilding()
    assert obj_2.id_num == 2

    assert obj_1 != obj_2
    assert not obj_1.foundations
    assert not obj_2.foundations


def test_add_single_foundation(reset_class_counters):
    obj_1 = certification.PhxPHBuilding()
    f_1 = ground.PhxFoundation()
    obj_1.add_foundation(f_1)

    assert len(obj_1.foundations) == 1
    assert f_1 in obj_1.foundations
