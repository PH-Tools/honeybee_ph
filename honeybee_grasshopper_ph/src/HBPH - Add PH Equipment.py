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
Add one or more detailed Passive House style electric-equipment objects to the 
honeybee Rooms.
-
EM June 11, 2022

    Args:
        phius_defaults_: (int) Optional. Input either:
        > "1" for Single Family Residential appliance set.
        > "2" for Multifamily Residential appliance set.
            Note - for Multifamily, be sure to add in the Int. / Ext. Lighting and MEL from
            the Phius MF Calculator using a 'Create PH Appliance' HBPH Component.
        > "3" for Multifamily NonResidential appliance set (none).
            Note - for Multifamily, be sure to add in the Int. / Ext. Lighting and MEL from
            the Phius MF Calculator using a 'Create PH Appliance' HBPH Component.
        
        phi_defaults_: (bool) default=False. Set True to add the default PHI equipment
            set to the model.
        
        equipment_: (List[PhEquipment]) A List of Passive-House style electric
            equipment to add onto the Honeybee-Room.
            
    Returns:
        hb_rooms_: (List[Room]) A list of the Honeybee Rooms with the new appliances
            added to them.
"""

import Grasshopper.Kernel as ghK

from honeybee_ph_utils import preview
from honeybee_ph_rhino.gh_compo_io import ghio_add_ph_equipment

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add PH Equipment"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_11_2022')
if DEV:
    reload(preview)
    reload(ghio_add_ph_equipment)

#-------------------------------------------------------------------------------
# -- Create the HBPH-Equipment set
if phius_defaults_:
    ph_equipment = ghio_add_ph_equipment.add_Phius_default_equipment_to_list(equipment_, phius_defaults_)
elif phi_defaults_:
    ph_equipment = ghio_add_ph_equipment.add_Phi_default_equipment_to_list(equipment_, phi_defaults_)
else:
    ph_equipment = equipment_

#-------------------------------------------------------------------------------
# -- Find and collect all the unique HBE-ElectricEquipment objects on the HB-Rooms
hb_ee_collection = ghio_add_ph_equipment.HBElecEquipCollection()
hb_rooms = ghio_add_ph_equipment.clean_rooms_elec_equip(_hb_rooms)
for hb_room in hb_rooms:
    hb_ee_collection.add_to_collection(hb_room)


#-------------------------------------------------------------------------------
# --- Add the PH-equipment to each of the unique HBE-ElectricEquipment .properties.ph objects found
for ph_equip_item in ph_equipment:
    for hb_ElecEquipWithRooms_obj in hb_ee_collection.values():
        hb_ElecEquipWithRooms_obj.add_hbph_equipment(ph_equip_item)


#-------------------------------------------------------------------------------
# --- Add the new modified Elec-Equipment with the new PH-Equip back onto the HB-Rooms
hb_rooms_ = []
for obj in hb_ee_collection.values():
    """
    try:
        obj.set_hb_ee_wattage()
    except NotImplementedError:
        msg = "Warning: Cannot set the Honeybee-Energy Elec-Equipment Watts/m2 for the appliances."\
            "Cannot calc. values for Phius Standard MEL and Lighting since their methods are not shared."
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg) 
    """
    obj.set_hb_room_ee()
    hb_rooms_ += obj.hb_rooms


#-------------------------------------------------------------------------------
# -- Preview
for device in ph_equipment:
    preview.object_preview(device)