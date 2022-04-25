from PHX.model import project
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxProjectData(reset_class_counters):
    d1 = project.PhxProjectData()
    result = generate_WUFI_XML_from_object(d1, _header="")
    assert xml_string_to_list(result) == [
        '<Year_Construction>0</Year_Construction>',
        '<OwnerIsClient>false</OwnerIsClient>',
        '<Date_Project></Date_Project>',
        '<WhiteBackgroundPictureBuilding>None</WhiteBackgroundPictureBuilding>',
        '<Customer_Name></Customer_Name>',
        '<Customer_Street></Customer_Street>',
        '<Customer_Locality></Customer_Locality>',
        '<Customer_PostalCode></Customer_PostalCode>',
        '<Customer_Tel></Customer_Tel>',
        '<Customer_Email></Customer_Email>',
        '<Building_Name></Building_Name>',
        '<Building_Street></Building_Street>',
        '<Building_Locality></Building_Locality>',
        '<Building_PostalCode></Building_PostalCode>',
        '<Owner_Name></Owner_Name>',
        '<Owner_Street></Owner_Street>',
        '<Owner_Locality></Owner_Locality>',
        '<Owner_PostalCode></Owner_PostalCode>',
        '<Responsible_Name></Responsible_Name>',
        '<Responsible_Street></Responsible_Street>',
        '<Responsible_Locality></Responsible_Locality>',
        '<Responsible_PostalCode></Responsible_PostalCode>',
        '<Responsible_Tel></Responsible_Tel>',
        '<Responsible_LicenseNr></Responsible_LicenseNr>',
        '<Responsible_Email></Responsible_Email>'
    ]
