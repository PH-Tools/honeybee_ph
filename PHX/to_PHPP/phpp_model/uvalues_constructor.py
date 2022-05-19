# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Data-entry constructor for the U-Values Worksheet."""

from dataclasses import dataclass
from typing import List, Tuple
from functools import partial

from PHX.model import constructions

from PHX.to_PHPP import xl_data
from PHX.to_PHPP.phpp_localization import shape_model


@dataclass
class ConstructorBlock:
    """A single U-Value/Constructor entry block."""

    __slots__ = ("shape", "phx_construction")
    shape: shape_model.UValues
    phx_construction: constructions.PhxConstructionOpaque

    def _create_range(self, _field_name: str, _row_offset: int, _start_row: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        col = getattr(self.shape.constructor.input_columns, _field_name)
        return f'{col}{_start_row + _row_offset}'

    def create_xl_items(self, _sheet_name: str, _start_row: int) -> List[xl_data.XlItem]:
        create_range = partial(self._create_range, _start_row=_start_row)

        # -- Build the basic assembly attributes
        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('display_name', 2), self.phx_construction.display_name),
            (create_range('r_si', 4), 0.0),
            (create_range('r_se', 5), 0.0),
        ]

        # -- Build all the layers of the assembly
        for i, layer in enumerate(self.phx_construction.layers, start=8):
            layer_items: List[Tuple[str, xl_data.xl_writable]] = [
                (create_range('sec_1_description', i), layer.material.display_name),
                (create_range('sec_1_conductivity', i), layer.material.conductivity),
                (create_range('thickness', i), layer.thickness * 1000),
            ]
            items.extend(layer_items)

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
