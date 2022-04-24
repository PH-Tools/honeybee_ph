from PHX.model.loads import ventilation


def test_default_room_ventilation(reset_class_counters):
    rm_vent_1 = ventilation.PhxRoomVentilation()
    rm_vent_2 = ventilation.PhxRoomVentilation()

    assert rm_vent_1 != rm_vent_2
    assert rm_vent_1.id_num == 1
    assert rm_vent_2.id_num == 2
