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
Assign Honeybee Rooms to a specific 'Buildiing Segment' within the PHX Model. In WUFI, this is used
as the 'Case', while in C3RRO this will be considered the 'Variant'. For PHIUS
projects, use this component to break mixed-use projects into separate residential-case
and non-residential-case variants.
-
EM April 8, 2022
    Args:
        name_:
        latitude_: (deg) default = 40.6 (NYC)
        longitude_: (deg) default = -73.8 (NYC)
        altitude_: (m) default = 5.0
        daily_temp_variation_: (deg K) default = 8.0K
        avg_wind_speed_: (m/s) default = 4.0 m/s
        copy_from_excel_: Copy/Paste from a PHPP-Style Climate data. Copy the 
            yellow cells (not the top line with ID / long / lat and not the left
            column with headings.) default = NYC Climate.
    
    Returns:
        ph_climate_: A new PHX Climate Object. Apply this to a WUFI Config PyPH Component.
"""

import honeybee_ph.site
import honeybee_ph_utils.preview
import honeybee_ph_rhino.climate

# --
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Phius Climate"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_08_2022')

if DEV:
    reload(honeybee_ph.site)
    reload(honeybee_ph_utils.preview)
    reload(honeybee_ph_rhino.climate)

# -- Climate
ph_climate_ = honeybee_ph.site.Climate()
ph_climate_.display_name = name_ or '__unnamed_location__'
ph_climate_.summer_daily_temperature_swing = daily_temp_variation_ or 8.0
ph_climate_.average_wind_speed = avg_wind_speed_ or 4

# -- Location
ph_climate_.location.latitude = latitude_ or 40.6
ph_climate_.location.longitude = longitude_ or -73.8
ph_climate_.location.weather_station_elevation = altitude_ or 5.0
ph_climate_.location.climate_zone = 1
ph_climate_.location.hours_from_UTC = -4

# -- Monthly
ph_climate_.monthly_temperature_air.values = [1.2,-0.2,5.6,10.9,16.1,21.7,25.0,24.8,19.9,14.0,7.3,3.3]
ph_climate_.monthly_temperature_dewpoint.values = [-4.3,-7.4,0.3,4.7,9.1,15.8,20.3,17.1,13.2,7.9,2.1,-2.8]
ph_climate_.monthly_temperature_sky.values = [-17.4,-20.0,-10.9,-4.8,1.0,9.8,14.5,8.4,5.8,-2.8,-8.6,-11.4]

ph_climate_.monthly_radiation_north.values = [21,29,34,39,56,60,59,50,34,30,20,16]
ph_climate_.monthly_radiation_east.values = [32,46,57,65,82,76,78,84,60,54,33,28]
ph_climate_.monthly_radiation_south.values = [83,106,103,86,80,73,78,104,97,129,87,87]
ph_climate_.monthly_radiation_west.values = [48,70,92,95,114,121,120,130,91,94,47,45]
ph_climate_.monthly_radiation_global.values = [50,72,111,133,170,176,177,182,124,109,62,46]

# -- Peak Loads
ph_climate_.peak_heating_1.temp = -6.7
ph_climate_.peak_heating_1.rad_north = 46
ph_climate_.peak_heating_1.rad_east = 80
ph_climate_.peak_heating_1.rad_south = 200
ph_climate_.peak_heating_1.rad_west = 113
ph_climate_.peak_heating_1.rad_global = 121

ph_climate_.peak_heating_2.temp = -4.2
ph_climate_.peak_heating_2.rad_north = 16
ph_climate_.peak_heating_2.rad_east = 22
ph_climate_.peak_heating_2.rad_south = 46
ph_climate_.peak_heating_2.rad_west = 26
ph_climate_.peak_heating_2.rad_global = 38

ph_climate_.peak_cooling_1.temp = 26.1
ph_climate_.peak_cooling_1.rad_north = 64
ph_climate_.peak_cooling_1.rad_east = 106
ph_climate_.peak_cooling_1.rad_south = 132
ph_climate_.peak_cooling_1.rad_west = 159
ph_climate_.peak_cooling_1.rad_global = 230

ph_climate_.peak_cooling_2.temp = 26.1
ph_climate_.peak_cooling_2.rad_north = 64
ph_climate_.peak_cooling_2.rad_east = 106
ph_climate_.peak_cooling_2.rad_south = 132
ph_climate_.peak_cooling_2.rad_west = 159
ph_climate_.peak_cooling_2.rad_global = 230

if copy_from_excel_:
    ph_climate_ = honeybee_ph_rhino.climate.parse_copy_from_excel(ph_climate_, copy_from_excel_)

# -- Preview
honeybee_ph_utils.preview.object_preview(ph_climate_)