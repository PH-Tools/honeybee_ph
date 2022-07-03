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
Create a new HBPH Window Construction with PH-Style values.
- -
Note: For north-american modeling (code compliance) you must use NFRC values which are different
than the ISO values used for Passive House modeling. This component allows you to input both types of 
values and will approximate the NFRC values from the ISO inputs. However, do note that this approximation 
is NOT valid for north-american code compliance modeling and is included here only to help those doing 
Passive House modeling. Be sure to enter both the ISO *AND* NFRC values if you need both. The NFRC values 
will be used for all EnergyPlus simulatiuons, while the ISO values will be used for all Passive House
models and outputs.

-
EM July 2, 2022
    Args:
        _name_: (str)
        
        _frame: (PhWindowFrame) A HBPH Window Frame to build the window construction from.
        
        _glazing: (PhWindowGlazing) A HBPH Window Glazing to build the window construction from.
       
        nfrc_u_factor_: (float) Optional NRFC U-Factor for the Window Construction. If none is supplied, 
            this value will be approximated from the ISO values of the _glazing and _frame. 
            Note that this is an approximation only. Strictly speaking this ISO value is not valid 
            as input for north-american code compliance modeling.
        
        nfrc_shgc_: (float) Optional NFRC SHGC-Value for the Window Construction. If none is supplied, 
            this value will be approximated from the ISO values of the _glazing. Note that this
            is an approximation only. Strictly speaking this ISO value is valid as input for 
            north-american code compliance modeling.
       
        t_vis_: (float) default=0.6 - Transmittance of the glazing system.
       
    Returns:
        construction_: A new HB Window Construction which can applied to the apertures 
            directly using the HBE "HB Apply Window Construction" component or used as 
            part of an HB Construction Set.
"""

try:
    from honeybee_ph_utils import preview
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_utils:\t{}'.format(e))

try:
    from honeybee_ph_rhino.gh_compo_io import ghio_ph_win_constr
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_rhino:\t{}'.format(e))


# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create PH Window Construction"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUL_02_2022')

if DEV:
    reload(ghio_ph_win_constr)
    reload(preview)


# -------------------------------------------------------------------------------------
if _glazing and _frame:

    ghio_win_const = ghio_ph_win_constr.IPhWindowConstruction()
    ghio_win_const.display_name = _name_
    ghio_win_const.frame = _frame
    ghio_win_const.glazing = _glazing
    ghio_win_const.nfrc_u_factor = nfrc_u_factor_
    ghio_win_const.nfrc_shgc = nfrc_shgc_
    ghio_win_const.t_vis = t_vis_
    
    construction_ = ghio_win_const.create_HBPH_Object()
    
    # ---------------------------------------------------------------------------------
    preview.object_preview(construction_.properties.ph)