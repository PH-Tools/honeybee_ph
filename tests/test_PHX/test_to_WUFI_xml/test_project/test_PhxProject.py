from PHX.model import project
from PHX.to_WUFI_XML.xml_builder import generate_WUFI_XML_from_object
from tests.test_PHX.test_to_WUFI_xml._utils import xml_string_to_list


def test_default_PhxProject(reset_class_counters):
    p1 = project.PhxProject()
    result = generate_WUFI_XML_from_object(p1, _header="")
    assert xml_string_to_list(result) == [
        '<DataVersion>48</DataVersion>',
        '<UnitSystem>48</UnitSystem>',
        '<ProgramVersion>3.2.0.1</ProgramVersion>',
        '<Scope>3</Scope>',
        '<DimensionsVisualizedGeometry>2</DimensionsVisualizedGeometry>',
        '<ProjectData>',
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
        '<Responsible_Email></Responsible_Email>',
        '</ProjectData>',
        '<UtilisationPatternsVentilation count="0"/>',
        '<UtilizationPatternVent count="0"/>',
        '<Variants count="0"/>',
        '<Assemblies count="0"/>',
        '<WindowTypes count="0"/>'
    ]
