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
Collects and organizes data for a Ventilator Unit (HRV/ERV). Used to build up a 
PH-Style Ventilation System.
-
EM April 28, 2022
    Args:
        unit_name_: (Optional[float]) The name of the Ventilator Unit
        sensible_hr_: (Optional[float]) Input the Ventialtion Unit's Heat Recovery %. Default is 75% 
        latent_hr_: (Optional[float]) Input the Ventialtion Unit's Moisture Recovery %. Default is 0% (HRV)
        elec_efficiency_: (Optional[float]) Input the Electrical Efficiency of the Ventialtion 
            Unit (W/m3h). Default is 0.55 W/m3h
        frost_temp_: (Optional[float]) Min Temp [C] for frost protection to kick in. [deg.  C]. Default is -5 C
        inside_: (bool) True=Unt is installed inside the conditioned space. False=installed outside.
    Returns:
        unit_: A Ventilator object for the Ventilation System. Connect to the 
            'ventUnit_' input on the 'Create Vent System' to build a PH-Style Ventilation System.
"""

import honeybee_energy_ph.hvac.ventilation
import honeybee_ph_utils.preview

# --- 
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Ventilator"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_28_2022')
if DEV:
    reload(honeybee_energy_ph.hvac.ventilation)
    reload(honeybee_ph_utils.preview)

# ------------------------------------------------------------------------------
unit_ = honeybee_energy_ph.hvac.ventilation.Ventilator()
if unit_name_: unit_.name = unit_name_
if sensible_hr_: unit_.sensible_heat_recovery = sensible_hr_
if latent_hr_: unit_.latent_heat_recovery = latent_hr_
if elec_efficiency_: unit_.electric_efficiency = elec_efficiency_
if frost_protection_ is not None:
    unit_.frost_protection_reqd = frost_protection_
if frost_temp_: unit_.temperature_below_defrost_used = frost_temp_
if inside_ is not None:
    unit_.in_conditioned_space = inside_

# ------------------------------------------------------------------------------
honeybee_ph_utils.preview.object_preview(unit_)