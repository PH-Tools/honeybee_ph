from honeybee_energy_ph.load import ph_equipment

def test_empty_collection_round_trip():
    c1 = ph_equipment.PhEquipmentCollection(_host=None)
    d1 = c1.to_dict()
    c2 = ph_equipment.PhEquipmentCollection.from_dict(d1, _host=None)

    assert c2.to_dict() == d1

def test_collection_with_single_equip_round_trip():
    c1 = ph_equipment.PhEquipmentCollection(_host=None)
    c1.add_equipment(ph_equipment.PhDishwasher())
    
    d1 = c1.to_dict()
    c2 = ph_equipment.PhEquipmentCollection.from_dict(d1, _host=None)

    assert c2.to_dict() == d1

def test_collection_with_multiple_equip_round_trip():
    c1 = ph_equipment.PhEquipmentCollection(_host=None)
    c1.add_equipment(ph_equipment.PhDishwasher())
    c1.add_equipment(ph_equipment.PhClothesDryer())
    c1.add_equipment(ph_equipment.PhClothesWasher())
    c1.add_equipment(ph_equipment.PhCooktop())
    c1.add_equipment(ph_equipment.PhFreezer())
    c1.add_equipment(ph_equipment.PhFridgeFreezer())
    c1.add_equipment(ph_equipment.PhRefrigerator())
    
    d1 = c1.to_dict()
    c2 = ph_equipment.PhEquipmentCollection.from_dict(d1, _host=None)

    assert c2.to_dict() == d1