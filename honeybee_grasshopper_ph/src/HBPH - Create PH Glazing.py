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
EM April 23, 2022
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

try:  # import the core honeybee dependencies
    from honeybee.typing import clean_and_id_ep_string, clean_ep_string
except ImportError as e:
    raise ImportError('Failed to import honeybee:\t{}'.format(e))

try:
    from honeybee_energy_ph.construction import window
except ImportError as e:
    raise ImportError('Failed to import honeybee_energy_ph:\t{}'.format(e))
    
try:
    from honeybee_ph_utils import preview
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_utils:\t{}'.format(e))


# --
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create PH Glazing"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_23_2022')

if DEV:
    #reload(window)
    reload(preview)


# -- 
ident = clean_and_id_ep_string('PhWindowGlazing')
glazing_ = window.PhWindowGlazing(ident)
glazing_.display_name = ident if _name_ is None else clean_ep_string(_name_)
glazing_.u_factor = _u_factor if _u_factor is not None else 0.8
glazing_.g_value = _g_value if _g_value is not None else 0.4

# -- 
preview.object_preview(glazing_)