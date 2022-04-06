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
Create and apply a new Passive House fresh-air ventilation system to one or more Honeybee-Rooms. 
This component will suplement the normal honeybee-hvac fresh-aor equipment with additional 
detailed 'Passive House Style' inputs and parameters for elements like ducting and the HRV itself.
-
EM February 1, 2022
    Args:
        system_name_: (str) The name to give to the fresh-air ventilation system.
            
        system_type_: Choose either:
            1-Balanced PH ventilation with HR [Default]
            2-Extract air unit
            3-Only window ventilation
        
        vent_unit_: (Optional[]) The Venilator (ERV/HRV) to use to ventilate the
            honeybee-Rooms.
        
        duct_01_: The supply cold-air duct (from ventilator to the building-envelope)
        
        duct_02_: The exhaust cold-air duct (from ventilator to the building-envelope)
        
        _hb_rooms: (list[Room]) The Honeybee Rooms to add the new Passive House
            fresh-air ventilation system to.
    Returns:
    hb_rooms_ (list[Room]): The Honeybee Rooms with the new fresh-air ventilation
        system attributes added.
"""

import honeybee_energy_ph.hvac.ventilation
import honeybee_ph_utils.preview

# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Vent HVAC"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='FEB_01_2022')
if DEV:
    reload(honeybee_energy_ph.hvac.ventilation)
    reload(honeybee_ph_utils.preview)

# ------------------------------------------------------------------------------
# -- Build a new Passive House style ventilation system
ph_ventilation_sys = honeybee_energy_ph.hvac.ventilation.PhVentilationSystem()
ph_ventilation_sys.name = system_name_ or ph_ventilation_sys.name
ph_ventilation_sys.sys_type = system_type_ or 1
ph_ventilation_sys.ventilation_unit = vent_unit_ or honeybee_energy_ph.hvac.ventilation.Ventilator()

# ------------------------------------------------------------------------------
# -- Add the ventilator to the room's hb-e hvac
hb_rooms_ = []
for room in _hb_rooms:
    new_room = room.duplicate()
    
    # -- Set the new room's IdealAir values to match the PH-Ventilator Inputs
    if ph_ventilation_sys.ventilation_unit:
        new_hb_ideal_air_sys = room.properties.energy.hvac.duplicate()
        new_hb_ideal_air_sys.sensible_heat_recovery = ph_ventilation_sys.ventilation_unit.sensible_heat_recovery
        new_hb_ideal_air_sys.latent_heat_recovery = ph_ventilation_sys.ventilation_unit.latent_heat_recovery
        new_hb_ideal_air_sys.demand_controlled_ventilation = True
        new_room.properties.energy.hvac= new_hb_ideal_air_sys
    
    new_room.properties.energy.hvac.properties.ph.ventilation_system = ph_ventilation_sys
    
    hb_rooms_.append(new_room)

# ------------------------------------------------------------------------------
honeybee_ph_utils.preview.object_preview(ph_ventilation_sys)