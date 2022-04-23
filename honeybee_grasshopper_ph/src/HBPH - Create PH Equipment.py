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
Create a new detailed Passive House style equipment which can be added to the 
honeybee Rooms.
-
EM April 2, 2022
"""

import Grasshopper
import honeybee_ph_utils.preview
import honeybee_ph_rhino.gh_io
import honeybee_ph_rhino.gh_compo_io.ghio_equipment
import honeybee_energy_ph.load.ph_equipment

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create PH Equipment"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_01_2022')
if DEV:
    reload(honeybee_ph_rhino.gh_io)
    reload(honeybee_ph_rhino.gh_compo_io.ghio_equipment)
    #reload(honeybee_energy_ph.load.ph_equipment)
    reload(honeybee_ph_utils.preview)

#-------------------------------------------------------------------------------
class EquipmentTypeInputError(Exception):
    def __init__(self, _in, _valid_types):
        self.msg = "Error: Input Equipment type: '{}' not supported. Please only input: "\
        "{}".format(_in, _valid_types)
        super(EquipmentTypeInputError, self).__init__(self.msg)


#-------------------------------------------------------------------------------
# -- Setup the input nodes, get all the user input values
input_dict = honeybee_ph_rhino.gh_compo_io.ghio_equipment.get_component_inputs(_type)
honeybee_ph_rhino.gh_io.setup_component_inputs(ghenv, input_dict, _start_i=2)
input_values_dict = honeybee_ph_rhino.gh_io.get_component_input_values(ghenv)

#-------------------------------------------------------------------------------
# -- Build the new PH equipment object
equipment_classes = {
    1: honeybee_energy_ph.load.ph_equipment.PhDishwasher,
    2: honeybee_energy_ph.load.ph_equipment.PhClothesWasher,
    3: honeybee_energy_ph.load.ph_equipment.PhClothesDryer,
    4: honeybee_energy_ph.load.ph_equipment.PhRefrigerator,
    5: honeybee_energy_ph.load.ph_equipment.PhFreezer,
    6: honeybee_energy_ph.load.ph_equipment.PhFridgeFreezer,
    7: honeybee_energy_ph.load.ph_equipment.PhCooktop,
    13: honeybee_energy_ph.load.ph_equipment.PhPhiusMEL,
    14: honeybee_energy_ph.load.ph_equipment.PhPhiusLightingInterior,
    15: honeybee_energy_ph.load.ph_equipment.PhPhiusLightingExterior,
    16: honeybee_energy_ph.load.ph_equipment.PhPhiusLightingGarage,
    11: honeybee_energy_ph.load.ph_equipment.PhCustomAnnualElectric,
    17: honeybee_energy_ph.load.ph_equipment.PhCustomAnnualLighting,
    18: honeybee_energy_ph.load.ph_equipment.PhCustomAnnualMEL,
    }
if _type:
    try:
        equipment_class = equipment_classes[honeybee_ph_rhino.gh_io.input_to_int(_type)]
    except KeyError as e:
        raise EquipmentTypeInputError(_type, honeybee_ph_rhino.gh_compo_io.ghio_equipment.valid_equipment_types)

    equipment_ = equipment_class()
    for attr_name in vars(equipment_):
        if attr_name.startswith('_'):
            continue
        input_val = input_values_dict.get(attr_name)
        if input_val:
            setattr(equipment_, attr_name, input_val)
else:
    msg = "Set the 'equipment_type' to configure the user-inputs."
    ghenv.Component.AddRuntimeMessage(Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning, msg)


#-------------------------------------------------------------------------------
# -- Preview
honeybee_ph_utils.preview.object_preview(equipment_)