import pytest

from honeybee_energy_ph.properties.materials.opaque import EnergyMaterialPhProperties
from honeybee_ph_utils.color import PhColor


def test_energy_material_ph_properties_deprecated_properties() -> None:
    new_prop = EnergyMaterialPhProperties(None)
    with pytest.raises(DeprecationWarning):
        new_prop.percentage_of_assembly = 0.5

    with pytest.raises(DeprecationWarning):
        assert new_prop.percentage_of_assembly == 0.5

    with pytest.raises(DeprecationWarning):
        new_prop.base_materials = []

    with pytest.raises(DeprecationWarning):
        assert new_prop.base_materials == []

    with pytest.raises(DeprecationWarning):
        assert new_prop.add_base_material(None) == None

    with pytest.raises(DeprecationWarning):
        new_prop.clear_base_materials()


def test_energy_material_ph_properties_dict_round_trip() -> None:
    new_prop = EnergyMaterialPhProperties(None)
    new_prop.id_num = 0
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None

    # -- Dict round trip
    d = new_prop.to_dict()
    new_prop = EnergyMaterialPhProperties.from_dict(d["ph"], None)
    assert new_prop.to_dict() == d
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None


def test_energy_material_ph_properties_duplicate():
    new_prop = EnergyMaterialPhProperties(None)
    new_prop.id_num = 0
    new_prop_2 = new_prop.duplicate()
    assert new_prop_2.id_num == 0
    assert new_prop_2.ph_color is None


def test_energy_material_ph_properties_with_color() -> None:
    new_prop = EnergyMaterialPhProperties(None)
    new_prop.id_num = 0
    new_prop.ph_color = PhColor.from_argb(255, 255, 255, 255)
    assert new_prop.id_num == 0
    assert new_prop.ph_color.a == 255
    assert new_prop.ph_color.r == 255
    assert new_prop.ph_color.g == 255
    assert new_prop.ph_color.b == 255

    # -- Test dict round trip
    d = new_prop.to_dict()
    new_prop = EnergyMaterialPhProperties.from_dict(d["ph"], None)
    assert new_prop.to_dict() == d
    assert new_prop.id_num == 0
    assert new_prop.ph_color is not None
    assert new_prop.ph_color.a == 255
    assert new_prop.ph_color.r == 255
    assert new_prop.ph_color.g == 255
    assert new_prop.ph_color.b == 255

    # -- Test copy
    new_prop_2 = new_prop.duplicate()
    assert new_prop_2.id_num == 0
    assert new_prop_2.ph_color is not None
    assert new_prop_2.ph_color.a == 255
    assert new_prop_2.ph_color.r == 255
    assert new_prop_2.ph_color.g == 255
