from PHX.model import certification
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxPHCertification(reset_class_counters):
    c1 = certification.PhxPHCertification()
    result = generate_WUFI_XML_from_object(c1, _header="")
    assert xml_string_to_list(result) == [
        '<PH_CertificateCriteria>3</PH_CertificateCriteria>',
        '<PH_SelectionTargetData>2</PH_SelectionTargetData>',
        '<AnnualHeatingDemand>15.0</AnnualHeatingDemand>',
        '<AnnualCoolingDemand>15.0</AnnualCoolingDemand>',
        '<PeakHeatingLoad>10.0</PeakHeatingLoad>',
        '<PeakCoolingLoad>10.0</PeakCoolingLoad>',
        '<PH_Buildings count="0"/>'
    ]


def test_default_PhxPHCertification_with_Building(reset_class_counters):
    c1 = certification.PhxPHCertification()
    b1 = certification.PhxPhBuildingData()
    c1.ph_building_data = b1
    result = generate_WUFI_XML_from_object(c1, _header="")
    assert xml_string_to_list(result) == [
        '<PH_CertificateCriteria>3</PH_CertificateCriteria>',
        '<PH_SelectionTargetData>2</PH_SelectionTargetData>',
        '<AnnualHeatingDemand>15.0</AnnualHeatingDemand>',
        '<AnnualCoolingDemand>15.0</AnnualCoolingDemand>',
        '<PeakHeatingLoad>10.0</PeakHeatingLoad>',
        '<PeakCoolingLoad>10.0</PeakCoolingLoad>',
        '<PH_Buildings count="1">',
        '<PH_Building index="0">',
        '<IdentNr>1</IdentNr>',
        '<BuildingCategory>1</BuildingCategory>',
        '<OccupancyTypeResidential>1</OccupancyTypeResidential>',
        '<BuildingStatus>1</BuildingStatus>',
        '<BuildingType>1</BuildingType>',
        '<OccupancySettingMethod>2</OccupancySettingMethod>',
        '<NumberUnits>1</NumberUnits>',
        '<CountStories>1</CountStories>',
        '<EnvelopeAirtightnessCoefficient>1.0</EnvelopeAirtightnessCoefficient>',
        '<FoundationInterfaces count="0"/>',
        '</PH_Building>',
        '</PH_Buildings>'
    ]


def test_customized_PhxPHCertification_with_Building(reset_class_counters):
    c1 = certification.PhxPHCertification()
    c1.certification_criteria.annual_heating_demand = 123.45
    c1.certification_criteria.annual_cooling_demand = 234.56
    c1.certification_criteria.peak_heating_load = 345.67
    c1.certification_criteria.peak_cooling_load = 456.78

    b1 = certification.PhxPhBuildingData()
    c1.ph_building_data = b1
    result = generate_WUFI_XML_from_object(c1, _header="")
    assert xml_string_to_list(result) == [
        '<PH_CertificateCriteria>3</PH_CertificateCriteria>',
        '<PH_SelectionTargetData>2</PH_SelectionTargetData>',
        '<AnnualHeatingDemand>123.45</AnnualHeatingDemand>',
        '<AnnualCoolingDemand>234.56</AnnualCoolingDemand>',
        '<PeakHeatingLoad>345.67</PeakHeatingLoad>',
        '<PeakCoolingLoad>456.78</PeakCoolingLoad>',
        '<PH_Buildings count="1">',
        '<PH_Building index="0">',
        '<IdentNr>1</IdentNr>',
        '<BuildingCategory>1</BuildingCategory>',
        '<OccupancyTypeResidential>1</OccupancyTypeResidential>',
        '<BuildingStatus>1</BuildingStatus>',
        '<BuildingType>1</BuildingType>',
        '<OccupancySettingMethod>2</OccupancySettingMethod>',
        '<NumberUnits>1</NumberUnits>',
        '<CountStories>1</CountStories>',
        '<EnvelopeAirtightnessCoefficient>1.0</EnvelopeAirtightnessCoefficient>',
        '<FoundationInterfaces count="0"/>',
        '</PH_Building>',
        '</PH_Buildings>'
    ]
