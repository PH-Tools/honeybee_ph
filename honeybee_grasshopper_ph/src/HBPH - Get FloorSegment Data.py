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
EM January 29, 2022
    Args:
        _group_by_name: (bool): If True, will attempt to group the Floor Segments 
            found based on their number/name
        
        _floor_seg_geom: (List[Geometry]): The input Rhino Geometry to try and get
            the data for.
    
    Returns:
        flr_seg_srfcs_: (Tree[Geometry]) The geometry found. 
        
        flr_seg_name_: (Tree[str]) Any space names found on the geometry.
        
        flr_seg_numbers_: (Tree[str]) Any space numbers found on the geometry.
"""

from Grasshopper import DataTree
from System import Object
from Grasshopper.Kernel.Data import GH_Path
from collections import defaultdict, namedtuple

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

import honeybee_ph_rhino.make_spaces.floor_segment

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Get FloorSegment Data"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JAN_29_2022')
if DEV:
    reload(honeybee_ph_rhino.gh_io)
DEV = True
if DEV:
    reload(honeybee_ph_rhino.make_spaces.floor_segment)

# ------------------------------------------------------------------------------
# -- GH Interface
IGH = honeybee_ph_rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

# ------------------------------------------------------------------------------
# -- Try and get any data from the Rhino side
flr_seg_srfcs_ = DataTree[Object]()
flr_seg_data = honeybee_ph_rhino.make_spaces.floor_segment.handle_floor_seg_user_input(IGH, _floor_seg_geom, '_floor_seg_geom')

# ------------------------------------------------------------------------------
# -- Organize outputs
flr_seg_name_ = DataTree[Object]()
flr_seg_numbers_ = DataTree[Object]()
NameGroupItem = namedtuple('NameGroupItem', ['breps', 'name', 'number'])
if _group_by_name:
    name_groups = defaultdict(list)
    for k, flr_seg in enumerate(flr_seg_data):
        new_entry = NameGroupItem(flr_seg.geometry, str(flr_seg.name).upper(), str(flr_seg.number).upper())
        name_groups[flr_seg.full_name].append(new_entry)
    
    for i, name_group in enumerate(name_groups.values()):
        for item in name_group:
            flr_seg_srfcs_.Add(item.breps, GH_Path(i))
            flr_seg_name_.Add(item.name, GH_Path(i))
            flr_seg_numbers_.Add(item.number, GH_Path(i))
else:
    for i, flr_seg in enumerate(flr_seg_data):
        flr_seg_srfcs_.Add(flr_seg.geometry, GH_Path(i))
        flr_seg_name_.Add(flr_seg.name, GH_Path(i))
        flr_seg_numbers_.Add(flr_seg.number, GH_Path(i))
