# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Utility functions for working with Honeybee-Energy Occupancy Loads and Schedules"""

from honeybee import room
import statistics


def hb_room_ppl_per_area(_hb_room):
    # type: (room.Room) -> float
    """Returns a honeybee-Room's occupancy load (people_per_area).

    Note all  honeybee-Rooms have an occupancy (stairs, etc) and so if there is 
    no energy.pepple found, will return 0

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeyebee-Room to get the value for.

    Returns:
    --------
        * (float): The honeybee-Room's occupancy load (people_per_area)
    """
    try:
        return _hb_room.properties.energy.people.people_per_area
    except AttributeError:
        return 0.0


def hb_room_peak_occupancy(_hb_room):
    # type: (room.Room) ->  float
    """Returns a peak occupancy (# ppl) of a honeybee-Room. 

    Not all honeybee rooms have an occupancy (stairs, etc..) and so if there is 
    no energy.people found, will return 0.

    Arguments:
    ----------
        * _hb_room (honeybee.room.Room): The honeyebee-Room to calculate values for.

    Returns:
    --------
        * (float): The honeybee-Room's peak occupancy (total number of people)
    """
    try:
        ppl_per_area = _hb_room.properties.energy.people.people_per_area
    except AttributeError:
        ppl_per_area = 0

    return _hb_room.floor_area * ppl_per_area


def hb_room_annual_avg_occupancy(_hb_room):
    # type: (room.Room) -> float
    """Returns the annual average occupancy (# ppl) of a honeybee-Room.

    Will return the 'mean_occupancy' if there is one on the Schedule. Otherwise 
    will calculate the value.

    Arguments:
    ----------
        * _hb_room (room.Room): The honeyebee-Room to calculate values for.

    Returns:
    --------
        * (float): The honeybee-Room's average annual occupancy (total number of people).
    """

    peak_occupancy = hb_room_peak_occupancy(_hb_room)
    try:
        mean_occupancy = _hb_room.properties.energy.people.occupancy_schedule.mean_occupancy
    except AttributeError:
        mean_occupancy = statistics.mean(
            _hb_room.properties.energy.people.occupancy_schedule.values())

    return peak_occupancy * mean_occupancy
