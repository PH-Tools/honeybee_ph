# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Climate worksheet."""

from __future__ import annotations
from typing import List

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_model import climate_entry


class Climate:
    """The PHPP Climate Worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use.
        * sheet_name (str): The localized name of the worksheet
    """

    def __init__(self, _xl: xl_app.XLConnection, sheet_name: str):
        self.xl = _xl
        self.sheet_name = sheet_name
        self.weather_data_start_rows: List[int] = []

    def get_start_rows(self) -> List[int]:
        # TODO: make this find the right starting rows.
        return [61]

    def write_climate_block(self, _climate_entry: climate_entry.ClimateDataBlock) -> None:
        if not self.weather_data_start_rows:
            self.weather_data_start_rows = self.get_start_rows()

        # Just use the first one for now....
        # TODO: Write all variants to different slots
        start_row = self.weather_data_start_rows[0]

        for item in _climate_entry.create_xl_items(self.sheet_name, start_row):
            self.xl.write_xl_item(item)

    def write_active_climate(self, _active_climate: climate_entry.ClimateSettings) -> None:
        start_row = 9
        for item in _active_climate.create_xl_items(self.sheet_name, start_row):
            self.xl.write_xl_item(item)
