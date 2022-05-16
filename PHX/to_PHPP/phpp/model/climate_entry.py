# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Data-entry constructor for the Climate Worksheet."""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union, ClassVar
from functools import partial

from PHX.to_PHPP.phpp import xl_data
from PHX.model import climate


@dataclass
class ClimateSettings:
    """The active climate data selections."""

    __slots__ = ("columns", "phx_location")
    columns: Dict[str, str]
    phx_location: climate.PhxLocation

    def _create_range(self, _field_name: str, _row_offset: int, _start_row: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_start_row + _row_offset}'

    def create_xl_items(self, _sheet_name: str, _start_row: int) -> List[xl_data.XlItem]:
        """Return a list of the XL items to write to the worksheet."""
        create_range = partial(self._create_range, _start_row=_start_row)

        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('country', 0), "ud-User Data"),
            (create_range('region', 1), "All"),
            (create_range('dataset', 3), f"ud---00-{self.phx_location.display_name}"),
            (create_range('elevation_override', 9), self.phx_location.site.elevation),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]


@dataclass
class ClimateDataBlock:
    """A single Climate / Weather-Station entry block."""

    __slots__ = ("columns", "phx_location")
    columns: Dict[str, Union[str, Dict]]
    phx_location: climate.PhxLocation
    month_order: ClassVar[List[str]] = ['jan', 'feb', 'mar', 'apr',
                                        'may', 'jun', 'jul', 'aug',
                                        'sep', 'oct', 'nov', 'dec']

    def _create_range(self, _field_name: str, _row_offset: int, _start_row: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_start_row + _row_offset}'

    def create_xl_items(self, _sheet_name: str, _start_row: int) -> List[xl_data.XlItem]:
        """Return a list of the XL items to write to the worksheet."""
        create_range = partial(self._create_range, _start_row=_start_row)
        phx_climate = self.phx_location.climate
        phx_site = self.phx_location.site

        # -- Build the Header assembly attributes
        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('latitude', 0), phx_site.latitude),
            (create_range('longitude', 0), phx_site.longitude),
            (create_range('elevation', 0), phx_climate.weather_station_elevation),
            (create_range('display_name', 0), self.phx_location.display_name),
            (create_range('summer_delta_t', 0), phx_climate.daily_temp_swing),
            (create_range('source', 0), self.phx_location.source),
        ]

        # -- Add in the monthly data
        for i, month in enumerate(self.month_order, start=0):
            layer_items: List[Tuple[str, xl_data.xl_writable]] = [
                (create_range(month, 1), phx_climate.monthly_temperature_air[i]),
                (create_range(month, 2), phx_climate.monthly_radiation_north[i]),
                (create_range(month, 3), phx_climate.monthly_radiation_east[i]),
                (create_range(month, 4), phx_climate.monthly_radiation_south[i]),
                (create_range(month, 5), phx_climate.monthly_radiation_west[i]),
                (create_range(month, 6), phx_climate.monthly_radiation_global[i]),
                (create_range(month, 7), phx_climate.monthly_temperature_dewpoint[i]),
                (create_range(month, 8), phx_climate.monthly_temperature_sky[i]),
            ]
            items.extend(layer_items)

        # -- Add in the peak-load data
        for col_name in ["peak_heating_1", "peak_heating_2", "peak_cooling_1", "peak_cooling_2"]:
            layer_items: List[Tuple[str, xl_data.xl_writable]] = [
                (create_range(col_name, 1), getattr(phx_climate, col_name).temp),
                (create_range(col_name, 2), getattr(phx_climate, col_name).rad_north),
                (create_range(col_name, 3), getattr(phx_climate, col_name).rad_east),
                (create_range(col_name, 4), getattr(phx_climate, col_name).rad_south),
                (create_range(col_name, 5), getattr(phx_climate, col_name).rad_west),
                (create_range(col_name, 6), getattr(phx_climate, col_name).rad_global),
            ]
            items.extend(layer_items)

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
