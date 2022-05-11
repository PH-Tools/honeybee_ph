# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""DEV SANDBOX: convert an HBJSON file over to WUFI XML format."""
import importlib
from rich import print
import pathlib
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_WUFI_XML import xml_builder, xml_txt_to_file
from PHX.model import (building, project, geometry, schedules, certification,
                       constructions, elec_equip, components)

SOURCE_DIR = pathlib.Path("tests", "_source_hbjson")
source_file_names = [
    "Default_Model_Single_Zone.hbjson",
    "Default_Room_Multiple_Zones_with_Apertures_Single_BldgSegment.hbjson",
    "Default_Room_Multiple_Zones_with_Apertures.hbjson",
    "Default_Room_Single_Zone_with_Apertures.hbjson",
    "Default_Room_Single_Zone_with_Shades.hbjson"
]
SOURCE_FILES = [pathlib.Path(SOURCE_DIR, n) for n in source_file_names]
TARGET_DIR = pathlib.Path("tests", "_reference_xml")


def reload_PHX():
    """Reload all the PHX model modules to reset counters. This is only needed 
    so that the tests align when converting multiple models in one run."""
    importlib.reload(geometry)
    importlib.reload(building)
    importlib.reload(project)
    importlib.reload(geometry)
    importlib.reload(schedules)
    importlib.reload(certification)
    importlib.reload(constructions)
    importlib.reload(elec_equip)
    importlib.reload(components)


def generate_xml_file(_source: pathlib.Path, _target_dir: pathlib.Path):
    # -- Re-set all the PHX modules (counters)
    reload_PHX()

    target_file = pathlib.Path(_target_dir, _source.stem + '.xml')

    # --- Read in an existing HB_JSON and re-build the HB Objects
    # -------------------------------------------------------------------------
    print("[bold green]- [/bold green]" * 50)
    print(
        f"[bold green]> Reading in the HBJSON file: ./{_source}[/bold green]")
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(_source)
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

    # --- Generate the PhxProject file.
    # -------------------------------------------------------------------------
    phx_project = create_project.convert_hb_model_to_PhxProject(
        hb_model, group_components=True)

    # --- Output the WUFI Project as an XML Text File
    # -------------------------------------------------------------------------
    print(
        f"[bold]> Generating XML Text for the Honeybee Model: [{hb_model}][/bold]")
    xml_txt = xml_builder.generate_WUFI_XML_from_object(phx_project)

    print(f"[bold]> Saving the XML file to: ./{target_file}[/bold]")
    xml_txt_to_file.write_XML_text_file(target_file, xml_txt, False)


if __name__ == '__main__':
    for source_file in SOURCE_FILES:
        generate_xml_file(source_file, TARGET_DIR)
