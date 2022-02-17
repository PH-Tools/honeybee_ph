# -*- coding: utf-8 -*-
# -*- Python Version: 3.7 -*-

"""Functions used to create Project elements from the Honeybee-Model"""

from typing import Optional
from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier
from honeybee import model, room
from PHX import schedules, project
from honeybee_ph_utils.schedules import calc_four_part_vent_sched_values_from_hb_room
from honeybee_energy.schedule import ruleset


def _room_has_ph_style_ventilation(_hb_room: room.Room) -> bool:
    """Returns True if the HB Room has detailed PH-Style ventilation schedule information, False if not.

    Arguments:
    ---------
        * _hb_room (room.Room): The Honeybee Room to look at.
    Returns:
    --------
        * bool:
    """

    if not _hb_room.properties.energy:
        return False
    elif _hb_room.properties.energy.ventilation.schedule is None:
        return False
    elif not _hb_room.properties.energy.ventilation.schedule.properties.ph.operating_periods:
        return False
    else:
        return True


def _get_room_vent_pattern_key(_hb_room: room.Room) -> str:
    """Returns the right 'key' for the Honeybee Room's ventilation pattern.

    When translating HB-Style ventilation over, each HB-Room will get a different 
    utilization-pattern key since the schedule-periods will be dependant on the rooms' occupancy 
    and size.

    Is there a way to 'group' HB-Style ventilation patterns ahead of time? 

    If there is detailed PH-Style ventilation schedule info, that can be used instead 
    of the HB-Style.

    Arguments:
    ---------
        * _hb_room (room.Room): The Honeybee Room to look at.
    Returns:
    --------
        * str: The ventilation pattern 'key'
    """

    if _room_has_ph_style_ventilation(_hb_room):
        return _hb_room.properties.energy.ventilation.schedule.identifier
    else:
        # Room ventilation pattern needs to be created from the HB info and
        # take into account occupancy, size, etc...
        return _hb_room.properties.energy.ventilation.identifier


def _create_vent_pattern_from_hb_style(_hb_room: room.Room) -> schedules.UtilizationPatternVent:
    """Returns a new PHX Utilization Pattern (Vent) based on the HB-Room's E+ 
    HB-Style info found on the energy.ventilation

    This is used when no detailed PH-Style info is set by the user and you want to 
    convert over an existing E+/HB style ventilation object to PH-Style.

    Arguments:
    ----------
        * _hb_room (room.Room): The Honeybee Room to build the new PHX UtilizationPatternVent from.

    Returns:
    --------
        * schedules.UtilizationPatternVent: A new PHX Util Pattern.
    """

    new_util_pattern = schedules.UtilizationPatternVent()

    wufi_sched = calc_four_part_vent_sched_values_from_hb_room(_hb_room)

    new_util_pattern.operating_periods.high.period_operating_hours = wufi_sched.high.period_operating_hours
    new_util_pattern.operating_periods.high.period_operation_speed = wufi_sched.high.period_speed
    new_util_pattern.operating_periods.standard.period_operating_hours = wufi_sched.standard.period_operating_hours
    new_util_pattern.operating_periods.standard.period_operation_speed = wufi_sched.standard.period_speed
    new_util_pattern.operating_periods.basic.period_operating_hours = wufi_sched.basic.period_operating_hours
    new_util_pattern.operating_periods.basic.period_operation_speed = wufi_sched.basic.period_speed
    new_util_pattern.operating_periods.minimum.period_operating_hours = wufi_sched.minimum.period_operating_hours
    new_util_pattern.operating_periods.minimum.period_operation_speed = wufi_sched.minimum.period_speed

    # -- Keep all the IDs in alignment....
    new_util_pattern.identifier = _hb_room.properties.energy.ventilation.identifier
    new_util_pattern.id_num = new_util_pattern._count
    _hb_room.properties.energy.ventilation.schedule.properties.ph.id_num = new_util_pattern.id_num  # <--- Important!
    new_util_pattern.name = _hb_room.properties.energy.ventilation.display_name

    return new_util_pattern


def _create_vent_pattern_from_ph_style(_hb_room: room.Room) -> schedules.UtilizationPatternVent:
    """Returns a new PHX Utilization Pattern (Vent) based on the HB-Room's detailed 
    PH-Style info found on the energy.ventilation.schedule.properties.ph

    Arguments:
    ----------
        * _hb_room (room.Room): The Honeybee Room to build the new PHX UtilizationPatternVent from.

    Returns:
    --------
        * schedules.UtilizationPatternVent: A new PHX Util Pattern.
    """

    new_util_pattern = schedules.UtilizationPatternVent()

    ph_sched_props = _hb_room.properties.energy.ventilation.schedule.properties.ph

    new_util_pattern.operating_days = ph_sched_props.operating_days_wk
    new_util_pattern.operating_weeks = ph_sched_props.operating_wks_yr

    new_util_pattern.operating_periods.high.period_operating_hours = ph_sched_props.operating_periods.high.operation_hours
    new_util_pattern.operating_periods.high.period_operation_speed = ph_sched_props.operating_periods.high.operation_fraction
    new_util_pattern.operating_periods.standard.period_operating_hours = ph_sched_props.operating_periods.standard.operation_hours
    new_util_pattern.operating_periods.standard.period_operation_speed = ph_sched_props.operating_periods.standard.operation_fraction
    new_util_pattern.operating_periods.basic.period_operating_hours = ph_sched_props.operating_periods.basic.operation_hours
    new_util_pattern.operating_periods.basic.period_operation_speed = ph_sched_props.operating_periods.basic.operation_fraction
    new_util_pattern.operating_periods.minimum.period_operating_hours = ph_sched_props.operating_periods.minimum.operation_hours
    new_util_pattern.operating_periods.minimum.period_operation_speed = ph_sched_props.operating_periods.minimum.operation_fraction

    # -- Keep all the IDs in alignment....
    new_util_pattern.identifier = _hb_room.properties.energy.ventilation.schedule.identifier
    new_util_pattern.id_num = new_util_pattern._count
    _hb_room.properties.energy.ventilation.schedule.properties.ph.id_num = new_util_pattern.id_num  # <--- Important!
    new_util_pattern.name = _hb_room.properties.energy.ventilation.schedule.display_name

    return new_util_pattern


def build_util_pat_from_hb_room(_hb_room: room.Room) -> Optional[schedules.UtilizationPatternVent]:
    """Build a new Ventilation Utilization Schedule based on a Honeybee-Room's energy.ventilation values.

    Arguments:
    ----------
        *_hb_room (room.Room): The Honeybee-Room to get the ventilation pattern data from.

    Returns:
    --------
        * schedules.UtilizationPatternVent | None: The new Ventilation Pattern or None if no
            energy.ventilation or energy.ventilation.schedule is found on the room.
    """

    if _hb_room.properties.energy.ventilation is None:
        return None
    elif _hb_room.properties.energy.ventilation.schedule is None:
        return None
    elif _room_has_ph_style_ventilation(_hb_room):
        # -- The room's ventilation DOES have detailed user-inputs for operation periods, so use those.
        # -- This is the case when a Honeybee-PH component is used to build the PH_ScheduleRuleset
        new_util_pattern = _create_vent_pattern_from_ph_style(_hb_room)
    else:
        # -- There IS a ventilation.schedule, BUT there are no detailed
        # -- Passive House style user-input operation periods set on it. This is the case when a normal
        # -- HB-Ventilation ScheduleRuleset is converted over to a PH_ScheduleRuleset
        new_util_pattern = _create_vent_pattern_from_hb_style(_hb_room)

    # -- Ensure that the operating hours add up to exactly 24
    new_util_pattern.force_max_utilization_hours()

    return new_util_pattern


def _add_default_vent_schedule_to_Rooms(_hb_model: model.Model) -> model.Model:
    """Add a default ventilation.schedule to the HB Model's Rooms if they have None. 

    Some HB Programs do not have a ventilation.schedule. I *think* this means 
    constant operation. So add the constant value (1) default ventilation schedule to the room.

    Arguments:
    ----------
        * _hb_model (model.Model): The Honeybee Model to add the new constant value
            ventilation schedules to.

    Returns:
    --------
        * model.Model: The Honeybee Model with new ventilation schedules added to 
            any Rooms which were missing them.
    """

    type_limit = schedule_type_limit_by_identifier('Fractional')
    default_ventilation_schedule = ruleset.ScheduleRuleset.from_constant_value(
        'default_schedule', 1.0, type_limit)

    for hb_room in _hb_model.rooms:
        if hb_room.properties.energy.ventilation.schedule is None:
            hb_room.properties.energy.ventilation.unlock()
            hb_room.properties.energy.ventilation.schedule = default_ventilation_schedule
            hb_room.properties.energy.ventilation.lock()

    return _hb_model


def build_util_patterns_ventilation_from_HB_Model(_project: project.Project, _hb_model: model.Model) -> None:
    """Build the Utilization Pattern collection for Ventilation patterns and add to the PHX-Project.

    Arguments:
    ----------
        * _project (project.Project): The PHX-Project to add the new Utilization Patterns to.
        * _hb_model (model.Model): Then Honeybee Model to build up the new Utilization Patterns from.

    Returns:
    --------
        * None
    """

    # -- FIRST: Have to clean up the HB-ventilation schedules where they are missing.
    _hb_model = _add_default_vent_schedule_to_Rooms(_hb_model)

    # -- NEXT: Build up the new Ventilation Patterns from the Room's data
    for hb_room in _hb_model.rooms:
        vent_pattern_id = _get_room_vent_pattern_key(hb_room)
        if _project.utilization_patterns_ventilation.key_is_in_collection(vent_pattern_id):
            # -- This is just to help speed things up.
            # -- Don't re-make the util-pattern if it is already in collection.
            continue

        new_util_pattern = build_util_pat_from_hb_room(hb_room)
        _project.utilization_patterns_ventilation.add_new_util_pattern(new_util_pattern)
