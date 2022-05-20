# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for the Ventilation worksheet various input items."""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from PHX.to_PHPP import xl_data
from PHX.to_PHPP.xl_data import xl_writable
from PHX.to_PHPP.phpp_localization import shape_model


@dataclass
class VerificationInput:
    """Ventilation Worksheet input data item."""

    shape: shape_model.Verification
    input_type: str
    input_data: xl_writable

    @classmethod
    def item(cls, shape: shape_model.Verification, input_type: str, input_data: xl_writable) -> VerificationInput:
        return cls(
            shape,
            input_type,
            input_data
        )

    @classmethod
    def enum(cls, shape: shape_model.Verification, input_type: str, input_enum_value: Enum) -> VerificationInput:
        shape_data = getattr(shape, input_type).options
        return cls(
            shape,
            input_type,
            shape_data[str(input_enum_value.value)]
        )

    def create_xl_item(self, _sheet_name: str, _row_num: int) -> xl_data.XlItem:
        """Returns a list of the XL Items to write for this Data item

        Arguments:
        ----------
            * _sheet_name: (str) The name of the worksheet to write to.
            * _row_num: (int) The row number to build the XlItems for

        Returns:
        --------
            * (XlItem): The XlItem to write to the sheet.
        """
        return xl_data.XlItem(
            sheet_name=_sheet_name,
            xl_range=f'{getattr(self.shape, self.input_type).input_column}{_row_num}',
            write_value=self.input_data
        )
