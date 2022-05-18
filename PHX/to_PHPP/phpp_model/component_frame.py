# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a PHPP Components/Window-Frame row."""

from dataclasses import dataclass
from typing import List, Tuple
from functools import partial

from PHX.model import constructions

from PHX.to_PHPP.phpp_localization import shape_model
from PHX.to_PHPP import xl_data


@dataclass
class FrameRow:
    """A single Areas/Surface entry row."""

    __slots__ = ('shape', 'phx_construction',)
    shape: shape_model.Components
    phx_construction: constructions.PhxConstructionWindow

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        col = getattr(self.shape.frames.input_columns, _field_name)
        return f'{col}{_row_num}'

    def create_xl_items(self, _sheet_name: str, _row_num: int) -> List[xl_data.XlItem]:
        """Returns a list of the XL Items to write for this Surface Entry

        Arguments:
        ----------
            * _sheet_name: (str) The name of the worksheet to write to.
            * _row_num: (int) The row number to build the XlItems for
        Returns:
        --------
            * (List[XlItem]): The XlItems to write to the sheet.
        """
        create_range = partial(self._create_range, _row_num=_row_num)
        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('description'), self.phx_construction.display_name),
            (create_range('u_value_left'), self.phx_construction.frame_left.u_value),
            (create_range('u_value_right'), self.phx_construction.frame_right.u_value),
            (create_range('u_value_bottom'), self.phx_construction.frame_bottom.u_value),
            (create_range('u_value_top'), self.phx_construction.frame_top.u_value),

            (create_range('width_left'), self.phx_construction.frame_left.width),
            (create_range('width_right'), self.phx_construction.frame_right.width),
            (create_range('width_bottom'), self.phx_construction.frame_bottom.width),
            (create_range('width_top'), self.phx_construction.frame_top.width),

            (create_range('psi_g_left'), self.phx_construction.frame_left.psi_glazing),
            (create_range('psi_g_right'), self.phx_construction.frame_right.psi_glazing),
            (create_range('psi_g_bottom'), self.phx_construction.frame_bottom.psi_glazing),
            (create_range('psi_g_top'), self.phx_construction.frame_top.psi_glazing),

            (create_range('psi_i_left'), self.phx_construction.frame_left.psi_install),
            (create_range('psi_i_right'), self.phx_construction.frame_right.psi_install),
            (create_range('psi_i_bottom'), self.phx_construction.frame_bottom.psi_install),
            (create_range('psi_i_top'), self.phx_construction.frame_top.psi_install),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
