# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP "Additional Vent" worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.xl_data import col_offset, xl_writable
from PHX.to_PHPP.phpp_model import vent_space, vent_units, vent_ducts
from PHX.to_PHPP.phpp_localization import shape_model


class Spaces:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.AddnlVent):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, _row_start: int = 1, _row_end: int = 100) -> int:
        """Return the row number of the 'Rooms' section header."""

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.rooms.locator_col_header,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data):
            if self.shape.rooms.locator_string_header in str(val):
                return i

        raise Exception(
            f'\nError: Not able to find the "Rooms" input section of '
            f'the "{self.shape.name}" worksheet? Please be sure the section '
            f'begins with the "{self.shape.rooms.locator_string_header}" '
            f'flag in column "{self.shape.rooms.locator_col_header}"?'
        )

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Rooms' section."""

        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.rooms.locator_col_entry,
            _row_start=self.section_header_row,
            _row_end=self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            try:
                val = str(int(val))  # Value comes in as  "1.0" from Excel?
            except:
                continue

            if val == self.shape.rooms.locator_string_entry:
                return i

        raise Exception(
            f'\n\tError: Not able to find the first room entry row in the'
            f'"Rooms" section of the "{self.shape.name}" worksheet?'
        )

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class VentUnits:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.AddnlVent):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, _row_start: int = 50, _row_end: int = 200) -> int:
        """Return the row number of the 'Units' section header."""

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.units.locator_col_header,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data, start=_row_start):
            if self.shape.units.locator_string_header in str(val):
                return i

        raise Exception(
            f'\nError: Not able to find the "Ventilation-Units" input section '
            f'of the "{self.shape.name}" worksheet? Please be sure the section '
            f'begins with the "{self.shape.units.locator_string_header}" '
            f'flag in column "{self.shape.units.locator_col_header}?" '
        )

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Rooms' section."""

        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.units.locator_col_entry,
            _row_start=self.section_header_row,
            _row_end=self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            try:
                val = str(int(val))  # Value comes in as  "1.0" from Excel?
            except:
                continue

            if val == self.shape.units.locator_string_entry:
                return i

        raise Exception(
            f'\nError: Not able to find the first vent-unit entry row on the '
            f'"{self.shape.name}" worksheet?'
        )

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_vent_unit_num_by_phpp_id(self, _phpp_id: str) -> xl_writable:
        """Return the phpp-number of the Ventilation unit from the Additional Ventilation worksheet.

        Arguments:
        ---------
            * _phpp_id: (str): The phpp style id name (ie: "01ud-MyVentUnit") of 
                the ventilation unit to find.

        Returns:
        --------
            * (xl_writable): The value from the PHPP indicating the number of
                the Ventilation unit.
        """

        if not self.section_first_entry_row:
            self.section_first_entry_row = self.find_section_first_entry_row()

        search_column = self.shape.units.input_columns.unit_selected

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=search_column,
            _row_start=self.section_first_entry_row,
            _row_end=self.section_first_entry_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_first_entry_row):
            if val == _phpp_id:
                num_col = col_offset(search_column, -3)
                return self.xl.get_data(self.shape.name, f"{num_col}{i}")

        raise Exception(
            f"Error: Cannot locate the Ventilation Unit: {_phpp_id} in"
            " the Additional Ventilation worksheet Units section?"
        )


class VentDucts:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.AddnlVent):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, _row_start: int = 100, _row_end: int = 300) -> int:
        """Return the row number of the 'Rooms' section header."""
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.ducts.locator_col_header,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data, start=_row_start):
            if self.shape.ducts.locator_string_header in str(val):
                return i

        raise Exception(
            f'\n\tError: Not able to find the "Vent-Ducts" input section'
            f'of the "{self.shape.name}" worksheet? Please be sure the section'
            f'begins with the "{self.shape.ducts.locator_string_header}" '
            f'flag in column {self.shape.ducts.locator_col_header}?'
        )

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Rooms' section."""
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        # -- There is no 'flag' or number or any other indication of the entry row?
        # -- So use the hard-coded offset of 9. I'm sure this will cause a problem someday...
        return self.section_header_row + 9

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class AddnlVent:
    """IO Controller for the PHPP Additional Vent worksheet."""

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.AddnlVent):
        self.xl = _xl
        self.shape = _shape
        self.spaces = Spaces(self.xl, self.shape)
        self.vent_units = VentUnits(self.xl, self.shape)
        self.vent_ducts = VentDucts(self.xl, self.shape)

    def write_spaces(self, _spaces: List[vent_space.VentSpaceRow]) -> None:
        if not self.spaces.section_first_entry_row:
            self.spaces.section_first_entry_row = self.spaces.find_section_first_entry_row()

        for i, space in enumerate(_spaces, start=self.spaces.section_first_entry_row):
            for item in space.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_vent_units(self, _vent_units: List[vent_units.VentUnitRow]) -> None:
        if not self.vent_units.section_first_entry_row:
            self.vent_units.section_first_entry_row = self.vent_units.find_section_first_entry_row()

        for i, vent_unit in enumerate(_vent_units, start=self.vent_units.section_first_entry_row):
            for item in vent_unit.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_vent_ducts(self, _vent_ducts: List) -> None:
        if not self.vent_ducts.section_first_entry_row:
            self.vent_ducts.section_first_entry_row = self.vent_ducts.find_section_first_entry_row()

        for i, vent_duct in enumerate(_vent_ducts, start=self.vent_ducts.section_first_entry_row):
            for item in vent_duct.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)
