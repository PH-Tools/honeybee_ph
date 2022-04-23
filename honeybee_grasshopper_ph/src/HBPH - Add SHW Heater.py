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
Add a new Hot-Water heater to the HB-Rooms. This is used to add a detailed 
Passive-House style heater to the HB-Room. Ensure that the HB-Room has a HB-Energy
'Service Hot Water' system before adding this heater. Use the 'HB SHW System' component to 
add that system to the HB Rooms if they do not already have them.
-
EM April 1, 2022
    Args:
        _heater: The new PH style HW-Heater to add to the HB-Rooms.
        
        _hb_rooms: Then honeybee-Rooms to add the new HW-Heater to.
    
    Returns:
        hb_rooms_: The honeybee-Rooms with the new HW-Heater added to their SHW System.
"""

import Grasshopper.Kernel as ghK
import honeybee_energy_ph.hvac.hot_water
import honeybee_ph_utils.preview

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add SHW Heater"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_01_2022')
if DEV:
    reload(honeybee_energy_ph.hvac.hot_water)
    reload(honeybee_ph_utils.preview)
    
# -----------------------------------------------------------------------------------------------
"""This part is a bit wierd since HB's SHW object does NOT get duplicated
by default when the normal duplicate method is called. This means that if 
you add a new heater, that change affects the object state throughout the application. 
Every time this component is run, a new heater would then be added, but since the obj already
includes all previous heaters, you would end up with duplicate heaters. 

To avoid those problems, first: collect the unique shw systems, next: manually duplicate them, and 
then last: add the new heater. Once that mutation is completed, now REPLACE the room's SHW with
the new one with the right heaters.
"""

class TempDataObject:
    """Temp class to organize some of the data"""
    def __init__(self):
        self.shw_object = None
        self.room_id_list = []
    def __str__(self):
        return 'Temp: shw_system={}, room_id_list={}'.format(self.shw_object, self.room_id_list)
    def __repr__(self):
        return str(self)


# -- Get the unique SHW systems in the rooms
shw_systems = {}
for room in _hb_rooms:
    new = TempDataObject()
    try:
        new.shw_object = room.properties.energy.shw.duplicate()
    except AttributeError as e:
        msg = "Error: The Honeybee Room: '{}' appears to be missing a 'shw' object? "\
            "Not all HB Programs included hot-water loads by default. If the Honeybee Room "\
            "you are adding this PH Hot-Water heater to does not already have a 'shw', "\
            "be sure to add it to the room BEFORE using this component. You can do this by "\
            "using the Honeybee 'Apply Loads' or 'Apply Absolute Loads' componenent and assigning "\
            "a load to the 'hot_wtr_flow_' input, then using a 'HB SHW System' component to  "\
            "create assign the actual honeybee shw object to the room.".format(room)
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Error, msg)
        print msg
        break
        
    try:
        shw_systems[new.shw_object.identifier].room_id_list.append(room.identifier)
    except KeyError:
        shw_systems[new.shw_object.identifier] = new
        shw_systems[new.shw_object.identifier].room_id_list.append(room.identifier)
        

# --- Add the new heater to each of the unique systems found

for data in shw_systems.values():
    data.shw_object.properties.ph.add_heater(_heater)


# --- Add the new modified SHW System back onto the Rooms
hb_rooms_ = []
for room in _hb_rooms:
    
    new_room = room.duplicate()
    for data in shw_systems.values():
        if new_room.identifier in data.room_id_list:
            
            new_room.properties.energy.shw = data.shw_object
    hb_rooms_.append(new_room)


# -- 
honeybee_ph_utils.preview.object_preview(_heater)