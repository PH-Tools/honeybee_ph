# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Areas worksheet."""

from __future__ import annotations
from typing import List, Optional

from PHX.to_PHPP.phpp import xl_app
from PHX.to_PHPP.phpp.model import areas_surface


class AreasHeaderRowError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the "Areas input" input section of the "Areas" worksheet?'\
            'Please be sure the section begins with the "Areas input" flag in column L.'
        super().__init__(self.msg)


class AreasStartRowError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the first surface entry row in the "Areas input" section?'
        super().__init__(self.msg)


class ThermalBridgeInputError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the "Thermal bridge inputs" input section of the "Areas" worksheet?'\
            'Please be sure the section begins with the "Thermal bridge inputs" flag in column L.'
        super().__init__(self.msg)


# -----------------------------------------------------------------------------

class Surfaces:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        self.xl = _xl
        self.sheet_name = _sheet_name
        self.section_header_row: Optional[int] = None
        self.section_first_entry_row: Optional[int] = None

    def find_section_header_row(self) -> int:
        xl_data = self.xl.get_single_column_data(self.sheet_name, 'K', 1, 100,)

        for i,  val in enumerate(xl_data):
            if 'Area input' == val:
                return i
        else:
            raise AreasHeaderRowError()

    def find_section_first_entry_row(self) -> int:
        if not self.section_header_row:
            self.section_header_row = self.find_section_header_row()

        xl_data = self.xl.get_single_column_data(
            self.sheet_name, 'K', self.section_header_row, self.section_header_row+25,
        )

        for i, val in enumerate(xl_data, start=self.section_header_row):
            if val == 1:
                return i
        else:
            raise AreasStartRowError()

    def find_section_shape(self) -> None:
        self.section_start_row = self.find_section_header_row()
        self.section_first_entry_row = self.find_section_first_entry_row()


class ThermalBridges:

    def __init__(self, _xl: xl_app.XLConnection, _sheet_name: str):
        pass


class Areas:
    """The PHPP Areas worksheet.

    Arguments:
    ----------
        * xl: (xl_app.XLConnection) The Excel Connection to use
    """

    sheet_name = 'Areas'

    def __init__(self, _xl: xl_app.XLConnection):
        self.xl = _xl
        self.surfaces = Surfaces(self.xl, self.sheet_name)
        self.thermal_bridges = ThermalBridges(self.xl, self.sheet_name)

    def write_surfaces(self, _surfaces: List[areas_surface.SurfaceRow]) -> None:
        if not self.surfaces.section_first_entry_row:
            self.surfaces.section_first_entry_row = self.surfaces.find_section_first_entry_row()

        for i, surface in enumerate(_surfaces, start=self.surfaces.section_first_entry_row):
            for item in surface.create_xl_items(self.sheet_name, _row_num=i):
                self.xl.write_xl_item(item)
