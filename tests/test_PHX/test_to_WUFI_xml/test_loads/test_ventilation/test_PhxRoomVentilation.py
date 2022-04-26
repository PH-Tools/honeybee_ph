from PHX.model.loads import ventilation
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxRoomVentilation(reset_class_counters):
    v1 = ventilation.PhxRoomVentilation()
    result = generate_WUFI_XML_from_object(v1, _header="")
    assert xml_string_to_list(result) == [
        '<Name>Unnamed_Space</Name>',
        '<Type>99</Type>',
        '<IdentNrUtilizationPatternVent>0</IdentNrUtilizationPatternVent>',
        '<IdentNrVentilationUnit>0</IdentNrVentilationUnit>',
        '<Quantity>1</Quantity>',
        '<AreaRoom unit="m²">0.0</AreaRoom>',
        '<ClearRoomHeight unit="m">2.5</ClearRoomHeight>',
        '<DesignVolumeFlowRateSupply unit="m³/h">0.0</DesignVolumeFlowRateSupply>',
        '<DesignVolumeFlowRateExhaust unit="m³/h">0.0</DesignVolumeFlowRateExhaust>'
    ]
