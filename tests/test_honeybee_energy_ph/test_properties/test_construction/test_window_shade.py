import pytest
from honeybee_energy_ph.properties.construction import windowshade

def test_window_construction_shade_properties_dict_round_trip():
    s1 = windowshade.WindowConstructionShadePhProperties("test_shade_prop")
    d1 = s1.to_dict()
    s2 = windowshade.WindowConstructionShadePhProperties.from_dict(d1["ph"], None)
    
    assert d1 == s2.to_dict()

def test_window_construction_shade_properties_duplicate():
    s1 = windowshade.WindowConstructionShadePhProperties("test_shade_prop")
    s2 = s1.duplicate()
    
    assert s1.to_dict() == s2.to_dict()

def test_window_construction_shade_properties_wrong_type_from_dict():
    wrong_dict = {
        "type": "not_allowed_type",
    }
    with pytest.raises(windowshade.WindowConstructionShadePhProperties_FromDictError):
        s1 = windowshade.WindowConstructionShadePhProperties.from_dict(wrong_dict, None)