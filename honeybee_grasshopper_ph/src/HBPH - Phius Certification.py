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
EM April 8, 2022
    Args:
        _PHIUS_annual_heating_demand_kWh_m2:
        _PHIUS_annual_cooling_demand_kWh_m2:
        _PHIUS_peak_heating_load_W_m2:
        _PHIUS_peak_cooling_load_W_m2:
        bldg_status_: Input either -
            "1-In planning" (default)
            "2-Under construction"
            "3-Completed"
        
        bldg_type_: Input either -
            "1-New construction" (default)
            "2-Retrofit"
            "3-Mixed - new construction/retrofit"
    Returns:
        certification_:
"""

import honeybee_ph.phius
import honeybee_ph_utils.preview

# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Phius Certification"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_08_2022')

if DEV:
    reload(honeybee_ph.phius)
    reload(honeybee_ph_utils.preview)

certification_ = honeybee_ph.phius.PhiusCertification()

certification_.PHIUS2021_heating_demand = _PHIUS_annual_heating_demand_kWh_m2 or 15
certification_.PHIUS2021_cooling_demand = _PHIUS_annual_cooling_demand_kWh_m2 or 15
certification_.PHIUS2021_heating_load = _PHIUS_peak_heating_load_W_m2 or 10
certification_.PHIUS2021_cooling_load = _PHIUS_peak_cooling_load_W_m2 or 10

certification_.building_status.value = bldg_status_ or 1  # In Planning
certification_.building_type.value = bldg_type_ or 1  # New Construction

honeybee_ph_utils.preview.object_preview(certification_)