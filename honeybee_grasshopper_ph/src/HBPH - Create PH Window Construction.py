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
EM April 23, 2022
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


try:  # import the core honeybee dependencies
    from honeybee.typing import clean_and_id_ep_string, clean_ep_string
except ImportError as e:
    raise ImportError('Failed to import honeybee:\t{}'.format(e))

try:  # import the honeybee-energy dependencies
    from honeybee_energy.material.glazing import EnergyWindowMaterialSimpleGlazSys
    from honeybee_energy.construction.window import WindowConstruction
    from honeybee_energy.lib.materials import window_material_by_identifier
except ImportError as e:
    raise ImportError('Failed to import honeybee_energy:\t{}'.format(e))

try:
    from honeybee_energy_ph.construction import window
except ImportError as e:
    raise ImportError('Failed to import honeybee_energy_ph:\t{}'.format(e))
    
try:
    from honeybee_ph_utils import preview, iso_10077_1
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_utils:\t{}'.format(e))



# --
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create PH Window Construction"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_23_2022')

if DEV:
    #reload(window)
    reload(preview)
    reload(iso_10077_1)


# --
if _glazing and _frame:

    # -- Create a new HB Simple Window Material
    mat_name = clean_and_id_ep_string('WindowMaterial') if _name_ is None else \
        clean_ep_string(_name_)

    # -- Set the NFRC/HBmaterial properties
    nfrc_u_factor = nfrc_u_factor_ or iso_10077_1.calculate_window_uw(_frame, _glazing)
    nfrc_shgc = nfrc_shgc_ or _glazing.g_value
    t_vis = t_vis_ or 0.6
    window_mat = EnergyWindowMaterialSimpleGlazSys(mat_name, nfrc_u_factor, nfrc_shgc, t_vis)
    if _name_ is not None:
        window_mat.display_name = _name_

    # -- Create a new HB Window Construction
    const_name = clean_and_id_ep_string('WindowConstruction') if _name_ is None else \
        clean_ep_string(_name_)
    construction_ = WindowConstruction(const_name, [window_mat])
    
    
    # -- Set the PH Properties on the WindowConstructionProperties
    construction_.properties.ph.ph_frame = _frame
    construction_.properties.ph.ph_glazing = _glazing


    # -- 
    preview.object_preview(construction_.properties.ph)