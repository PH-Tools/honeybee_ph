import pytest

from honeybee_energy_ph.properties.construction import opaque


def test_default_opaque_construction_properties_dict_round_trip():
    s1 = opaque.OpaqueConstructionPhProperties("host")
    d1 = s1.to_dict()
    s2 = opaque.OpaqueConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_custom_opaque_construction_properties_dict_round_trip():
    s1 = opaque.OpaqueConstructionPhProperties("host")
    s1.id_num = 11223
    d1 = s1.to_dict()
    s2 = opaque.OpaqueConstructionPhProperties.from_dict(d1["ph"], None)

    assert d1 == s2.to_dict()


def test_default_opaque_construction_properties_duplicate():
    s1 = opaque.OpaqueConstructionPhProperties("host")
    s2 = s1.duplicate()

    assert s1.to_dict() == s2.to_dict()


def test_custom_opaque_construction_properties__wrong_type_from_dict():
    wrong_dict = {
        "type": "not_allowed_type",
    }
    with pytest.raises(opaque.OpaqueConstructionPhProperties_FromDictError):
        s1 = opaque.OpaqueConstructionPhProperties.from_dict(wrong_dict, None)
