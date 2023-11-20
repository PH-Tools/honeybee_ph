from honeybee_energy_ph.load import ph_equipment

# -- Basics

def test_PhDishwasher_round_trip():
    e1 = ph_equipment.PhDishwasher()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhClothesWasher_round_trip():
    e1 = ph_equipment.PhClothesWasher()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhClothesDryer_round_trip():
    e1 = ph_equipment.PhClothesDryer()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhRefrigerator_round_trip():
    e1 = ph_equipment.PhRefrigerator()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhFreezer_round_trip():
    e1 = ph_equipment.PhFreezer()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhFridgeFreezer_round_trip():
    e1 = ph_equipment.PhFridgeFreezer()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhCooktop_round_trip():
    e1 = ph_equipment.PhCooktop()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1


# -- Phius, MEL

def test_PhPhiusMEL_round_trip():
    e1 = ph_equipment.PhPhiusMEL()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhPhiusLightingInterior_round_trip():
    e1 = ph_equipment.PhPhiusLightingInterior()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhPhiusLightingExterior_round_trip():
    e1 = ph_equipment.PhPhiusLightingExterior()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1
    assert e2.in_conditioned_space == False

def test_PhPhiusLightingGarage_round_trip():
    e1 = ph_equipment.PhPhiusLightingGarage()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1
    assert e2.in_conditioned_space == False

def test_PhCustomAnnualElectric_round_trip():
    e1 = ph_equipment.PhCustomAnnualElectric()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhCustomAnnualLighting_round_trip():
    e1 = ph_equipment.PhCustomAnnualLighting()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhCustomAnnualMEL_round_trip():
    e1 = ph_equipment.PhCustomAnnualMEL()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

 #--- Elevators

def test_PhElevatorHydraulic_round_trip():
    e1 = ph_equipment.PhElevatorHydraulic()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhElevatorGearedTraction_round_trip():
    e1 = ph_equipment.PhElevatorGearedTraction()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1

def test_PhElevatorGearlessTraction_round_trip():
    e1 = ph_equipment.PhElevatorGearlessTraction()
    d1 = e1.to_dict()
    e2 = ph_equipment.PhEquipmentBuilder.from_dict(d1)

    assert e2.to_dict() == d1
