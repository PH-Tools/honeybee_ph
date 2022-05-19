# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a single PHPP Addition Vent / Unit-Entry row."""

from dataclasses import dataclass
from typing import List, Tuple
from functools import partial

from PHX.model import hvac
from PHX.to_PHPP import xl_data
from PHX.to_PHPP.phpp_localization import shape_model


@dataclass
class VentUnitRow:
    """Model class for a single Ventilation Unit entry row."""

    __slots__ = ('shape', 'phx_vent_sys', 'phpp_id_ventilator')
    shape: shape_model.AddnlVent
    phx_vent_sys: hvac.PhxDeviceVentilator
    phpp_id_ventilator: str

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        col = getattr(self.shape.units.input_columns, _field_name)
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
            (create_range('quantity'), self.phx_vent_sys.quantity),
            (create_range('display_name'), self.phx_vent_sys.display_name),
            (create_range('unit_selected'), self.phpp_id_ventilator),
            (create_range('temperature_below_defrost_used'),
             self.phx_vent_sys.params.temperature_below_defrost_used),
        ]
        return [xl_data.XlItem(_sheet_name, *item) for item in items]
