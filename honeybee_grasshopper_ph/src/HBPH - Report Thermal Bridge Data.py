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
Create Thermal-Bridge geometry and notes for exporting to PDF. Note that this 
component will generate both the 'highlight' geometry for each thermal-bridge one 
at a time, and also the 'background' building geometry. Pass all of the outputs 
along to the "HBPH - Export PDFs" component for exporting to PDF.
-
EM July 10, 2022
    Args:
        _hb_model: (honeybee.model.Model) The Honeybee-Model to use as the source.
        
        _highlight_outline_color_: (Color) Default=(R255, G0, B183). The color for the highlighted
            thermal-bridge elements.
            
        _highlight_outline_weight_: (float) Default=1 The print weight for the hightlighting
            thermal-bridge elements.
            
        _default_srfc_color_: (Color) Default=(R245, G245, B245). The color of the background 
            surfaces.
            
        _default_outline_color_: (Color) Default=(R40, G40, B40). The color of the background 
            surfaces edges.
            
        _default_outline_weight_: (float) Default=0.1 The print weight of the background 
            surface edges.

    Returns:
        tb_names_: The honeyee-Rooms with building-segment information added.
        
        tb_geometry_: A Tree of geometry.
            
        tb_rh_attributes_: A Tree of ObjectAttributs for the geometry.
            
        tb_lengths_: A Tree of the total length for each thermal-bridge found. Use 
            a "HBPH - Create Text Annotation" component if you would like to 
            add this information onto a Layout Page.
"""

from System.Drawing import Color

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from honeybee_ph_rhino.reporting import build_thermal_bridges
from honeybee_ph_rhino import gh_io

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Report Thermal Bridge Data"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_10_2022')
if DEV:
    reload(build_thermal_bridges)

        
# ------------------------------------------------------------------------------
# -- GH Interface
IGH = gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

# ------------------------------------------------------------------------------
results = build_thermal_bridges.get_tb_data(
            IGH,
            _hb_model,
            _highlight_outline_color_ or Color.FromArgb(255, 255, 0, 183),
            _highlight_outline_weight_ or 1,
            _default_srfc_color_ or Color.FromArgb(255, 245, 245, 245),
            _default_outline_color_ or Color.FromArgb(255, 40, 40, 40),
            _default_outline_weight_ or 0.10,
            )

tb_names_, tb_geometry_, tb_rh_attributes_, tb_lengths_ = results