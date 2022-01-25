# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions used to create Project elements from the Honeybee-Model"""

from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier
from honeybee import model, room
from PHX import schedules, project
from honeybee_ph_utils.schedules import calc_four_part_vent_sched_values_from_hb_room
from honeybee_energy_ph.schedule import ruleset


def build_util_pat_from_hb_room(_hb_room: room.Room) -> schedules.UtilizationPatternVent:
    """Build a new Ventilation Utilization Schedule based on a Honeybee-Room's energy.ventilation values.

    Arguments:
    ----------
        *_hb_room (room.Room): The Honeybee-Room to get the ventilation pattern data from.

    Returns:
    --------
        * schedules.UtilizationPatternVent: The new Ventilation Pattern
    """
    new_util_pattern = schedules.UtilizationPatternVent()

    if not _hb_room.properties.energy.ventilation.schedule.properties.ph.operating_periods:
        # -- There IS a ventilation.schedule, BUT there are no detailed
        # -- user-input operation periods set on it. This is the case when a normal
        # -- HB-Ventilation ScheduleRuleset is converted over to a PH_ScheduleRuleset

        wufi_sched = calc_four_part_vent_sched_values_from_hb_room(_hb_room)

        new_util_pattern.operating_periods.high.period_operating_hours = wufi_sched.high.period_operating_hours
        new_util_pattern.operating_periods.high.period_operation_speed = wufi_sched.high.period_speed
        new_util_pattern.operating_periods.standard.period_operating_hours = wufi_sched.standard.period_operating_hours
        new_util_pattern.operating_periods.standard.period_operation_speed = wufi_sched.standard.period_speed
        new_util_pattern.operating_periods.basic.period_operating_hours = wufi_sched.basic.period_operating_hours
        new_util_pattern.operating_periods.basic.period_operation_speed = wufi_sched.basic.period_speed
        new_util_pattern.operating_periods.minimum.period_operating_hours = wufi_sched.minimum.period_operating_hours
        new_util_pattern.operating_periods.minimum.period_operation_speed = wufi_sched.minimum.period_speed

    elif _hb_room.properties.energy.ventilation.schedule.properties.ph.operating_periods:
        # -- The room's ventilation does have detailed user-inputs for operation periods, so use those.
        # -- This is the case when a Honeybee-PH component is used to build the PH_ScheduleRuleset
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
    new_util_pattern.identifier = _hb_room.properties.energy.ventilation.identifier
    new_util_pattern.id_num = new_util_pattern._count
    _hb_room.properties.energy.ventilation.schedule.properties.ph.id_num = new_util_pattern.id_num  # <--- Important!
    new_util_pattern.name = _hb_room.properties.energy.ventilation.display_name

    # -- Ensure that the operting hours add up to exactly 24
    new_util_pattern.force_max_utilization_hours()

    return new_util_pattern


def add_default_vent_schedule(_hb_model: model.Model, _sched: ruleset.PH_ScheduleRuleset) -> model.Model:
    """Add a default ventilation.schedule is the room has None. 

    Some HB Programs do not have a ventilation.schedule. I *think* this means 
    constant operation. So add the default ventilation schedule to the room.

    Arguments:
    ----------
        * _hb_model (model.Model):
        * _sched (ruleset.PH_ScheduleRuleset)

    Returns:
    --------
        * model.Model: 
    """

    for hb_room in _hb_model.rooms:
        if hb_room.properties.energy.ventilation.schedule is None:
            hb_room.properties.energy.ventilation.unlock()
            hb_room.properties.energy.ventilation.schedule = _sched
            hb_room.properties.energy.ventilation.lock()

    return _hb_model


def build_util_patterns_ventilation_from_HB_Model(_project: project.Project, _hb_model: model.Model) -> None:
    """Build the Utilization Pattern collection for Ventilation patterns and add to the PHX-Project.

    Arguments:
    ----------
        * _project (project.Project): The PHX-Project to add the new Utilization Patterns to.
        * _hb_model (model.Model): 

    Returns:
    --------
        * None
    """
    # -- FIRST: Havr to clean up the HB-ventilation schedules where they are missing.
    type_limit = schedule_type_limit_by_identifier('Fractional')
    default_ventilation_schedule = ruleset.PH_ScheduleRuleset.from_constant_value(
        'default_schedule', 1.0, type_limit)
    _hb_model = add_default_vent_schedule(_hb_model, default_ventilation_schedule)

    # -- Build up the new Ventilation Patterns
    for hb_room in _hb_model.rooms:
        vent_pattern_id = hb_room.properties.energy.ventilation.identifier
        if _project.utilisation_patterns_ventilation.key_is_in_collection(vent_pattern_id):
            # -- This is just to help speed things up.
            # -- Don't re-make the util pattern if it is already in collection.
            continue

        pat = build_util_pat_from_hb_room(hb_room)
        _project.utilisation_patterns_ventilation.add_new_util_pattern(pat)
