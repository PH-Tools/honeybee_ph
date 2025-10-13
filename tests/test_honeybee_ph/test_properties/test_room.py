import pytest

from honeybee_ph.properties import room
from honeybee_ph_utils import enumerables


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


def test_specific_heat_capacity_enum_valid_values():
    """Test that PhSpecificHeatCapacity accepts valid values."""
    valid_values = ["1-LIGHTWEIGHT", "2-MIXED", "3-MASSIVE", "6-USER_DEFINED", 1, 2, 3, 6]
    
    for value in valid_values:
        shc = room.PhSpecificHeatCapacity(value)
        assert shc is not None


def test_specific_heat_capacity_enum_invalid_values():
    """Test that PhSpecificHeatCapacity rejects values 4 and 5."""
    invalid_values = [4, 5]
    
    for value in invalid_values:
        with pytest.raises(enumerables.ValueNotAllowedError):
            room.PhSpecificHeatCapacity(value)


def test_specific_heat_capacity_enum_number_property():
    """Test that PhSpecificHeatCapacity.number returns the correct numeric index."""
    shc1 = room.PhSpecificHeatCapacity("1-LIGHTWEIGHT")
    assert shc1.number == 1
    
    shc2 = room.PhSpecificHeatCapacity("2-MIXED")
    assert shc2.number == 2
    
    shc3 = room.PhSpecificHeatCapacity("3-MASSIVE")
    assert shc3.number == 3
    
    shc6 = room.PhSpecificHeatCapacity("6-USER_DEFINED")
    assert shc6.number == 6


def test_specific_heat_capacity_wh_m2k_default():
    """Test that specific_heat_capacity_wh_m2k defaults to None."""
    p1 = room.RoomPhProperties(_host=None)
    assert p1.specific_heat_capacity_wh_m2k is None


def test_specific_heat_capacity_wh_m2k_set_and_retrieve():
    """Test setting and retrieving specific_heat_capacity_wh_m2k."""
    p1 = room.RoomPhProperties(_host=None)
    p1.specific_heat_capacity_wh_m2k = 60
    assert p1.specific_heat_capacity_wh_m2k == 60


def test_specific_heat_capacity_wh_m2k_roundtrip():
    """Test serialization/deserialization of specific_heat_capacity_wh_m2k."""
    p1 = room.RoomPhProperties(_host=None)
    p1.specific_heat_capacity_wh_m2k = 75
    
    d = p1.to_dict()
    assert d["ph"]["specific_heat_capacity_wh_m2k"] == 75
    
    p2 = room.RoomPhProperties.from_dict(d["ph"], host=p1.host)
    assert p2.specific_heat_capacity_wh_m2k == 75


def test_specific_heat_capacity_wh_m2k_duplicate():
    """Test that duplicate preserves specific_heat_capacity_wh_m2k."""
    p1 = room.RoomPhProperties(_host=None)
    p1.specific_heat_capacity_wh_m2k = 85
    
    p2 = p1.duplicate()
    assert p2.specific_heat_capacity_wh_m2k == 85


def test_specific_heat_capacity_roundtrip():
    """Test serialization/deserialization of specific_heat_capacity enum."""
    p1 = room.RoomPhProperties(_host=None)
    p1.specific_heat_capacity = room.PhSpecificHeatCapacity("3-MASSIVE")
    
    d = p1.to_dict()
    assert d["ph"]["specific_heat_capacity"] == "3-MASSIVE"
    
    p2 = room.RoomPhProperties.from_dict(d["ph"], host=p1.host)
    assert p2.specific_heat_capacity.value == "3-MASSIVE"


def test_specific_heat_capacity_duplicate():
    """Test that duplicate preserves specific_heat_capacity."""
    p1 = room.RoomPhProperties(_host=None)
    p1.specific_heat_capacity = room.PhSpecificHeatCapacity("2-MIXED")
    
    p2 = p1.duplicate()
    assert p2.specific_heat_capacity.value == "2-MIXED"


def test_room_prop_deserialization_when_spec_heat_wh_m2k_is_missing():
    """Test deserialization when specific_heat_capacity_wh_m2k is missing (backwards compatibility)."""
    obj_1 = room.RoomPhProperties(_host=None)
    obj_1.specific_heat_capacity_wh_m2k = 90
    d1 = obj_1.to_dict()
    d1["ph"].pop("specific_heat_capacity_wh_m2k", None)

    obj_2 = room.RoomPhProperties.from_dict(d1["ph"], obj_1.host)

    assert isinstance(obj_2, room.RoomPhProperties)
    assert obj_2.specific_heat_capacity_wh_m2k is None


def test_both_specific_heat_attributes_together():
    """Test that both specific heat attributes can be set and work together."""
    p1 = room.RoomPhProperties(_host=None)
    p1.specific_heat_capacity = room.PhSpecificHeatCapacity("6-USER_DEFINED")
    p1.specific_heat_capacity_wh_m2k = 100
    
    d = p1.to_dict()
    assert d["ph"]["specific_heat_capacity"] == "6-USER_DEFINED"
    assert d["ph"]["specific_heat_capacity_wh_m2k"] == 100
    
    p2 = room.RoomPhProperties.from_dict(d["ph"], host=p1.host)
    assert p2.specific_heat_capacity.value == "6-USER_DEFINED"
    assert p2.specific_heat_capacity_wh_m2k == 100
    
    p3 = p2.duplicate()
    assert p3.specific_heat_capacity.value == "6-USER_DEFINED"
    assert p3.specific_heat_capacity_wh_m2k == 100


# TODO: Test with spaces, scale, ...
