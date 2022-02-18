# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Run script to convert an HBJSON file over to WUFI XML format."""

import pathlib
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_WUFI_XML import xml_builder, xml_txt_to_file

# --- Input / Output file Path
# -----------------------------------------------------------------------------
SOURCE_FILE = pathlib.Path("sample", "hbjson", "Undercliff_220218.hbjson")
TARGET_FILE_XML = pathlib.Path("sample", "wufi_xml", "Undercliff_220218.xml")

# --- Read in an existing HB_JSON and re-build the HB Objects
# -----------------------------------------------------------------------------
print("- " * 50)
print(f"> Reading in the HBJSON file: ./{SOURCE_FILE}")
hb_json_dict = read_HBJSON_file.read_hb_json_from_file(SOURCE_FILE)
hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

# --- Generate the WUFI Project file.
wufi_Project = create_project.convert_HB_model_to_WUFI_Project(
    hb_model, group_components=True)

# # --- Output the WUFI Project as an XML Text File
# # ---------------------------------------------------------------------------
print(f"> Generating XML Text for the Honeybee Model: [{hb_model}]")
xml_txt = xml_builder.generate_WUFI_XML_for_Project(wufi_Project)

print(f"> Saving the XML file to: ./{TARGET_FILE_XML}")
xml_txt_to_file.write_XML_text_file(TARGET_FILE_XML, xml_txt)
