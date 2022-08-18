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
Create new HB-Energy SHW Object. This can then be applied to one or more Honeybee Rooms 
using the 'Apply SHW System' component. Note that many elements here replicate the existing 
Honeybee-Energy "HB SHW System" component, but allow for additional HB-PH elements such as 
piping and storage tanks to be added as well.
-
EM August 18, 2022

    Args:
        _system_type: [str] Text for the specific type of service hot water system and equipment.
            The "HB SHW Templates" component has a full list of the supported
            system templates.
        
        _name_: [str] Text to set the name for the Service Hot Water system and to be
            incorporated into unique system identifier. If the name is not
            provided, a random name will be assigned.
        
        _efficiency_: [float] A number for the efficiency of the heater within the system.
            For Gas systems, this is the efficiency of the burner. For HeatPump
            systems, this is the rated COP of the system. For electric systems,
            this should usually be set to 1. If unspecified this value will
            automatically be set based on the equipment_type. See below for
            the default value for each equipment type:
                * Gas_WaterHeater - 0.8
                * Electric_WaterHeater - 1.0
                * HeatPump_WaterHeater - 3.5
                * Gas_TanklessHeater - 0.8
                * Electric_TanklessHeater - 1.0
        
        _condition_: [float] A number for the ambient temperature in which the hot water tank
            is located [C]. This can also be a Room in which the tank is
            located. (Default: 22).
        
        _loss_coeff_: [float] A number for the loss of heat from the water heater tank to the
            surrounding ambient conditions [W/K]. (Default: 6 W/K).
        
        _tank_1_: [PhSHWTank] A new Passive House hot-water storage tank to add to the SHW System.
        
        _tank_2_: [PhSHWTank] A new Passive House hot-water storage tank to add to the SHW System.        
        
        _buffer_tank_: [PhSHWTank] A new Passive House hot-water buffer tank to add to the SHW System.
        
        _solar_tank_: [PhSHWTank] A new Passive House Solar-thermal hot-water storage tank to add to the SHW System.
    
        _heaters: List[PhHotWaterHeater] A list of any PH style HW-Heaters to add to the SHW System.
    
        _branch_piping: List[PhPipeElement] A List of any Branch Piping elements to
            add to the SHW System.
        
        _recirc_piping: List[PhPipeElement] A List of any Recirculation Piping elements to
            add to the SHW System.
    
    Returns:
        hb_shw_: [SHWSystem] A new Honeybee SHW System object which can be applied 
            to one or more Honeybee Rooms using the 'Apply SHW SYstem' component.
"""

from honeybee_ph_rhino.gh_compo_io import ghio_create_shw

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create SHW System"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='AUG_18_2022')
if DEV:
    #from honeybee_ph_rhino.gh_compo_io import ghio_validators
    #reload(ghio_validators)
    #reload(ghio_create_shw)
    #from honeybee_ph_utils import units
    #reload(units)
    pass

if _system_type:
    shw_sys = ghio_create_shw.ICreateSHWSystem(
        _system_type,
        _name_,
        _efficiency_,
        _condition_,
        _loss_coeff_,
        _tank_1_,
        _tank_2_,
        _buffer_tank_,
        _solar_tank_,
        _heaters, 
        _branch_piping,
        _recirc_piping
    )

    hb_shw_ = shw_sys.create_hb_shw_obj()