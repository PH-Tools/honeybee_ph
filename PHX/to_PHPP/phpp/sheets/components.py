# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Components worksheet."""

from __future__ import annotations
from typing import List, Optional
from dataclasses import dataclass, field

from PHX.to_PHPP.phpp import xl_app
from PHX.model import constructions
from PHX.to_PHPP.phpp import xl_typing


class GlazingComponentsError(Exception):
    def __init__(self, _c1):
        self.msg = f'\n\tError: Not able to find the "Glazing" section of the Components worksheet in colum "{_c1}"?'
        super().__init__(self.msg)


class FrameComponentsError(Exception):
    def __init__(self, _c1):
        self.msg = f'\n\tError: Not able to find the "Window frames" section of the Components worksheet in colum "{_c1}"?'
        super().__init__(self.msg)


@dataclass
class GlazingEntry:
    """An individual Glazing entry/row"""

    row_num: int
    description_value: xl_typing.xl_range_value

    @property
    def description_range(self) -> str:
        return f'IE{self.row_num}'

    def write_data_to_sheet(self, _xl: xl_app.XLConnection,
                            _sheet_name: str,
                            _phx_const: constructions.PhxConstructionWindow) -> None:
        """Add the PhxConstructionWindow attributes to the Components worksheet.

        Arguments:
        ----------
            * _xl: (xl_app.XLConection) The XL connection to use.
            * _sheet_name: (str) The name of the worksheet to write to.
            * _phx_const: (construction.PhxConstructionWindow) The PHX Window
                construciton to add to the PHPP library.
        """
        _xl.write_data(
            _sheet_name, f'IE{self.row_num}', _phx_const.display_name)
        _xl.write_data(
            _sheet_name, f'IF{self.row_num}', _phx_const.glass_g_value)
        _xl.write_data(
            _sheet_name, f'IG{self.row_num}', _phx_const.u_value_glass)

    def clear(self, _xl: xl_app.XLConnection, _sheet_name: str) -> None:
        """Clear all the values from the excel worksheet's row

        Arguments:
        ----------
            * _xl: (xl_app.XLConnection) The Excel connection to use.
            * _sheet_name: (str) The name of the worksheet to clear the values on.
        """
        _xl.clear_data(_sheet_name, f'IE{self.row_num}:IG{self.row_num}')


@dataclass
class FrameEntry:
    row: int
    description_value: xl_typing.xl_range_value

    @property
    def description_range(self) -> str:
        return f'IL{self.row}'

    def write_data_to_sheet(self, _xl: xl_app.XLConnection,
                            _sheet_name: str,
                            _phx_const: constructions.PhxConstructionWindow) -> None:
        """Add the PhxConstructionOpaueattributes to the Components worksheet.

        Arguments:
        ----------
            * _xl: (xl_app.XLConection) The XL connection to use.
            * _sheet_name: (str) The name of the worksheet to write to.
            * _phx_const: (construction.PhxConstructionWindow) The PHX Construction
                construciton to add to the PHPP library.
        """
        _xl.write_data(_sheet_name, f'IL{self.row}', _phx_const.display_name)

        _xl.write_data(_sheet_name, f'IM{self.row}',
                       _phx_const.frame_left.u_value)
        _xl.write_data(_sheet_name, f'IN{self.row}',
                       _phx_const.frame_right.u_value)
        _xl.write_data(_sheet_name, f'IO{self.row}',
                       _phx_const.frame_bottom.u_value)
        _xl.write_data(_sheet_name, f'IP{self.row}',
                       _phx_const.frame_top.u_value)

        _xl.write_data(_sheet_name, f'IQ{self.row}',
                       _phx_const.frame_left.width)
        _xl.write_data(_sheet_name, f'IR{self.row}',
                       _phx_const.frame_right.width)
        _xl.write_data(_sheet_name, f'IS{self.row}',
                       _phx_const.frame_bottom.width)
        _xl.write_data(
            _sheet_name, f'IT{self.row}', _phx_const.frame_top.width)

        _xl.write_data(_sheet_name, f'IU{self.row}',
                       _phx_const.frame_left.psi_glazing)
        _xl.write_data(_sheet_name, f'IV{self.row}',
                       _phx_const.frame_right.psi_glazing)
        _xl.write_data(_sheet_name, f'IW{self.row}',
                       _phx_const.frame_bottom.psi_glazing)
        _xl.write_data(_sheet_name, f'IX{self.row}',
                       _phx_const.frame_top.psi_glazing)

        _xl.write_data(_sheet_name, f'IY{self.row}',
                       _phx_const.frame_left.psi_install)
        _xl.write_data(_sheet_name, f'IZ{self.row}',
                       _phx_const.frame_right.psi_install)
        _xl.write_data(_sheet_name, f'JA{self.row}',
                       _phx_const.frame_bottom.psi_install)
        _xl.write_data(_sheet_name, f'JB{self.row}',
                       _phx_const.frame_top.psi_install)

    def clear(self, _xl: xl_app.XLConnection, _sheet_name: str) -> None:
        """Clear all the values from the excel worksheet's row

        Arguments:
        ----------
            * _xl: (xl_app.XLConnection) The Excel connection to use.
            * _sheet_name: (str) The name of the worksheet to clear the values on.
        """
        _xl.clear_data(_sheet_name, f'IL{self.row}:JB{self.row}')


@dataclass
class ComponentsShape:
    glazings: List[GlazingEntry] = field(default_factory=list)
    frames: List[FrameEntry] = field(default_factory=list)


class Components:
    """The PHPP Components worksheet.

    Arguments:
    ----------
        * xl (xl_app.XLConnection): The Excel Connection to use.
    """

    sheet_name = 'Components'

    def __init__(self, _xl):
        self.xl: xl_app.XLConnection = _xl
        self.shape = ComponentsShape()

    def get_glazing_entries(self) -> List[GlazingEntry]:
        """Return a list of all the glazing entry locations on the worksheet.

        This will try and find the cell marked "Glazing" in column 'ID' and use that
        as the reference point for all entry lines.

        Returns:
        -------
            (List[GlazingEntry]): A list of all the GlazingEntry elements/locations found.
        """
        col_1 = 'ID'
        col_2 = 'IE'
        glazing_block_start = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.sheet_name,
            row_start=1,
            row_end=100,
            col=col_1,
            find='Glazing')

        if not glazing_block_start:
            raise FrameComponentsError(col_1)

        glazing_data_row_start = glazing_block_start + 5
        glazing_data_row_end = glazing_block_start + 105

        # -- Get the block data from Excel in one operation
        col_data = self.xl.get_multiple_column_data(
            _sheet_name=self.sheet_name,
            _col_start=col_1,
            _col_end=col_2,
            _row_start=glazing_data_row_start,
            _row_end=glazing_data_row_end,
        )

        # -- Find the rows
        glazing_entries: List[GlazingEntry] = []
        for i, column_val in enumerate(col_data, start=glazing_data_row_start):

            desc = str(column_val[1]) if column_val[1] else None
            glazing_entries.append(GlazingEntry(i, desc))

        return glazing_entries

    def get_frame_entries(self) -> List[FrameEntry]:
        """Return a list of all the frame entry locations on the worksheet.

        This will try and find the cell marked "Window frames" in column 'IK' and use that
        as the reference point for all entry lines.

        Returns:
        -------
            (List[FrameEntry]): A list of all the GlazingEntry elements/locations found.
        """
        col_1 = 'IK'
        col_2 = 'IL'
        frame_block_start = self.xl.get_row_num_of_value_in_column(
            sheet_name=self.sheet_name,
            row_start=1,
            row_end=100,
            col=col_1,
            find='Window frames')

        if not frame_block_start:
            raise GlazingComponentsError(col_1)
        frame_data_row_start = frame_block_start + 5
        frame_data_row_end = frame_block_start + 105

        # -- Get the block data from Excel in one operation
        col_data = self.xl.get_multiple_column_data(
            _sheet_name=self.sheet_name,
            _col_start=col_1,
            _col_end=col_2,
            _row_start=frame_data_row_start,
            _row_end=frame_data_row_end,
        )

        # -- Find the rows
        frame_entries: List[FrameEntry] = []
        for i, column_val in enumerate(col_data, start=frame_data_row_start):

            desc = str(column_val[1]) if column_val[1] else None
            frame_entries.append(FrameEntry(i, desc))

        return frame_entries

    def get_worksheet_shape(self) -> None:
        """Find the worksheet entry locations for all Glazing and Frames.

        This method will set the values for the shape.glazings and shape.frames
        While this method can be called at any time, it should not have to be rebuilt 
        unless the user has added / deleted rows or moved input locations around in the 
        PHPP document.
        """
        self.shape.glazings = self.get_glazing_entries()
        self.shape.frames = self.get_frame_entries()

    def get_next_empty_glazing_entry(self, _check_shape: bool = False) -> GlazingEntry:
        """Return the next empty GlazingEntry slot found in the worksheet.

        Arguments:
        ----------
            * _check_shape: (Optional[bool]) default=False. Set True to re-run the 
            worksheet shape finder in case the user has added/deleted any rows.

        Returns:
        --------
            * (GlazingEntry): The first empty GlazingEntry slot found in the worksheet library.
        """

        if _check_shape or not self.shape.glazings:
            self.get_worksheet_shape()

        for glazing_entry in self.shape.glazings:
            if self.xl.get_data(self.sheet_name, glazing_entry.description_range) is None:
                return glazing_entry

        raise Exception(
            'Error: Can not find an empty Glazing Entry in the {self.sheet_name} sheet?')

    def get_next_empty_frame_entry(self, _check_shape: bool = False) -> FrameEntry:
        """Return the next empty FrameEntry slot found in the worksheet.

        Arguments:
        ----------
            * _check_shape: (Optional[bool]) default=False. Set True to re-run the 
            worksheet shape finder in case the user has added/deleted any rows.

        Returns:
        --------
            * (FrameEntry): The first empty FrameEntry slot found in the worksheet library.
        """
        if _check_shape or not self.shape.frames:
            self.get_worksheet_shape()

        for frame_entry in self.shape.frames:
            if self.xl.get_data(self.sheet_name, frame_entry.description_range) is None:
                return frame_entry

        raise Exception(
            'Error: Can not find an empty Frame Entry in the {self.sheet_name} sheet?')

    def clear_sheet(self) -> None:
        """Remove all the values in the Glazing and Frame sections of the Worksheet."""
        if not self.shape.glazings or not self.shape.frames:
            self.get_worksheet_shape()

        for glazing_entry in self.shape.glazings:
            glazing_entry.clear(self.xl, self.sheet_name)

        for frame_entry in self.shape.frames:
            frame_entry.clear(self.xl, self.sheet_name)

    def write_phx_construction_to_sheet(self, _phx_const: constructions.PhxConstructionWindow) -> None:
        """Write a new PHX-Construction to the PHPP Components Library.

        This will add both glazing and frame values from the PHX-Construction.

        Arguments:
        ---------
            * _phx_const: (constructions.PhxConstructionWindow) The PHX Construction to add to the
                PHPP Components library.
        """
        if not self.shape.glazings or not self.shape.frames:
            self.get_worksheet_shape()

        # -- Glazings
        for exg_glazing_entry in self.shape.glazings:
            if exg_glazing_entry.description_value == _phx_const.display_name:
                glazing_entry = exg_glazing_entry
                break
        else:
            glazing_entry = self.get_next_empty_glazing_entry()

        glazing_entry.clear(self.xl, self.sheet_name)
        glazing_entry.write_data_to_sheet(self.xl, self.sheet_name, _phx_const)
        glazing_entry.description_value = _phx_const.display_name

        # -- Frames
        for exg_frame_entry in self.shape.frames:
            if exg_frame_entry.description_value == _phx_const.display_name:
                frame_entry = exg_frame_entry
                break
        else:
            frame_entry = self.get_next_empty_frame_entry()

        frame_entry.clear(self.xl, self.sheet_name)
        frame_entry.write_data_to_sheet(self.xl, self.sheet_name, _phx_const)
        frame_entry.description_value = _phx_const.display_name
