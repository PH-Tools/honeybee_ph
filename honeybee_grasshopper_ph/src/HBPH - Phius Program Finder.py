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
        _name_: (str) The name of the Phius program to search the dataset for.
        
        description_: (Optional[str]) Search within the 'description' field of the Phius
            program data set instead of the name.
        
        protocol_: (Optional[str]) A sub-category "Protocol" to filter the Phius programs by. For
            instance - "PHIUS_MultiFamily" or "PHIUS_NonRes", etc...
            
        base_program_: (Optional[honeybee_energy.programtype.ProgramType]) A base program 
            to use for the Phius Program, to fill in any missing info (hot-water, gas, etc..)
            
    Returns:
        programs_ (List[honeybee_energy.programtype.ProgramType]) A list of the Honeybee
            ProgramTypes found in the Phius dataset which match the search criteria.
"""

import Grasshopper.Kernel as ghK
from honeybee_ph_standards.programtypes import PHIUS_programs

from honeybee_energy_ph.library import programtypes
from honeybee_energy_ph.properties import ruleset

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Phius Program Finder"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_06_2022')
if DEV:
    reload(ruleset)
    reload(programtypes)
    reload(PHIUS_programs)
    
 
# ------------------------------------------------------------------------------   
# -- Get the data from in the Phius data set
if _name_:
    prog_data = programtypes.load_data_from_Phius_standards(_name_, 'name', protocol_)
    if not prog_data:
        msg = "No Phius data found for name: '{}'".format(_name_)
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)
elif description_:
    prog_data = programtypes.load_data_from_Phius_standards(description_, 'description', protocol_)
    if not prog_data:
        msg = "No Phius data found for description: '{}'".format(description_)
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)
else:
    prog_data = []
    msg = "No Phius data found for name: '{}' or description: '{}'".format(_name_, description_)
    ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)


# ------------------------------------------------------------------------------
# -- Turn the datasets found into a HB Programs
programs_ = []
for data in prog_data:
    prog = programtypes.build_hb_program_from_Phius_data(data)
    programs_.append(prog)