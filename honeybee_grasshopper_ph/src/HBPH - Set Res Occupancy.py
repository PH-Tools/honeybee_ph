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
Set the residential PH-Style occupancy for the Honeybee-Rooms input. For Phius, the 
total occupancy with be the number-of-bedrooms + 1 for each dwelling unit.
-
EM April 6, 2022
    Args:
        _num_bedrooms: (list[int]) A list of number of bedrooms for each Honeybee-Room input.
            This should ideally be the same length as the '_hb_rooms' input, and in the same 
            order. If only a single value is input, that value will get applied to al of the 
            Honeybee-Rooms input. Note that this value is the number of bedrooms PER-HB-ROOM, 
            not the total number of bedrooms in the entire model.
        
        _hb_rooms: (List[Room]) A list of Honeybee-Rooms to set the bedroom counts on.
            
    Returns:
        hb_rooms_ (List[Room]) A list of the Honeybee Rooms with the ph-style occupancy set.
"""

from honeybee_energy.load.people import People

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Set Res Occupancy"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_06_2022')
if DEV:
    pass
    
def dup_load(hb_obj, object_name, object_class):
    """Duplicate a load object assigned to a Room or ProgramType."""
    # try to get the load object assgined to the Room or ProgramType
    try:  # assume it's a Room
        load_obj = hb_obj.properties
        for attribute in ('energy', object_name):
            load_obj = getattr(load_obj, attribute)
    except AttributeError:  # it's a ProgramType
        load_obj = getattr(hb_obj, object_name)

    load_id = '{}_{}'.format(hb_obj.identifier, object_name)
    try:  # duplicate the load object
        dup_load = load_obj.duplicate()
        dup_load.identifier = load_id
        return dup_load
    except AttributeError:  # create a new object
        try:  # assume it's People, Lighting, Equipment or Infiltration
            return object_class(load_id, 0, always_on)
        except:  # it's a Ventilation object
            return object_class(load_id)


hb_rooms_ = []
for i, room in enumerate(_hb_rooms):
    try:
        room_num_bedrooms = _num_bedrooms[i]
    except IndexError:
        try:
            room_num_bedrooms = _num_bedrooms[0]
        except IndexError:
            hb_rooms_.append(room)
            continue
      
    new_room = room.duplicate()
    new_hb_ppl_obj = dup_load(new_room, 'people', People)
    
    # -- Set the properties
    new_hb_ppl_obj.properties.ph.number_bedrooms = room_num_bedrooms
    new_hb_ppl_obj.properties.ph.number_people = room_num_bedrooms + 1
    ppl_per_m2 = new_hb_ppl_obj.properties.ph.number_people / room.floor_area
    new_hb_ppl_obj.people_per_area = ppl_per_m2
    new_hb_ppl_obj.properties.ph.is_dwelling_unit = True
    
    new_room.properties.energy.people = new_hb_ppl_obj
    hb_rooms_.append(new_room)