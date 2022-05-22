# coding=utf-8
# -*- Python Version: 2.7 -*-

"""Module for reading in HBJSON and converting to PHX-Model.

Running the 'convert_hbjson_to_PHX' function will call a new subprocess using the 
Ladybug Tools Python 3.7 interpreter.
"""

from __future__ import division

import os
import subprocess

try:
    from typing import List
except ImportError:
    pass  # Python 2.7

try:  # import the core honeybee dependencies
    from honeybee.config import folders as hb_folders
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


def _run_subprocess(commands):
    # type: (List[str]) -> None
    """Run a python subprocess using the supplied commands"""
    use_shell = True if os.name == 'nt' else False
    process = subprocess.Popen(
        commands,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=use_shell
    )

    stdout, stderr = process.communicate()

    if stderr:
        raise Exception(stderr)

    for _ in str(stdout).split('\\n'):
        print(_)


def convert_hbjson_to_WUFI_XML(_hbjson_file, _save_file_name, _save_folder):
    # type: (str, str, str) -> tuple[str, str]
    """Read in an hbjson file and output a new WUFI XML file in the designated location.

    Arguments:
    ---------
        * _hbjson (str): File path to an HBJSON file to be read in and converted to a PHX-Model.
        * _save_file_name (str): The XML filename.
        * _save_folder (str): The folder to save the new XML file in.

    Returns:
    --------
        * tuple
            - [0] (str): The path to the output XML file.
            - [1] (str): The output xml filename.
    """

    # -- Specify the path to the subprocess python script to run
    run_file_path = os.path.join(
        hb_folders.python_package_path,  'PHX', 'hbjson_to_wufi_xml.py')

    # -- check the file paths
    assert os.path.isfile(
        _hbjson_file), 'No HBJSON file found at {}.'.format(_hbjson_file)
    assert os.path.isfile(
        run_file_path), 'No Python file to run found at: {}'.format(run_file_path)

    # -------------------------------------------------------------------------
    # -- Read in the HBJSON, convert to WUFI XML
    commands = [
        hb_folders.python_exe_path,
        run_file_path,
        _hbjson_file,
        _save_file_name,
        _save_folder
    ]
    _run_subprocess(commands)

    # -------------------------------------------------------------------------
    # -- return the dir and filename of the xml created
    directory, file_name = os.path.split(_hbjson_file)
    return directory, file_name


def write_hbjson_to_phpp(_hbjson_file, _shape_file):
    # type: (str, str) -> None
    """Read in an hbjson file and write out to a PHPP file.

    Arguments:
    ---------
        * _hbjson (str): File path to an HBJSON file to be read in and converted to a PHX-Model.
        * _shape_file (str): Full path to the designated PHPP Shape File to use.
    """

    # -- Specify the path to the subprocess python script to run
    run_file_path = os.path.join(
        hb_folders.python_package_path, 'PHX', 'hbjson_to_phpp.py')

    # -- check the file paths
    if not os.path.isfile(_hbjson_file):
        raise Exception('\nNo HBJSON file found at {}?'.format(_hbjson_file))
    if not os.path.isfile(run_file_path):
        raise Exception('\nNo Python file to run found at: {}?'.format(run_file_path))
    if not os.path.isfile(_shape_file):
        raise Exception('\nNo PHPP-Shapefile to found at: {}?'.format(_shape_file))

    # -------------------------------------------------------------------------
    # -- Read in the HBJSON, write our to PHPP
    commands = [
        hb_folders.python_exe_path,
        run_file_path,
        _hbjson_file,
        _shape_file
    ]
    _run_subprocess(commands)
