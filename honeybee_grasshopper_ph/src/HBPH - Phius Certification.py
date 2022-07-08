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
Enter the relevant Phius Certification threshold data for the building-segment.
-
EM June 4, 2022
    Args:
        building_category_type_: Input either -
            "1-Residential building" (default)
            "2-Non-residential building"
        
        building_use_type_: Input either - 
            "1-Residential" (default)
            "4-Office/Administrative building"
            "5-School"
            "6-Other"
            "7-Undefined/unfinished"
        
        building_status_: Input either -
            "1-In planning" (default)
            "2-Under construction"
            "3-Completed"
        
        
        building_type_: Input either -
            "1-New construction" (default)
            "2-Retrofit"
            "3-Mixed - new construction/retrofit"
        
        
        _PHIUS_annual_heating_demand_kWh_m2:
        
        _PHIUS_annual_cooling_demand_kWh_m2:
        
        _PHIUS_peak_heating_load_W_m2:
        
        _PHIUS_peak_cooling_load_W_m2:
        
    Returns:
        certification_:
"""

from honeybee_ph_rhino import gh_io
from honeybee_ph_utils import preview, enumerables
from honeybee_ph import phius

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Phius Certification"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_04_2022')

if DEV:
    reload(gh_io)
    reload(phius)
    reload(preview)

#-------------------------------------------------------------------------------
certification_ = phius.PhiusCertification()

certification_.building_category_type = gh_io.input_to_int(building_category_type_)
certification_.building_use_type = gh_io.input_to_int(building_use_type_)
certification_.building_status = gh_io.input_to_int(building_status_)
certification_.building_type = gh_io.input_to_int(building_type_)

certification_.PHIUS2021_heating_demand = _PHIUS_annual_heating_demand_kWh_m2 or 15
certification_.PHIUS2021_cooling_demand = _PHIUS_annual_cooling_demand_kWh_m2 or 15
certification_.PHIUS2021_heating_load = _PHIUS_peak_heating_load_W_m2 or 10
certification_.PHIUS2021_cooling_load = _PHIUS_peak_cooling_load_W_m2 or 10


#-------------------------------------------------------------------------------
preview.object_preview(certification_)