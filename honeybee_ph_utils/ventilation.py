# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Honeybee-Energy Ventilation Loads and Schedules."""

from honeybee import room
from honeybee_ph_utils import occupancy


def hb_room_peak_airflows(_hb_room):
    # type: (room.Room) -> tuple[float, float]
    """Returns a tuple of the peak airflow rates for Zone-based Ventilation, and Occupancy-based Ventilation.

    Not all honeybee-Rooms have ventilation loads. If that is the case, will return (0, 0).

    Arguments:
    ----------
        * _hb_room (room.Room): The honeyebee room to calculate values for.

    Returns:
    --------
        * tuple[float, float]
            * [0] : Total airflow  (m3/s) For the Ventilation-based airflow (per zone, per area, ach).
            * [1] : Total airflow  (m3/s) For the Occupancy-based airflow (per person).
    """

    peak_occupancy = occupancy.hb_room_peak_occupancy(_hb_room)

    try:
        vent_m3s_for_zone = _hb_room.properties.energy.ventilation.flow_per_zone
        vent_m3s_for_area = _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
        vent_m3h_for_ach = (
            _hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume) / 3600

        vent_m3s_total = vent_m3s_for_zone + vent_m3s_for_area + vent_m3h_for_ach
        occ_m3s_total = _hb_room.properties.energy.ventilation.flow_per_person * peak_occupancy
    except AttributeError:
        vent_m3s_total = 0
        occ_m3s_total = 0

    return (vent_m3s_total, occ_m3s_total)


def hb_toom_total_ventilation_m3sec(_hb_room):
    # type: (room.Room) -> float
    """Returns the total peak ventilation airflow for a Honeybee Room

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The Honeybee Room to calculate values of.

    Returns:
    --------
        * (float): The Honeybee Room's total ventilation airflow in M3/second.
    """

    flow_per_achour = _hb_room.properties.energy.ventilation.air_changes_per_hour * _hb_room.volume
    # Convert from Air-Change/hour -> Air-Change/minute
    flow_per_acminute = flow_per_achour / 3600
    flow_per_area = _hb_room.properties.energy.ventilation.flow_per_area * _hb_room.floor_area
    flow_per_zone = _hb_room.properties.energy.ventilation.flow_per_zone
    room_avg_occupancy = occupancy.hb_room_annual_avg_occupancy(_hb_room)
    flow_per_person = _hb_room.properties.energy.ventilation.flow_per_person * room_avg_occupancy

    total_vent = 0.0
    total_vent += flow_per_acminute
    total_vent += flow_per_area
    total_vent += flow_per_zone
    total_vent += flow_per_person

    return total_vent


def hb_room_avg_ventilation_ach(_hb_room):
    # type: (room.Room) -> float
    """Returns the honeybee-Room's average annual ACH due to ventilation.

    This value includes the effect of mechanical ventilation and windows, and the
    variation in occupancy (assumes demand-controlled ventilation flow rates) BUT
    excludes infiltration airflow.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeybee-Room to calcualte the ventilation ACH for.

    Returns:
    --------
        * (float) The Room's ventilation average annual ACH (air changes per hour).
    """

    # -- First, find the average anuual flow-fraction
    # TODO: Need func....
    hb_ventilation_schedule = _hb_room.properties.energy.ventilation.schedule
    if not hb_ventilation_schedule:
        avg_flow_fraction = 1.0
    else:
        avg_flow_fraction = 0.0

    # -- Calc the annual average airflow (m3/h)
    design_airflow_m3s = hb_toom_total_ventilation_m3sec(_hb_room)
    design_airflow_m3h = design_airflow_m3s * 3600
    avg_annual_flow_m3h = design_airflow_m3h * avg_flow_fraction

    return avg_annual_flow_m3h / _hb_room.volume
