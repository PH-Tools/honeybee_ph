from PHX.model import elec_equip


def test_default_ElecEquipment(reset_class_counters):
    obj_1 = elec_equip.PhxElectricalDevice()
    obj_2 = elec_equip.PhxElectricalDevice()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxDishwasher(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceDishwasher()
    obj_2 = elec_equip.PhxDeviceDishwasher()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxClothesWasher(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceClothesWasher()
    obj_2 = elec_equip.PhxDeviceClothesWasher()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxClothesDryer(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceClothesDryer()
    obj_2 = elec_equip.PhxDeviceClothesDryer()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxRefrigerator(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceRefrigerator()
    obj_2 = elec_equip.PhxDeviceRefrigerator()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxFreezer(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceFreezer()
    obj_2 = elec_equip.PhxDeviceFreezer()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxFridgeFreezer(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceFridgeFreezer()
    obj_2 = elec_equip.PhxDeviceFridgeFreezer()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCooktop(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceCooktop()
    obj_2 = elec_equip.PhxDeviceCooktop()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxMEL(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceMEL()
    obj_2 = elec_equip.PhxDeviceMEL()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxLightingInterior(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceLightingInterior()
    obj_2 = elec_equip.PhxDeviceLightingInterior()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxLightingExterior(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceLightingExterior()
    obj_2 = elec_equip.PhxDeviceLightingExterior()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxLightingGarage(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceLightingGarage()
    obj_2 = elec_equip.PhxDeviceLightingGarage()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCustomElec(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceCustomElec()
    obj_2 = elec_equip.PhxDeviceCustomElec()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCustomLighting(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceCustomLighting()
    obj_2 = elec_equip.PhxDeviceCustomLighting()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2


def test_PhxCustomMEL(reset_class_counters):
    obj_1 = elec_equip.PhxDeviceCustomMEL()
    obj_2 = elec_equip.PhxDeviceCustomMEL()

    assert obj_1 != obj_2
    assert obj_1.id_num == 1
    assert obj_2.id_num == 2
