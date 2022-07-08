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
EM June 19, 2022
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

from honeybee_ph_standards.sourcefactors import factors, phius_CO2_factors, phius_source_energy_factors
from honeybee_ph_utils import preview
from honeybee_ph_rhino.gh_compo_io import ghio_bldg_segment


# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Bldg Segment"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_19_2022')
if DEV:
    reload(preview)
    reload(ghio_bldg_segment)


# -------------------------------------------------------------------------------------
# -- Build the BldgSegment Interface
ghio_segment = ghio_bldg_segment.IBldgSegment()
ghio_segment.display_name = _segment_name_
ghio_segment.num_floor_levels = num_floor_levels_
ghio_segment.num_dwelling_units = num_dwelling_units_
ghio_segment.site = site_
ghio_segment.phius_certification = phius_certification_
ghio_segment.phi_certification = phi_certification_
ghio_segment.set_points.winter = winter_set_temp_
ghio_segment.set_points.summer = summer_set_temp_

# -- Collect all the Thermal Bridges from all the Rooms input
# -- note that only one instance of each TB will be maintained on the 
# -- final Building Segment
tb_dict = {}
for room in _hb_rooms:
    tb_dict.update(room.properties.ph.ph_bldg_segment.thermal_bridges)
ghio_segment.thermal_bridges = tb_dict


# -------------------------------------------------------------------------------------
# -- Sort out the fuel factors 
for factor in factors.build_factors_from_library(phius_source_energy_factors.factors_2021) + source_energy_factors_:
    ghio_segment._source_energy_factors.add_factor(factor) 
for factor in factors.build_factors_from_library(phius_CO2_factors.factors_2021) + co2e_factors_:
    ghio_segment._co2e_factors.add_factor(factor) 


allowed_fuels = list(set(
    list(phius_source_energy_factors.factors_2021.keys()) +
    list(phius_CO2_factors.factors_2021.keys())
))
ghio_segment.co2e_factors.validate_fuel_types(allowed_fuels)


# -------------------------------------------------------------------------------------
# -- Create the actual HBPH Building Segment Object
hbph_segment = ghio_segment._create_hbph_bldg_segment()


# -------------------------------------------------------------------------------------
# -- Set the new HBPH Building Segment on the HB rooms
hb_rooms_ = []
for i, hb_room in enumerate(_hb_rooms):
    new_room = hb_room.duplicate()
    new_room.properties.ph.ph_bldg_segment = hbph_segment
    hb_rooms_.append(new_room)

# -------------------------------------------------------------------------------------
# -- Preview
preview.object_preview(hbph_segment)

