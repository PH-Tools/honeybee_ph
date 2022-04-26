from PHX.model import elec_equip
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxDeviceCooktop(reset_class_counters):
    d1 = elec_equip.PhxDeviceCooktop()
    result = generate_WUFI_XML_from_object(d1, "", "_PhxElectricalDevice")
    assert xml_string_to_list(result) == [
        '<Comment></Comment>',
        '<ReferenceQuantity>1</ReferenceQuantity>',
        '<Quantity>1</Quantity>',
        '<InConditionedSpace>true</InConditionedSpace>',
        '<ReferenceEnergyDemandNorm>2</ReferenceEnergyDemandNorm>',
        '<EnergyDemandNorm>100</EnergyDemandNorm>',
        '<EnergyDemandNormUse>100</EnergyDemandNormUse>',
        '<CEF_CombinedEnergyFactor>0</CEF_CombinedEnergyFactor>',
        '<Type>7</Type>',
        '<CookingWith>1</CookingWith>'
    ]
