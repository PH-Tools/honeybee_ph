from PHX.model import geometry
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_single_Vertix_to_XML(reset_class_counters):
    v1 = geometry.PhxVertix(0, 0, 0)
    result = generate_WUFI_XML_from_object(v1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<X>0</X>',
        '<Y>0</Y>',
        '<Z>0</Z>',
    ]


def test_multiple_Vertix_to_XML(reset_class_counters):
    v1 = geometry.PhxVertix(0, 0, 0)
    result_1 = generate_WUFI_XML_from_object(v1, _header="")
    assert xml_string_to_list(result_1) == [
        '<IdentNr>1</IdentNr>',
        '<X>0</X>',
        '<Y>0</Y>',
        '<Z>0</Z>',
    ]

    v2 = geometry.PhxVertix(1, 2, 3)
    result_2 = generate_WUFI_XML_from_object(v2, _header="")
    assert xml_string_to_list(result_2) == [
        '<IdentNr>2</IdentNr>',
        '<X>1</X>',
        '<Y>2</Y>',
        '<Z>3</Z>',
    ]

    v3 = geometry.PhxVertix(0.5, 0.23, 0.98)
    result_3 = generate_WUFI_XML_from_object(v3, _header="")
    assert xml_string_to_list(result_3) == [
        '<IdentNr>3</IdentNr>',
        '<X>0.5</X>',
        '<Y>0.23</Y>',
        '<Z>0.98</Z>',
    ]
