# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP U-Values worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.xl_data import col_offset
from PHX.to_PHPP.phpp_model import uvalues_constructor
from PHX.to_PHPP.phpp_localization import shape_model


class UValues:
    """IO Controller for the PHPP U-Values worksheet."""

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.UValues):
        self.xl = _xl
        self.shape = _shape
        self.constructor_start_rows: List[int] = []

    def get_start_rows(self, _row_start: int = 1, _row_end: int = 500) -> List[int]:
        """Reads through the U-Values worksheet and finds each of the constructor 'start' (title) rows.

        Arguments:
        ----------
            * _row_start: (int) default=1
            * _row_end: (int) default=500

        Returns:
        -------
            * (List[int]): A list of all of the starting title row numbers found.
        """

        # -- Get the data from Excel in one operation
        col_data = self.xl.get_multiple_column_data(
            _sheet_name=self.shape.name,
            _col_start=self.shape.constructor.locator_col_header,
            _col_end=col_offset(self.shape.constructor.locator_col_header, 1),
            _row_start=_row_start,
            _row_end=_row_end
        )

        # -- Find the starting row numbers
        constructors: List[int] = []
        for i, column_val in enumerate(col_data):
            if column_val[0] == self.shape.constructor.locator_string_header:
                constructors.append(i)

        return constructors

    def get_constructor_phpp_id_by_name(self, _name, _row_start: int = 1, _row_end: int = 500) -> Optional[str]:
        """Returns the full PHPP-style value for the constructor with a specified name.

        ie: "Exterior Wall" in constructor 1 will return "01ud-Exterior Wall"

        Argument:
        ---------
            * _name: (str) The name to search for.
            * _row_start: (int) default=1
            * _row_end: (int) default=500

        Returns:
        --------
            * (Optional[str]): The full PHPP-style id for the construction. ie: "01ud-MyConstruction"
        """

        row = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.shape.name,
            row_start=_row_start,
            row_end=_row_end,
            col=self.shape.constructor.input_columns.display_name,
            find=_name
        )

        if not row:
            return

        prefix = self.xl.get_data(
            self.shape.name,
            f'{col_offset(self.shape.constructor.input_columns.display_name, -1)}{row}'
        )

        return f'{prefix}-{_name}'

    def write_construction_blocks(self, _const_blocks: List[uvalues_constructor.ConstructorBlock]) -> None:
        if not self.constructor_start_rows:
            self.constructor_start_rows = self.get_start_rows()

        for construction, start_row in zip(_const_blocks, self.constructor_start_rows):
            for item in construction.create_xl_items(self.shape.name, start_row):
                self.xl.write_xl_item(item)
