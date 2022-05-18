# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Components worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.xl_data import col_offset
from PHX.to_PHPP.phpp_model import component_frame, component_glazing, component_vent
from PHX.to_PHPP.phpp_localization import shape_model


class Glazings:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Components):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.glazings.locator_col_header,
            _row_start=1,
            _row_end=100
        )

        for i,  val in enumerate(xl_data):
            if self.shape.glazings.locator_string_header == val:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.glazings.locator_string_header}'"
            f"header on the '{self.shape.name}' sheet, column {self.shape.glazings.locator_col_header}?")

    def find_section_first_entry_row(self) -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.glazings.locator_col_entry,
            _row_start=self.section_header_row,
            _row_end=self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == self.shape.glazings.locator_string_entry:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.glazings.locator_string_entry}' "
            f" entry start on the '{self.shape.name}' sheet, column {self.shape.glazings.locator_col_entry}?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_glazing_phpp_id_by_name(self, _name: str) -> Optional[str]:
        row = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.shape.name,
            row_start=1,
            row_end=500,
            col=self.shape.glazings.input_columns.description,
            find=_name)

        if not row:
            return

        prefix = self.xl.get_data(
            self.shape.name,
            f'{col_offset(self.shape.glazings.input_columns.description, -1)}{row}'
        )
        return f'{prefix}-{_name}'


class Frames:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Components):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.frames.locator_col_header,
            _row_start=1,
            _row_end=100
        )

        for i,  val in enumerate(xl_data):
            if self.shape.frames.locator_string_header == val:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.frames.locator_string_header}' "
            f"header on the '{self.shape.name}' sheet, column {self.shape.frames.locator_col_header}?")

    def find_section_first_entry_row(self) -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.frames.locator_col_entry,
            _row_start=self.section_header_row,
            _row_end=self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == self.shape.frames.locator_string_entry:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.frames.locator_string_entry}'"
            f"entry start on the 'Components' sheet, column {self.shape.frames.locator_col_entry}?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_frame_phpp_id_by_name(self, _name: str) -> str:
        row = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.shape.name,
            row_start=1,
            row_end=500,
            col=self.shape.frames.input_columns.description,
            find=_name
        )

        if not row:
            msg = f'Error: Cannot find a Frame component named: "{_name}" in'\
                  f'column {self.shape.frames.input_columns.description}?'
            raise Exception(msg)

        prefix = self.xl.get_data(
            self.shape.name,
            f'{col_offset(self.shape.frames.input_columns.description, -1)}{row}'
        )

        return f'{prefix}-{_name}'


class Ventilators:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Components):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.ventilators.locator_col_header,
            _row_start=1,
            _row_end=100
        )

        for i,  val in enumerate(xl_data):
            if self.shape.ventilators.locator_string_header == val:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.ventilators.locator_string_header}' header on the "
            f"'{self.shape.name}' sheet, column {self.shape.ventilators.locator_col_header}?"
        )

    def find_section_first_entry_row(self) -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.ventilators.locator_col_entry,
            _row_start=self.section_header_row,
            _row_end=self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == self.shape.ventilators.locator_string_entry:
                return i

        raise Exception(
            f"Error: Cannot find the '{self.shape.ventilators.locator_string_entry}' entry start on "
            f"the '{self.shape.name}' sheet, column {self.shape.ventilators.locator_col_entry}?")

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_ventilator_phpp_id_by_name(self, _name: str) -> str:
        row = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.shape.name,
            row_start=1,
            row_end=500,
            col=self.shape.ventilators.input_columns.display_name,
            find=_name
        )

        if not row:
            msg = f'Error: Cannot find a Ventilator component named: "{_name}"]'\
                f'in column {self.shape.ventilators.input_columns.display_name}?'
            raise Exception(msg)

        prefix = self.xl.get_data(
            self.shape.name,
            f'{col_offset(self.shape.ventilators.input_columns.display_name, -1)}{row}'
        )
        return f'{prefix}-{_name}'


class Components:
    """IO Controller for PHPP "Components" worksheet."""

    def __init__(self, _xl: xl_app.XLConnection, shape: shape_model.Components):
        self.xl = _xl
        self.shape = shape
        self.glazings = Glazings(self.xl, self.shape)
        self.frames = Frames(self.xl, self.shape)
        self.ventilators = Ventilators(self.xl, self.shape)

    def write_glazings(self, _glazing_rows: List[component_glazing.GlazingRow]) -> None:
        if not self.glazings.section_first_entry_row:
            self.glazings.section_first_entry_row = self.glazings.find_section_first_entry_row()

        for i, glazing_row in enumerate(_glazing_rows, start=self.glazings.section_first_entry_row):
            for item in glazing_row.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_frames(self, _frame_row: List[component_frame.FrameRow]) -> None:
        if not self.frames.section_first_entry_row:
            self.frames.section_first_entry_row = self.frames.find_section_first_entry_row()

        for i, frame_row in enumerate(_frame_row, start=self.frames.section_first_entry_row):
            for item in frame_row.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_ventilators(self, _ventilator_row: List[component_vent.VentilatorRow]) -> None:
        if not self.ventilators.section_first_entry_row:
            self.ventilators.section_first_entry_row = self.ventilators.find_section_first_entry_row()

        for i, ventilator_row in enumerate(_ventilator_row, start=self.ventilators.section_first_entry_row):
            for item in ventilator_row.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)
