# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP "Additional Vent" worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.xl_data import col_offset
from PHX.to_PHPP.phpp_model import vent_space, vent_units, vent_ducts


class Spaces:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        """Return the row number of the 'Rooms' section header."""
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'C', 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Room' in str(val):
                return i
        else:
            msg = f'\n\tError: Not able to find the "Rooms" input section of the "Additional Vent" '\
                'worksheet? Please be sure the section begins with the "Room no." flag in column C?'
            raise Exception(msg)

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Rooms' section."""
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, 'C', self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == 1:
                return i
        else:
            msg = f'\n\tError: Not able to find the first room entry row in the'\
                f'"Rooms" section of the "Additional Vent" worksheet?'
            raise Exception(msg)

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class VentUnits:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        """Return the row number of the 'Rooms' section header."""
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'C', 50, 200,)

        for i,  val in enumerate(xl_data, start=50):
            if 'Venti-' in str(val):
                return i
        else:
            msg = f'\n\tError: Not able to find the "Vent-Units" input section of the "Additional Vent" '\
                'worksheet? Please be sure the section begins with the "Venti-." flag in column C?'
            raise Exception(msg)

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Rooms' section."""
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, 'C', self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == 1:
                return i
        else:
            msg = f'\n\tError: Not able to find the first room entry row in the'\
                '"Vent-Units" section of the "Additional Vent" worksheet?'
            raise Exception(msg)

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_vent_unit_num_by_phpp_id(self, _phpp_id: str, _srch_col: str):
        """Return the Unit number of the Ventilation unit from the Additional Ventilation worksheet."""
        if not self.section_first_entry_row:
            self.section_first_entry_row = self.find_section_first_entry_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name,
            _srch_col,
            self.section_first_entry_row,
            self.section_first_entry_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_first_entry_row):
            if val == _phpp_id:
                num_col = col_offset(_srch_col, -3)
                return self.xl.get_data(self.sheet_name, f"{num_col}{i}")
        else:
            msg = f"Error: Cannot locate the Ventilaton Unit: {_phpp_id} on"\
                "the Additional Ventilation worksheet?"
            raise Exception(msg)


class VentDucts:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        """Return the row number of the 'Rooms' section header."""
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'E', 50, 200,)

        for i,  val in enumerate(xl_data, start=50):
            if 'Round' in str(val):
                return i
        else:
            msg = f'\n\tError: Not able to find the "Vent-Ducts" input section of the "Additional Vent" '\
                'worksheet? Please be sure the section begins with the "Round" flag in column E?'
            raise Exception(msg)

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Rooms' section."""
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        # -- There is not 'flag' or number or any other indication of the entry row
        return self.section_header_row + 9

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class AddnlVent:
    """The PHPP Additional Vent worksheet."""

    def __init__(self, _xl: xl_app.XLConnection, sheet_name: str):
        self.xl = _xl
        self.sheet_name = sheet_name
        self.spaces = Spaces(self.xl, self.sheet_name)
        self.vent_units = VentUnits(self.xl, self.sheet_name)
        self.vent_ducts = VentDucts(self.xl, self.sheet_name)

    def write_spaces(self, _spaces: List[vent_space.VentSpaceRow]) -> None:
        if not self.spaces.section_first_entry_row:
            self.spaces.section_first_entry_row = self.spaces.find_section_first_entry_row()

        for i, space in enumerate(_spaces, start=self.spaces.section_first_entry_row):
            for item in space.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_vent_units(self, _vent_units: List[vent_units.VentUnitRow]) -> None:
        if not self.vent_units.section_first_entry_row:
            self.vent_units.section_first_entry_row = self.vent_units.find_section_first_entry_row()

        for i, vent_unit in enumerate(_vent_units, start=self.vent_units.section_first_entry_row):
            for item in vent_unit.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)

    def write_vent_ducts(self, _vent_ducts: List) -> None:
        if not self.vent_ducts.section_first_entry_row:
            self.vent_ducts.section_first_entry_row = self.vent_ducts.find_section_first_entry_row()

        for i, vent_duct in enumerate(_vent_ducts, start=self.vent_ducts.section_first_entry_row):
            for item in vent_duct.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)
