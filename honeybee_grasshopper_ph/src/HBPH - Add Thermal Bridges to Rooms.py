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
Add new PH Thermal Bridge objects to a Honeybee Room or Rooms. Note that the 
thermal bridges here are added to the Room's PH Building Segment. If Rooms are 
combined together into a single building segment before export to the PHPP / WUFI-Passive, 
the thermal bridges here will only get accounted for once. If the same thermal bridge object
is added to more than one room, it will only show up once for each building-segment.
-
EM June 18, 2022

    Args:
        _thermal_bridges: (List[PhThermalBridge]) A list of the new PH Thermal Bridge
            objects to add to the Honeybee Rooms.
            
        _hb_rooms: (List[float]) A list of the Honeybee Rooms to have the 
            thermal bridges added. 
            
    Returns:
        hb_rooms_: (List[room.Room]) A list of Honeybee-Rooms with the new 
            thermal bridges added to the Room's PH Building-Segment.
"""

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add Thermal Bridges to Rooms"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_18_2022')
if DEV:
    pass

#-------------------------------------------------------------------------------
hb_rooms_ = []
for hb_room in _hb_rooms:
    new_room = hb_room.duplicate()
    
    # -- add the new TBs to the HB-Room Building Segment
    for tb in _thermal_bridges:
        new_room.properties.ph.ph_bldg_segment.thermal_bridges[str(tb.identifier)] = tb
    
    hb_rooms_.append(new_room)