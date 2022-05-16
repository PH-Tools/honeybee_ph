# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a PHPP Components/Window-Frame row."""

from dataclasses import dataclass
from typing import List, Tuple, Dict
from functools import partial

from PHX.model import hvac

from PHX.to_PHPP import xl_data


@dataclass
class VentilatorRow:
    """A single Ventilator Component entry row."""

    __slots__ = ('columns', 'phx_vent_sys',)
    columns: Dict[str, str]
    phx_vent_sys: hvac.PhxDeviceVentilator

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
        def frost(_reqd: bool) -> str:
            if _reqd:
                return 'yes'
            return 'no'

        create_range = partial(self._create_range, _row_num=_row_num)
        params = self.phx_vent_sys.params
        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('display_name'), self.phx_vent_sys.display_name),
            (create_range('sensible_heat_recovery'), params.sensible_heat_recovery),
            (create_range('latent_heat_recovery'), params.latent_heat_recovery),
            (create_range('electric_efficiency'), params.electric_efficiency),
            (create_range('frost_protection_reqd'), frost(params.frost_protection_reqd)),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
