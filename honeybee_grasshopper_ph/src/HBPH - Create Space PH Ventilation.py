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
Create a List or Tree of new SpacePhVentFlowRates objects which can be used to 
set the PH-Style ventilation flow rates for a Space.
-
EM June 11, 2022
    Args:
        _v_sup: (float): A list or Tree of Supply-air ventilation flow rates.
        
        _v_eta: (float): A list or Tree of Extract-air ventilation flow rates.
        
        _v_tran: (float): A list or Tree of Transfer-air ventilation flow rates.

    Returns:
        space_ph_vent_: (Tree[SpacePhVentFlowRates]) A DataTree of the Space Flow rate objects.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from honeybee_ph_rhino.gh_compo_io import ghio_spc_vent

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Space PH Ventilation"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_11_2022')
if DEV:
    reload(ghio_spc_vent)

# ------------------------------------------------------------------------------
# -- GH Interface
IGH = honeybee_ph_rhino.gh_io.IGH(ghdoc, ghenv, sc, rh, rs, ghc, gh)

# ------------------------------------------------------------------------------
ghio_obj = ghio_spc_vent.ISpacePhVentFlows(IGH, _v_sup, _v_eta, _v_tran)
space_ph_vent_ = ghio_obj.create_output()
