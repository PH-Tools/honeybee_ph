# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for converting Honeybee schedules into WUFI schedules."""

from honeybee import room
from honeybee_ph_utils import ventilation, histogram


def calc_four_part_vent_sched_values_from_hb_room(_hb_room, _use_dcv=True):
    # type: (room.Room, bool) -> dict
    """Returns a WUFI-Style four_part schedule values for the Ventilation airflow, based on the HB Room.

    Arguments:
    ----------
        * _hb_room (): The Honyebee Room to build the schedule for.
        * _use_dcv (bool): Use Demand-Controled Ventilation? default=True. Set 'True' in
            order to take the Occupancy Schedule and Airflow-per-person loads into account.
            If False, will asssume constant airflow for occupancy-related ventilation loads.

    Returns:
    --------
        * dict: The four_part Sched values. * dict: ie: 
        {0:{
            'average_value':12, # <-- (default = meters/second)
            'frequency':0.25},
        1:{
            ...
        }, 
        ...}
    """

    # -------------------------------------------------------------------------
    # 1) Calc the Peak Airflow Loads (for Ventilation, for Occupancy)
    vent_m3s_total, occ_m3s_total = ventilation.hb_room_peak_airflows(_hb_room)

    # -------------------------------------------------------------------------
    # 2) Get the Occupancy + Ventilation Schedules hourly value generators
    # -- Use try/ excpting since some honeybee programs don't have these attrs.
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
    hourly_m3s_for_vent = (vent_m3s_total * _ for _ in schd_vent_values)
    if _use_dcv:
        # -- YES DCV = Modulate the flow rates based on occupancy level.
        hourly_m3s_for_occ = (occ_m3s_total * _ for _ in schd_occ_values)
    else:
        # -- No DCVC = Use constant flow rate, regardless of occupancy level.
        hourly_m3s_for_occ = (occ_m3s_total * 1 for _ in schd_occ_values)

    #  ------------------------------------------------------------------------
    # 4) Calc the Percentage of Peak airflow for each hourly value
    peak_total_m3s = vent_m3s_total + occ_m3s_total
    if peak_total_m3s == 0:
        return {0: {"average_value": 1.0, "frequency": 1.0}}

    hourly_total_vent_percentage_rate = [
        (a + b) / peak_total_m3s for a, b in zip(hourly_m3s_for_vent, hourly_m3s_for_occ)
    ]

    #  ------------------------------------------------------------------------
    # 6) Histogram that shit
    four_part_sched_dict = histogram.generate_histogram(
        _data=hourly_total_vent_percentage_rate,
        _num_bins=4,
    )

    return four_part_sched_dict
