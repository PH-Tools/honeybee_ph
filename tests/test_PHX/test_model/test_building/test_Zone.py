from PHX.model import building


def test_default_building(reset_class_counters):
    z1 = building.PhxZone()
    z2 = building.PhxZone()

    assert z1.id_num == 1
    assert z2.id_num == 2
    assert z1 != z2

    assert not z1.wufi_rooms
    assert not z2.wufi_rooms
    assert not z1.elec_equipment_collection
    assert not z2.elec_equipment_collection
