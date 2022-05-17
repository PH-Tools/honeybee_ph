# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP "Ventilation" worksheet."""

from __future__ import annotations
from typing import Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_model import ventilation_inputs


class VentilationInputItem:
    """Generic input item for Ventilation worksheet items."""

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str, _search_col: str, _search_item: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.search_col = _search_col
        self.search_item = _search_item
        self.row: Optional[int] = None

    def find_input_row(self) -> int:
        """Return the row number where the search-item is found input."""
        xl_data = self.xl.get_single_column_data(
            self.sheet_name, self.search_col, 1, 100,)

        for i,  val in enumerate(xl_data, start=1):
            if self.search_item in str(val):
                return i
        else:
            msg = f'\n\tError: Not able to find the "{self.search_item}" input '\
                f'section of the "{self.sheet_name}" worksheet? Please be sure '\
                f'the section begins with the "{self.search_item}" flag in column {self.search_col}?'
            raise Exception(msg)


class Ventilation:
    """The PHPP Ventilation worksheet."""

    def __init__(self, _xl: xl_app.XLConnection, sheet_name: str):
        self.xl = _xl
        self.sheet_name = sheet_name
        self.io_vent_type = VentilationInputItem(
            self.xl, self.sheet_name, "I", "Please select")
        self.io_wind_coeff_e = VentilationInputItem(
            self.xl, self.sheet_name, "I", "Wind protection coefficient, e")
        self.io_wind_coeff_f = VentilationInputItem(
            self.xl, self.sheet_name, "I", "Wind protection coefficient, f")
        self.io_air_change_rate = VentilationInputItem(
            self.xl, self.sheet_name, "I", "Air change rate at press. test")
        self.io_multi_vent_worksheet_on = VentilationInputItem(
            self.xl, self.sheet_name, "I", "Multiple ventilation units, non-res")

    def _write_input(self, _input_item: VentilationInputItem, _phpp_model_item) -> None:
        """Generic write input function used by specific input items below."""
        if not _input_item.row:
            _input_item.row = _input_item.find_input_row()
        xl_item = _phpp_model_item.create_xl_item(self.sheet_name, _input_item.row)
        self.xl.write_xl_item(xl_item)

    def write_ventilation_type(self, _phpp_model_obj: ventilation_inputs.VentTypeInput) -> None:
        self._write_input(self.io_vent_type, _phpp_model_obj)

    def write_wind_coeff_e(self, _phpp_model_obj: ventilation_inputs.VentWindCoeffE) -> None:
        self._write_input(self.io_wind_coeff_e, _phpp_model_obj)

    def write_wind_coeff_f(self, _phpp_model_obj: ventilation_inputs.VentWindCoeffF) -> None:
        self._write_input(self.io_wind_coeff_f, _phpp_model_obj)

    def write_airtightness_n50(self, _phpp_model_obj: ventilation_inputs.VentAirChangeRateN50) -> None:
        self._write_input(self.io_air_change_rate, _phpp_model_obj)

    def write_airtightness_q50(self, _phpp_model_obj: ventilation_inputs.VentAirChangeRateQ50) -> None:
        self._write_input(self.io_air_change_rate, _phpp_model_obj)

    def write_multi_vent_wrksheet_on(self, _phpp_model_obj: ventilation_inputs.VentMultiUnitOn) -> None:
        self._write_input(self.io_multi_vent_worksheet_on, _phpp_model_obj)
