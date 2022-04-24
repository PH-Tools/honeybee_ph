from PHX.model import elec_equip


def test_empty_collection(reset_class_counters):
    collection_1 = elec_equip.PhxElectricEquipmentCollection()
    collection_2 = elec_equip.PhxElectricEquipmentCollection()

    assert not collection_1
    assert not collection_1.equipment

    assert not collection_2
    assert not collection_2.equipment


def test_add_single_equip_to_collection(reset_class_counters):
    collection_1 = elec_equip.PhxElectricEquipmentCollection()
    ee_1 = elec_equip.PhxElectricalEquipment()
    collection_1.add_new_equipment(str(ee_1.identifier), ee_1)

    assert len(collection_1.equipment) == 1
    assert collection_1.equipment_in_collection(str(ee_1.identifier))
    assert collection_1.get_equipment_by_key(str(ee_1.identifier)) == ee_1
    assert collection_1.get_equipment_by_key('not in collection') == None
