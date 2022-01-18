# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to create Project elements from the Honeybee-Model"""

from honeybee import model, room
from PHX import schedules, project
from honeybee_ph_utils.schedules import calc_four_part_vent_sched_values_from_hb_room


def build_util_pat_from_hb_room(_hb_room: room.Room) -> schedules.UtilizationPatternVent:
    """Build a new Ventilation Utilization Schedule based on a Honeybee-Room's Attributes.

    Arguments:
    ----------
        *_hb_room (room.Room): The Honeybee-Room to get the ventilation pattern data from.

    Returns:
    --------
        * schedules.UtilizationPatternVent: The new Ventilation Pattern
    """
    new_util_pattern = schedules.UtilizationPatternVent()

    # --
    new_util_pattern.identifier = _hb_room.properties.energy.ventilation.identifier
    new_util_pattern.id_num = new_util_pattern._count
    new_util_pattern.name = _hb_room.properties.energy.ventilation.display_name

    # --
    wufi_sched = calc_four_part_vent_sched_values_from_hb_room(_hb_room)
    new_util_pattern.operating_periods.high.period_operating_hours = wufi_sched.high.period_speed
    new_util_pattern.operating_periods.high.period_operation_speed = wufi_sched.high.period_operating_hours
    new_util_pattern.operating_periods.standard.period_operating_hours = wufi_sched.standard.period_speed
    new_util_pattern.operating_periods.standard.period_operation_speed = wufi_sched.standard.period_operating_hours
    new_util_pattern.operating_periods.basic.period_operating_hours = wufi_sched.basic.period_speed
    new_util_pattern.operating_periods.basic.period_operation_speed = wufi_sched.basic.period_operating_hours
    new_util_pattern.operating_periods.minimum.period_operating_hours = wufi_sched.minimum.period_speed
    new_util_pattern.operating_periods.minimum.period_operation_speed = wufi_sched.minimum.period_operating_hours

    # -- Ensure that the hours add up to 24
    new_util_pattern.force_max_utilization_hours()

    return new_util_pattern


def build_util_patterns_ventilation_from_HB_Model(_project: project.Project, _hb_model: model.Model) -> None:
    """Build the Utilization Pattern collection for Ventilation patterns.

    Arguments:
    ----------
        * _project (project.Project):
        * _hb_model (model.Model): 

    Returns:
    --------
        * None
    """
    for hb_room in _hb_model.rooms:
        vent_pattern_id = hb_room.properties.energy.ventilation.identifier
        if _project.utilisation_patterns_ventilation.key_is_in_collection(vent_pattern_id):
            # -- This is just to help speed things up.
            # -- Don't re-make the util pattern if it is already in collection.
            continue

        pat = build_util_pat_from_hb_room(hb_room)
        _project.utilisation_patterns_ventilation.add_new_util_pattern(pat)
