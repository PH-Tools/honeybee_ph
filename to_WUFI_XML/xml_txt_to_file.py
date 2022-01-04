# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""
Functions for writing a Text XML file out to disk.
"""

from datetime import datetime
import os
import shutil
from pathlib import Path
from rich import print


def write_XML_text_file(_file_address: Path, _xml_text: str) -> None:
    """Write the PH 'Project' xml string out to a file.

    Arguments:
    ----------
        * _file_address (pathlib.Path): The file path object to save to.
        * _xml_text (str): The XML text to write out to file.

    Returns:
    --------
        * None
    """

    def clean_filename(_file_address):
        old_file_name, old_file_extension = os.path.splitext(_file_address)
        t = datetime.now()
        return f"{old_file_name}_{t.month}_{t.day}_{t.hour}_{t.minute}_{t.second}{old_file_extension}"

    # -- Sort out the filenames and paths
    save_dir = os.path.dirname(_file_address)
    save_filename = os.path.basename(_file_address)
    save_filename_clean = clean_filename(save_filename)

    # -- Make subdirs as needed
    os.makedirs(save_dir, exist_ok=True)

    try:
        save_address_1 = os.path.join(save_dir, save_filename)
        save_address_2 = os.path.join(save_dir, save_filename_clean)
        with open(save_address_1, "w", encoding="utf8") as f:
            f.writelines(_xml_text)

        #  Make a working copy
        shutil.copyfile(save_address_1, save_address_2)

    except PermissionError:
        # - In case the file is being used by WUFI or something else, make a new copy.
        print(
            f"Target file: {save_filename} is currently being used by another process and is protected.\n"
            f"Writing to a new file: {save_address_2}"
        )

        with open(save_address_2, "w", encoding="utf8") as f:
            f.writelines(_xml_text)

    print("[bold green]> Successfully wrote to file.[/bold green]")
