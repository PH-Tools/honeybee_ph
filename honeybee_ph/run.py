# coding=utf-8
# -*- Python Version: 2.7 -*-

"""Module for reading in HBJSON and converting to PHX-Model.

Running the 'convert_hbjson_to_PHX' function will call a new subprocess using the 
Ladybug Tools Python 3.7 interpreter.
"""

from __future__ import division

import os
import subprocess

try:  # import the core honeybee dependencies
    from honeybee.config import folders as hb_folders
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))


def _run_hbjson2PHX_windows(_hbjson, _save_file_name, _save_folder):
    # type: (str, str, str) -> tuple[str, str]
    raise NotImplementedError


def _run_hbjson2PHX_unix(_hbjson, _save_file_name, _save_folder):
    # type: (str, str, str) -> tuple[str, str]
    """Convert an HBJSON to a PHX using LBT's Python 3.7 interpreter.

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

    # -- check the input file
    assert os.path.isfile(_hbjson), 'No HBJSON file found at {}.'.format(_hbjson)
    directory, file_name = os.path.split(_hbjson)

    # -- Resolve the file paths
    python_dir = os.path.split(os.path.split(hb_folders.python_exe_path)[0])[0]
    run_file_path = os.path.join(python_dir, 'lib', 'python3.7',
                                 'site-packages', 'PHX', 'hbjson_to_wufi_xml.py')

    # -- read in the hbjson file, convert to PHX
    cmds = [hb_folders.python_exe_path,
            run_file_path,
            _hbjson,
            _save_file_name,
            _save_folder]
    use_shell = True if os.name == 'nt' else False
    process = subprocess.Popen(cmds,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=use_shell)
    stdout, stderr = process.communicate()

    if stderr:
        raise Exception(stderr)

    for _ in str(stdout).split('\\n'):
        print(_)

    return directory, file_name


def convert_hbjson_to_PHX(_hbjson, _save_file_name, _save_folder):
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
    # run the simulation
    if os.name == 'nt':
        # we are on Windows
        directory, file_name = _run_hbjson2PHX_windows(
            _hbjson, _save_file_name, _save_folder)
    else:
        # we are on Mac, Linux, or some other unix-based system
        directory, file_name = _run_hbjson2PHX_unix(
            _hbjson, _save_file_name, _save_folder)

    return directory, file_name
