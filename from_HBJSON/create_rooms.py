# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions to build WUFI 'Rooms' from Honeybee-PH Spaces"""


from PHX import ventilation
from honeybee_ph import space
from honeybee_ph_utils.ventilation import hb_room_peak_ventilation_airflow_total


def create_room_from_space(_space: space.Space) -> ventilation.RoomVentilation:
    """Create a new RoomVentialtion object with attributes based on a Honeybee-PH Space

    Arguments:
    ----------
        * _space (space.Space): The Honeybee-PH Space to use as the source.

    Returns:
    --------
        * ventilation.RoomVentilation: The new Room with attributes based on the Honeybee Space.
    """

    new_room = ventilation.RoomVentilation()

    new_room.name = _space.full_name
    new_room.wufi_type = _space.wufi_type
    new_room.quantity = _space.quantity
    new_room.weighted_floor_area = _space.weighted_floor_area
    new_room.clear_height = _space.avg_clear_height
    new_room.net_volume = _space.net_volume

    peak_airflow_rate = hb_room_peak_ventilation_airflow_total(
        _space.host) * 3600  # m3/s --> m3/h
    new_room.ventilation_load.flow_supply = peak_airflow_rate
    new_room.ventilation_load.flow_extract = peak_airflow_rate

    return new_room
