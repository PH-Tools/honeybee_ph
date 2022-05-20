# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP "Areas" worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP import xl_app
from PHX.to_PHPP.xl_data import col_offset
from PHX.to_PHPP.phpp_model import areas_surface, areas_data
from PHX.to_PHPP.phpp_localization import shape_model


class AreasInputLocation:
    """Generic input item for Areas worksheet items."""

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


class Surfaces:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Areas):
        self.xl = _xl
        self.shape = _shape
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self, _row_start: int = 1, _row_end: int = 100) -> int:
        """Return the row number of the 'Area input' section header."""

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.surface_rows.locator_col_header,
            _row_start=_row_start,
            _row_end=_row_end
        )

        for i,  val in enumerate(xl_data):
            if val == self.shape.surface_rows.locator_string_header:
                return i

        raise Exception(
            f'\n\tError: Not able to find the "Areas input" input section of '
            f'the "{self.shape.name}" worksheet? Please be sure the section begins '
            f'with the "{self.shape.surface_rows.locator_string_header}" flag in '
            f'column {self.shape.surface_rows.locator_col_header}.'
        )

    def find_section_first_entry_row(self) -> int:
        """Return the row number of the very first user-input entry row in the 'Area input' section."""

        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            _sheet_name=self.shape.name,
            _col=self.shape.surface_rows.locator_col_entry,
            _row_start=self.section_header_row,
            _row_end=self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            try:
                val = str(int(val))  # Value comes in as  "1.0" from Excel?
            except:
                continue

            if val == self.shape.surface_rows.locator_string_entry:
                return i

        raise Exception(
            f'\n\tError: Not able to find the first surface entry row in the "Areas input" section?'
        )

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()

    def get_surface_phpp_id_by_name(self, _name: str) -> str:
        """Return the PHPP-Style id ("1-NorthRoofSurface", ...) when given the surface name."""

        if not self.section_first_entry_row:
            self.section_first_entry_row = self.find_section_header_row()

        row = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.shape.name,
            row_start=self.section_first_entry_row,
            row_end=self.section_first_entry_row+500,
            col=self.shape.surface_rows.input_columns.description,
            find=_name
        )

        if not row:
            raise Exception(
                f'Error: Cannot locate the phpp surface named: {_name} in'
                f'column {self.shape.surface_rows.input_columns.description}?'
            )

        prefix = self.xl.get_data(
            self.shape.name,
            f'{col_offset(self.shape.surface_rows.input_columns.description, -1)}{row}'
        )

        return f'{int(prefix)}-{_name}'


class ThermalBridges:

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Areas):
        pass


class Areas:
    """IO Controller for the PHPP Areas worksheet."""

    def __init__(self, _xl: xl_app.XLConnection, _shape: shape_model.Areas):
        self.xl = _xl
        self.shape = _shape
        self.surfaces = Surfaces(self.xl, self.shape)
        self.thermal_bridges = ThermalBridges(self.xl, self.shape)

    def write_surfaces(self, _surfaces: List[areas_surface.SurfaceRow]) -> None:
        if not self.surfaces.section_first_entry_row:
            self.surfaces.section_first_entry_row = self.surfaces.find_section_first_entry_row()

        for i, surface in enumerate(_surfaces, start=self.surfaces.section_first_entry_row):
            for item in surface.create_xl_items(self.shape.name, _row_num=i):
                self.xl.write_xl_item(item)

    def _create_input_location_object(self, _phpp_model_obj: areas_data.AreasInput) -> AreasInputLocation:
        """Create and setup the AreasInputLocation object with the correct data."""
        phpp_obj_shape: shape_model.AreasInputItem = getattr(
            self.shape, _phpp_model_obj.input_type)
        return AreasInputLocation(
            _xl=self.xl,
            _sheet_name=self.shape.name,
            _search_col=phpp_obj_shape.locator_col,
            _search_item=phpp_obj_shape.locator_string,
            _input_row_offset=phpp_obj_shape.input_row_offset
        )

    def write_item(self, _phpp_model_obj: areas_data.AreasInput) -> None:
        """Write the VerificationInputItem item out to the PHPP Areas Worksheet."""
        input_object = self._create_input_location_object(_phpp_model_obj)
        input_row = input_object.find_input_row()
        xl_item = _phpp_model_obj.create_xl_item(self.shape.name, input_row)
        self.xl.write_xl_item(xl_item)
