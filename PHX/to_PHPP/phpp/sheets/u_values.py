# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP U-Values worksheet."""

from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass, field

from PHX.to_PHPP.phpp import xl_app
from PHX.model import constructions


@dataclass
class UValueConstructor:
    """A single U-Value 'Constructor' block of the U-Values worksheet."""

    start_row: int
    title_range: str
    title_value: Optional[str]

    """
    NOTE: I don't love that 'title_value' is maintaining state outside the XL
    document. But constantly reading the XL each time is really slow. So for performance: 
    keeping track of which constructors are used, and their names is being done here. 
    Will probably come back to bite us at some point....
    """

    def write_data_to_sheet(self,
                            _xl: xl_app.XLConnection,
                            _sheet_name: str,
                            _phx_const: constructions.PhxConstructionOpaque) -> None:
        """Add the PhxConstructionWindow attributes to the Components worksheet.

        Arguments:
        ----------
            * _xl: (xl_app.XLConection) The XL connection to use.
            * _sheet_name: (str) The name of the worksheet to write to.
            * _phx_const: (construction.PhxConstructionOpaque) The PHX-Construction
                to add to the PHPP library.
        """

        _xl.write_data(
            _sheet_name, f'M{self.start_row}', _phx_const.display_name)

        # -- default surface films for now.
        _xl.write_data(_sheet_name, f'M{self.start_row+2}', 0.0)
        _xl.write_data(_sheet_name, f'M{self.start_row+3}', 0.0)

        # -- build the body of the construction
        for i, layer in enumerate(_phx_const.layers):
            _xl.write_data(
                _sheet_name, f'L{self.start_row+6+i}', layer.material.display_name)
            _xl.write_data(
                _sheet_name, f'M{self.start_row+6+i}', layer.material.conductivity)
            _xl.write_data(
                _sheet_name, f'S{self.start_row+6+i}', layer.thickness*1000)

    def clear(self, _xl: xl_app.XLConnection, _sheet_name: str) -> None:
        """Clear all the values from the excel worksheet's row

        Arguments:
        ----------
            * _xl: (xl_app.XLConnection) The Excel connection to use.
            * _sheet_name: (str) The name of the worksheet to clear the values on.
        """
        _xl.clear_data(_sheet_name, f'M{self.start_row}')
        _xl.clear_data(_sheet_name, f'S{self.start_row}')
        _xl.clear_data(_sheet_name, f'M{self.start_row+2}')
        _xl.clear_data(_sheet_name, f'M{self.start_row+3}')
        _xl.clear_data(_sheet_name, f'O{self.start_row+15}')
        _xl.clear_data(_sheet_name, f'Q{self.start_row+15}')
        _xl.clear_data(_sheet_name, f'M{self.start_row+17}')

        for i in range(8):
            _xl.clear_data(
                _sheet_name, f'L{self.start_row+6+i}:S{self.start_row+6+i}')


@dataclass
class UValuesShape:
    constructors: List[UValueConstructor] = field(default_factory=list)


class UValues:
    """The PHPP U-Values worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use.
    """

    sheet_name = 'U-Values'

    def __init__(self, _xl):
        self.xl: xl_app.XLConnection = _xl
        self.shape = UValuesShape()

    def get_worksheet_shape(self) -> None:
        """Find and save the relevant worksheet shape reference points (row/columns)."""
        self.shape.constructors = self.get_constructor_title_rows()

    def get_constructor_title_rows(self,
                                   _search_row_start: int = 1,
                                   _search_row_end: int = 500,
                                   _search_key: str = 'Assembly no.',
                                   _search_column: str = "L"
                                   ) -> List[UValueConstructor]:
        """Reads through the U-Values worksheet and finds each of the constructor 'start' (title) rows.

        Arguments:
        ----------
            * _search_row_start: (int) default=1
            * _search_row_end: (int) default=500
            * _search_key: (str) default="Assembly no." The string value to search for
                which indicates the start of a new U-Value constructor.
            * _search_column: (str) default="L" The column to search for the key.

        Returns:
        -------
            * (List[UValueConstructor]) A list of all of the starting title rows found.
        """

        # -- Get the data from Excel in one operation
        col_1 = _search_column
        col_2 = chr(ord(col_1) + 1)
        col_data = self.xl.get_multiple_column_data(
            _sheet_name=self.sheet_name,
            _col_start=col_1,
            _col_end=col_2,
            _row_start=_search_row_start,
            _row_end=_search_row_end,
        )

        # -- Find the starting rows
        constructors: List[UValueConstructor] = []
        for i, column_val in enumerate(col_data):

            if column_val[0] != _search_key:
                continue

            constructors.append(UValueConstructor(
                int(i+2),
                f"{col_2}{i+2}",
                str(col_data[i+1][1]) if col_data[i+1][1] else None)
            )

        return constructors

    def get_next_empty_constructor(self, _check_shape: bool = False) -> UValueConstructor:
        """Finds the first 'empty' U-Value constructor in the U-Values worksheet.
            Looks at the 'Title' to tell if a constructor is empty or not.

        Arguments:
        ----------
            * _check_shape: (bool) default=False. Set true to re-check the worksheet shape
                before reading. This is done if there is a risk that rows have been added or
                deleted since the last time the shape was checked but will slow down the process.

        Returns:
        --------
            * (int): The first blank UValueConstructor found in the sheet.
        """
        if _check_shape or not self.shape.constructors:
            self.get_worksheet_shape()

        for constructor in self.shape.constructors:
            if self.xl.get_data(self.sheet_name, constructor.title_range) is None:
                return constructor

        raise Exception(
            'Error: Can not find an empty constructor in the {self.sheet_name} sheet?')

    def clear_sheet(self) -> None:
        if not self.shape.constructors:
            self.get_worksheet_shape()

        for constructor in self.shape.constructors:
            constructor.clear(self.xl, self.sheet_name)

    def write_phx_construction_to_sheet(self, _phx_const: constructions.PhxConstructionOpaque) -> None:
        """Adds a PhxConstructionOpaque to the U-Values worksheet. 

        If a construction with the same name already exists in the U-Values worksheet 
        then it will get overwritten with new values. But if no existing construction 
        exists with the same name, a new entry will get added to the U-Values worksheet.

        Arguments:
        ----------
            * _phx_const (constructions.PhxConstructionOpaque): The PhxConstructionOpaque 
                object to add to the worksheet.
        """
        if not self.shape.constructors:
            self.get_worksheet_shape()

        for exg_constructor in self.shape.constructors:
            if exg_constructor.title_value == _phx_const.display_name:
                constructor = exg_constructor
                break
        else:
            constructor = self.get_next_empty_constructor()

        constructor.clear(self.xl, self.sheet_name)
        constructor.write_data_to_sheet(self.xl, self.sheet_name, _phx_const)
        constructor.title_value = _phx_const.display_name
