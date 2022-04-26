from PHX.model import constructions
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxLayer(reset_class_counters):
    l1 = constructions.PhxLayer()
    result = generate_WUFI_XML_from_object(l1, _header="")
    assert xml_string_to_list(result) == [
        '<Thickness>0.0</Thickness>',
        '<Material>',
        '<Mass></Mass>',
        '<ThermalConductivity>0.0</ThermalConductivity>',
        '<BulkDensity>0.0</BulkDensity>',
        '<Porosity>0.0</Porosity>',
        '<HeatCapacity>0.0</HeatCapacity>',
        '<WaterVaporResistance>0.0</WaterVaporResistance>',
        '<ReferenceW>0.0</ReferenceW>',
        '</Material>'
    ]
