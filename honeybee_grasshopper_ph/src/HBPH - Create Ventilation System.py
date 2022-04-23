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
Create new PH-Style Ventilation Equpment which can be aded to HB-Rooms.
-
EM April 16, 2022
    Args:
        system_name_: (str) The name to give to the fresh-air ventilation system.
            
        system_type_: Choose either -
            1-Balanced PH ventilation with HR [Default]
            2-Extract air unit
            3-Only window ventilation
        
        vent_unit_: (Optional[]) The Venilator (ERV/HRV) to use to ventilate the
            honeybee-Rooms.
        
        duct_01_: The supply cold-air duct (from ventilator to the building-envelope)
        
        duct_02_: The exhaust cold-air duct (from ventilator to the building-envelope)
        
    Returns:
        vent_system_: The new HBPH Ventilation System object.
"""

from honeybee_energy_ph.hvac import ventilation
from honeybee_ph_utils import preview

# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Ventilation System"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_16_2022')
if DEV:
    reload(ventilation)
    reload(preview)

# ------------------------------------------------------------------------------
# -- Build a new Passive House style ventilation system
vent_system_ = ventilation.PhVentilationSystem()
vent_system_.display_name = system_name_ or vent_system_.display_name
vent_system_.sys_type = system_type_ or 1
vent_system_.ventilation_unit = vent_unit_ or ventilation.Ventilator()

# ------------------------------------------------------------------------------
preview.object_preview(vent_system_)