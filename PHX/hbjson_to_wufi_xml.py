# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Run script to convert an HBJSON file over to WUFI XML format."""

from os import mkdir
from typing import Tuple, List
import sys
import pathlib
from PHX.from_HBJSON import read_HBJSON_file, create_project
from PHX.to_WUFI_XML import xml_builder, xml_txt_to_file


class InputFileError(Exception):
    def __init__(self, path):
        self.msg = f'\nError: Cannot find HBJSON file: {path}'
        super().__init__(self.msg)


def resolve_paths(_args: List[str]) -> Tuple[pathlib.Path, pathlib.Path]:
    """Sort out the file input and output paths. Make the output directory if needed.

    Arguments:
    ----------
        * _args (Tuple): sys.args Tuple of inputs.

    Returns:
    --------
        * Tuple
            - [0] (pathlib.Path): The HBJSON Source file path.
            - [1] (pathlib.Path): The WUFI XML Target file path.
    """

    print('> Resolving file paths...')
    src = pathlib.Path(_args[1])
    if not src.exists():
        raise InputFileError(src)

    target_dir = pathlib.Path(_args[3])
    target_file = f'{_args[2]}.xml'

    if not target_dir.exists():
        mkdir(target_dir)

    target = pathlib.Path(target_dir, target_file)

    return src, target


if __name__ == '__main__':
    print("- " * 50)

    # --- Input / Output file Path
    # -----------------------------------------------------------------------------
    SOURCE_FILE, TARGET_FILE_XML = resolve_paths(sys.argv)

    # --- Read in the existing HB_JSON and re-build the HB Objects
    # -----------------------------------------------------------------------------
    print(f"> Reading in the HBJSON file: ./{SOURCE_FILE}")
    hb_json_dict = read_HBJSON_file.read_hb_json_from_file(SOURCE_FILE)
    hb_model = read_HBJSON_file.convert_hbjson_dict_to_hb_model(hb_json_dict)

    # --- Generate the WUFI Project file.
    print(f'> Generating the PHX-Project from the Honeybee-Model: "{hb_model}"')
    phx_Project = create_project.convert_HB_model_to_WUFI_Project(
        hb_model, group_components=True)

    # --- Output the WUFI Project as an XML Text File
    # ---------------------------------------------------------------------------
    print(f'> Generating XML Text for the PHX-Project: "{phx_Project}"')
    xml_txt = xml_builder.generate_WUFI_XML_from_object(phx_Project)

    print(f"> Saving the XML file to: ./{TARGET_FILE_XML}")
    xml_txt_to_file.write_XML_text_file(TARGET_FILE_XML, xml_txt)
