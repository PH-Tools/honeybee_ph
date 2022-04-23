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
Creates Passive House Service Hot Water Tank which can be added to the a SHW System.
-
EM April 1, 2022
    Args:
        _tank_type: ("0-No storage tank", "1-DHW and heating", "2-DHW only") The type of use for this tank.
        
        _name_: (str) The name / identifier for the hot water tank.
        
        quantity_: (int) Optional number of tanks. Default=1
        
        for_solar_: (bool) Is this tank hooked up to a Solar HW system?
        
        heat_loss_rate_: (W/k) Heat Loss rate from the tank. Default is 4.0 W/k
        
        volume_: (litres) Nominal tank volume. Default is 300 litres (80 gallons)
        
        standby_frac_: (%) The Standby Fraction. Default is 0.30 (30%)
        
        in_conditioned_space_: (bool) Default=True.
        
        location_temp_: (Deg C) The avg air-temp of the tank location, if the tank is outside the building. 
    
    Returns:
        storage_tank_: A new HW Tank Object. You can add this tank to a Service Hot Water system.
"""

import honeybee_ph_utils.preview
import honeybee_energy_ph.hvac.hot_water

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create SHW Tank"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_01_2022')
if DEV:
    reload(honeybee_ph_utils.preview)
    reload(honeybee_energy_ph.hvac.hot_water)


#-------------------------------------------------------------------------------
# Creat Storage Tank
storage_tank_ = honeybee_energy_ph.hvac.hot_water.PhSHWTank()
if _tank_type: storage_tank_.type = _tank_type
storage_tank_.name = _name_ or '_unnamed_tank_'
storage_tank_.quantity = quantity_ or 1
if for_solar_ is not None: storage_tank_.for_solar = for_solar_
if heat_loss_rate_: storage_tank_.heat_loss_rate = heat_loss_rate_
if volume_: storage_tank_.volume = volume_
if standby_frac_: storage_tank_.standby_fraction = tank_standby_frac_
if in_conditioned_space_ is not None:
    storage_tank_.location = in_conditioned_space_
else:
    storage_tank_.location = True
storage_tank_.location_temp = location_temp_ or 20


# ------------------------------------------------------------------------------
honeybee_ph_utils.preview.object_preview(storage_tank_)