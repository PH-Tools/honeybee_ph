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
Set the Climate and Location data for the project. For PHI / PHPP, you can also set the optional
Country / Region / Data-Set codes to use one of the climates pre-loaded into the PHPP.
-
EM June 13, 2022
    Args:
        _display_name: Optional name for the Site.
        
        _location: Optional - detailed geographic location data to use for the project.
        
        _climate_data: Optional - detailed climate data to use for the project.
        
        _phpp_climate: Optional - if you prefer, input a "HBPH - PHPP Climate" object here with 
            the PHPP region, country and dataset codes specfied. This will then set the PHPP
            climate to the input values, allowing you to select a pre-loaded PHPP Climate data set
            as the active climate for your project. Note: this has no effect on WUFI-Passive and is
            only used for PHPP climate data.

    Returns:
        site_: A new HBPH Site object which can be passed along the "Building Segment" and will 
            be used to set location and climate information in the PHPP and WUFI-Passive models.
"""

from honeybee_ph import site
from honeybee_ph_utils import preview

# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - PH Site"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_13_2022')

if DEV:
    reload(site)
    reload(preview)

# -------------------------------------------------------------------------------------
# -- Collect the new Site elements
site_ = site.Site()
site_.display_name = _display_name or site_.display_name
site_.location = _location or site_.location
site_.climate = _climate_data or site_.climate
site_.phpp_library_codes = _phpp_climate or site_.phpp_library_codes

# -------------------------------------------------------------------------------------
preview.object_preview(site_)