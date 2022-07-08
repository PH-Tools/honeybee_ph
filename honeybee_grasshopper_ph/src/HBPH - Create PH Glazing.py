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
Create a new HBPH Window Glazing.

-
EM July 2, 2022
    Args:
        _name_: (str)
        
        _u_factor: (float) W/m2k - The COG U-value for the glazing, as per EN-673. Note that
            this value is not the same as the NFRC value.
            default = 0.8 W/m2k
        
        _g_value: (float) % - The g-Value of the glazing as per EN-410. Note that this 
            is not the same as the SHGC value.
            default = 0.4
    Returns:
        glazing_: A new HBPH WindowGlazing which can be used to build an HBPH Window Constrution.
"""
   
try:
    from honeybee_ph_utils import preview
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_utils:\t{}'.format(e))

try:
    from honeybee_ph_rhino.gh_compo_io import ghio_ph_glazing
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_rhino:\t{}'.format(e))


# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create PH Glazing"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUL_02_2022')

if DEV:
    #reload(ghio_ph_glazing)
    reload(preview)


# -------------------------------------------------------------------------------------
ghio_glazing = ghio_ph_glazing.IPhWindowGlazing()
ghio_glazing.display_name = _name_
ghio_glazing.u_factor = _u_factor
ghio_glazing.g_value = _g_value

glazing_ = ghio_glazing.create_HBPH_Object()


# -------------------------------------------------------------------------------------
preview.object_preview(glazing_)