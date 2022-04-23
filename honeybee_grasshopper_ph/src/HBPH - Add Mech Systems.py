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
Add HBPH mechanical ventilation, heating, and cooling to HB-Rooms.
-
EM April 16, 2022
    Args:
        _vent_system: (PhVentilationSystem) Enter the type of heating system.
        
        _space_heating_systems: (list[PhHeatingSystem]) A list of the HBPH Heating Systems to add to the hb-rooms.
        
        _space_cooling_systems: (list[PhCoolingSystem]) A list of the HBPH Cooling Systems to add to the hb-rooms.
        
        _hb_rooms: (list[Room]) A list of the hb-rooms to add the mechanical systems to.
        
    Returns:
        hb_rooms_: The input hb-rooms with the new HBPH Mechanical Systems added.
"""

from copy import copy

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add Mech Systems"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_16_2022')
if DEV:
    pass


#-------------------------------------------------------------------------------
hb_rooms_ = []
for hb_room in _hb_rooms:
    # -- Build up the new HB-HVAC
    new_hvac = copy(hb_room.properties.energy.hvac.duplicate())
    
    # --------------------------------------------------------------------------
    # -- Fresh-Air Ventilation
    if _vent_system: print 'True=', _vent_system
    if _vent_system:
        new_hvac.properties.ph.ventilation_system = _vent_system
        
        
        if _vent_system.ventilation_unit:
            # -- Set the new h-hvac's values to match the PH-Ventilator Inputs, if any
            
            new_hvac.sensible_heat_recovery = _vent_system.ventilation_unit.sensible_heat_recovery
            new_hvac.latent_heat_recovery = _vent_system.ventilation_unit.latent_heat_recovery
            new_hvac.demand_controlled_ventilation = True
    
    # --------------------------------------------------------------------------
    # -- Space Heating
    for ph_heating_system in _space_heating_systems:
        new_hvac.properties.ph.heating_systems.add(ph_heating_system)
        
    # --------------------------------------------------------------------------
    # -- Space Cooling
    for ph_cooling_system in _space_cooling_systems:
        new_hvac.properties.ph.cooling_systems.add(ph_cooling_system)    
    
    new_room = hb_room.duplicate()
    new_room.properties.energy.hvac = new_hvac
    hb_rooms_.append(new_room)
