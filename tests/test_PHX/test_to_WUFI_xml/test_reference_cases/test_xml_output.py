import pytest
from pathlib import Path
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.from_WUFI_XML import read_WUFI_XML_file
from PHX.to_WUFI_XML import xml_builder


@pytest.mark.parametrize('hbjson_file,xml_file',
                         [
                             (
                                 Path('tests', '_source_hbjson',
                                      'Default_Model_Single_Zone.hbjson'),
                                 Path('tests', '_reference_xml',
                                      'Default_Model_Single_Zone.xml')
                             ),
                             (
                                 Path('tests', '_source_hbjson',
                                      'Default_Room_Multiple_Zones_wih_Apertures_Single_BldgSegment.hbjson'),
                                 Path('tests', '_reference_xml',
                                      'Default_Room_Multiple_Zones_wih_Apertures_Single_BldgSegment.xml')
                             ),
                             (
                                 Path('tests', '_source_hbjson',
                                      'Default_Room_Multiple_Zones_wih_Apertures.hbjson'),
                                 Path('tests', '_reference_xml',
                                      'Default_Room_Multiple_Zones_wih_Apertures.xml')
                             ),
                             (
                                 Path('tests', '_source_hbjson',
                                      'Default_Room_Single_Zone_wih_Apertures.hbjson'),
                                 Path('tests', '_reference_xml',
                                      'Default_Room_Single_Zone_wih_Apertures.xml')
                             ),
                             (
                                 Path('tests', '_source_hbjson',
                                      'Default_Room_Single_Zone_wih_Shades.hbjson'),
                                 Path('tests', '_reference_xml',
                                      'Default_Room_Single_Zone_wih_Shades.xml')
                             ),
                         ])
def test_xml_output(reset_class_counters, hbjson_file, xml_file):
    # -- HB Model
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(hbjson_file)
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

    # -- PhxProject file.
    phx_project = create_project.convert_hb_model_to_PhxProject(
        hb_model, group_components=True)

    # -- WUFI text
    new_xml_txt = xml_builder.generate_WUFI_XML_from_object(phx_project)

    # -- Load the reference case
    ref_xml_text = read_WUFI_XML_file.read_WUFI_XML_from_file(xml_file)

    assert new_xml_txt == ref_xml_text
