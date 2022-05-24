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
EM May 23, 2022
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
    
    Returns:
        settings_: The new HBPH Settings which are used to configure the LBT-Radiation
            shading solver.
"""


import Rhino

from honeybee_ph_utils import sky_matrix

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Shading Factor Settings - LBT Rad"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='MAY_23_2022')
if DEV:
    reload(sky_matrix)


# ------------------------------------------------------------------------------
class Settings:
    def __init__(self, _wsm, _ssm, _mshp, _gs, _lgp):
        self.winter_sky_matrix = _wsm
        self.summer_sky_matrix = _ssm
        self.mesh_params = _mshp
        self.grid_size = _gs
        self.legend_par = _lgp

winter_period = (10,3) # October 1 to March 31
summer_period = (6, 9) # June 1 to September 30

if _epw_file:
    settings_ = Settings(
        _winter_sky_matrix_ or sky_matrix.gen_matrix(_epw_file, winter_period, north_),
        _summer_sky_matrix_ or sky_matrix.gen_matrix(_epw_file, summer_period, north_),
        _shading_mesh_settings_ or Rhino.Geometry.MeshingParameters.Default,
        _grid_size_ or 1.0,
        _legend_par_ or None,
        )
        