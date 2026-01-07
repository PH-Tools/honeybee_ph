# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Honeybee-Energy Ventilation Loads and Schedules."""


from honeybee_ph_utils import occupancy


def hb_room_vent_flowrates(_hb_room):
    # type: (room.Room) -> tuple[float, float, float, float]
    """Return the honeybee-Room's four ventilation flow rates in m3/s, or 0 if no ventilation
        program is found on the room.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeyebee-Room to get the value for.

    Returns:
    --------
        * tuple[float, float, float, float]:
            - [0] (m3s): The honeybee-Room's ventilation flow_per_person
            - [1] (m3s): The honeybee-Room's ventilation flow_per_area
            - [2] (m3s): The honeybee-Room's ventilation flow_by_air_changes_per_hour
            - [3] (m3s): The honeybee-Room's ventilation flow_per_zone
    """
    default_flow_rates = (0.0, 0.0, 0.0, 0.0)
    try:
        vent_program = _hb_room.properties.energy.ventilation
    except:
        return default_flow_rates

    if vent_program is None:
        # -- Not all programs have a ventilation. If so, return 0 for all flows.
        return default_flow_rates
    else:
        return (
            vent_program.flow_per_person,
            vent_program.flow_per_area,
            vent_program.air_changes_per_hour * _hb_room.volume / 3600,
            vent_program.flow_per_zone,
        )


def hb_room_peak_ventilation_airflow_by_zone(_hb_room):
    # type: (room.Room) -> float
    """Return the Peak Ventilation Airflow (m3/s) for the 'Zone' related elements of a honeybee-Room.

    This will return a sum of the room's flow_per_zone, flow_per_area, and air_changes_per_hour
    but will ignore any occupancy related flow-rates. To get the occupancy-related ventilation
    airflow, use the 'hb_room_peak_ventilation_airflow_by_occupancy' function and to get the
    total airflow (by-zone + by-occupancy) use the 'hb_room_peak_ventilation_airflow_total'

    Arguments:
    ----------
        * _hb_room (room.Room):

    Returns:
    --------
        * float (m/s): Total airflow  (m3/s) For the Ventilation-based airflow (per zone, per area, ach).
    """
    try:
        rm_vent_program = _hb_room.properties.energy.ventilation
        vent_m3s_for_zone = rm_vent_program.flow_per_zone
        vent_m3s_for_area = rm_vent_program.flow_per_area * _hb_room.floor_area
        vent_m3h_for_ach = rm_vent_program.air_changes_per_hour * _hb_room.volume / 3600
        return vent_m3s_for_zone + vent_m3s_for_area + vent_m3h_for_ach
    except AttributeError:
        return 0.0


def hb_room_peak_ventilation_airflow_by_occupancy(_hb_room):
    # type: (room.Room) -> float
    """Return the Peak Ventilation Airflow (m3/s) for the 'Occupancy' related elements of a honeybee-Room.

    This will return the room's flow_per_person, but will ignore any 'zone' related flow-rates.
    such as flow_per_zone or flow_per_area, To get the zone-related ventilation
    airflow, use the 'hb_room_peak_ventilation_airflow_by_zone' function and to get the
    total airflow (by-zone + by-occupancy) use the 'hb_room_peak_ventilation_airflow_total'

    Arguments:
    ----------
        * _hb_room (room.Room):

    Returns:
    --------
        * float (m/s): Total airflow  (m3/s) For the Occupancy-based airflow (per person).
    """

    try:
        peak_occupancy = occupancy.hb_room_peak_occupancy(_hb_room)
        return _hb_room.properties.energy.ventilation.flow_per_person * peak_occupancy
    except AttributeError:
        return 0.0


def hb_room_peak_ventilation_airflow_total(_hb_room):
    # type: (room.Room) -> float
    """Return the total peak ventilation flow rate (m/s). Total of occupancy- and zone-related airlfows.

    Not all honeybee-Rooms have ventilation loads. If that is the case, will return 0.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeyebee room to calculate values for.

    Returns:
    --------
        * float: The total ventilation peak airflow for the honeybee-Room.
    """

    vent_m3s_total = hb_room_peak_ventilation_airflow_by_zone(_hb_room)
    occ_m3s_total = hb_room_peak_ventilation_airflow_by_occupancy(_hb_room)

    return vent_m3s_total + occ_m3s_total
