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
class VerificationInputItem:
    """Ventilation Worksheet input item."""

    shape: shape_model.Verification
    input_data: xl_writable
    input_type: str

    def create_xl_item(self, _sheet_name: str, _row_num: int) -> xl_data.XlItem:
        """Returns a list of the XL Items to write for this Surface Entry

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

    @classmethod
    def certification_type(cls, shape: shape_model.Verification, input_data: Enum) -> VerificationInputItem:
        return cls(
            shape=shape,
            input_data=shape.cert_type.options[str(input_data.value)],
            input_type='cert_type'
        )

    @classmethod
    def certification_class(cls, shape: shape_model.Verification, input_data: Enum) -> VerificationInputItem:
        return cls(
            shape=shape,
            input_data=shape.cert_class.options[str(input_data.value)],
            input_type='cert_class'
        )

    @classmethod
    def pe_type(cls, shape: shape_model.Verification, input_data: Enum) -> VerificationInputItem:
        return cls(
            shape=shape,
            input_data=shape.pe_type.options[str(input_data.value)],
            input_type='pe_type'
        )

    @classmethod
    def enerphit_type(cls, shape: shape_model.Verification, input_data: Enum) -> VerificationInputItem:
        return cls(
            shape=shape,
            input_data=shape.enerphit_type.options[str(input_data.value)],
            input_type='enerphit_type'
        )

    @classmethod
    def retrofit_type(cls, shape: shape_model.Verification, input_data: Enum) -> VerificationInputItem:
        return cls(
            shape=shape,
            input_data=shape.retrofit_type.options[str(input_data.value)],
            input_type='retrofit_type'
        )
