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
Add PH-Spaces to honeybee-Rooms. Spaces represent smaller units than HB-Rooms and 
can be made up of one or more individual volumes. This is useful if you are calculating 
interior net-floor-area or volume as in the Passive House models. Each Space will map to 
a single entry in the WUFI 'Ventilation Rooms' or a PHPP 'Additional Ventilation'.
-
EM January 29, 2022
    Args:
        _spaces: (list[Space]) A list of the new PH-Spaces to add to the Honeybee-Rooms.
        
        _offset_dist_: (float) Default=0.1 An optional value to offset the 'test points' being 
            used to determine the right honeybee-Room to host the space in. This value 
            will be used to move the test point 'up' (world Z) by some dimension before 
            testing if it is 'inside' the honeybee-Room. This is useful you drew your
            floor-segments directly 'on' the floor surface of the honeybee room as this 
            sometimes leads to errors when testing for 'inside'.
        
        _hb_rooms: (list[Room]) The list of honeybee-Rooms to add to the spaces to.
            
    Returns:
        check_pts_: A preview of the test points being used to evaluate the right
            honeybee-Room to use for the host of the space. Useful for debugging 
            if you run into hosting problems.
            
        hb_rooms_: The honeyee-Rooms with the PH Spaces added to them.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from ladybug_rhino.fromgeometry import from_point3d
import honeybee_ph_rhino
from honeybee_ph_rhino.make_spaces import space

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add Spaces"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JAN_29_2022')
if DEV:
    reload(honeybee_ph_rhino.gh_io)


# ------------------------------------------------------------------------------
# -- GH Interface
IGH = honeybee_ph_rhino.gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

# ------------------------------------------------------------------------------
# -- Clean up the inpt spaces, host in the HB-Rooms
offset_dist = _offset_dist_ or 0.1
spaces = [space.offset_space_reference_points(IGH, sp, offset_dist) for sp in _spaces]
hb_rooms_, un_hosted_spaces = space.add_spaces_to_honeybee_rooms(spaces, _hb_rooms)

# ------------------------------------------------------------------------------
# -- if any un_hosted_spaces, pull out their center points for troubelshooting
# -- and raise a user-warning
check_pts_ = [from_point3d(lbt_pt) for space_data in  un_hosted_spaces for lbt_pt in space_data.reference_points]
if un_hosted_spaces:
    msg = 'Error: Host Honeybee-Rooms not found for the Spaces: {}'.format('\n'.join([ spd.space.full_name for spd in un_hosted_spaces]))
    IGH.error(msg)