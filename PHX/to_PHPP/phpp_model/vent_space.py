# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Model class for a single PHPP Addition Vent / Space(room)-Entry row."""

from dataclasses import dataclass
from typing import List, Tuple
from functools import partial

from PHX.model import loads, schedules
from PHX.to_PHPP import xl_data
from PHX.to_PHPP.xl_data import xl_writable
from PHX.to_PHPP.phpp_localization import shape_model


@dataclass
class VentSpaceRow:
    """Model class for a single Ventilation Space/Room entry row."""

    __slots__ = ('shape', 'phx_room_vent', 'phpp_row_ventilator', 'phx_vent_pattern')
    shape: shape_model.AddnlVent
    phx_room_vent: loads.PhxRoomVentilation
    phpp_row_ventilator: xl_writable
    phx_vent_pattern: schedules.UtilizationPatternVent

    def _create_range(self, _field_name: str, _row_num: int) -> str:
        """Return the XL Range ("P12",...) for the specific field name."""
        col = getattr(self.shape.rooms.input_columns, _field_name)
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
        # -- Handle the percentage bullshit so always adds up to 100% hours
        periods = self.phx_vent_pattern.operating_periods
        high_time = periods.high.period_operating_hours / 24.0
        standard_time = periods.standard.period_operating_hours / 24.0
        minimum_time = 1-(high_time + standard_time)
        minimum_speed = ((periods.basic.period_operation_speed * periods.basic.period_operating_hours) +
                         (periods.minimum.period_operation_speed * periods.minimum.period_operating_hours)) / (periods.basic.period_operating_hours + periods.minimum.period_operating_hours)

        # --
        create_range = partial(self._create_range, _row_num=_row_num)
        items: List[Tuple[str, xl_data.xl_writable]] = [
            (create_range('quantity'), self.phx_room_vent.quantity),
            (create_range('display_name'), self.phx_room_vent.display_name),
            (create_range('vent_unit_assigned'), self.phpp_row_ventilator),
            (create_range('weighted_floor_area'), self.phx_room_vent.weighted_floor_area),
            (create_range('clear_height'), self.phx_room_vent.clear_height),
            (create_range('V_sup'), self.phx_room_vent.flow_rates.flow_supply),
            (create_range('V_eta'), self.phx_room_vent.flow_rates.flow_extract),
            (create_range('V_trans'), self.phx_room_vent.flow_rates.flow_transfer),
            # -- Operating Days / weeks
            (create_range('operating_days'), self.phx_vent_pattern.operating_days),
            (create_range('operating_weeks'), self.phx_vent_pattern.operating_weeks),
            (create_range('holiday_days'), self.phx_vent_pattern.holiday_days),
            # -- Operating hours / speeds
            (create_range('period_high_speed'), periods.high.period_operation_speed),
            (create_range('period_high_time'), high_time),
            (create_range('period_standard_speed'), periods.standard.period_operation_speed),
            (create_range('period_standard_time'), standard_time),
            (create_range('period_minimum_speed'), minimum_speed),
            (create_range('period_minimum_time'), minimum_time),
        ]

        return [xl_data.XlItem(_sheet_name, *item) for item in items]
