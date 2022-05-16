# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Components worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.xl_data import col_offset
from PHX.to_PHPP.phpp_model import component_frame, component_glazing, component_vent


class Glazings:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, search_col: str = 'ID') -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, search_col, 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Glazing' == val:
                return i
        else:
            raise Exception(
                f"Error: Cannot find the 'Glazing' header on the 'Components' sheet, column {search_col}?")

    def find_section_first_entry_row(self, search_col: str = 'ID') -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, search_col, self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == '01ud':
                return i
        else:
            raise Exception(
                f"Error: Cannot find the 'Glazing' entry start on the 'Components' sheet, column {search_col}?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_glazing_phpp_id_by_name(self, _name: str, search_col: str = 'IE') -> Optional[str]:
        row = self.xl.get_row_num_of_value_in_column(
            self.sheet_name, 1, 500, search_col, _name)
        if not row:
            return
        prefix = self.xl.get_data(self.sheet_name, f'{col_offset(search_col, -1)}{row}')
        return f'{prefix}-{_name}'


class Frames:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, search_col: str = 'IK') -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, search_col, 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Window frames' == val:
                return i
        else:
            raise Exception(
                f"Error: Cannot find the 'Window frames' header on the 'Components' sheet, column {search_col}?")

    def find_section_first_entry_row(self, search_col: str = 'IK') -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, search_col, self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == '01ud':
                return i
        else:
            raise Exception(
                f"Error: Cannot find the 'Window frames' entry start on the 'Components' sheet, column {search_col}?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_frame_phpp_id_by_name(self, _name: str, search_col: str = 'IL') -> str:
        row = self.xl.get_row_num_of_value_in_column(
            self.sheet_name, 1, 500, search_col, _name)
        if not row:
            msg = f'Error: Cannot find a Frame component named: "{_name}" in column {search_col}?'
            raise Exception(msg)
        prefix = self.xl.get_data(self.sheet_name, f'{col_offset(search_col, -1)}{row}')
        return f'{prefix}-{_name}'


class Ventilators:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, search_col: str = 'JG') -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, search_col, 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Ventilation units with heat recovery' == val:
                return i
        else:
            raise Exception(
                f"Error: Cannot find the 'Ventilation units...' header on the "
                f"'Components' sheet, column {search_col}?"
            )

    def find_section_first_entry_row(self, search_col: str = 'JG') -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, search_col, self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == '01ud':
                return i
        else:
            raise Exception(
                f"Error: Cannot find the 'Ventilation units...' entry start on "
                f"the 'Components' sheet, column {search_col}?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_ventilator_phpp_id_by_name(self, _name: str, search_col: str = 'JH') -> str:
        row = self.xl.get_row_num_of_value_in_column(
            self.sheet_name, 1, 500, search_col, _name)
        if not row:
            msg = f'Error: Cannot find a Ventilator component named: "{_name}" in column {search_col}?'
            raise Exception(msg)
        prefix = self.xl.get_data(self.sheet_name, f'{col_offset(search_col, -1)}{row}')
        return f'{prefix}-{_name}'


class Components:
    """The PHPP Components worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use.
        * sheet_name (str):
    """

    def __init__(self, _xl: xl_app.XLConnection, sheet_name: str):
        self.xl = _xl
        self.sheet_name = sheet_name
        self.glazings = Glazings(self.xl, self.sheet_name)
        self.frames = Frames(self.xl, self.sheet_name)
        self.ventilators = Ventilators(self.xl, self.sheet_name)

    def write_glazings(self, _glazing_rows: List[component_glazing.GlazingRow]) -> None:
        if not self.glazings.section_first_entry_row:
            self.glazings.section_first_entry_row = self.glazings.find_section_first_entry_row()

        for i, glazing_row in enumerate(_glazing_rows, start=self.glazings.section_first_entry_row):
            for item in glazing_row.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_frames(self, _frame_row: List[component_frame.FrameRow]) -> None:
        if not self.frames.section_first_entry_row:
            self.frames.section_first_entry_row = self.frames.find_section_first_entry_row()

        for i, frame_row in enumerate(_frame_row, start=self.frames.section_first_entry_row):
            for item in frame_row.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_ventilators(self, _ventilator_row: List[component_vent.VentilatorRow]) -> None:
        if not self.ventilators.section_first_entry_row:
            self.ventilators.section_first_entry_row = self.ventilators.find_section_first_entry_row()

        for i, ventilator_row in enumerate(_ventilator_row, start=self.ventilators.section_first_entry_row):
            for item in ventilator_row.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)
