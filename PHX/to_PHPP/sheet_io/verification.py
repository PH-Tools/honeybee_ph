# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Climate worksheet."""

from __future__ import annotations

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_localization import shape_model
from PHX.to_PHPP.phpp_model import verification_data


class VerificationInputLocation:
    """Generic input item for Verification worksheet items."""

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str, _search_col: str, _search_item: str, _input_row_offset: int):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.search_col = _search_col
        self.search_item = _search_item
        self.input_row_offset = _input_row_offset

    def find_input_row(self, _row_start: int = 1, _row_end: int = 200) -> int:
        """Return the row number where the search-item is found input."""
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.sheet_name,
            _col=self.search_col,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data, start=_row_start):
            if self.search_item in str(val):
                return i + self.input_row_offset

        raise Exception(
            f'\n\tError: Not able to find the "{self.search_item}" input '
            f'section of the "{self.sheet_name}" worksheet? Please be sure '
            f'the item is note with the "{self.search_item}" flag in column {self.search_col}?'
        )


class Verification:
    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Verification):
        self.xl = _xl
        self.shape = _shape

    def _create_input_location_object(self, _phpp_model_obj: verification_data.VerificationInput) -> VerificationInputLocation:
        """Create and setup the VerificationInputLocation object with the correct data."""
        phpp_obj_shape: shape_model.VerificationInputItem = getattr(
            self.shape, _phpp_model_obj.input_type)
        return VerificationInputLocation(
            _xl=self.xl,
            _sheet_name=self.shape.name,
            _search_col=phpp_obj_shape.locator_col,
            _search_item=phpp_obj_shape.locator_string,
            _input_row_offset=phpp_obj_shape.input_row_offset
        )

    def write_item(self, _phpp_model_obj: verification_data.VerificationInput) -> None:
        """Write the VerificationInputItem item out to the PHPP Verification Worksheet."""
        input_object = self._create_input_location_object(_phpp_model_obj)
        input_row = input_object.find_input_row()
        xl_item = _phpp_model_obj.create_xl_item(self.shape.name, input_row)
        self.xl.write_xl_item(xl_item)
