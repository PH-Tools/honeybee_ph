# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Controller Class for the PHPP Components worksheet."""

from __future__ import annotations
from typing import List, Optional, Collection
from dataclasses import dataclass, field

from PHX.model import geometry, building
from PHX.model.enums.building import ComponentExposureExterior, ComponentFaceType, ComponentFaceOpacity, ComponentColor
from PHX.to_PHPP.phpp import xl_app
from PHX.to_PHPP.phpp import sheets


class AreasInputError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the "Areas input" input section of the "Areas" worksheet?'\
            'Please be sure the section begins with the "Areas input" flag in column L.'
        super().__init__(self.msg)


class AreasTerminationError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the end of the "Area inputs" input section'\
            'of the "Areas" worksheet? Please be sure that the TB section ends with the "Aend" flag in column L?'
        super().__init__(self.msg)


class ThermalBridgeInputError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the "Thermal bridge inputs" input section of the "Areas" worksheet?'\
            'Please be sure the section begins with the "Thermal bridge inputs" flag in column L.'
        super().__init__(self.msg)


class ThermalBridgeTerminationError(Exception):
    def __init__(self):
        self.msg = f'\n\tError: Not able to find the end of the "Thermal bridge inputs" input section'\
            'of the "Areas" worksheet? Please be sure that the TB section ends with the "TBend" flag in column L?'
        super().__init__(self.msg)


@dataclass
class SurfaceEntry:
    """A single surface entry row"""
    row_num: int
    surface_num: int
    description_value: Optional[str]

    @property
    def description_range(self) -> str:
        return f'L{self.row_num}'

    def get_phpp_group_number(self, _phx_component: building.PhxComponent) -> int:
        if _phx_component.face_type == ComponentFaceType.WALL:
            if _phx_component.exposure_exterior == ComponentExposureExterior.EXTERIOR:
                return 8
            else:
                return 9
        elif _phx_component.face_type == ComponentFaceType.FLOOR:
            return 11
        elif _phx_component.face_type == ComponentFaceType.ROOF_CEILING:
            return 10
        else:
            return 12

    def write_data_to_sheet(self, _xl: xl_app.XLConnection,
                            _sheet_name: str,
                            _phx_polygon: geometry.PhxPolygon,
                            _phx_component: building.PhxComponent,
                            _phpp_assembly_id: Optional[str]) -> None:
        """Add the PhxPolygon attributes to the Areas worksheet.

        Arguments:
        ----------
            * _xl: (xl_app.XLConnection) The XL connection to use.
            * _sheet_name: (str) The name of the worksheet to write to.
            * _phx_polygon: (geometry.PhxPolygon) The PHX-Polygon to add to the 
                Areas worksheet.
            * _phx_component: (building.PhxComponent) The host PhxComponent with 
                assembly, exposure data.
        """

        _xl.write_data(
            _sheet_name, f'L{self.row_num}', _phx_polygon.display_name)
        _xl.write_data(
            _sheet_name, f'M{self.row_num}', self.get_phpp_group_number(_phx_component))
        _xl.write_data(
            _sheet_name, f'P{self.row_num}', 1)
        _xl.write_data(
            _sheet_name, f'V{self.row_num}', _phx_polygon.area)
        _xl.write_data(
            _sheet_name, f'AC{self.row_num}', _phpp_assembly_id)
        _xl.write_data(
            _sheet_name, f'AJ{self.row_num}', 0.5)
        _xl.write_data(
            _sheet_name, f'AK{self.row_num}', 0.6)
        _xl.write_data(
            _sheet_name, f'AL{self.row_num}', 0.9)

    def clear(self, _xl: xl_app.XLConnection, _sheet_name: str) -> None:
        """Clear all the values from the excel worksheet's row

        Arguments:
        ----------
            * _xl: (xl_app.XLConnection) The Excel connection to use.
            * _sheet_name: (str) The name of the worksheet to clear the values on.
        """
        _xl.clear_data(_sheet_name, f'L{self.row_num}:M{self.row_num}')


@dataclass
class ThermalBridgeEntry:
    """A single thermal-bridge entry row"""
    row_num: int
    surface_num: int
    description_value: Optional[str]

    @property
    def description_range(self) -> str:
        return f'L{self.row_num}'


@dataclass
class AreasShape:
    surface_entries: List[SurfaceEntry] = field(default_factory=list)
    thermal_bridge_entries: List[ThermalBridgeEntry] = field(default_factory=list)


class Areas:
    """The PHPP Areas worksheet.

    Arguments:
    ----------
        * xl: (xl_app.XLConnection) The Excel Connection to use 
        * _u_value: (sheets.UValues) The PHPP U-Values worksheet object which is 
            needed when referencing U-Value names.
    """

    sheet_name = 'Areas'

    def __init__(self, _xl: xl_app.XLConnection, _u_value: sheets.UValues):
        self.xl = _xl
        self.u_values = _u_value
        self.shape = AreasShape()

    def get_worksheet_shape(self) -> None:
        """Find and save the relevant worksheet shape reference points (row/columns)."""
        self.shape.surface_entries = self.get_surface_entry_rows()
        self.shape.thermal_bridge_entries = self.get_thermal_bridge_entry_rows()

    def get_surface_entry_rows(self,
                               _search_key: str = 'Area input',
                               _search_column: str = 'K') -> List[SurfaceEntry]:
        """Reads through the Areas worksheet and finds the surface-entry rows."""

        # -- Find the 'Area input' section start.
        block_start_row = self.xl.get_row_num_of_value_in_column(
            self.sheet_name, 1, 100, _search_column, _search_key)

        if not block_start_row:
            raise AreasInputError()

        # -- Get the 'Area input' info in one list
        col_1 = _search_column
        col_2 = chr(ord(col_1) + 1)
        data = self.xl.get_multiple_column_data(
            _sheet_name=self.sheet_name,
            _col_start=col_1,
            _col_end=col_2,
            _row_start=1,
            _row_end=500,
        )

        # -- Identify and build the Entry rows
        surface_entries: List[SurfaceEntry] = []
        for i, column_vals in enumerate(data, start=1):
            if column_vals[0] == 'Aend':
                break

            # -- Ignore blank rows
            if not column_vals[0]:
                continue

            # -- If col "L" value isn't a number, ignore row
            try:
                srfc_num = int(column_vals[0])
            except:
                continue

            # -- otherwise, build a new SurfaceEntry for the row
            surface_entries.append(SurfaceEntry(
                int(i),
                srfc_num,
                str(column_vals[1]) if column_vals[1] else None)
            )
        else:
            raise AreasTerminationError()

        return surface_entries

    def get_thermal_bridge_entry_rows(self,
                                      _search_key: str = 'Thermal bridge inputs',
                                      _search_column: str = 'K') -> List[ThermalBridgeEntry]:
        """Reads through the Areas worksheet and finds the thermal-bridge-entry rows."""

        # -- Find the 'Area input' section start.
        block_start_row = self.xl.get_row_num_of_value_in_column(
            self.sheet_name, 100, 600, _search_column, _search_key)

        if not block_start_row:
            raise ThermalBridgeInputError()

        # -- Get the 'Area input' info in one list
        col_1 = _search_column
        col_2 = chr(ord(col_1) + 1)
        data = self.xl.get_multiple_column_data(
            _sheet_name=self.sheet_name,
            _col_start=col_1,
            _col_end=col_2,
            _row_start=1,
            _row_end=500,
        )

        # -- Identify and build the Entry rows
        tb_entries: List[ThermalBridgeEntry] = []
        for i, column_vals in enumerate(data, start=1):
            if column_vals[0] == 'TBend':
                break

            # -- Ignore blank rows
            if not column_vals[0]:
                continue

            # -- If col "L" value isn't a number, ignore row
            try:
                srfc_num = int(column_vals[0])
            except:
                continue

            # -- otherwise, build a new SurfaceEntry for the row
            tb_entries.append(ThermalBridgeEntry(
                int(i),
                srfc_num,
                str(column_vals[1]) if column_vals[1] else None)
            )
        else:
            raise ThermalBridgeTerminationError()

        return tb_entries

    def get_next_empty_surface_entry(self, _check_shape: bool = False) -> SurfaceEntry:
        """Return the next empty SurfaceEntry slot found in the worksheet.

        Arguments:
        ----------
            * _check_shape: (Optional[bool]) default=False. Set True to re-run the 
            worksheet shape finder in case the user has added/deleted any rows.

        Returns:
        --------
            * (SurfaceEntry): The first empty SurfaceEntry slot found in the worksheet library.
        """

        if _check_shape or not self.shape.surface_entries:
            self.get_worksheet_shape()

        for surface_entry in self.shape.surface_entries:
            if self.xl.get_data(self.sheet_name, surface_entry.description_range) is None:
                return surface_entry

        raise Exception(
            'Error: Can not find an empty Surface Entry in the {self.sheet_name} sheet?')

    def write_phx_component_to_sheet(self, _phx_component: building.PhxComponent) -> None:
        if not self.shape.surface_entries or not self.shape.thermal_bridge_entries:
            self.get_worksheet_shape()

        assembly_phpp_id = self.u_values.get_constructor_phpp_id_by_name(
            _phx_component.assembly.display_name)

        for phx_polygon in _phx_component.polygons:

            for exg_srfc_entry in self.shape.surface_entries:
                if exg_srfc_entry.description_value == phx_polygon.display_name:
                    surface_entry = exg_srfc_entry
                    break
            else:
                surface_entry = self.get_next_empty_surface_entry()

            surface_entry.clear(self.xl, self.sheet_name)
            surface_entry.write_data_to_sheet(
                self.xl, self.sheet_name, phx_polygon, _phx_component, assembly_phpp_id)
            surface_entry.description_value = phx_polygon.display_name
