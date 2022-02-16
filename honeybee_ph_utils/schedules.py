# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for converting Honeybee schedules into WUFI schedules."""

from honeybee import room
from honeybee_ph_utils import ventilation, histogram


class SchedItem:
    def __init__(self, _av, _fr):
        # type: (float, float) -> None
        self.period_speed = _av
        self.period_operating_hours = _fr

    def __str__(self):
        return '{}(average_value={!r}, frequency={!r})'.format(self.__class__.__name__, self.period_speed, self.period_operating_hours)

    def __repr__(self):
        return str(self)


class FourPartSched:
    def __init__(self, _h, _s, _b, _m):
        # type: (SchedItem, SchedItem, SchedItem, SchedItem) -> None
        self.high = _h
        self.standard = _s
        self.basic = _b
        self.minimum = _m

    def __str__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format(self.__class__.__name__, self.high, self.standard, self.basic, self.minimum)

    def __repr__(self):
        return str(self)


def calc_four_part_vent_sched_values_from_hb_room(_hb_room, _use_dcv=True):
    # type: (room.Room, bool) -> FourPartSched
    """Returns a WUFI-Style four_part schedule values for the Ventilation airflow, based on the HB Room.

    Arguments:
    ----------
        * _hb_room (): The Honeybee Room to build the schedule for.
        * _use_dcv (bool): Use Demand-Controlled Ventilation? default=True. Set 'True' in
            order to take the Occupancy Schedule and Airflow-per-person loads into account.
            If False, will assume constant airflow for occupancy-related ventilation loads.

    Returns:
    --------
        * namedtuple: ie:
            (
                high=('average_value':18, 'frequency':0.25),
                standard=('average_value':12, 'frequency':0.25),
                basic=('average_value':10, 'frequency':0.25),
                minimum=('average_value':8, 'frequency':0.25),
            )
    """

    # -------------------------------------------------------------------------
    # 1) Calc the Peak Airflow Loads (for Ventilation, for Occupancy)
    vent_m3s_total = ventilation.hb_room_peak_ventilation_airflow_by_zone(_hb_room)
    occ_m3s_total = ventilation.hb_room_peak_ventilation_airflow_by_occupancy(_hb_room)

    # -------------------------------------------------------------------------
    # 2) Get the Occupancy + Ventilation Schedules hourly value generators
    # -- Use try/ excepting since some honeybee programs don't have these attrs.
    # -- If schedule is missing, use a default constant value (1) schedule.
    try:
        schd_occ_values = _hb_room.properties.energy.people.occupancy_schedule.values()
    except AttributeError:
        schd_occ_values = (1 for _ in range(8760))

    try:
        schd_vent_values = _hb_room.properties.energy.ventilation.schedule.values()
    except AttributeError:
        schd_vent_values = (1 for _ in range(8760))

    # -------------------------------------------------------------------------
    # 3) Calc the Hourly Airflows, taking the Schedules into account
    # Note: Should BOTH the by_zone AND the by_person flow-rates be modulated?
    # currently yes: both are being affected. Should ONLY the by_person rates be affected?
    if _use_dcv:
        # -- YES DCV = Modulate the flow rates based on occupancy level.
        hourly_m3s_for_occ = (occ_m3s_total * _ for _ in schd_occ_values)
        hourly_m3s_for_vent = (vent_m3s_total * _ for _ in schd_vent_values)
    else:
        # -- No DCV = Use constant flow rate, regardless of occupancy level.
        hourly_m3s_for_occ = (occ_m3s_total * 1 for _ in schd_occ_values)
        hourly_m3s_for_vent = (vent_m3s_total * 1 for _ in schd_vent_values)

    #  ------------------------------------------------------------------------
    # 4) Calc the Percentage of Peak airflow for each hourly value
    peak_total_m3s = vent_m3s_total + occ_m3s_total
    if peak_total_m3s == 0:
        return FourPartSched(
            SchedItem(1.0, 1.0),
            SchedItem(0.0, 0.0),
            SchedItem(0.0, 0.0),
            SchedItem(0.0, 0.0)
        )

    hourly_total_vent_percentage_rate = [
        (a + b) / peak_total_m3s for a, b in zip(hourly_m3s_for_vent, hourly_m3s_for_occ)
    ]

    #  ------------------------------------------------------------------------
    # 6) Histogram that shit
    # -- Average_value = the speed, 'frequency' = hours per day
    four_part_sched_dict = histogram.generate_histogram(
        _data=hourly_total_vent_percentage_rate,
        _num_bins=4,
    )

    # --- Organize Output
    output = FourPartSched(
        SchedItem(
            four_part_sched_dict.get(0, {}).get('average_value', 0),
            four_part_sched_dict.get(0, {}).get('frequency', 0) * 24,
        ),
        SchedItem(
            four_part_sched_dict.get(1, {}).get('average_value', 0),
            four_part_sched_dict.get(1, {}).get('frequency', 0) * 24,
        ),
        SchedItem(
            four_part_sched_dict.get(2, {}).get('average_value', 0),
            four_part_sched_dict.get(2, {}).get('frequency', 0) * 24,
        ),
        SchedItem(
            four_part_sched_dict.get(3, {}).get('average_value', 0),
            four_part_sched_dict.get(3, {}).get('frequency', 0) * 24,
        )
    )

    return output
