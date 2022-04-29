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
Create a new Hot-Water Heater with detailed Passive-House style inputs which 
can then be added to the HB-Energy SHW.
-
EM April 29, 2022
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from honeybee_ph_rhino import gh_io
import honeybee_ph_rhino.gh_compo_io.ghio_hw_heaters
import honeybee_energy_ph.hvac.hot_water
import honeybee_ph_utils.preview

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create SHW Heater"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_29_2022')
if DEV:
    reload(gh_io)
    reload(honeybee_ph_rhino.gh_compo_io.ghio_hw_heaters)
    reload(honeybee_energy_ph.hvac.hot_water)
    reload(honeybee_ph_utils.preview)

# ------------------------------------------------------------------------------
# -- GH Interface
IGH = gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

#-------------------------------------------------------------------------------
class HeaterTypeInputError(Exception):
    def __init__(self, _in, _valid_types):
        self.msg = "Error: Input Heater Type: '{}' not supported. Please only input: "\
        "{}".format(_in, _valid_types)
        super(HeaterTypeInputError, self).__init__(self.msg)

#-------------------------------------------------------------------------------
# -- Setup the input nodes, get all the user input values
input_dict = honeybee_ph_rhino.gh_compo_io.ghio_hw_heaters.get_component_inputs(heater_type)
honeybee_ph_rhino.gh_io.setup_component_inputs(IGH, input_dict)
input_values_dict = honeybee_ph_rhino.gh_io.get_component_input_values(ghenv)


#-------------------------------------------------------------------------------
# -- Build the new HW Heater object
heater_classes = {
    1: honeybee_energy_ph.hvac.hot_water.PhSHWHeaterElectric,
    2: honeybee_energy_ph.hvac.hot_water.PhSHWHeaterBoiler,
    3: honeybee_energy_ph.hvac.hot_water.PhSHWHeaterBoilerWood,
    4: honeybee_energy_ph.hvac.hot_water.PhSHWHeaterDistrict,
    5: honeybee_energy_ph.hvac.hot_water.PhSHWHeaterHeatPump,
    6: honeybee_energy_ph.hvac.hot_water.PhSHWHeaterHeatPump,
    }
if heater_type:
    try: 
        heater_class = heater_classes[honeybee_ph_rhino.gh_io.input_to_int(heater_type)]
    except KeyError as e:
        raise HeaterTypeInputError(heater_type, honeybee_ph_rhino.gh_compo_io.ghio_hw_heaters.valid_heater_types)

    heater_ = heater_class()
    for attr_name in dir(heater_):
        input_val = input_values_dict.get(attr_name)
        if input_val:
            setattr(heater_, attr_name, input_val)
else:
    msg = "Set the 'heater_type' to configure the user-inputs."
    ghenv.Component.AddRuntimeMessage(gh.Kernel.GH_RuntimeMessageLevel.Warning, msg)

#-------------------------------------------------------------------------------
# -- Preview
honeybee_ph_utils.preview.object_preview(heater_)