# -*- Python Version: 2.7 -*-
# -*- coding: utf-8 -*-

"""Functions for converting values between SI and IP units."""

try:
    from typing import Union, Optional, Tuple
except ImportError:
    pass  # IronPython 2.7

import re


# {Unit You have: {Unit you Want}, {...}, ...}
CONVERSION_SCHEMAS = {
    # -- SI -> IP
    "C": {"SI": "{}*1", "C": "{}*1", "F": "{}*1.8+32"},
    "DELTA-C": {"SI": "{}*1", "DELTA-C": "{}*1", "DELTA-F": "{}*1.8"},
    "LITER": {"SI": "{}*1", "LITER": "{}*1", "GALLON": "{}*0.264172", "FT3": "{}*0.035314667", "M3": "{}*0.001"},
    "MM": {"SI": "{}*1", "MM": "{}*1", "FT": "{}*0.00328084", "IN": "{}*0.0394"},
    "M": {"SI": "{}*1", "M": "{}*1", "FT": "{}*3.280839895", "IN": "{}*39.3701"},
    "M/DAY": {"SI": "{}*1", "M/DAY": "{}*1", "FT/DAY": "{}*3.280839895"},
    "M2": {"SI": "{}*1", "M2": "{}*1", "FT2": "{}*10.76391042"},
    "M3": {"SI": "{}*1", "M3": "{}*1", "FT3": "{}*35.31466672", "LITER": "{}*1000", "GALLON": "{}*264.1720524"},
    "M3/HR": {"SI": "{}*1", "M3/HR": "{}*1", "CFM": "{}*0.588577779"},
    "WH/M3": {"SI": "{}*1", "WH/M3": "{}*1", "W/CFM": "{}*1.699010796"},
    "WH/KM2": {"SI": "{}*1", "WH/KM2": "{}*1", "BTU/FT2": "{}*0.176110159"},
    "KWH/M2": {"SI": "{}*1", "KWH/M2": "{}*1",  "KBTU/FT2": "{}*0.316998286", "KWH/FT2": "{}*0.092903040"},
    "MJ/M3K": {"SI": "{}*1", "MJ/M3K": "{}*1", "BTU/FT3-F": "{}*14.91066014"},
    "W/M2K": {"SI": "{}*1", "W/M2K": "{}*1", "BTU/HR-FT2-F": "{}*0.176110159", "HR-FT2-F/BTU": "{}**-1*5.678264134"},
    "M2K/W": {"SI": "{}*1", "M2K/W": "{}*1", "HR-FT2-F/BTU": "{}*5.678264134"},
    "W/MK": {"SI": "{}*1", "W/MK": "{}*1", "HR-FT2-F/BTU-IN": "{}**-1*0.144227909", "BTU/HR-FT-F": "{}*0.577789236"},
    "W/K": {"SI": "{}*1", "W/K": "{}*1", "BTU/HR-F": "{}*1.895633976"},
    "KW": {"SI": "{}*1", "KW": "{}*1", "BTU/HR": "{}*3412.141156", "KBTU/HR": "{}*3.412141156"},
    "W/W": {"SI": "{}*1", "W/W": "{}*1", "BTUHR/W": "{}*3.412141156"},  # SEER
    # -- IP -> SI
    "F": {"SI": "({}-32)/1.8", "C": "({}-32)/1.8"},
    "DELTA-F": {"SI": "{}*0.555555556", "DELTA-C": "{}*0.555555556", "DELTA-F": "{}*1"},
    "IN": {"SI": "{}*0.0254", "M": "{}*0.0254", "MM": "{}*25.4", "FT": "{}/12", "IN": "{}*1"},
    "FT": {"SI": "{}*0.3048", "M": "{}*0.3048", "MM": "{}*304.8", "FT": "{}*1", "IN": "{}*12"},
    "BTU/HR-FT-F": {"SI": "{}*1.730734908", "W/MK": "{}*1.730734908", "HR-FT2-F/BTU-IN": "1/({}*12)"},
    "HR-FT2-F/BTU-IN": {"SI": "{}*1.730734908", "W/MK": "(1/({}*12))*1.730734908", "BTU/HR-FT-F": "1/({}*12)"},
}


def _standardize_input_unit(_in):
    """Standardize unit nomenclature. ie: 'FT3/M' and 'CFM' both return 'CFM'."""

    codes = {
        'FT': 'FT', "'": 'FT',
        'IN': 'IN', '"': 'IN',
        'MM': 'MM',
        'CM': 'CM',
        'M': 'M',
        'IP': 'IP',
        'FT3': 'FT3',
        'M3': 'M3',
        'F': 'F', 'DEG F': 'F',
        'C': 'C', 'DEG C': 'C',
        'CFM': 'CFM', 'FT3/M': 'CFM', 'FT3M': 'CFM',
        'CFH': 'CFH', 'FT3/H': 'CFH', 'FT3H': 'CFH',
        'L': 'LITER', "LITER": "LITER",
        'GA': 'GA', 'GALLON': 'GA',
        'BTU/H': 'BTUH', 'BTUH': 'BTUH',
        'KBTU/H': 'KBTUH', 'KBTUH': 'KBTUH',
        'TON': 'TON',
        'W': 'W',
        'WH': 'WH',
        'KW': 'KW',
        'KWH': 'KWH',
        'W/M2K': 'W/M2K', 'WM2K': 'WM2K',
        'W/MK': 'W/MK',
        'W/K': 'W/K',
        'M3/H': 'M3/H', 'M3H': 'M3/H', 'CMH': 'M3/H',
        'W/W': 'W/W',
        'BTU/WH': 'BTU/WH', 'BTUH/W': 'BTU/WH', 'BTU/W': 'BTU/WH',
        'R/IN': 'R/IN', 'R-IN': 'R/IN', 'HR-FT2-F/BTU-IN': 'HR-FT2-F/BTU-IN',
        'HR-FT2-F/BTU': 'HR-FT2-F/BTU',
        'BTU/HR-FT-F': 'BTU/HR-FT-F',
    }
    # Note: BTU/W conversion isn't really right, but I think many folks use that
    # when they mean Btu/Wh (or Btu-h/W)

    _input_string = str(_in).upper()
    try:
        input_unit = codes[_input_string]
    except KeyError:
        raise Exception(
            "Error: I do not know how to read the input: {}?".format(_input_string)
        )

    return input_unit


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
    input_unit = _standardize_input_unit(input_unit)
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
        conversion_equation = schema[target_unit]
    except KeyError:
        raise Exception(
            "Error: Unit conversion schema for '{}' does not include '{}'. Input only: {}".format(
                input_unit, target_unit, list(schema.keys()))
        )

    return eval("{}".format(conversion_equation).format(_value))


def parse_input(_input_string):
    # type: (str) -> Tuple[str, Optional[str]]
    """Parse an input string into the 'value part' and the 'units part'.

    examples:
        '0.5 in' returns -> ('0.5', 'IN')
        '0.5" ' returns -> ('0.5', 'IN')
        0.5 returns -> ('0.5', None)
        '0.5Btu/hr-Ft2-F' returns -> ('0.5', 'BTU/HR-FT2-F')
    """

    # -- First, try and split the input string at the first alpha-character found
    # -- ie: the input string: "0.5 HR-FT2-F/BTU-IN" will get split at index=4
    # --                           ^
    # -- You can't just look for the numbers, since some units have numbers in them ('FT2', ...)

    input_string = str(_input_string).strip().upper()
    rx = re.compile(r"[^\d. ]", re.IGNORECASE)
    match = rx.search(input_string)

    if not match:
        # -- No alpha part
        return (input_string, None)

    found_span = match.span()
    alpha_part = _input_string[found_span[0]:].strip()
    numeric_part = _input_string[:found_span[0]].strip()

    return numeric_part, alpha_part
