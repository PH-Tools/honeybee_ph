# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a single PHPP Addition Vent / Space(room)-Entry row."""

from dataclasses import dataclass
from typing import List, Tuple, Dict
from functools import partial

from PHX.model import loads
from PHX.to_PHPP import xl_data


@dataclass
class VentSpaceRow:
    """A single Ventilation Space/Room entry row."""

    __slots__ = ('columns', 'phx_room_vent', 'phpp_row_ventilator')
    columns: Dict[str, str]
    phx_room_vent: loads.PhxRoomVentilation
    phpp_row_ventilator: int

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
            (create_range('quantity'), self.phx_room_vent.quantity),
            (create_range('display_name'), self.phx_room_vent.display_name),
            (create_range('vent_unit_assigned'), self.phpp_row_ventilator),
            (create_range('weighted_floor_area'), self.phx_room_vent.weighted_floor_area),
            (create_range('clear_height'), self.phx_room_vent.clear_height),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
