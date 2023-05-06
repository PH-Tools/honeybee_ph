from honeybee_ph.properties import room


def test_default_room_prop():
    p1 = room.RoomPhProperties(_host=None)
    assert p1


def test_empty_prop_dict_roundtrip():
    p1 = room.RoomPhProperties(_host=None)
    d = p1.to_dict()

    p2 = room.RoomPhProperties.from_dict(d["ph"], host=p1.host)
    assert p2.to_dict() == d


def test_duplicate_empty_prop_dict():
    p1 = room.RoomPhProperties(_host=None)
    p2 = p1.duplicate()
    assert p2.to_dict() == p1.to_dict()


def test_room_prop_deserialization_when_spec_heat_is_missing():
    """when deserializing from dict, if spec_heat is missing, (old hbjson files))"""
    obj_1 = room.RoomPhProperties(_host=None)
    d1 = obj_1.to_dict()
    d1["ph"].pop("specific_heat_capacity", None)

    obj_2 = room.RoomPhProperties.from_dict(d1["ph"], obj_1.host)

    assert isinstance(obj_2, room.RoomPhProperties)


# TODO: Test with spaces, scale, ...
