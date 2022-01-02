# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Run script to convert an HBJSON file over to WUIF XML format."""

import pathlib
import from_HBJSON.read_HBJSON_file
import from_HBJSON.convert_HBJSON
import to_WUFI_XML.xml_builder
import to_WUFI_XML.xml_txt_to_file

# --- Input / Output file Path
# ------------------------------------------------------------------------------
SOURCE_FILE = pathlib.Path("sample", "hbjson", "Townsend_St_Input_220102.hbjson")
TARGET_FILE_XML = pathlib.Path("sample", "wufi_xml", "Townsend_St_Input_220102.xml")

# --- Read in an existing HB_JSON and re-build the HB Objects
# ------------------------------------------------------------------------------
print("- " * 50)
print(f"> Reading in the HBJSON file: ./{SOURCE_FILE}")
hb_model = from_HBJSON.read_HBJSON_file.read_hb_json(SOURCE_FILE)

# --- Generate the WUFI Project file.
hb_model = from_HBJSON.convert_HBJSON.add_PH_Properties_to_model(hb_model)
wufi_Project = from_HBJSON.convert_HBJSON.convert_HB_model_to_WUFI_Project(hb_model)

# # --- Output the WUFI Project as an XML Text File
# # ----------------------------------------------------------------------------
print(f"> Generating XML Text for the Honeybee Model: [{hb_model}]")
xml_txt = to_WUFI_XML.xml_builder.generate_WUFI_XML_for_Project(wufi_Project)

print(f"> Saving the XML file to: ./{TARGET_FILE_XML}")
to_WUFI_XML.xml_txt_to_file.write_XML_text_file(TARGET_FILE_XML, xml_txt)
