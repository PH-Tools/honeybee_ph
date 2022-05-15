# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP U-Values worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP.phpp import xl_app
from PHX.to_PHPP.phpp.xl_data import col_offset
from PHX.to_PHPP.phpp.model import uvalues_constructor


class UValues:
    """The PHPP U-Values worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use.
        * sheet_name (str): The localized name of the worksheet
    """

    def __init__(self, _xl: xl_app.XLConnection, sheet_name: str):
        self.xl = _xl
        self.sheet_name = sheet_name
        self.constructor_start_rows: List[int] = []

    def get_start_rows(self,
                       _search_row_start: int = 1,
                       _search_row_end: int = 500,
                       _search_key: str = 'Assembly no.',
                       _search_column: str = "L"
                       ) -> List[int]:
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
            * (List[int]) A list of all of the starting title row numbers found.
        """

        # -- Get the data from Excel in one operation
        col_1 = _search_column
        col_2 = col_offset(col_1, 1)
        col_data = self.xl.get_multiple_column_data(
            _sheet_name=self.sheet_name,
            _col_start=col_1,
            _col_end=col_2,
            _row_start=_search_row_start,
            _row_end=_search_row_end,
        )

        # -- Find the starting row numbers
        constructors: List[int] = []
        for i, column_val in enumerate(col_data):
            if column_val[0] == _search_key:
                constructors.append(i)

        return constructors

    def get_constructor_phpp_id_by_name(self, _name) -> Optional[str]:
        """Returns the full PHPP-style value for the constructor with a specified name.

        ie: "Exterior Wall" in constructor 1 will return "01ud-Exterior Wall"

        Argument:
        ---------
            * _name: (str) The name to search for.

        Returns:
        --------
            * (Optional[str]): The full PHPP-style id for the construction. ie: "01ud-MyConstruction"
        """
        search_col = 'M'
        row = self.xl.get_row_num_of_value_in_column(
            self.sheet_name, 1, 500, search_col, _name)
        if not row:
            return
        prefix = self.xl.get_data(self.sheet_name, f'{col_offset(search_col, -1)}{row}')
        return f'{prefix}-{_name}'

    def write_construction_blocks(self, _phx_constructions: List[uvalues_constructor.ConstructorBlock]) -> None:
        if not self.constructor_start_rows:
            self.constructor_start_rows = self.get_start_rows()

        for construction, start_row in zip(_phx_constructions, self.constructor_start_rows):
            for item in construction.create_xl_items(self.sheet_name, start_row):
                self.xl.write_xl_item(item)
