# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Climate worksheet."""

from __future__ import annotations
from typing import List

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_localization import shape_model


class Verification:
    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Verification):
        self.xl = _xl
        self.shape = _shape
