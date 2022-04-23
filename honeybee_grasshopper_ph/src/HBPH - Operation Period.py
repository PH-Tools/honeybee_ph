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
Create a new Operation Period with a fractional rate and an hours/ day of operation. 
These Operationg Periods are used in the creation of HB-PH Schedules.
-
EM April 6, 2022
    Args:
        name_: (str) Optional name for the period (ie: "high", "low", "on", off", etc..)
        
        _hours_per_day: (0-24) The number of hours per day to operate at the
            specified rate.
        _operating_fraction: (0-1.0) The fractional value to operate at for the
            hours / day specified.
    
    Returns:
        op_period_: The HB-PH Operation Period. Connect this to an HB-PH Schedule
            in order to describe the operating fraction.
"""

import honeybee_energy_ph.properties.ruleset
import honeybee_ph_utils.preview

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Operation Period"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_06_2022')
if DEV:
    reload(honeybee_ph_utils.preview)

# ------------------------------------------------------------------------------
op_period_ = honeybee_energy_ph.properties.ruleset.DailyOperationPeriod.from_operating_hours(
    _hours_per_day or 0.0,
    _operating_fraction or 0.0,
    name_ or ''
)

# ------------------------------------------------------------------------------
honeybee_ph_utils.preview.object_preview(op_period_)