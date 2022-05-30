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
Create the 'punched' building geometry and all aperture 'reveals' which are
used when calculating detailed shading factors.
-
EM May 23, 2022
    Args:
        _hb_rooms: The Honeybee Rooms with apertures.
    
    Returns:
        window_surfaces_: The window surfaces as Brep objects, 'inset' into the 
            Honeybee-room. These are useful for visualization purposes.
        
        shading_surfaces_: The Honeybee-Room building surfaces as Brep objects
            with all the apertures 'punched' out and all side reveals for apertures
            added. These are used to calculate accurate shading factors for 
            apertures.
            
        hb_rooms_: The Honeybe Rooms.
"""

from honeybee_ph_rhino.gh_compo_io import ghio_win_shade_surfaces

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Building Shading"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='MAY_23_2022')
if DEV:
    reload(ghio_win_shade_surfaces)

# ------------------------------------------------------------------------------
shading_surfaces_ = []
shading_surfaces_.extend(ghio_win_shade_surfaces.create_punched_geometry(_hb_rooms))
shading_surfaces_.extend(ghio_win_shade_surfaces.create_window_reveals(_hb_rooms))

window_surfaces_ = ghio_win_shade_surfaces.create_inset_aperture_surfaces(_hb_rooms)

hb_rooms_ = _hb_rooms