# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions for importing / converting Honeybee Models into PHX Models"""

# -- Dev Note: Required to import all the base packages to run the __init__ startup routines
# -- which ensures that .ph properties slot is added to all HB Objects. This must be done before
# -- running read_hb_json to ensure there is a place for all the .ph properties to go.
# -- Dev Note: Do not remove --
import honeybee
import honeybee_ph
import honeybee_energy
import honeybee_energy_ph
# -- Dev Note: Do not remove --

import json
import pathlib
from typing import Dict

from honeybee import model


class HBJSONModelReadError(Exception):
    def __init__(self, _in):
        self.message = f"Error: Can only convert a Honeybee 'Model' to WUFI XML.\n"\
            "Got a Honeybee object of type: {_in}."

        super(HBJSONModelReadError, self).__init__(self.message)


def read_hb_json_from_file(_file_address: pathlib.Path) -> Dict:
    """Read in the HBJSON file and return it as a python dictionary.

    Arguments:
    ----------
        _file_address (pathlib.Path): A valid file path for the HBJSON file to read.

    Returns:
    --------
        Dict: The HBJSON dictionary, read in from the HBJSON file.
    """

    with open(_file_address) as json_file:
        data = json.load(json_file)

    if data.get('type', None) != 'Model':
        raise HBJSONModelReadError(data.get('type', None))
    else:
        return data


def convert_hbjson_dict_to_hb_model(_data: Dict) -> model.Model:
    """Convert an HBJSON python dictionary into an HB-Model

    Arguments:
    ----------
        _data (Dict): An HBJSON dictionary with all the model information.

    Returns:
    --------
        model.Model: A Honeybee Model, rebuilt from the HBJSON file.
    """

    return model.Model.from_dict(_data)
