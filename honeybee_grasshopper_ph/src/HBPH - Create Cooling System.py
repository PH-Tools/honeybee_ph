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
Create a new PH-Style Cooling Equipment which can be added to HB-Rooms.
-
EM April 16, 2022
    Args:
        _system_type: (int) Enter the type of cooling system.
        
    Returns:
        cooling_system_: The new HBPH-Cooling System which can be added to HB-Rooms.
"""

import Grasshopper
from honeybee_ph_utils import preview
from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.gh_compo_io import ghio_cooling
from honeybee_energy_ph.hvac import cooling



#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Cooling System"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_16_2022')
if DEV:
    reload(gh_io)
    reload(ghio_cooling)
    reload(preview)
    

#-------------------------------------------------------------------------------
class CoolingTypeInputError(Exception):
    def __init__(self, _in, _valid_types):
        self.msg = "Error: Input Cooling type: '{}' not supported by this"\
        "GH-Component. Please only input: '{}'".format(_in, _valid_types)
        super(CoolingTypeInputError, self).__init__(self.msg)
        
        
#-------------------------------------------------------------------------------
# -- Setup the input nodes, get all the user input values
input_dict = ghio_cooling.get_component_inputs(_system_type)
gh_io.setup_component_inputs(ghenv, input_dict, _start_i=1)
input_values_dict = gh_io.get_component_input_values(ghenv)


#-------------------------------------------------------------------------------
# -- Build the new HBPH Cooling System object
cooling_classes = {
    1: cooling.PhCoolingVentilation,
    2: cooling.PhCoolingRecirculation,
    3: cooling.PhCoolingDehumidification,
    4: cooling.PhCoolingPanel,
    }
if _system_type:
    try:
        cooling_class = cooling_classes[gh_io.input_to_int(_system_type)]
    except KeyError as e:
        raise CoolingTypeInputError(_system_type, ghio_cooling.valid_cooling_types)

    cooling_system_ = cooling_class()
    for attr_name in dir(cooling_system_):
        if attr_name.startswith('_'):
            continue

        input_val = input_values_dict.get(attr_name)
        if input_val:
            
            setattr(cooling_system_, attr_name, input_val)
else:
    msg = "Set the '_system_type' to configure the user-inputs."
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg)


#-------------------------------------------------------------------------------
# -- Preview
preview.object_preview(cooling_system_)