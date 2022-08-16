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
Add new PH DHW Piping to a Honeybee Room's SHW System. Note: the Honeybee rooms should 
have a SHW system already, and if it does not please use the 'HB SHW System' component
in order to add it.
-
EM August 16, 2022

    Args:
        _branch_piping: (List[PhPipeElement]) A list of the Branch Piping objects to add.
        
        _recirc_piping: (List[PhPipeElement]) A list of the Recirculation Piping objects to add.
            
        _hb_rooms: (List[room.Room]) A list of the Honeybee Rooms to add the piping to.
        

    Returns:
        hb_rooms_: (List[PhPipeElement]) The Honeybee Rooms with the new piping added
            to the room's SHW system.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from honeybee_ph_rhino import gh_io

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add DHW Piping"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='AUG_16_2022')
if DEV:
    pass
    
# ------------------------------------------------------------------------------
# -- GH Interface
IGH = gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

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
    if not room:
        continue
    
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
        IGH.error(msg)
        print msg
        break
        
    try:
        shw_systems[new.shw_object.identifier].room_id_list.append(room.identifier)
    except KeyError:
        shw_systems[new.shw_object.identifier] = new
        shw_systems[new.shw_object.identifier].room_id_list.append(room.identifier)
        

# --- Add the new piping to each of the unique systems found
for data in shw_systems.values():
    for branch_pipe in _branch_piping:
        data.shw_object.properties.ph.add_branch_piping(branch_pipe)
    for recirc_pipe in _recirc_piping:
        data.shw_object.properties.ph.add_recirc_piping(recirc_pipe)


# --- Add the new modified SHW System back onto the Rooms
hb_rooms_ = []
for room in _hb_rooms:
    if not room:
        continue
        
    new_room = room.duplicate()
    for data in shw_systems.values():
        if new_room.identifier in data.room_id_list:
            
            new_room.properties.energy.shw = data.shw_object
    hb_rooms_.append(new_room)
