from honeybee_energy_ph.properties.materials.opaque import EnergyMaterialPhProperties, EnergyMaterialNoMassPhProperties, EnergyMaterialVegetationPhProperties
from honeybee_ph_utils.color import PhColor

# -----------------------------------------------------------------------------
# -- Test EnergyMaterialPhProperties
def test_energy_material_ph_properties():
    new_prop = EnergyMaterialPhProperties(None)
    new_prop.id_num = 0
    new_prop.percentage_of_assembly = 0.5
    assert new_prop.id_num == 0
    assert new_prop.percentage_of_assembly == 0.5
    assert new_prop.ph_color is None
    assert new_prop.base_materials == []
    
    # -- Test to dict
    d = new_prop.to_dict()
    assert d == { "ph": {
            "id_num": 0,
            "percentage_of_assembly": 0.5,
            "base_material_dict": {}
        }
    }

    # -- Test from dict
    new_prop = EnergyMaterialPhProperties.from_dict(d['ph'], False)
    assert new_prop.id_num == 0
    assert new_prop.percentage_of_assembly == 0.5
    assert new_prop.ph_color is None
    assert new_prop.base_materials == []

def test_energy_material_ph_properties_with_color():
    new_prop = EnergyMaterialPhProperties(None)
    new_prop.id_num = 0
    new_prop.percentage_of_assembly = 0.5
    new_prop.ph_color = PhColor.from_argb(255, 255, 255, 255)
    assert new_prop.id_num == 0
    assert new_prop.percentage_of_assembly == 0.5
    assert new_prop.ph_color.a == 255
    assert new_prop.ph_color.r == 255
    assert new_prop.ph_color.g == 255
    assert new_prop.ph_color.b == 255
    assert new_prop.base_materials == []
    
    # -- Test to dict
    d = new_prop.to_dict()
    assert d == { "ph": {
            "id_num": 0,
            "percentage_of_assembly": 0.5,
            "base_material_dict": {},
            "ph_color": {'a': 255, 'r': 255, 'g': 255, 'b': 255}
        }
    }

    # -- Test from dict
    new_prop = EnergyMaterialPhProperties.from_dict(d['ph'], False)
    assert new_prop.id_num == 0
    assert new_prop.percentage_of_assembly == 0.5
    assert new_prop.ph_color is not None
    assert new_prop.ph_color.a == 255
    assert new_prop.ph_color.r == 255
    assert new_prop.ph_color.g == 255
    assert new_prop.ph_color.b == 255
    assert new_prop.base_materials == []
    
    # -- Test copy
    new_prop_2 = new_prop.duplicate()
    assert new_prop_2.id_num == 0
    assert new_prop_2.percentage_of_assembly == 0.5
    assert new_prop_2.ph_color is not None
    assert new_prop_2.ph_color.a == 255
    assert new_prop_2.ph_color.r == 255
    assert new_prop_2.ph_color.g == 255
    
# -----------------------------------------------------------------------------
# -- Test EnergyMaterialNoMassPhProperties
def test_energy_material_no_mass_ph_properties():
    new_prop = EnergyMaterialNoMassPhProperties(None)
    new_prop.id_num = 0
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None
    
    # -- Test to dict
    d = new_prop.to_dict()
    assert d == { "ph": {
            "id_num": 0,
        }
    }

    # -- Test from dict
    new_prop = EnergyMaterialNoMassPhProperties.from_dict(d['ph'], False)
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None

def test_energy_material_no_mass_ph_properties_with_color():
    new_prop = EnergyMaterialNoMassPhProperties(None)
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
    assert d == { "ph": {
            "id_num": 0,
            "ph_color": {'a': 255, 'r': 255, 'g': 255, 'b': 255}
        }
    }

    # -- Test from dict
    new_prop = EnergyMaterialNoMassPhProperties.from_dict(d['ph'], False)
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

# -----------------------------------------------------------------------------
# -- Test EnergyMaterialVegetationPhProperties
def test_energy_material_vegetation_ph_properties():
    new_prop = EnergyMaterialVegetationPhProperties(None)
    new_prop.id_num = 0
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None
    
    # -- Test to dict
    d = new_prop.to_dict()
    assert d == { "ph": {
            "id_num": 0,
        }
    }

    # -- Test from dict
    new_prop = EnergyMaterialVegetationPhProperties.from_dict(d['ph'], False)
    assert new_prop.id_num == 0
    assert new_prop.ph_color is None

def test_energy_material_vegetation_ph_properties_with_color():
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
    assert d == { "ph": {
            "id_num": 0,
            "ph_color": {'a': 255, 'r': 255, 'g': 255, 'b': 255}
        }
    }

    # -- Test from dict
    new_prop = EnergyMaterialVegetationPhProperties.from_dict(d['ph'], False)
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