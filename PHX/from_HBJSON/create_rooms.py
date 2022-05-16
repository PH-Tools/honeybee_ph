# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions to build PHX 'RoomVentilation' entities from Honeybee-PH Spaces"""

from PHX.model.loads import ventilation
from honeybee_ph import space
from honeybee_ph_utils.occupancy import hb_room_ppl_per_area
from honeybee_ph_utils.ventilation import hb_room_vent_flowrates


def calc_space_ventilation_flow_rate(_space: space.Space) -> float:
    """Calculate and return the total peak ventilation flow rate for a Space.

    This function will determine the peak flow by-person, by-area, by-zone, and by-ach
    and return the sum of all four flow-rate types.
    """
    (flow_per_person, flow_per_area,
        air_changes_per_hour, flow_per_zone) = hb_room_vent_flowrates(_space.host)
    # TODO: Unweighted or weighted? Which is right?
    ref_flr_area = _space.floor_area

    # -- Basic flow rates
    m3s_by_occupancy = ref_flr_area * hb_room_ppl_per_area(_space.host) * flow_per_person
    m3s_by_area = ref_flr_area * flow_per_area

    # -- Figure out % of the HB-Room that the Space represents
    # -- For the Flow-by-Zone and Flow-by_ACH, need to calc the Room total flow
    # -- and then calc the % of that total that this one space represents.
    hb_room_total_space_fa = _space.host.properties.ph.total_space_floor_area
    space_percent_of_total = ref_flr_area / hb_room_total_space_fa

    m3s_by_ach = (air_changes_per_hour * space_percent_of_total)/3600
    m3s_by_zone = flow_per_zone * space_percent_of_total

    return (m3s_by_occupancy + m3s_by_area + m3s_by_zone + m3s_by_ach) * 3600


def create_room_from_space(_space: space.Space) -> ventilation.PhxRoomVentilation:
    """Create a new RoomVentilation object with attributes based on a Honeybee-PH Space

    Arguments:
    ----------
        * _space (space.Space): The Honeybee-PH Space to use as the source.

    Returns:
    --------
        * ventilation.RoomVentilation: The new PHX-Room with attributes based on the Honeybee Space.
    """
    new_room = ventilation.PhxRoomVentilation()

    new_room.display_name = _space.full_name
    new_room.wufi_type = _space.wufi_type
    new_room.quantity = _space.quantity
    new_room.floor_area = _space.floor_area
    new_room.weighted_floor_area = _space.weighted_floor_area
    new_room.clear_height = _space.avg_clear_height
    new_room.net_volume = _space.net_volume

    # -- Ventilation flow rates
    space_peak_flow_rate = calc_space_ventilation_flow_rate(_space)
    new_room.flow_rates.flow_supply = space_peak_flow_rate
    new_room.flow_rates.flow_extract = space_peak_flow_rate
    new_room.vent_pattern_id_num = _space.host.properties.energy.ventilation.schedule.properties.ph.id_num

    # -- Ventilation Equipment
    if _space.host.properties.energy.hvac.properties.ph.ventilation_system:
        new_room.vent_unit_id_num = _space.host.properties.energy.hvac.properties.ph.ventilation_system.id_num

    return new_room
