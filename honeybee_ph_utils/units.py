# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for converting values between SI and IP units."""

try:
    from typing import Union, Optional
except ImportError:
    pass  # IronPython 2.7


# {Unit You have: {Unit you Want}, {...}, ...}
CONVERSION_SCHEMAS = {
    "C": {"SI": "*1", "C": "*1", "F": "*1.8+32"},
    "DELTA-C": {"SI": "*1", "DELTA-C": "*1", "DELTA-F": "*1.8"},
    "LITER": {"SI": "*1", "LITER": "*1", "GALLON": "*0.264172", "FT3": "*0.035314667", "M3": "*0.001"},
    "MM": {"SI": "*1", "MM": "*1", "FT": "*0.00328084", "IN": "*0.0394"},
    "M": {"SI": "*1", "M": "*1", "FT": "*3.280839895", "IN": "*39.3701"},
    "M/DAY": {"SI": "*1", "M/DAY": "*1", "FT/DAY": "*3.280839895"},
    "M2": {"SI": "*1", "M2": "*1", "FT2": "*10.76391042"},
    "M3": {"SI": "*1", "M3": "*1", "FT3": "*35.31466672", "LITER": "*1000", "GALLON": "*264.1720524"},
    "M3/HR": {"SI": "*1", "M3/HR": "*1", "CFM": "*0.588577779"},
    "WH/M3": {"SI": "*1", "WH/M3": "*1", "W/CFM": "*1.699010796"},
    "WH/KM2": {"SI": "*1", "WH/KM2": "*1", "BTU/FT2": "*0.176110159"},
    "KWH/M2": {"SI": "*1", "KWH/M2": "*1",  "KBTU/FT2": "*0.316998286", "KWH/FT2": "*0.092903040"},
    "MJ/M3K": {"SI": "*1", "MJ/M3K": "*1", "BTU/FT3-F": "*14.91066014"},
    "W/M2K": {"SI": "*1", "W/M2K": "*1", "BTU/HR-FT2-F": "*0.176110159", "HR-FT2-F/BTU": "**-1*5.678264134"},
    "M2K/W": {"SI": "*1", "M2K/W": "*1", "HR-FT2-F/BTU": "*5.678264134"},
    "W/MK": {"SI": "*1", "W/MK": "*1", "HR-FT2-F/BTU-IN": "**-1*0.144227909", "BTU/HR-FT-F": "*0.577789236"},
    "W/K": {"SI": "*1", "W/K": "*1", "BTU/HR-F": "*1.895633976"},
    "KW": {"SI": "*1", "KW": "*1", "BTU/HR": "*3412.141156", "KBTU/HR": "*3.412141156"},
    "W/W": {"SI": "*1", "W/W": "*1", "BTUHR/W": "*3.412141156"}  # SEER
}


def convert(_value, _input_unit, _target_unit):
    # type: (Optional[Union[float, int, str]], str, str) -> Optional[Union[int, float]]
    """Convert an input value between SI and IP.

    Arguments:
    ----------
        * _value (Optional[Union[float, int, str]]): The Value to convert.
        * _input_unit (str): The input value's starting unit.
        * _target_unit (str): The input value's desired target unit.

    Returns:
    --------
        * (Optional[Union[float, int]]): The converted value in the target units.
    """
    if _value is None:
        return None

    # -- Clean user inputs
    input_unit = str(_input_unit).upper().strip().replace(" ", "")
    target_unit = str(_target_unit).upper().strip().replace(" ", "")

    # -- Get the right conversion Schema for the starting unit
    try:
        schema = CONVERSION_SCHEMAS[input_unit]
    except KeyError:
        raise Exception(
            "Error: Unit conversion schema does not include '{}'. Input only: {}".format(
                input_unit, list(CONVERSION_SCHEMAS.keys()))
        )

    # -- Get the right conversion factor based on the target unit
    try:
        conversion_factor = schema[target_unit]
    except KeyError:
        raise Exception(
            "Error: Unit conversion schema for '{}' does not include '{}'. Input only: {}".format(
                input_unit, target_unit, list(schema.keys()))
        )

    return eval("{}{}".format(_value, conversion_factor))
