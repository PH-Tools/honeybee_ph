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
This component is used to create PDF report pages from the Honeybee-Model geometry. This 
is especially useful when submitting projects for compliance review and you need to generate
a batch of standardized report pages. This component will accept DataTrees where each brach of the 
DataTree represents a separate PDF file to output. 
-
This component will temporarily bake geometry and text annotations to the Rhnio scene, set the layer-states, and 
control the active view. Once the PDF export is complete, the component should reset the Rhino
layer-states and active-view to the same state as before export.
-
Note: printing from Rhino is a huge pain. This exporter *seems* to work best when you set your DetailView to 
'Wireframe' display mode most of the time. If you are getting funny results, try setting your Display Mode
and turning off things like shadows to see if that helps. If you are having trouble with 'draw-order' (ie: 
some things 'in front' are showing up 'behind' etc., try setting '_raster' to True. Vector export seems to 
cause all sorts of unexpected results sometimes.
-
Set the component '_export_pdfs' to 'True' to run the exporter.
-
EM July 10, 2022
    Args:
        _save_folder: (str) The name of the target folder to save the PDF files to.
        
        _file_names: (Tree[str]) A Tree where each branch contains the name of the PDF file to export.
        
        _layout_name: (str) The name of the Rhino-Layout to use when exporting the PDF report.
        
        _layers_on: (List[str]) A list of the Layer names to leave 'on' (visible) when exporting
            to PDF. When the exporter is run, all layers EXCEPT the ones listed here will be turned
            off, and then the original layer-state will be reset when the PDF export is complete.
            
        _clipping_plane_locations: (Tree[ClippingPlaneLocation]): A Tree of ClippingPlaneLocation
            objects which describe the location, normal, and target views of any Clipping Planes
            in the Scene. This is useful when outputting things like floor plans and you would like 
            to isolate just a certain portion of the Rhino scene when exporting PDF drawings.
            
        _geom: (Tree[Rhino.Geometry]) A Tree of Rhino Geometry. Each branch of the tree will be baked
            to the Rhino scene, exported as a PDF, and then removed from the scene.
            
        _geom_attributes: (Tree[ObjectAttributes]) A Tree of Rhino ObjectAttributes which will be 
            used to bake the objects to the scene.
        
        _model_annotations: (Tree[TextAnnotation]) A Tree of TextAnnotation objects. Create these objects 
            using the "HBPH - Create Text Annotation" component. Any TextAnnotations input here will be 
            baked to the Rhino Scene (Model-space).
            
        _layout_annotations: (Tree[TextAnnotation]) A Tree of TextAnnotation objects. Create these objects 
            using the "HBPH - Create Text Annotation" component. Any TextAnnotations input here will be 
            baked to the Rhino Layout (Paper-space).
            
        _raster: (bool) default=False (vector). Set True to output the PDF as a raster image. This is 
            sometimes needed when Rhino is unable to properly output vector artwork. If you are 
            having trouble with draw-order or line-weights / types, try setting to True.
            
        _export_pdfs: (bool) Set True to run the exporter.

    Returns:
        file_paths_: The full path(s) to the PDF files created.
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh

from honeybee_ph_rhino.reporting import to_pdf
from honeybee_ph_rhino import gh_io

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Export PDFs"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_10_2022')
if DEV:
    reload(to_pdf)

        
# ------------------------------------------------------------------------------
# -- GH Interface
IGH = gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

# ------------------------------------------------------------------------------
file_paths_ = to_pdf.gen_file_paths(_save_folder, _file_names, _geom.BranchCount)

if file_paths_ and _geom and _layout_name and _export_pdfs:
    to_pdf.export_pdfs(
                IGH,
                file_paths_,
                _layout_name,
                _layers_on,
                _clipping_plane_locations,
                _geom,
                _geom_attributes,
                _layout_annotations,
                _model_annotations,
                _raster,
                )
    