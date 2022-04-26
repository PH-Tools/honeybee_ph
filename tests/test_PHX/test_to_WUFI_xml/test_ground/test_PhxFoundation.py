from PHX.model import ground
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxProjectData(reset_class_counters):
    g1 = ground.PhxFoundation()
    result = generate_WUFI_XML_from_object(g1, _header="")
    assert xml_string_to_list(result) == [
        '<Name></Name>',
        '<SettingFloorSlabType choice="User defined">6</SettingFloorSlabType>',
        '<FloorSlabType choice="None">5</FloorSlabType>'
    ]
