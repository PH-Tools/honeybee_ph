from PHX.model import constructions
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxMaterial(reset_class_counters):
    m1 = constructions.PhxMaterial()
    result = generate_WUFI_XML_from_object(m1, _header="")
    assert xml_string_to_list(result) == [
        '<Mass></Mass>',
        '<ThermalConductivity>0.0</ThermalConductivity>',
        '<BulkDensity>0.0</BulkDensity>',
        '<Porosity>0.0</Porosity>',
        '<HeatCapacity>0.0</HeatCapacity>',
        '<WaterVaporResistance>0.0</WaterVaporResistance>',
        '<ReferenceW>0.0</ReferenceW>'
    ]
