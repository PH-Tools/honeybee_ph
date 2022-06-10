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
Create new PH-Spaces. 
-
Spaces represent smaller units than HB-Rooms and can be made up of one or more individual 
volumes. This is useful if you are calculating interior net-floor-area or volume 
as in the Passive House models. Each Space will map to a single entry in the WUFI 
'Ventilation Rooms' or a PHPP 'Additional Ventilation'.
-
A single Space is made of one or more 'Volumes'. ie: a bedroom might have a volume for 
the main space, and another volume for the closet which is separated by the thicknes of 
a wall. 
-
Each Volume is made of one or more floor-segments. Each floor-segment can have a
'weighting factor' applied for calculating the TFA/iCFA for Passive House certification.
-
EM June 10, 2022
    Args:
        _flr_seg_geom: (Tree[Geometry]) The Rhino geometry that you would like to use 
            to create the Floor-Segments of the various Spaces. Each branch should be a list 
            of Rhino geometry objects that will be used to create a single new Space.
        
        _weighting_factors: (Tree[float]) An optional input Tree of TFA/iCFA weighting
            factors to apply to the input floor-segment geometry.
        
        _volume_geometry: (Tree[Geometry]) An optional input Tree of Rhino Geometry
            describing the space-shape of the individual volumes. 
        
        _volume_heights: (Tree[float]) Default=2.5m An optional input Tree of heights
            to use when building the volume geometry.
        
        _space_names: (Tree[float]) Default="_Unnamed_" An optional input Tree of names
            to use when building the spaces
        
        _space_numbers: Default="000" An optional input Tree of space numbers
            to use when building the spaces
    
    Returns:
        floor_breps_: Preview of the Space Floor geometry created. Useful for debugging.
        
        volume_breps_: Preview of the Space Volume geometry created. Useful for debugging.
        
        spaces_: The new PH-Spaces created
"""

import scriptcontext as sc
import Rhino as rh
import rhinoscriptsyntax as rs
import ghpythonlib.components as ghc
import Grasshopper as gh
from Grasshopper import DataTree
from System import Object, Double, String
from Grasshopper.Kernel.Data import GH_Path

from ladybug_rhino.fromgeometry import from_face3d

from honeybee_ph import space
from honeybee_ph_rhino import gh_io
from honeybee_ph_rhino.make_spaces import make_floor, make_volume

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create Spaces"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUN_10_2022')
if DEV:
    pass
    #reload(space)
    #reload(gh_io)
    #reload(make_spaces)

# ------------------------------------------------------------------------------
# -- GH Interface
IGH = gh_io.IGH( ghdoc, ghenv, sc, rh, rs, ghc, gh )

# ------------------------------------------------------------------------------
# -- Organize the input trees, lists, lengths, defaults
def clean_input_tree(_input_tree, branch_count, default, type=Object):
    # type (DataTree, int, Any, Any) -> DataTree[<type>]
    """Align the input Datatrees so they are all the same length. Apply defaults."""
    
    new_tree = DataTree[type]()
    for i in range(branch_count):
        try:
            new_tree.AddRange(_input_tree.Branch(i), GH_Path(i))
        except ValueError:
            new_tree.Add(default, GH_Path(i))
    return new_tree

# ------------------------------------------------------------------------------
input_len = len(_flr_seg_geom.Branches)
weighting_factors = clean_input_tree(_weighting_factors, input_len, 1.0, Double)
volume_heights = clean_input_tree(_volume_heights, input_len, 2.5, Double)
space_names = clean_input_tree(_space_names, input_len, '_Unnamed_', String)
space_numbers = clean_input_tree(_space_numbers, input_len, '000', String)

# ------------------------------------------------------------------------------
spaces_ = []
floor_breps_ = DataTree[Object]()
volume_breps_ = DataTree[Object]()
# -- Build one Space for each branch on the _flr_seg_geom input tree
for i, flr_srfc_list in enumerate(_flr_seg_geom.Branches):
    new_space = space.Space()
    new_space.name = space_names.Branch(i)[0]
    new_space.number = space_numbers.Branch(i)[0]
    
    space_floors, e = make_floor.space_floor_from_rh_geom(IGH, list(flr_srfc_list))
    if e:
        error_ = [from_face3d(s) for s in e]
        msg='Error: There was a problem joining together one or more group of floor surfaces?'\
            'Check the "error_" output for a preview of the surfaces causing the problem'\
            'Check the names and numbers of the surfaces, and make sure they can be properly merged?'
        IGH.error(msg)
    space_volumes = make_volume.volumes_from_floors(IGH, space_floors, volume_heights.Branch(i))
    new_space.add_new_volumes(space_volumes)
    
    spaces_.append(new_space)
    
    # -- Output Preview
    floor_breps_.AddRange([from_face3d(flr.geometry) for flr in space_floors], GH_Path(i))
    for srfc_list in [IGH.convert_to_rhino_geom(vol.geometry) for vol in space_volumes]:
        vol_brep = ghc.BrepJoin(srfc_list).breps
        volume_breps_.Add(vol_brep, GH_Path(i))