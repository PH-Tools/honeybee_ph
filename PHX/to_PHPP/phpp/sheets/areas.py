# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Components worksheet."""

from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class AreasShape:
    ...


class Areas:
    """The PHPP Areas worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use 
    """

    sheet_name = 'Areas'

    def __init__(self, _xl):
        self.xl = _xl
        self.shape = AreasShape()
