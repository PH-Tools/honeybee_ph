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
Create a new HBPH Window Frame Element. A full HBPH Window Frame is made of 4 of 
these elements (top, right, bottom, left).
-
EM April 23, 2022
    Args:
        _name_: (str)
        
        _width: (float) Face width of the frame (m)
            default = 0.1m (~4")
            
        _u_factor: (float) Frame U-f (W/m2k) as per ISO-10077-2. Note that this value 
            is not the same as the NFRC value.
            default = 1.0 W/m2k
            
        psi_glazing_: (float) Psi-Value of the glazing edge (W/mk) as per ISO-10077-2
            default = 0.04 W/mk
            
        psi_install_: (float) Psi-Value of the window installation (W/mk) as per ISO-10077-2
            default = 0.04 W/mk
        
        chi_: (float) Optional extra Chi-value (W/k) for point thermal bridging due to 
            elements such as glass-carriers in curtain walls or sim.
    
    Returns:
        frame_element_: A new HBPH WindowFrameElement which can be used to build up a complete
            HBPH WindowFrame.
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
ghenv.Component.Name = "HBPH - Create PH Window Frame Element"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_23_2022')

if DEV:
    #reload(window)
    reload(preview)

# --
ident = clean_and_id_ep_string('PhWindowFrameElement')
frame_element_ = window.PhWindowFrameElement(ident)
frame_element_.display_name = ident if _name_ is None else clean_ep_string(_name_)
frame_element_.width = _width or 0.1
frame_element_.u_factor = _u_factor or 1.0
frame_element_.psi_glazing = psi_glazing_ if psi_glazing_ is not None else 0.04
frame_element_.psi_install = psi_install_ if psi_install_ is not None else 0.04
frame_element_.chi = chi_ if chi_ is not None else 0


# -- 
preview.object_preview(frame_element_)