from honeybee_energy_ph.properties.materials.opaque import EnergyMaterialVegetationPhProperties
from honeybee_ph_utils.color import PhColor


def test_energy_material_vegetation_ph_properties() -> None:
    new_prop = EnergyMaterialVegetationPhProperties(None)
    new_prop.id_num = 0
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None

    # -- Test dict round trip
    d = new_prop.to_dict()
    new_prop = EnergyMaterialVegetationPhProperties.from_dict(d["ph"], None)
    assert new_prop.to_dict() == d
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None


def test_energy_material_vegetation_ph_properties_with_color() -> None:
    new_prop = EnergyMaterialVegetationPhProperties(None)
    new_prop.id_num = 0
    new_prop.ph_color = PhColor.from_argb(255, 255, 255, 255)
    assert new_prop.id_num == 0
    assert new_prop.ph_color is not None
    assert new_prop.ph_color.a == 255
    assert new_prop.ph_color.r == 255
    assert new_prop.ph_color.g == 255
    assert new_prop.ph_color.b == 255

    # -- Test to dict
    d = new_prop.to_dict()
    new_prop = EnergyMaterialVegetationPhProperties.from_dict(d["ph"], None)
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
    assert new_prop_2.ph_color.b == 255
