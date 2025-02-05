import pytest

from honeybee_energy_ph.load.ph_equipment import PhDishwasher
from honeybee_energy_ph.properties.load.process import ProcessPhProperties, ProcessPhProperties_FromDictError


def test_Process():
    obj = ProcessPhProperties(_host="test")
    assert obj.host == "test"


def test_Process_with_no_ph_equipment():
    obj = ProcessPhProperties(_host="test")
    assert obj.ph_equipment == None


def test_Process_with_ph_equipment():
    obj = ProcessPhProperties(_host="test")
    obj.ph_equipment = PhDishwasher.phius_default()
    d = obj.to_dict()
    obj2 = ProcessPhProperties.from_dict(d["ph"], "test")
    assert obj2.to_dict() == d


def test_Process_dict_round_trip():
    obj = ProcessPhProperties(_host="test")
    d = obj.to_dict()
    obj2 = ProcessPhProperties.from_dict(d["ph"], "test")
    assert obj2.to_dict() == d


def test_from_dict_wrong_type():
    with pytest.raises(ProcessPhProperties_FromDictError):
        ProcessPhProperties.from_dict({"type": "wrong"}, "test")


def test_Process_duplicate():
    obj = ProcessPhProperties(_host="test")
    obj2 = obj.duplicate()
    assert obj.to_dict() == obj2.to_dict()
    assert obj is not obj2
