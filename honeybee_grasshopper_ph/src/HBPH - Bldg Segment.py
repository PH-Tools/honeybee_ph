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
Use this component to add one or more honeybee-Rooms to a PH-Building-Segment. This 
'building-segment' could be a single floor, a 'wing' or an entire building and will 
map to a single 'Case' in WUFI or a single PHPP file.
-
Since Passive House models only allow for a single thermal zone, any honeybee-rooms 
that are part of the building-segment will be merged / joined when exported to 
WUFI-Passive or PHPP. When merged, only the exterior surfaces will be retained, and 
any faces with a 'Surface' boundary condition well be removed from the Passive House 
model. Only Honeybee Faces with boundary conditions of "Outdoors", "Ground" and 
"Adiabatic" will be included in the new Honeybee Room. 
-
Use this before passing the honeybee-rooms on to the 'HB Model' component.
-
EM January 29, 2022
    Args:
        segment_name_: Name for the building-segment
        
        occupancy_type_: Input either -
            "1-Residential" (default)
            "2-Non-residential"
        
        usage_type_: Input either -
            "1-Residential" (default)
            "4-Office/Administrative building"
            "5-School"
            "6-Other"
            "7-Undefined/unfinished"
        
        num_floor_levels_: (int) Total number of floor levels for the group of 
            Honeybee rooms input. Default=1
        
        num_dwelling_units_: (int) Total number of 'units' for the group of Honeybee rooms
            input For residential, this is the total number of dwelling units
            in the group of HB-Room. For non-residential, leave this set to "1".
        
        climate_: Optional Passive House monthly climate data.
        
        phius_certification_: Optional Phius certification thresholds.
        
        winter_set_temp_: default = 20C [68F]
        
        summer_set_temp_: default = 25C [77F]
    
    Returns:
        hb_rooms_: The honeyee-Rooms with building-segment information added.
"""

from honeybee.typing import clean_and_id_string

import honeybee_ph.phius
import honeybee_ph.bldg_segment
import honeybee_ph.climate
import honeybee_ph_utils.preview

# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Bldg Segment"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JAN_29_2022')
if DEV:
    reload(honeybee_ph.phius)
    # reload(honeybee_ph.bldg_segment) # Breaks everyting.... sigh: Python 2
    reload(honeybee_ph.climate)
    reload(honeybee_ph_utils.preview)


def get_new_room_name(_br_count):
    # type: (int) -> str
    try:
        display_name = clean_and_id_string(_segment_name_.Branch(_br_count)[0])
    except:
        try:
            display_name = clean_and_id_string(_segment_name_.Branch(0)[0])
        except ValueError:
            display_name = 'Segment'
    
    return  clean_and_id_string(display_name)

# -- Sort our the new BldgSegment data
segment = honeybee_ph.bldg_segment.BldgSegment()
segment.name = _segment_name_ or 'Unnamed_Bldg_Segment'
segment.occupancy_type.value = occupancy_type_ or 1 #Residential
segment.usage_type.value = usage_type_ or 1
segment.num_floor_levels = num_floor_levels_ or 1
segment.num_dwelling_units = num_dwelling_units_ or 1
segment.climate = climate_ or honeybee_ph.climate.Climate()
segment.ph_certification = phius_certification_ or honeybee_ph.phius.PhiusCertifiction()
honeybee_ph_utils.preview.object_preview(segment)

# -- Apply the segment to the rooms
hb_rooms_ = []
for i, hb_room in enumerate(_hb_rooms):
    new_room = hb_room.duplicate()
    new_room.properties.ph.ph_bldg_segment = segment
    hb_rooms_.append(new_room)