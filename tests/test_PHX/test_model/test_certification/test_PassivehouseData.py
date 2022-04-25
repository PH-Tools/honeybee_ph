from PHX.model import certification


def test_default_PassivehouseData(reset_class_counters):
    obj_1 = certification.PhxPHCertification()
    assert not obj_1.building_data


def test_add_single_PH_Building(reset_class_counters):
    obj = certification.PhxPHCertification()
    phb = certification.PhxPHBuilding()
    obj.add_ph_building(phb)
    assert phb in obj.building_data
