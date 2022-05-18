# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP "Ventilation" worksheet."""

from __future__ import annotations

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.phpp_localization import shape_model
from PHX.to_PHPP.phpp_model import ventilation_data


class VentilationInputLocation:
    """Generic input item for Ventilation worksheet items."""

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str, _search_col: str, _search_item: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.search_col = _search_col
        self.search_item = _search_item

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

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Ventilation):
        self.xl = _xl
        self.shape = _shape

        self.io_vent_type = VentilationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.input_blocks.vent_type.locator_col,
            self.shape.input_blocks.vent_type.locator_string
        )
        self.io_wind_coeff_e = VentilationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.input_blocks.wind_coeff_e.locator_col,
            self.shape.input_blocks.wind_coeff_e.locator_string
        )
        self.io_wind_coeff_f = VentilationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.input_blocks.wind_coeff_f.locator_col,
            self.shape.input_blocks.wind_coeff_f.locator_string
        )
        self.io_air_change_rate = VentilationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.input_blocks.airtightness_n50.locator_col,
            self.shape.input_blocks.airtightness_n50.locator_string
        )
        self.io_multi_vent_worksheet_on = VentilationInputLocation(
            self.xl,
            self.shape.name,
            self.shape.input_blocks.multi_unit_on.locator_col,
            self.shape.input_blocks.multi_unit_on.locator_string
        )

    def _write_input(self,
                     _input_item: VentilationInputLocation,
                     _phpp_model_item: ventilation_data.VentilationInputItem) -> None:
        """Generic write input function used by specific input items below."""

        input_row = _input_item.find_input_row()
        xl_item = _phpp_model_item.create_xl_item(self.shape.name, input_row)
        self.xl.write_xl_item(xl_item)

    def write_ventilation_type(self, _phpp_model_obj: ventilation_data.VentilationInputItem) -> None:
        self._write_input(self.io_vent_type, _phpp_model_obj)

    def write_wind_coeff_e(self, _phpp_model_obj: ventilation_data.VentilationInputItem) -> None:
        self._write_input(self.io_wind_coeff_e, _phpp_model_obj)

    def write_wind_coeff_f(self, _phpp_model_obj: ventilation_data.VentilationInputItem) -> None:
        self._write_input(self.io_wind_coeff_f, _phpp_model_obj)

    def write_airtightness_n50(self, _phpp_model_obj: ventilation_data.VentilationInputItem) -> None:
        self._write_input(self.io_air_change_rate, _phpp_model_obj)

    def write_airtightness_q50(self, _phpp_model_obj: ventilation_data.VentilationInputItem) -> None:
        self._write_input(self.io_air_change_rate, _phpp_model_obj)

    def write_multi_vent_worksheet_on(self, _phpp_model_obj: ventilation_data.VentilationInputItem) -> None:
        self._write_input(self.io_multi_vent_worksheet_on, _phpp_model_obj)
