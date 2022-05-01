# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""DEV SANDBOX: export an HBJSON file to a PHPP XL file."""

from rich import print
import pathlib
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_PHPP.phpp import phpp_app
import xlwings as xw

if __name__ == '__main__':
    # --- Input file Path
    # -------------------------------------------------------------------------
    SOURCE_FILE = pathlib.Path("tests", "_source_hbjson",
                               "Default_Room_Single_Zone_wih_Apertures.hbjson")

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
    # -------------------------------------------------------------------------
    phpp_conn = phpp_app.PHPPConnection()
    if phpp_conn.xl.connection_is_open():
        file = phpp_conn.xl.wb.name
        print(f'[bold green]> connected to excel doc: {file}[/bold green]')
    with phpp_conn.xl.in_silent_mode():
        # phpp_conn.u_values.clear_sheet()
        for phx_construction in phx_project.assembly_types:
            phpp_conn.u_values.write_phx_construction_to_sheet(phx_construction)

        # phpp_conn.components.clear_sheet()
        for phx_construction in phx_project.window_types:
            phpp_conn.components.write_phx_construction_to_sheet(phx_construction)

        # print(phpp_conn.u_values.get_next_empty_constructor_row_num())

        #print('[bold green]> writing to excel....[/bold green]')
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
