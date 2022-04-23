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
Create a Site conversion factor for a specific fuel-type. These conversion factors are used to 
convert site-energy into source (primary) energy and CO2e emissions. For more information on Phius
specific conversion factors, see: https://www.phius.org/PHIUS+2021/Phius%20Core_Phius%20Zero_Final%20Modeling%20Protocol%20v1.1.pdf
-
EM April 8, 2022
    Args:
        _fuel_name: (str) The name of the fuel-type to create the factor for. For a list of 
            allowable names, see WUFI or https://www.phius.org/PHIUS+2021/Phius%20Core_Phius%20Zero_Final%20Modeling%20Protocol%20v1.1.pdf
        
        _factor: (float) The conversion factor for the fuel. 
    
    Returns:
        hb_rooms_: The honeyee-Rooms with building-segment information added.
"""

from honeybee_ph_standards.sourcefactors import factors 

# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Conversion Factor"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_08_2022')

if DEV:
    reload(factors)

if _fuel_name and _factor:
    factor_ = factors.Factor()
    factor_.fuel_name = factors.clean_input(_fuel_name)
    factor_.value = _factor
    