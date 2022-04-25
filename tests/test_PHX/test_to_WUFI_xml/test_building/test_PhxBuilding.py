from PHX.model import building
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxProject(reset_class_counters):
    b1 = building.PhxBuilding()
    result = generate_WUFI_XML_from_object(b1, _header="")
    assert xml_string_to_list(result) == [
        '<Components count="0"/>',
        '<Zones count="0"/>'
    ]
