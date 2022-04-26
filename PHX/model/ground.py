# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""PHX Foundation Class"""

from dataclasses import dataclass


@dataclass
class PhxFoundation:
    floor_setting_num: int = 6  # User Defined
    floor_setting_str: str = 'User defined'

    floor_type_num: int = 5
    floor_type_str: str = 'None'
