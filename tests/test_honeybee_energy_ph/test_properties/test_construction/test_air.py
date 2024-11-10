import pytest

from honeybee_energy_ph.properties.construction import air


def test_default_air_construction_properties_dict_round_trip():
    s1 = air.AirBoundaryConstructionPhProperties("host")
    d1 = s1.to_dict()
    s2 = air.AirBoundaryConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_custom_air_construction_properties_dict_round_trip():
    s1 = air.AirBoundaryConstructionPhProperties("host")
    s1.id_num = 11223
    d1 = s1.to_dict()
    s2 = air.AirBoundaryConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_default_air_construction_properties_duplicate():
    s1 = air.AirBoundaryConstructionPhProperties("host")
    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_custom_air_construction_properties__wrong_type_from_dict():
    wrong_dict = {
        "type": "not_allowed_type",
    }
    with pytest.raises(air.AirBoundaryConstructionPhProperties_FromDictError):
        s1 = air.AirBoundaryConstructionPhProperties.from_dict(wrong_dict, None)
