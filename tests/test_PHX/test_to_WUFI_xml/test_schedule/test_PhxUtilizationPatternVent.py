from PHX.model import schedules
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxRoomVentilation(reset_class_counters):
    s1 = schedules.UtilizationPatternVent()
    result = generate_WUFI_XML_from_object(s1, _header="")
    assert xml_string_to_list(result) == [
        '<Name>__unamed_vent_pattern__</Name>',
        '<IdentNr>1</IdentNr>',
        '<OperatingDays>7</OperatingDays>',
        '<OperatingWeeks>52</OperatingWeeks>',
        '<Maximum_DOS>0.0</Maximum_DOS>',
        '<Maximum_PDF>0.0</Maximum_PDF>',
        '<Standard_DOS>0.0</Standard_DOS>',
        '<Standard_PDF>0.0</Standard_PDF>',
        '<Basic_DOS>0.0</Basic_DOS>',
        '<Basic_PDF>0.0</Basic_PDF>',
        '<Minimum_DOS>0.0</Minimum_DOS>',
        '<Minimum_PDF>0.0</Minimum_PDF>'
    ]
