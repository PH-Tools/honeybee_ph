# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a PHPP Windows/Window-Entry row"""

from dataclasses import dataclass
from typing import ClassVar, Dict, List, Tuple, Optional
from functools import partial

from PHX.model import building, geometry

from PHX.to_PHPP.phpp import xl_data


@dataclass
class WindowRow:
    """A single Window entry row."""

    columns: ClassVar[Dict[str, str]] = {
        'quantity': 'L',
        'description': 'M',
        'width': 'Q',
        'height': 'R',
        'host': 'S',
        'glazing_id': 'T',
        'frame_id': 'U',
        'psi_i_left': 'AA',
        'psi_i_right': 'AB',
        'psi_i_bottom': 'AC',
        'psi_i_top': 'AD',
        'comfort_exempt': 'BR',
        'comfort_temp': 'BR',
    }

    __slots__ = ('phx_polygon', 'phpp_host_surface_id_name',
                 'phpp_id_frame', 'phpp_id_glazing')
    phx_polygon: geometry.PhxPolygon
    phpp_host_surface_id_name: Optional[str]
    phpp_id_frame: Optional[str]
    phpp_id_glazing: Optional[str]

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
            (create_range('quantity'), 1),
            (create_range('description'), self.phx_polygon.display_name),
            (create_range('host'), self.phpp_host_surface_id_name),
            (create_range('glazing_id'), self.phpp_id_frame),
            (create_range('frame_id'), self.phpp_id_glazing),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
