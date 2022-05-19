# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Windows worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_model import windows_rows
from PHX.to_PHPP.phpp_localization import shape_model


class Windows:
    """IO Controller Class for PHPP "Windows" worksheet."""

    header_row: Optional[int] = None
    first_entry_row: Optional[int] = None

    def __init__(self, _xl: xl_app.XLConnection, shape: shape_model.Windows):
        self.xl = _xl
        self.shape = shape

    def find_header_row(self, _row_start: int = 1, _row_end: int = 100) -> int:
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.window_rows.locator_col_header,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data):
            if self.shape.window_rows.locator_string_header == val:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.window_rows.locator_string_header}' "
            f"header on the '{self.shape.name}' sheet, column {self.shape.window_rows.locator_string_header}?"
        )

    def find_first_entry_row(self) -> int:
        if not self.header_row:
            self.header_row = self.find_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.window_rows.locator_col_entry,
            _row_start=self.header_row,
            _row_end=self.header_row+50
        )

        for i, val in enumerate(xl_data, start=self.header_row):
            if self.shape.window_rows.locator_string_entry in str(val):
                return i + 2

        raise Exception(
            f"Error: Cannot find the '{self.shape.window_rows.locator_string_entry}' "
            f"marker on the '{self.shape.name}' sheet, column {self.shape.window_rows.locator_col_entry}?"
        )

    def find_section_shape(self) -> None:
        self.header_row = self.find_header_row()
        self.first_entry_row = self.find_first_entry_row()

    def write_windows(self, _window_rows: List[windows_rows.WindowRow]) -> None:
        if not self.first_entry_row:
            self.first_entry_row = self.find_first_entry_row()

        for i, window_row in enumerate(_window_rows, start=self.first_entry_row):
            for item in window_row.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)
