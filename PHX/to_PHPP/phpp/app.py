# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the XL-Connection and read/write operations."""

import xlwings as xw
from pathlib import Path
from typing import Optional, Union, List
from contextlib import contextmanager

from PHX.to_PHPP.phpp.sheets import areas, u_values

xl_writable = Union[str, float, int, list, tuple]  # TypeAlias in 3.10


class ReadRowsError(Exception):
    def __init__(self, row_start, row_end):
        self.msg = f'Error: row_start should be less than row_end. Got {row_start}, {row_end}'
        super().__init__(self.msg)


class NoActiveExcelRunningError(Exception):
    def __init__(self):
        self.msg = '\n\tError: No active instance of Excel running? Please open a valid PHPP file and try again.'
        super().__init__(self.msg)


class Connection:
    """Facade class for Excel Interop"""

    def __init__(self, _phpp_file: Optional[Path] = None):
        self.phpp_file = _phpp_file

        # Setup all the individual worksheet Classes
        self.areas = areas.Areas(self)
        self.u_values = u_values.U_Values(self)

        assert self.xl_connection_is_open() == True

    @property
    def wb(self) -> xw.main.Book:
        try:
            return xw.books.active
        except:
            raise NoActiveExcelRunningError

    @property
    def phpp_file(self) -> Optional[Path]:
        return self._phpp_file

    @phpp_file.setter
    def phpp_file(self, _in: Optional[Path]) -> None:
        if _in:
            raise NotImplementedError
        else:
            self._phpp_file = _in

    @contextmanager
    def silent(self):
        """Context Manager which turns off screen-refresh and auto-calc in the
            Excel App in order to help speed up read/write. Turns back on screen-refresh
            and auto-calc in the Excel App when done or on any error.
        """
        try:
            self.wb.app.screen_updating = False
            self.wb.app.display_alerts = False
            self.wb.app.calculation = 'manual'
            yield
        finally:
            self.wb.app.screen_updating = True
            self.wb.app.display_alerts = True
            self.wb.app.calculation = 'automatic'
            self.wb.app.calculate()

    def xl_connection_is_open(self) -> bool:
        if self.wb == None:
            return False
        return True

    def find_item_row(self, sheet_name: str, row_start: int, row_end: int, col: str, find: str) -> Optional[int]:
        """ Traverses a column in the Excel sheet row-by-row looking for the specifed cell value

        Arguments:
        ----------
            * sheet_name: (str) The name of the sheet to be looking in
            * row_start: (int) The row number to begin looking from
            * row_end: (int) The row number to stop looking on
            * col: (str) The column to look in
            * find: (Optional[str]) The string to search for (or 'None' for blank cell)

        Returns:
        --------
            * Optional[int]: The row number where the first instance of the specified 
                item is found or None if no instances are found.
        """

        if row_start < row_end:
            raise ReadRowsError(row_start, row_end)

        row: int = row_start
        sh: xw.main.Sheet = self.get_sheet_by_name(sheet_name)

        while row <= row_end:
            if sh.range(f'{col}{row}').value != find:
                row += 1
            else:
                return row
        return None

    def get_sheet_by_name(self, _sheet_name: str) -> xw.main.Sheet:
        return self.wb.sheets[_sheet_name]

    def write(self, _sheet_name: str, _range: str, _val: xl_writable) -> None:
        """Writes a value to a specific cell range in the excel sheet 

        Arguments:
        ---------
            * _sheet_name: (str) The name of the sheet to write to
            * _range: (str) The cell range to write to (ie: "A1") or a set of ranges (ie: "A1:B4")
            * _val: (xl_writable) The cell value(s) to write. Accepts single value or list
         """

        # '_val is not None' verbosely cus' otherwise won't write zeros
        if _val is not None and _sheet_name and _range:
            self.get_sheet_by_name(_sheet_name).range(_range).value = _val

    def clear(self, _sheet_name: str, _range: str) -> None:
        """Sets the specified excel sheet's range to 'None'

        Arguments:
        ---------
            * _sheet_name: (str) The name of the sheet to write to
            * _range: (str) The cell range to write to (ie: "A1") or a set of ranges (ie: "A1:B4")
         """

        if _sheet_name and _range:
            self.get_sheet_by_name(_sheet_name).range(_range).value = None

    def read_columns(self,
                     _sheet_name: str,
                     _col_start: int,
                     _col_end: Optional[int] = None,
                     _row_start: int = 1,
                     _row_end: int = 100,
                     _ndim: Optional[int] = None
                     ) -> List:
        """Return a list with the values read from a specified block of the xl document.

        Arguments:
        ----------
            _sheet_name: (str) The Worksheet to read from
            _col: (str) The Column letter to read from
            _row_start: (int) default=1
            _row_end: (int) default=100
            _ndim: (Optional[int]) default=None. Number of dimensions. Optional parameter 
                to pass to the xl range.
        Returns:
        --------
            (list): data from Excel worksheet as a list
        """

        if not _col_end:
            _col_end = _col_start

        if _sheet_name and _col_start:
            range = f'{_col_start}{_row_start}:{_col_end}{_row_end}'
            if _ndim:
                return self.get_sheet_by_name(_sheet_name).range(range).options(ndim=_ndim).value
            else:
                return self.get_sheet_by_name(_sheet_name).range(range).value
        else:
            return []
