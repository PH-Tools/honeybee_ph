from PHX.model import elec_equip


def test_default_ElecEquipment(reset_class_counters):
    obj_1 = elec_equip.PhxElectricalEquipment()
    obj_2 = elec_equip.PhxElectricalEquipment()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxDishwasher(reset_class_counters):
    obj_1 = elec_equip.PhxDishwasher()
    obj_2 = elec_equip.PhxDishwasher()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxClothesWasher(reset_class_counters):
    obj_1 = elec_equip.PhxClothesWasher()
    obj_2 = elec_equip.PhxClothesWasher()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxClothesDryer(reset_class_counters):
    obj_1 = elec_equip.PhxClothesDryer()
    obj_2 = elec_equip.PhxClothesDryer()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxRefrigerator(reset_class_counters):
    obj_1 = elec_equip.PhxRefrigerator()
    obj_2 = elec_equip.PhxRefrigerator()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxFreezer(reset_class_counters):
    obj_1 = elec_equip.PhxFreezer()
    obj_2 = elec_equip.PhxFreezer()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxFridgeFreezer(reset_class_counters):
    obj_1 = elec_equip.PhxFridgeFreezer()
    obj_2 = elec_equip.PhxFridgeFreezer()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCooktop(reset_class_counters):
    obj_1 = elec_equip.PhxCooktop()
    obj_2 = elec_equip.PhxCooktop()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxMEL(reset_class_counters):
    obj_1 = elec_equip.PhxMEL()
    obj_2 = elec_equip.PhxMEL()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxLightingInterior(reset_class_counters):
    obj_1 = elec_equip.PhxLightingInterior()
    obj_2 = elec_equip.PhxLightingInterior()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxLightingExterior(reset_class_counters):
    obj_1 = elec_equip.PhxLightingExterior()
    obj_2 = elec_equip.PhxLightingExterior()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxLightingGarage(reset_class_counters):
    obj_1 = elec_equip.PhxLightingGarage()
    obj_2 = elec_equip.PhxLightingGarage()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCustomElec(reset_class_counters):
    obj_1 = elec_equip.PhxCustomElec()
    obj_2 = elec_equip.PhxCustomElec()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCustomLighting(reset_class_counters):
    obj_1 = elec_equip.PhxCustomLighting()
    obj_2 = elec_equip.PhxCustomLighting()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCustomMEL(reset_class_counters):
    obj_1 = elec_equip.PhxCustomMEL()
    obj_2 = elec_equip.PhxCustomMEL()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2
