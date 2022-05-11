
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.from_WUFI_XML import read_WUFI_XML_file
from PHX.to_WUFI_XML import xml_builder


def test_xml_output(to_xml_reference_cases):
    # -- Get the test-case file paths
    hbjson_file, xml_file = to_xml_reference_cases

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
    #assert new_xml_txt == ref_xml_text
