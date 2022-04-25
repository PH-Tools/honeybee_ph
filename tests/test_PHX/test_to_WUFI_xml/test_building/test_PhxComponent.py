from PHX.model import building
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxProject(reset_class_counters):
    c1 = building.PhxComponent()
    result = generate_WUFI_XML_from_object(c1, _header="")
    assert xml_string_to_list(result) == [
        '<IdentNr>1</IdentNr>',
        '<Name></Name>',
        '<Visual>true</Visual>',
        '<Type>1</Type>',
        '<IdentNrColorI>1</IdentNrColorI>',
        '<IdentNrColorE>1</IdentNrColorE>',
        '<InnerAttachment>1</InnerAttachment>',
        '<OuterAttachment>-1</OuterAttachment>',
        '<IdentNr_ComponentInnerSurface>-1</IdentNr_ComponentInnerSurface>',
        '<IdentNrAssembly>-1</IdentNrAssembly>',
        '<IdentNrWindowType>-1</IdentNrWindowType>',
        '<IdentNrPolygons count="0"/>'
    ]
