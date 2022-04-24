from PHX.model import certification


def test_default_PassivehouseData(reset_class_counters):
    obj_1 = certification.PassivehouseData()
    assert not obj_1.ph_buildings


def test_add_single_PH_Building(reset_class_counters):
    obj = certification.PassivehouseData()
    phb = certification.PH_Building()
    obj.add_ph_building(phb)
    assert phb in obj.ph_buildings
