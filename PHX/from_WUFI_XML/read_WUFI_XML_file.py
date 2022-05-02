# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for importing / converting WUFI-XML into PHX Models"""

import pathlib


def read_WUFI_XML_from_file(_file_address: pathlib.Path) -> str:
    """Read in the WUFI-XML file and return it as a string.

    Arguments:
    ----------
        _file_address (pathlib.Path): A valid file path for the WUFI-XML file to read.

    Returns:
    --------
        str: The WUFI XML text, read in from the WUFI-XML file.
    """

    with open(_file_address) as xml_file:
        data = xml_file.read()

    return data
