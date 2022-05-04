# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a PHPP Components/Window-Frame row."""

from dataclasses import dataclass
from typing import List, Tuple, ClassVar, Dict
from functools import partial

from PHX.model import constructions

from PHX.to_PHPP.phpp import xl_data


@dataclass
class FrameRow:
    """A single Areas/Surface entry row."""
    columns: ClassVar[Dict] = {
        'description': 'IL',
        'u_value_left': 'IM',
        'u_value_right': 'IN',
        'u_value_bottom': 'IO',
        'u_value_top': 'IP',
        'width_left': 'IQ',
        'width_right': 'IR',
        'width_bottom': 'IS',
        'width_top': 'IT',
        'psi_g_left': 'IU',
        'psi_g_right': 'IV',
        'psi_g_bottom': 'IW',
        'psi_g_top': 'IX',
        'psi_i_left': 'IY',
        'psi_i_right': 'IZ',
        'psi_i_bottom': 'JA',
        'psi_i_top': 'JB',
    }

    __slots__ = ('phx_construction',)
    phx_construction: constructions.PhxConstructionWindow

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        return f'{self.columns[_field_name]}{_row_num}'

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
