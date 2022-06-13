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
Set the detailed monthly and peak-hourly climate data to use for the PHPP and WUFI-Passive model.
- 
Note: if you would like to use one of the pre-loaded PHPP cliamte data sets instead of providing detailed
info here (for PHPP only) you can use the "HBPH - PH PHPP Climate" component to set the dataset to use.
-
EM June 13, 2022
    Args:
        _display_name: (str) Optional name for the climate data set.
        
        _startion_elevation: (m) default = 5.0
        
        _daily_temp_swing: (deg K) default = 8.0K
        
        _avg_wind_speed: (m/s) default = 4.0 m/s
        
    Returns:
        climate_data_: A new HBPH Climate Data object that can passed along to an "HBPH - Site" component.
"""

from honeybee_ph import site
from honeybee_ph_utils import preview

# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - PH Climate Data"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_13_2022')

if DEV:
    reload(site)
    reload(preview)

# -------------------------------------------------------------------------------------
# -- Collect the new Climate inputs
climate_data_ = site.Climate()
climate_data_.display_name = _display_name or climate_data_.display_name
climate_data_.station_elevation = _station_elevation or climate_data_.station_elevation
climate_data_.summer_daily_temperature_swing = _daily_temp_swing or climate_data_.summer_daily_temperature_swing
climate_data_.dataset_name = _avg_wind_speed or climate_data_.average_wind_speed

# -------------------------------------------------------------------------------------
# -- Set the default Climate Data
# -- Monthly
climate_data_.monthly_temperature_air.values = [1.2,-0.2,5.6,10.9,16.1,21.7,25.0,24.8,19.9,14.0,7.3,3.3]
climate_data_.monthly_temperature_dewpoint.values = [-4.3,-7.4,0.3,4.7,9.1,15.8,20.3,17.1,13.2,7.9,2.1,-2.8]
climate_data_.monthly_temperature_sky.values = [-17.4,-20.0,-10.9,-4.8,1.0,9.8,14.5,8.4,5.8,-2.8,-8.6,-11.4]

climate_data_.monthly_radiation_north.values = [21,29,34,39,56,60,59,50,34,30,20,16]
climate_data_.monthly_radiation_east.values = [32,46,57,65,82,76,78,84,60,54,33,28]
climate_data_.monthly_radiation_south.values = [83,106,103,86,80,73,78,104,97,129,87,87]
climate_data_.monthly_radiation_west.values = [48,70,92,95,114,121,120,130,91,94,47,45]
climate_data_.monthly_radiation_global.values = [50,72,111,133,170,176,177,182,124,109,62,46]

# -- Peak Loads
climate_data_.peak_heating_1.temp = -6.7
climate_data_.peak_heating_1.rad_north = 46
climate_data_.peak_heating_1.rad_east = 80
climate_data_.peak_heating_1.rad_south = 200
climate_data_.peak_heating_1.rad_west = 113
climate_data_.peak_heating_1.rad_global = 121

climate_data_.peak_heating_2.temp = -4.2
climate_data_.peak_heating_2.rad_north = 16
climate_data_.peak_heating_2.rad_east = 22
climate_data_.peak_heating_2.rad_south = 46
climate_data_.peak_heating_2.rad_west = 26
climate_data_.peak_heating_2.rad_global = 38

climate_data_.peak_cooling_1.temp = 26.1
climate_data_.peak_cooling_1.rad_north = 64
climate_data_.peak_cooling_1.rad_east = 106
climate_data_.peak_cooling_1.rad_south = 132
climate_data_.peak_cooling_1.rad_west = 159
climate_data_.peak_cooling_1.rad_global = 230

climate_data_.peak_cooling_2.temp = 26.1
climate_data_.peak_cooling_2.rad_north = 64
climate_data_.peak_cooling_2.rad_east = 106
climate_data_.peak_cooling_2.rad_south = 132
climate_data_.peak_cooling_2.rad_west = 159
climate_data_.peak_cooling_2.rad_global = 230


# -------------------------------------------------------------------------------------
preview.object_preview(climate_data_)