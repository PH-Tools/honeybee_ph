# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Climate worksheet."""

from __future__ import annotations

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_localization import shape_model
from PHX.to_PHPP.phpp_model import verification_data


class VerificationInputLocation:
    """Generic input item for Verification worksheet items."""

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str, _search_col: str, _search_item: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.search_col = _search_col
        self.search_item = _search_item

    def find_input_row(self, _row_start: int = 1, _row_end: int = 200, _offset: int = 1) -> int:
        """Return the row number where the search-item is found input."""
        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.sheet_name,
            _col=self.search_col,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data, start=_row_start):
            if self.search_item in str(val):
                return i + _offset

        raise Exception(
            f'\n\tError: Not able to find the "{self.search_item}" input '
            f'section of the "{self.sheet_name}" worksheet? Please be sure '
            f'the item is note with the "{self.search_item}" flag in column {self.search_col}?'
        )


class Verification:
    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Verification):
        self.xl = _xl
        self.shape = _shape

        self.io_cert_type = VerificationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.cert_type.locator_col,
            self.shape.cert_type.locator_string
        )
        self.io_cert_class = VerificationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.cert_class.locator_col,
            self.shape.cert_class.locator_string
        )
        self.io_pe_type = VerificationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.pe_type.locator_col,
            self.shape.pe_type.locator_string
        )
        self.io_enerphit_type = VerificationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.enerphit_type.locator_col,
            self.shape.enerphit_type.locator_string
        )
        self.io_retrofit_type = VerificationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.retrofit_type.locator_col,
            self.shape.retrofit_type.locator_string
        )

    def _write_input(self,
                     _input_item: VerificationInputLocation,
                     _phpp_model_item: verification_data.VerificationInputItem,
                     _offset: int = 1) -> None:
        """Generic write input function used by specific input items below."""

        input_row = _input_item.find_input_row(_offset=_offset)
        xl_item = _phpp_model_item.create_xl_item(self.shape.name, input_row)
        self.xl.write_xl_item(xl_item)

    def write_certification_type(self, _phpp_model_obj: verification_data.VerificationInputItem) -> None:
        self._write_input(self.io_cert_type, _phpp_model_obj, _offset=2)

    def write_certification_class(self, _phpp_model_obj: verification_data.VerificationInputItem) -> None:
        self._write_input(self.io_cert_class, _phpp_model_obj, _offset=1)

    def write_pe_type(self, _phpp_model_obj: verification_data.VerificationInputItem) -> None:
        self._write_input(self.io_pe_type, _phpp_model_obj, _offset=1)

    def write_enerphit_type(self, _phpp_model_obj: verification_data.VerificationInputItem) -> None:
        self._write_input(self.io_enerphit_type, _phpp_model_obj, _offset=1)

    def write_retrofit_type(self, _phpp_model_obj: verification_data.VerificationInputItem) -> None:
        self._write_input(self.io_retrofit_type, _phpp_model_obj, _offset=1)
