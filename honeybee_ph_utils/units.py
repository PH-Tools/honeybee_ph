# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for converting values between SI and IP units."""

try:
    from typing import Union, Optional, Tuple
except ImportError:
    pass  # IronPython 2.7

import re
from copy import copy

# {Unit You have: {Unit you Want}, {...}, ...}
CONVERSION_SCHEMAS = {
    # -- SI -> IP
    "C": {"SI": "{}*1", "C": "{}*1", "F": "{}*1.8+32"},
    "DELTA-C": {"SI": "{}*1", "DELTA-C": "{}*1", "DELTA-F": "{}*1.8"},
    "LITER": {"SI": "{}*1", "LITER": "{}*1", "GALLON": "{}*0.264172", "FT3": "{}*0.035314667", "M3": "{}*0.001"},
    "MM": {"SI": "{}*1", "MM": "{}*1", "M": "{}*0.001", "CM": "{}*0.1", "FT": "{}*0.00328084", "IN": "{}*0.0394"},
    "M": {"SI": "{}*1", "M": "{}*1", "CM": "{}*100", "MM": "{}*1000", "FT": "{}*3.280839895", "IN": "{}*39.3701"},
    "M/DAY": {"SI": "{}*1", "M/DAY": "{}*1", "FT/DAY": "{}*3.280839895", "M/S": "{}/24/60/60"},
    "M/S": {"SI": "{}*1", "M/S": "{}*1", "M/DAY": "{}*24*60*60", "FT/S": "{}*3.280839895", "FT/DAY": "{}*3.280839895*24*60*60", "MPH": "{}/0.44704"},
    "M2": {"SI": "{}*1", "M2": "{}*1", "FT2": "{}*10.76391042"},
    "M3": {"SI": "{}*1", "M3": "{}*1", "FT3": "{}*35.31466672", "LITER": "{}*1000", "GALLON": "{}*264.1720524"},
    "M3/HR": {"SI": "{}*1", "M3/HR": "{}*1", "CFM": "{}*0.588577779"},
    "WH/M3": {"SI": "{}*1", "WH/M3": "{}*1", "W/CFM": "{}*1.699010796"},
    "WH/KM2": {"SI": "{}*1", "WH/KM2": "{}*1", "BTU/FT2": "{}*0.176110159"},
    "KWH/M2": {"SI": "{}*1", "KWH/M2": "{}*1",  "KBTU/FT2": "{}*0.316998286", "KWH/FT2": "{}*0.092903040"},
    "MJ/M3K": {"SI": "{}*1", "MJ/M3K": "{}*1", "BTU/FT3-F": "{}*14.91066014"},
    "W/M2K": {"SI": "{}*1", "W/M2K": "{}*1", "BTU/HR-FT2-F": "{}*0.176110159", "HR-FT2-F/BTU": "{}**-1*5.678264134"},
    "WH/M3": {"SI": "{}*1", "WH/M3": "{}*1", "W/CFM": "{}*1.699010796"},
    "M2K/W": {"SI": "{}*1", "M2K/W": "{}*1", "HR-FT2-F/BTU": "{}*5.678264134"},
    "W/MK": {"SI": "{}*1", "W/MK": "{}*1", "HR-FT2-F/BTU-IN": "{}**-1*0.144227909", "BTU/HR-FT-F": "{}*0.577789236"},
    "W/K": {"SI": "{}*1", "W/K": "{}*1", "BTU/HR-F": "{}*1.895633976"},
    "W/M2": {"SI": "{}*1", "W/M2": "{}*1", "BTU/HR-FT2": "{}*0.316998286", "W/FT2": "{}*0.09290304"},
    "KW": {"SI": "{}*1", "KW": "{}*1", "BTU/HR": "{}*3412.141156", "KBTU/HR": "{}*3.412141156"},
    "W/W": {"SI": "{}*1", "W/W": "{}*1", "BTUHR/W": "{}*3.412141156"},  # SEER
    # -- IP -> SI
    "F": {"SI": "({}-32)/1.8", "C": "({}-32)/1.8"},
    "DELTA-F": {"SI": "{}*0.555555556", "DELTA-C": "{}*0.555555556", "DELTA-F": "{}*1"},
    "IN": {"SI": "{}*0.0254", "M": "{}*0.0254", "CM": "{}*2.54", "MM": "{}*25.4", "FT": "{}/12", "IN": "{}*1"},
    "FT": {"SI": "{}*0.3048", "M": "{}*0.3048", "CM": "{}*30.48", "MM": "{}*304.8", "FT": "{}*1", "IN": "{}*12"},
    "BTU/HR-FT-F": {"SI": "{}*1.730734908", "W/MK": "{}*1.730734908", "HR-FT2-F/BTU-IN": "1/({}*12)"},
    
    "HR-FT2-F/BTU-IN": {"SI": "{}*1.730734908", "W/MK": "(1/({}*12))*1.730734908", "BTU/HR-FT-F": "1/({}*12)"},
    "HR-FT2-F/BTU": {"SI": "1/((1/{})*5.678264134)", "M2K/W": "1/((1/{})*5.678264134)",  "W/M2K": "(1/{})*5.678264134"},
    
    "W/FT2": {"SI": "{}*10.76391042", "W/M2": "{}*10.76391042", "BTU/HR-FT2": "{}/3.412141156"},
    "BTU/HR-FT2": {"SI": "{}*3.154591186", "W/M2": "{}*3.154591186", "W/FT2": "{}*0.293071111"},
    "BTU/HR-F": {"SI": "{}*0.527528", "W/K": "{}*0.527528"},
    "BTU/HR-FT2-F": {"SI": "{}*5.678264134", "W/M2K": "{}*5.678264134"},
    "KBTU/FT2": {"SI": "{}*3.154591186", "KWH/M2": "{}*3.154591186", "KWH/FT2": "{}*0.293071111"},
    "MPH": {"SI": "{}*0.44704", "M/S": "{}*0.44704", "M/DAY": "{}*0.44704*60*60*24"},
    "FT/S": {"SI": "{}*0.3048", "M/S": "{}*0.3048", "M/DAY": "{}*0.3048*60*60*24"},
    "FT/DAY": {"SI": "{}*0.3048", "M/DAY": "{}*0.3048"},
    "W/CFM": {"SI": "{}*0.588577779", "WH/M3": "{}*0.588577779"},
}


def _standardize_input_unit(_in):
    """Standardize unit nomenclature. ie: 'FT3/M' and 'CFM' both return 'CFM'."""

    codes = {
        'FT': 'FT', "'": 'FT',
        'IN': 'IN', '"': 'IN', "IN.": "IN",
        'MM': 'MM',
        'CM': 'CM',
        'M': 'M',
        'IP': 'IP',
        'FT3': 'FT3',
        'FT2': 'FT2',
        'M3': 'M3',
        'M2': 'M2',
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
        'WH/M3': 'WH/M3', 'W/M3HR': 'WH/M3', 'W/M3H': 'WH/M3',
        'W/M2K': 'W/M2K', 'WM2K': 'W/M2K', 'U-SI': 'W/M2K',
        'W/MK': 'W/MK',
        'W/K': 'W/K',
        'M3/H': 'M3/HR', 'M3H': 'M3/HR', 'CMH': 'M3/HR', 'M3/HR': 'M3/HR',
        'W/W': 'W/W',
        'BTU/WH': 'BTU/WH', 'BTUH/W': 'BTU/WH', 'BTU/W': 'BTU/WH',
        'R/IN': 'R/IN', 'R-IN': 'R/IN', 'HR-FT2-F/BTU-IN': 'HR-FT2-F/BTU-IN',
        'HR-FT2-F/BTU': 'HR-FT2-F/BTU', 'R-IP': 'HR-FT2-F/BTU',
        'BTU/HR-FT-F': 'BTU/HR-FT-F',
        'BTU/HR-F': 'BTU/HR-F', 'BTU/H-F': 'BTU/HR-F', 'BTUH/F': 'BTU/HR-F', 'BTUHR/F': 'BTU/HR-F',
        'BTU/HR-FT2-F': 'BTU/HR-FT2-F', 'BTU/H-FT2-F': 'BTU/HR-FT2-F', 'BTU/HR-SF-F': 'BTU/HR-FT2-F', 'U-IP':'BTU/HR-FT2-F',
        'BTU/HR-FT2': 'BTU/HR-FT2', 'BTU/HR-SF': 'BTU/HR-FT2', 'BTUH/FT2': 'BTU/HR-FT2', 'BTUH/SF': 'BTU/HR-FT2',
        'DELTA-C': 'DELTA-C', 'DELTA-F': 'DELTA-F',
        'KWH/M2': 'KWH/M2',
        'KBTU/FT2': 'KBTU/FT2', 'KBTU/SF': 'KBTU/FT2',
        'M2K/W': 'M2K/W', 'R-SI': 'M2K/W',
        'M/S': 'M/S', 'METER/SEC': 'M/S', 'METER/SECOND': 'M/S', 'M/DAY': 'M/DAY',
        'FT/S': 'FT/S', 'FT/DAY': 'FT/DAY',
        'MPH': 'MPH',
        'W/CFM': 'W/CFM',
        'W/M2': 'W/M2',
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
    # type: (Optional[Union[float, int, str]], Optional[str], str) -> Optional[Union[int, float]]
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
    if not _input_unit:
        _input_unit = copy(_target_unit)
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
    
    return eval("{}".format(conversion_equation).format(float(_value)))


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
    # -- Exclude the '.' and '-' characters from the find so that float and
    # -- negative values don't cause an error.
    # --
    # -- https://regex101.com/

    input_string = str(_input_string).strip().upper()
    rx = re.compile(r"[^\d.-]", re.IGNORECASE)
    match = rx.search(input_string)

    if not match:
        # -- No alpha part
        return (input_string, None)

    found_span = match.span()
    alpha_part = _input_string[found_span[0]:].strip()
    numeric_part = _input_string[:found_span[0]].strip()

    return numeric_part, alpha_part
