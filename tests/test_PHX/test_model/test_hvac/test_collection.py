from PHX.model.hvac import _base, collection, heating, cooling, water, ventilation


def test_default_PhxMechanicalEquipmentCollection(reset_class_counters):
    c1 = collection.PhxMechanicalEquipmentCollection()
    c2 = collection.PhxMechanicalEquipmentCollection()

    assert c1.id_num == 1
    assert c2.id_num == 2


def test_add_subsystem(reset_class_counters):
    c1 = collection.PhxMechanicalEquipmentCollection()
    sys = _base.PhxMechanicalSubSystem()
    c1.add_new_mech_subsystem(sys.identifier, sys)

    assert c1.subsystem_in_collection(sys.identifier)
    assert not c1.subsystem_in_collection('not_a_key')


def test_get_subsystem_None_key(reset_class_counters):
    c1 = collection.PhxMechanicalEquipmentCollection()
    sys = c1.get_mech_subsystem_by_key("")
    assert sys is None


def test_get_subsystem(reset_class_counters):
    c1 = collection.PhxMechanicalEquipmentCollection()
    sys_1 = _base.PhxMechanicalSubSystem()
    c1.add_new_mech_subsystem(sys_1.identifier, sys_1)
    sys_2 = c1.get_mech_subsystem_by_key(sys_1.identifier)

    assert sys_1 == sys_2
