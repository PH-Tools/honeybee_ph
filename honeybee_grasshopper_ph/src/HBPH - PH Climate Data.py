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
Set the detailed monthly and peak-load climate data to use for the Passive House models.
- 
    - PHI: https://passipedia.org/planning/climate_data_tool
    - PHIUS: https://www.phius.org/climate-data
-
Note also that this component will *NOT* reset any of the Honeybee EnergyPlus climate, and you will need to set
that separately using a normal EPW file with hourly data.
-
Note: if you would like to use one of the pre-loaded PHPP climate data sets instead of providing detailed
info here (for PHPP only) you can use the "HBPH - PH PHPP Climate" component to simply specify the dataset to load.
-
EM September 7, 2022
    Args:
        _display_name_: (str) Optional name for the climate data set.
        
        _station_elevation_: (m) default = 5.0 The elevation of the weather station the data
            is coming from is located.
        
        _daily_temp_swing_: (deg K) default = 8.0K The summer average dailty temperature swing.
        
        _avg_wind_speed_: (m/s) default = 4.0 m/s The summer average wind speed.
        
        _monthly_temps_: Connect a 'HBPH - PH Climate Monthly Temps' component to set the climate data.
            If none is input, all Zero values will be set as the default.
            
        _monthly_radiation_: Connect a 'HBPH - PH Climate Monthly Radiation' component to set the climate data.
            If none is input, all Zero values will be set as the default.
            
        _peak_heat_load_1_: (HBPH_Climate_PeakLoadValueSet) Connect a "HBPH - PH Climate Peak Load"
            component to set the data for the peak heat load 1 case.
        
        _peak_heat_load_2_: (HBPH_Climate_PeakLoadValueSet) Connect a "HBPH - PH Climate Peak Load"
            component to set the data for the peak heat load 2 case.   
            
        _peak_cooling_load_1_: (HBPH_Climate_PeakLoadValueSet) Connect a "HBPH - PH Climate Peak Load"
            component to set the data for the peak cooling load 1 case.
        
        _peak_cooling_load_2_: (HBPH_Climate_PeakLoadValueSet) Connect a "HBPH - PH Climate Peak Load"
            component to set the data for the peak cooling load 2 case.        
            
    Returns:
        climate_data_: A new HBPH Climate Data object that can passed along to an "HBPH - PH Site" component.
"""

from honeybee_ph_utils import preview
from honeybee_ph_rhino.gh_compo_io import ghio_climate

# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - PH Climate Data"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='SEP_07_2022')

if DEV:
    from honeybee_ph import site
    reload(site)
    from honeybee_ph_utils import units
    reload(units)
    from honeybee_ph_rhino.gh_compo_io import ghio_validators
    reload(ghio_validators)
    reload(ghio_climate)
    reload(preview)
    
# -------------------------------------------------------------------------------------
IClimate_PeakLoads_ = ghio_climate.IClimate_PeakLoads(
        _peak_heat_load_1_,
        _peak_heat_load_2_,
        _peak_cooling_load_1_,
        _peak_cooling_load_2_,
    )
peak_loads_ = IClimate_PeakLoads_.create_hbph_obj()

IClimate_ = ghio_climate.IClimate(
        _display_name_,
        _station_elevation_,
        _daily_temp_swing_,
        _avg_wind_speed_,
        _monthly_temps_,
        _monthly_radiation_,
        peak_loads_,
    )
climate_data_ = IClimate_.create_hbph_obj()


# -------------------------------------------------------------------------------------
preview.object_preview(climate_data_)