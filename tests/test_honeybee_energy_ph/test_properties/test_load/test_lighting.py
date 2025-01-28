import pytest

from honeybee_energy_ph.load.ph_equipment import PhDishwasher
from honeybee_energy_ph.properties.load.lighting import LightingPhProperties, LightingPhProperties_FromDictError

def test_Lighting():
    obj = LightingPhProperties(_host='test')
    assert obj.id_num == 0
    assert obj.host == 'test'

def test_Lighting_with_no_ph_equipment():
    obj = LightingPhProperties(_host='test')
    assert obj.ph_equipment == None

def test_Lighting_with_ph_equipment():
    obj = LightingPhProperties(_host='test')
    obj.ph_equipment = PhDishwasher.phius_default()
    d = obj.to_dict()
    obj2 = LightingPhProperties.from_dict(d['ph'], 'test')
    assert obj2.to_dict() == d

def test_Lighting_dict_round_trip():
    obj = LightingPhProperties(_host='test')
    d = obj.to_dict()
    obj2 = LightingPhProperties.from_dict(d['ph'], 'test')
    assert obj2.to_dict() == d

def test_from_dict_wrong_type():
    with pytest.raises(LightingPhProperties_FromDictError):
        LightingPhProperties.from_dict({"type": "wrong"}, 'test')

def test_Lighting_duplicate():
    obj = LightingPhProperties(_host='test')
    obj2 = obj.duplicate()
    assert obj.to_dict() == obj2.to_dict()
    assert obj is not obj2
