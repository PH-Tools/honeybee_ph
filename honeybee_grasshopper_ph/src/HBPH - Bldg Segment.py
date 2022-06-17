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
Use this component to add one or more honeybee-Rooms to a PH-Building-Segment. This 
'building-segment' could be a single floor, a 'wing' or an entire building and will 
map to a single 'Case' in WUFI or a single PHPP file.
-
Since Passive House models only allow for a single thermal zone, any honeybee-rooms 
that are part of the building-segment will be merged / joined when exported to 
WUFI-Passive or PHPP. When merged, only the exterior surfaces will be retained, and 
any faces with a 'Surface' boundary condition well be removed from the Passive House 
model. Only Honeybee Faces with boundary conditions of "Outdoors", "Ground" and 
"Adiabatic" will be included in the new Honeybee Room. 
-
Use this before passing the honeybee-rooms on to the 'HB Model' component.
-
EM June 13, 2022
    Args:
        segment_name_: Name for the building-segment
               
        num_floor_levels_: (int) Total number of floor levels for the group of 
            Honeybee rooms input. Default=1
        
        num_dwelling_units_: (int) Total number of 'units' for the group of Honeybee rooms
            input For residential, this is the total number of dwelling units
            in the group of HB-Room. For non-residential, leave this set to "1".
        
        climate_: Optional Passive House monthly climate data.
        
        source_energy_factors_: (Optional) A list of source energy (site->source) energy 
            factors to use for assessing overall source (primary) energy usage. By default, 
            this component will use the standard Phius 2021 source energy factors which can be 
            found at https://www.phius.org/PHIUS+2021/Phius%20Core_Phius%20Zero_Final%20Modeling%20Protocol%20v1.1.pdf
            -
            Use the "Create Conversion Factor" component to define custom factors if you would 
            like to use your own. Be sure to define all of the fuel-factors required by Phius / WUFI.

        co2e_factors_: (Optional) A list of CO2e (site->CO2e) conversion 
            factors to use for assessing overall GHG emissions. By default, 
            this component will use the standard Phius 2021 CO2e factors which can be 
            found at https://www.phius.org/PHIUS+2021/Phius%20Core_Phius%20Zero_Final%20Modeling%20Protocol%20v1.1.pdf
            -
            Use the "Create Conversion Factor" component to define custom factors if you would 
            like to use your own. Be sure to define all of the fuel-factors required by Phius / WUFI.
        
        phius_certification_: Optional Phius certification thresholds.
        
        phi_certification_: Optional PHI certification configuration and settings.
        
        winter_set_temp_: default = 20C [68F]
        
        summer_set_temp_: default = 25C [77F]
    
    Returns:
        hb_rooms_: The honeyee-Rooms with building-segment information added.
"""

from honeybee.typing import clean_and_id_string

import honeybee_ph.phius
import honeybee_ph.phi
import honeybee_ph.bldg_segment
import honeybee_ph.location
from honeybee_ph_standards.sourcefactors import factors, phius_CO2_factors, phius_source_energy_factors
import honeybee_ph_utils.preview


# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Bldg Segment"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_13_2022')
if DEV:
    reload(honeybee_ph.phius)
    reload(honeybee_ph.phi)
    #reload(honeybee_ph.bldg_segment) # Breaks everyting.... sigh: Python 2
    reload(honeybee_ph.location)
    reload(honeybee_ph_utils.preview)
    reload(factors)
    reload(phius_CO2_factors)
    reload(phius_source_energy_factors)

def get_new_room_name(_br_count):
    # type: (int) -> str
    try:
        display_name = clean_and_id_string(_segment_name_.Branch(_br_count)[0])
    except:
        try:
            display_name = clean_and_id_string(_segment_name_.Branch(0)[0])
        except ValueError:
            display_name = 'Segment'
    
    return  clean_and_id_string(display_name)

# -- Sort our the new BldgSegment data
segment = honeybee_ph.bldg_segment.BldgSegment()

segment.name = _segment_name_ or 'Unnamed_Bldg_Segment'
segment.num_floor_levels = num_floor_levels_ or 1
segment.num_dwelling_units = num_dwelling_units_ or 1
segment.site = site_ or segment.site
segment.phius_certification = phius_certification_ or honeybee_ph.phius.PhiusCertification()
segment.phi_certification = phi_certification_ or honeybee_ph.phi.PhiCertification()

segment.set_points.winter = winter_set_temp_ or 20
segment.set_points.summer = summer_set_temp_ or 25


# -- CO2 and Source Energy Factors
ALLOWED_FUELS = list(set(
    list(phius_source_energy_factors.factors_2021.keys()) +
    list(phius_CO2_factors.factors_2021.keys())
))

src_factors = source_energy_factors_ or factors.build_factors_from_library(
                                phius_source_energy_factors.factors_2021)
co2_factors = co2e_factors_ or factors.build_factors_from_library(
                                phius_CO2_factors.factors_2021)

segment.source_energy_factors = factors.FactorCollection('Source_Energy', src_factors)
segment.co2e_factors = factors.FactorCollection('CO2', co2_factors)
segment.source_energy_factors.validate_fuel_types(ALLOWED_FUELS)
segment.co2e_factors.validate_fuel_types(ALLOWED_FUELS)

# -- Preview
honeybee_ph_utils.preview.object_preview(segment)

# -- Apply the segment to the rooms
hb_rooms_ = []
for i, hb_room in enumerate(_hb_rooms):
    new_room = hb_room.duplicate()
    new_room.properties.ph.ph_bldg_segment = segment
    hb_rooms_.append(new_room)