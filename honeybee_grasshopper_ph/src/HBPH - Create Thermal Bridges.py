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
Create a new HBPH Thermal Bridge object which can be added to an HB Model. Note that
these thermal bridges will have no effect on the EnergyPlus/OpenStudio simualtion and 
will only be considered when the model is exported to the PHPP/WUFI-Passive.
-
EM June 18, 2022

    Args:
        _names: (List[str]) A list of the HBPH Thermal Bridge names.
            
        _psi_values: (List[float]) The Psi-Values (W/mk) values to use. If 
            None are provied, default=0.1 W/mk
            
        _fRsi_values: (List[float]) The temperature-factor (fRsi) values. If 
            None are provided, default=0.75
        
        _lengths: (List[float]) The lengths (m). If None are provided, 
            default=0.0 m
            
    Returns:
        thermal_bridges_: (List[PhThermalBridge]) A list of the new HBPH
            thermal bridge objects. These can be added to a Honeybee room
            using the "HBPH - Add Thermal Bridges" component.
"""

from itertools import izip_longest

from honeybee_energy_ph.construction import thermal_bridge
from honeybee_ph_rhino.gh_compo_io import ghio_create_tb
from honeybee_ph_utils import input_tools, preview

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Thermal Bridges"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_18_2022')
if DEV:
    #reload(thermal_bridge)
    #reload(ghio_create_tb)
    #reload(input_tools)
    reload(preview)

#-------------------------------------------------------------------------------
thermal_bridges_ = []
for i in range(len(_names)):
    ITb = ghio_create_tb.IThermalBridge()
    ITb.display_name = input_tools.clean_get(_names, i)
    ITb.psi_value = input_tools.clean_get(_psi_values, i)
    ITb.fRsi_value = input_tools.clean_get(_fRsi_values, i, 0.75)
    ITb.length = input_tools.clean_get(_lengths, i, 0)

    thermal_bridges_.append(ITb.create_hbph_thermal_bridge())
    
#-------------------------------------------------------------------------------
# -- Preview
for tb in thermal_bridges_:
    preview.object_preview(tb)