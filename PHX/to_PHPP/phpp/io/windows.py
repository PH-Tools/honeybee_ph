# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Windows worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP.phpp import xl_app
from PHX.to_PHPP.phpp.model import windows_rows


class Windows:
    sheet_name = "Windows"
    header_row: Optional[int] = None
    first_entry_row: Optional[int] = None

    def __init__(self, _xl: xl_app.XLConnection):
        self.xl = _xl

    def find_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'L', 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Windows' == val:
                return i
        else:
            raise Exception(
                "Error: Cannot find the 'Windows' header on the 'Windows' sheet, column L?")

    def find_first_entry_row(self) -> int:
        if not self.header_row:
            self.header_row = self.find_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, 'L', self.header_row, self.header_row+50,
        )

        for i, val in enumerate(xl_data, start=self.header_row):
            if 'Quan' in str(val):
                return i + 2
        else:
            raise Exception(
                "Error: Cannot find the 'Quantity' marker on the 'Windows' sheet, column L?")

    def find_section_shape(self) -> None:
        self.header_row = self.find_header_row()
        self.first_entry_row = self.find_first_entry_row()

    def write_windows(self, _window_rows: List[windows_rows.WindowRow]) -> None:
        if not self.first_entry_row:
            self.first_entry_row = self.find_first_entry_row()

        for i, window_row in enumerate(_window_rows, start=self.first_entry_row):
            for item in window_row.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)
