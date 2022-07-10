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
Create a new Text Annotation object which can be used during PDF Export. These
annotations can be used to add titles or other data to Layouts, or to add notes or 
text directly into the Rhino-scene as well.
-
EM July 10, 2022
    Args:
        _text: (str) The Text for the annotation to show.
        
        _size: (float) The size of the Text to show. Default=0.25
        
        _location: (Rhino.Geometry.Point3d) The anchor point for the Text.
        
        _format: (str) Optional. A format string using the standard python
            'f-string' inputs. Incude the curly-braces. For example, if you 
            want to show the text "0.3456789" as "0.35 m3" you would pass 
            in "{:0.2f} m3" (inclding the curly braces).
            
        _justification: (int) Relative to the anchor point. Input either:
            0 [Bottom-Left]
            1 [Bottom-Center]
            2 [Bottom-Right]
            3 [Middle-Left]
            4 [Middle-Center]
            5 [Middle-Right]
            6 [Top-Left]
            7 [Top-Middle]
            8 [Top-Right]
            
    Returns:
        text_annotations_: The new TextAnnotations objects. These can be used by 
            the "HBPH - Export PDFs" component when exporting PDF documents.
"""


from System import Object
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
from Rhino.Geometry import Point3d

from honeybee_ph_rhino.reporting import to_pdf
from honeybee_ph_utils import input_tools

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Text Annotation"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_10_2022')
if DEV:
    reload(to_pdf)
    reload(input_tools)

text_annotations_ = DataTree[to_pdf.TextAnnotation]()

for i, branch in enumerate(_text.Branches):
    for k, txt in enumerate(branch):
        loc_branch = input_tools.clean_tree_get(_location, i, _default=[Point3d(0,0,0)])
        size_branch = input_tools.clean_tree_get(_size, i, _default=[0.25])
        format_branch = input_tools.clean_tree_get(_format, i, _default=["{}"])
        justify_branch = input_tools.clean_tree_get(_justification, i, _default=[4]) # Middle-Center
        
        location = input_tools.clean_get(loc_branch, k)
        size = input_tools.clean_get(size_branch, k)
        format = input_tools.clean_get(format_branch, k)
        justification = input_tools.clean_get(justify_branch, k)
    
        new_label = to_pdf.TextAnnotation(txt, size, location, format, justification)
        text_annotations_.Add(new_label, GH_Path(i))

