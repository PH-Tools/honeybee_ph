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
Adds new Passive House Service Hot Water (SHW) tanks to honeybee-Room's SHW System.
-
EM April 1, 2022
    Args:
        tank_1_: A new Passive House hot-water storage tank to add to the SHW System.
        tank_2_: A new Passive House hot-water storage tank to add to the SHW System.        
        buffer_tank_: A new Passive House hot-water buffer tank to add to the SHW System.
        solar_tank_: A new Passive House Solar-thermal hot-water storage tank to add to the SHW System.
        _hb_rooms: (Deg C) The avg air-temp of the tank location if outside the building. 
    
    Returns:
        hb_rooms_: The honeybee-Rooms with the new Tanks added to their SHW System.
"""

import Grasshopper.Kernel as ghK
import honeybee_ph_utils.preview

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add SHW Tank"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_01_2022')
if DEV:
    pass
    reload(honeybee_ph_utils.preview)


#-------------------------------------------------------------------------------
hb_rooms_ = []
for hb_room in _hb_rooms:
    new_room = hb_room.duplicate()
    
    if not new_room.properties.energy.shw:
        msg = "Error: The Honeybee Room: '{}' appears to be missing a 'shw' object? "\
            "Not all HB Programs included hot-water loads by default. If the Honeybee Room "\
            "you are adding this PH Hot-Water tank to does not already have a 'shw', "\
            "be sure to add it to the room BEFORE using this component. You can do this by "\
            "using the Honeybee 'Apply Loads' or 'Apply Absolute Loads' componenent and assigning "\
            "a load to the 'hot_wtr_flow_' input, then using a 'HB SHW System' component to  "\
            "create assign the actual honeybee shw object to the room.".format(hb_room)
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Error, msg)
        print msg
        break
    
    
    if tank_1_: new_room.properties.energy.shw.properties.ph.tank_1 = tank_1_
    if tank_2_: new_room.properties.energy.shw.properties.ph.tank_2 = tank_1_
    if buffer_tank_: new_room.properties.energy.shw.properties.ph.tank_buffer = buffer_tank_
    if solar_tank_: new_room.properties.energy.shw.properties.ph.tank_solar = solar_tank_

    hb_rooms_.append(new_room)
    