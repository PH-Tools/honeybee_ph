# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Export an HBJSON file to a PHPP excel document."""

import sys
from rich import print
import pathlib
import os

from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_PHPP import phpp_app
from PHX.to_PHPP.phpp_localization.shape_model import PhppShape

if __name__ == '__main__':

    # --- Command line arguments
    # -------------------------------------------------------------------------
    SOURCE_FILE = pathlib.Path(sys.argv[1]).resolve()
    SHAPE_FILE = pathlib.Path(sys.argv[2]).resolve()

    # --- Read in an existing HB_JSON and re-build the HB Objects
    # -------------------------------------------------------------------------
    print("- " * 20)
    print(f"> Reading in the HBJSON file: {SOURCE_FILE}")
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(SOURCE_FILE)
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

    # --- Generate the PhxProject file.
    # -------------------------------------------------------------------------
    print(f"> Converting HB-Model: {hb_model.display_name} to a PHX model")
    phx_project = create_project.convert_hb_model_to_PhxProject(
        hb_model, group_components=True)

    # --- Load the correct PHPP Shape, Connect to open instance of XL
    # -------------------------------------------------------------------------
    phpp_shape = PhppShape.parse_file(SHAPE_FILE)
    phpp_conn = phpp_app.PHPPConnection(phpp_shape)

    if phpp_conn.xl.connection_is_open():
        file = phpp_conn.xl.wb.name
        print(f'> Successfully connected to excel doc: {file}')
        if not phpp_conn.valid_phpp_document():
            msg = f"\nError: The excel file '{file}' does not appear to be a valid PHPP? "\
                "Please ensure this is a PHPP file, and if you have multiple Excel "\
                "documents open, ensure that the PHPP is the 'active' excel file. "\
                "If you continue to have trouble, try closing all other excel documents "\
                "except the PHPP."
            raise Exception(msg)

    with phpp_conn.xl.in_silent_mode():
        phpp_conn.write_certification_config(phx_project)
        phpp_conn.write_climate_data(phx_project)
        phpp_conn.write_project_constructions(phx_project)
        phpp_conn.write_project_tfa(phx_project)
        phpp_conn.write_project_opaque_surfaces(phx_project)
        phpp_conn.write_project_window_components(phx_project)
        phpp_conn.write_project_window_surfaces(phx_project)
        phpp_conn.write_project_ventilation_components(phx_project)
        phpp_conn.write_project_ventilators(phx_project)
        phpp_conn.write_project_spaces(phx_project)
        phpp_conn.write_project_ventilation_type(phx_project)
        phpp_conn.write_project_airtightness(phx_project)
        print("> Done writing data to PHPP.")
