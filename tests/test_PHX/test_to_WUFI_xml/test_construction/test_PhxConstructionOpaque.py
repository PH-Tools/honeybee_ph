from PHX.model import constructions
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxConstructionOpaque(reset_class_counters):
    a1 = constructions.PhxConstructionOpaque()
    result = generate_WUFI_XML_from_object(a1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<Name></Name>',
        '<Order_Layers>2</Order_Layers>',
        '<Grid_Kind>2</Grid_Kind>',
        '<Layers count="0"/>'
    ]
