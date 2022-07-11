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
Use to get any user-defined Floor-Segment geometry and data from the Rhino scene.
This is only useful if you  have assigned detailed space numbers and names to the 
floor-segment geometry back in the Rhino scene. This component will help gather and 
organize this data so that it can be passed along to the 'Create Spaces' component.
-
EM June 11, 2022
    Args:
        _group_by_name: (bool): If True, will attempt to group the Floor Segments 
            found based on their number/name
        
        _floor_seg_geom: (List[Geometry]): The input Rhino Geometry to try and get
            the data for.
    
    Returns:
        srfcs_: (Tree[Geometry]) The geometry found. 
        
        weighting_factors: (Tree[float]) Any TFA/iCFA weighting factors found.
        
        name_: (Tree[str]) Any space names found on the geometry.
        
        numbers_: (Tree[str]) Any space numbers found on the geometry.
        
        vent_rates_: (Tree[]) A Tree of any PH-Style ventilaion flow-rates found.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from honeybee_ph_rhino.gh_compo_io import ghio_get_flr_seg_data
from honeybee_ph_rhino import gh_io

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Get FloorSegment Data"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_11_2022')
if DEV:
    reload(ghio_get_flr_seg_data)


# ------------------------------------------------------------------------------
# -- GH Interface
IGH = gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )


# ------------------------------------------------------------------------------
ghio_obj = ghio_get_flr_seg_data.IGetFloorSegData(IGH, _group_by_name, _floor_seg_geom)
srfcs_, weighting_factors_, names_, numbers_, vent_rates_ = ghio_obj.create_output()
