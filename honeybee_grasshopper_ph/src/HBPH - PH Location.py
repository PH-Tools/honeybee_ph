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
Set the geographic location data for the project. Note: if none is supplied, the default
values for NYC, USA will be used.
-
EM June 13, 2022
    Args:
        _latitude: (deg) default = 40.6 (NYC)
        
        _longitude: (deg) default = -73.8 (NYC)
        
        _site_elevation: (m) default = None. If None, the weather-station elevation will be 
            used as the site-elevation.
        
        _hours_from_UTC: (hours) For WUFI-Passive

    Returns:
        location_: A new HBPH Location object which can be passed to an "HBPH - PH Site"
            component.
"""

from honeybee_ph import site
from honeybee_ph_utils import preview

# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - PH Location"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_13_2022')

if DEV:
    reload(site)
    reload(preview)
    
# -------------------------------------------------------------------------------------
# -- Collect the new Location inputs
location_ = site.Location()
location_.latitude = _latitude or location_.latitude
location_.longitude = _longitude or location_.longitude
location_.site_elevation = _site_elevation or location_.site_elevation
location_.hours_from_UTC = _hours_from_UTC or location_.hours_from_UTC

# -------------------------------------------------------------------------------------
preview.object_preview(location_)