# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions for importing / translating Honeybee Models into WUFI-JSON """

import json
from honeybee._base import _Base
import honeybee.dictutil as hb_dict_util
import honeybee_energy.dictutil as energy_dict_util
import honeybee_radiance.dictutil as radiance_dict_util

# -------------------------------------------------------------------------------


class DeserializationError(Exception):
    def __init__(self, _data):
        self.message = (
            "Error: Cannot convert input data to HB/PH Object? Got:\n"
            f"{_data} of type: {type(_data)}. Expected a dict?"
        )
        super(DeserializationError, self).__init__(self.message)


def _dict_to_obj(_dict: dict) -> _Base:
    """Takes a dict and recreates a Honeybee object from it.

    Arguments:
    ----------
        * _dict (dict): The dictionary with attributes for the HB Object

    Returns:
    --------
        * (_Base): The re-created Honeybee Object.
    """

    hb_obj = hb_dict_util.dict_to_object(_dict, False)

    if hb_obj is None:
        hb_obj = energy_dict_util.dict_to_object(_dict, False)

    if hb_obj is None:
        hb_obj = radiance_dict_util.dict_to_object(_dict, False)

    if hb_obj is None:
        raise DeserializationError(_dict)
    else:
        return hb_obj


def read_hb_json(_file_address: str) -> list:
    """Read in the HB_JSON from the Rhino File and convert back into HB Objects.

    Arguments:
    ----------
        _file_address (str): A valid file path for the 'HB_Json' file to read

    Returns:
    --------
        (list): A list of the HB Object(s), rebuilt from the input JSON
    """

    with open(_file_address) as json_file:
        data = json.load(json_file)

        if isinstance(data, (tuple, list)):
            return [_dict_to_obj(_) for _ in data]
        else:
            return _dict_to_obj(data)
