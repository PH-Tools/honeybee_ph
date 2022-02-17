# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Run script to convert an HBJSON file over to WUFI XML format."""

from rich import print
import pathlib
from PHX.from_HBJSON import read_HBJSON_file

from PHX.from_HBJSON import create_project
from PHX.to_WUFI_XML import xml_builder, xml_txt_to_file

# --- Input / Output file Path
# -----------------------------------------------------------------------------
SOURCE_FILE = pathlib.Path("sample", "hbjson", "Undercliff_220217.hbjson")
TARGET_FILE_XML = pathlib.Path("sample", "wufi_xml", "Undercliff_220217.xml")

# --- Read in an existing HB_JSON and re-build the HB Objects
# -----------------------------------------------------------------------------
print("[bold red]- [/bold red]" * 50)
print(f"[bold]> Reading in the HBJSON file: [/bold]./{SOURCE_FILE}")
hb_model = read_HBJSON_file.read_hb_json(SOURCE_FILE)

# --- Generate the WUFI Project file.
wufi_Project = create_project.convert_HB_model_to_WUFI_Project(
    hb_model, group_components=True)

# # --- Output the WUFI Project as an XML Text File
# # ---------------------------------------------------------------------------
print(f"[bold]> Generating XML Text for the Honeybee Model: [/bold][{hb_model}]")
xml_txt = xml_builder.generate_WUFI_XML_for_Project(wufi_Project)

print(f"[bold]> Saving the XML file to: [/bold]./{TARGET_FILE_XML}")
xml_txt_to_file.write_XML_text_file(TARGET_FILE_XML, xml_txt)
