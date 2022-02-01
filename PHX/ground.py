# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""PHX Passive House Ground / Foundation Classes"""

from dataclasses import dataclass


@dataclass
class Foundation:
    floor_setting_num: int = 6  # User Defined
    floor_setting_str: str = 'User defined'

    floor_type_num: int = 5
    floor_type_str: str = 'None'
