# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions for importing / translating Honeybee Models into WUFI-JSON """

# -- Required: Import base packages to run the __init__ startup routines
# -- which adds the .ph properties slot to all HB Objects. This must be done before
# -- running read_hb_json to ensure there is a place for all the .ph properties to go.
import honeybee
import honeybee_ph
import honeybee_energy
import honeybee_energy_ph
import ladybug_geometry
import ladybug_geometry_ph

import json
import pathlib
from honeybee.model import Model as HB_Model


class HBJSONModelReadError(Exception):
    def __init__(self, _in):
        self.message = f"Error: Can only convert a Honeybee 'Model' to WUFI XML.\n"\
            "Got a Honeybee object of type: {_in}."

        super(HBJSONModelReadError, self).__init__(self.message)


def read_hb_json(_file_address: pathlib.Path) -> HB_Model:
    """Read in the HB_JSON Model from the Rhino File and convert back into a HB-Model.

    Arguments:
    ----------
        _file_address (str): A valid file path for the 'HB_Json' file to read.

    Returns:
    --------
        HB_Model: The Honeybee Model, rebuilt from the HB-JSON file.
    """

    with open(_file_address) as json_file:
        data = json.load(json_file)

    if data.get('type', None) != 'Model':
        raise HBJSONModelReadError(data.get('type', None))

    model = HB_Model.from_dict(data)

    return model
