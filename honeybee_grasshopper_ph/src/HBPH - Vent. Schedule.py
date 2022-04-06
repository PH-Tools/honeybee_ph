#
# Honeybee-PH: A Plugin for adding Passive-House data to LadybugTools Honeybee-Energy Models
#
# This component is part of the PH-Tools toolkit <https://github.com/PH-Tools>.
#
# Copyright (c) 2022, PH-Tools and bldgtyp, llc <phtools@bldgtyp.com>
# Honeybee-PH is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3 of the License,
# or (at your option) any later version.
#
# Honeybee-PH is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License
# see <https://github.com/PH-Tools/honeybee_ph/blob/main/LICENSE>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
#
"""
Create a new Honeybee-Energy ScheduleRuleset for the fresh-air ventilation system 
operation using 'Passive House' style inputs. These inputs will be used to create an 
equivalent constant-value fresh air ventilation operation scheduled which can then be
used to control the Honeybee-Energy fresh air ventilation. Note that the values here
will also be stored and used as detailed inputs into  WUFI-Passive or PHPP upon export.
-
EM January 29, 2022
    Args:
        _name_: Optional name for the Ventilation Schedule
        
        operating_day_per_week_: (default=7) Value for the number of days/week to run
            at the specified flowrates.
        operating_weeks_per_year_: (default=52) Value for the number of weeks/year to 
            run at the specified flowrates.
        
        _op_period_high: Enter an Operation-Period decribing the high-speed period.
        _op_period_standard: Enter an Operation-Period decribing the normal-speed period.
        _op_period_basic: Enter an Operation-Period decribing the low-speed period.
        _op_period_minimum: Enter an Operation-Period decribing the minimum-speed period.
    
    Returns:
        ventilation_sch_: The HB-Ventilation Schedule which can be applied to HB Rooms
"""

import Grasshopper.Kernel as ghk
from honeybee.typing import clean_and_id_ep_string, clean_ep_string
from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier
from honeybee_energy.schedule.ruleset import ScheduleRuleset

import honeybee_ph_utils.preview
import honeybee_energy_ph.properties.ruleset

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Vent. Schedule"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JAN_29_2022')
if DEV:
    reload(honeybee_ph_utils.preview)
    reload(honeybee_energy_ph.properties.ruleset)
    reload(honeybee_energy_ph._extend_honeybee_energy_ph)

# ------------------------------------------------------------------------------
# -- Build the PhProperties object based on any PH-Style user-inputs on the honeybee-schedule
ph_properties = honeybee_energy_ph.properties.ruleset.ScheduleRulesetPhProperties(
    _host=None)

ph_properties.operating_days_wk = operating_day_per_week_ or 7
ph_properties.operating_wks_yr = operating_weeks_per_year_ or 52

ph_properties.operating_periods.high = _op_period_high or honeybee_energy_ph.properties.ruleset.DailyOperationPeriod(
    0, 0)
ph_properties.operating_periods.standard = _op_period_standard or honeybee_energy_ph.properties.ruleset.DailyOperationPeriod(
    0, 0)
ph_properties.operating_periods.basic = _op_period_basic or honeybee_energy_ph.properties.ruleset.DailyOperationPeriod(
    0, 0)
ph_properties.operating_periods.minimum = _op_period_minimum or honeybee_energy_ph.properties.ruleset.DailyOperationPeriod(
    0, 0)

# ------------------------------------------------------------------------------
# -- User Warnings
msg = ph_properties.validate_operating_period_hours()
if msg:
    ghenv.Component.AddRuntimeMessage(ghk.GH_RuntimeMessageLevel.Warning, msg)

# ------------------------------------------------------------------------------
# -- Create the HB-ScheduleRuleset's constant value based on the user-input
hb_schedule_const_value = ph_properties.annual_average_operating_fraction

# ------------------------------------------------------------------------------
# -- Create a new constant-value honeybee-energy-ScheduleRuleset object
# -- Set the properties.ph with the user-determined values above.
name = clean_and_id_ep_string('ConstantSchedule') if _name_ is None else \
    clean_ep_string(_name_)
type_limit = schedule_type_limit_by_identifier('Fractional')
ventilation_sch_ = ScheduleRuleset.from_constant_value(
    name, hb_schedule_const_value, type_limit)
ph_properties._host = ventilation_sch_._properties
ventilation_sch_._properties._ph = ph_properties
