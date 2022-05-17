# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for the Ventilation worksheet Misc. input."""

from dataclasses import dataclass
from typing import Dict, Any
from functools import partial

from PHX.to_PHPP import xl_data


@dataclass
class VentTypeInput:
    """The Ventilation-Type input"""

    __slots__ = ('columns', 'vent_type',)
    columns: Dict[str, str]
    vent_type: str

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
        create_range = partial(self._create_range, _row_num=_row_num)
        return xl_data.XlItem(_sheet_name, create_range('vent_type'), self.vent_type)


@dataclass
class VentWindCoeffE:
    """The Wind Coefficient "e" input"""

    __slots__ = ('columns', 'wind_coeff_e',)
    columns: Dict[str, str]
    wind_coeff_e: Any

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
        create_range = partial(self._create_range, _row_num=_row_num)
        return xl_data.XlItem(_sheet_name, create_range('wind_coeff_e'), self.wind_coeff_e)


@dataclass
class VentWindCoeffF:
    """The Wind Coefficient "e" input"""

    __slots__ = ('columns', 'wind_coeff_f',)
    columns: Dict[str, str]
    wind_coeff_f: Any

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
        create_range = partial(self._create_range, _row_num=_row_num)
        return xl_data.XlItem(_sheet_name, create_range('wind_coeff_f'), self.wind_coeff_f)


@dataclass
class VentAirChangeRateN50:
    """The Wind Coefficient "e" input"""

    __slots__ = ('columns', 'airtightness_n50',)
    columns: Dict[str, str]
    airtightness_n50: float

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
        create_range = partial(self._create_range, _row_num=_row_num)
        return xl_data.XlItem(_sheet_name, create_range('airtightness_n50'), self.airtightness_n50)


@dataclass
class VentAirChangeRateQ50:
    """The Wind Coefficient "e" input"""

    __slots__ = ('columns', 'airtightness_q50',)
    columns: Dict[str, str]
    airtightness_q50: float

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
        create_range = partial(self._create_range, _row_num=_row_num)
        return xl_data.XlItem(_sheet_name, create_range('airtightness_q50'), self.airtightness_q50)


@dataclass
class VentMultiUnitOn:
    """The MultiUnit worksheet 'on' or 'off'"""

    __slots__ = ('columns', 'multi_unit_on',)
    columns: Dict[str, str]
    multi_unit_on: str

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
        create_range = partial(self._create_range, _row_num=_row_num)
        return xl_data.XlItem(_sheet_name, create_range('multi_unit_on'), self.multi_unit_on)
