# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""DEV SANDBOX: export an HBJSON file to a PHPP XL file."""

from rich import print
import pathlib
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_PHPP.phpp import app

if __name__ == '__main__':
    # --- Input / Output file Path
    # -------------------------------------------------------------------------
    SOURCE_FILE = pathlib.Path("sample", "hbjson", "Ridgeway_VI_220429.hbjson")
    TARGET_FILE_PHPP = pathlib.Path(
        "sample", "wufi_xml", "Ridgeway_VI_220429.xlsx")

    # --- Read in an existing HB_JSON and re-build the HB Objects
    # -------------------------------------------------------------------------
    print("[bold green]- [/bold green]" * 50)
    print(
        f"[bold green]> Reading in the HBJSON file: ./{SOURCE_FILE}[/bold green]")
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(SOURCE_FILE)
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

    # --- Generate the PhxProject file.
    # -------------------------------------------------------------------------
    phx_project = create_project.convert_hb_model_to_PhxProject(
        hb_model, group_components=True)

    # --- Connect to open instance of XL
    phpp_conn = app.Connection()
    with phpp_conn.silent():
        print('[bold green]> writing to excel....[/bold green]')

        # phpp_conn.areas.clear_sheet()

        # --- Write the surfaces to Excel
        #phpp_conn.areas.add_new_surfaces([my_first_surface, my_second_surface])
        # phpp_conn.areas.add_new_surface( my_second_surface )

        # --- Write the Constructions to Excel
        #phpp_conn.u_values.add_new_construction( constr_1 )

    # # --- Output the WUFI Project as an XML Text File
    # # -------------------------------------------------------------------------
    # print(
    #     f"[bold]> Generating XML Text for the Honeybee Model: [{hb_model}][/bold]")
    # xml_txt = xml_builder.generate_WUFI_XML_from_object(phx_project)

    # print(f"[bold]> Saving the XML file to: ./{TARGET_FILE_XML}[/bold]")
    # xml_txt_to_file.write_XML_text_file(TARGET_FILE_XML, xml_txt)
