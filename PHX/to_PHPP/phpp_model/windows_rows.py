# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a PHPP Windows/Window-Entry row"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
from functools import partial

from PHX.model import constructions, geometry

from PHX.to_PHPP import xl_data
from PHX.to_PHPP.phpp_localization import shape_model


@dataclass
class WindowRow:
    """Model class for a single Window entry row."""

    __slots__ = ('shape', 'phx_polygon', 'phx_construction',
                 'phpp_host_surface_id_name', 'phpp_id_frame', 'phpp_id_glazing')
    shape: shape_model.Windows
    phx_polygon: geometry.PhxPolygonRectangular
    phx_construction: constructions.PhxConstructionWindow
    phpp_host_surface_id_name: Optional[str]
    phpp_id_frame: Optional[str]
    phpp_id_glazing: Optional[str]

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        col = getattr(self.shape.window_rows.input_columns, _field_name)
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
            (create_range('quantity'), 1),
            (create_range('description'), self.phx_polygon.display_name),
            (create_range('host'), self.phpp_host_surface_id_name),
            (create_range('glazing_id'), self.phpp_id_frame),
            (create_range('frame_id'), self.phpp_id_glazing),
            (create_range('width'), self.phx_polygon.width),
            (create_range('height'), self.phx_polygon.height),

            # -- TODO: Install condition, not Psi-Install
            (create_range('psi_i_left'), self.phx_construction.frame_left.psi_install),
            (create_range('psi_i_right'), self.phx_construction.frame_right.psi_install),
            (create_range('psi_i_bottom'), self.phx_construction.frame_bottom.psi_install),
            (create_range('psi_i_top'), self.phx_construction.frame_top.psi_install),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
