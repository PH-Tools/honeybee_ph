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
Settings and parameter values used when calculating the Window Shading Factors
using the Passive House LBT-Radiation solver.
-
EM September 7, 2022
    Args:
        _epw_file: 
        
        north_: Optional North Vetor or angle.
        
        _winter_sky_matrix: Optional winter-period Ladybug Sky Matrix. Default
            if None is supplied is October 1 - March 31
            
        _summer_sky_matrix: Optional summer-period Ladybug Sky Matrix. Default
            if None is supplied is June 1 - September 30
            
        _shading_mesh_setings: Optional Rhino Mesh settings. 
            default = Rhino.Geometry.MeshingParameters.Default
            
        _grid_size: default=1.0
            
        _legend_par_: Optional Ladybug legend parameter object to control the 
            output visualizations.
            
        _cpus_: (int) Optional. The number of computer CPUs to use to calculate the result.
    
    Returns:
        settings_: The new HBPH Settings which are used to configure the LBT-Radiation
            shading solver.
"""


from honeybee_ph_utils import preview
from honeybee_ph_rhino.gh_compo_io import ghio_lbt_shading

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Shading Factor Settings - LBT Rad"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='SEP_07_2022')
if DEV:
    reload(preview)
    reload(ghio_lbt_shading)

# ------------------------------------------------------------------------------
if _epw_file:
    IShadingLBTRadiationSettings_ = ghio_lbt_shading.IShadingLBTRadiationSettings(
            _epw_file,
            _north_,
            _winter_sky_matrix_,
            _summer_sky_matrix_,
            _shading_mesh_settings_,
            _grid_size_,
            _legend_par_,
            _cpus_ 
    )

    settings_ = IShadingLBTRadiationSettings_.create_hbph_obj()

# ------------------------------------------------------------------------------  
preview.object_preview(settings_)