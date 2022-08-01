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
Calculate detailed winter/summer seasonal shading factors and add them to all apertures in the 
Honeybee Rooms input.
---
This component uses the LadybugTools 'IncidentRadiation' method. As stated on that component:
---
"Note that NO REFLECTIONS OF SOLAR ENERGY ARE INCLUDED IN THE ANALYSIS
PERFORMED BY THIS COMPONENT and it is important to bear in mind that vertical
surfaces typically receive 20% - 30% of their solar energy from reflection off
of the ground. Also note that this component uses the CAD environment's ray
intersection methods, which can be fast for geometries with low complexity
but does not scale well for complex geometries or many test points. For such
complex cases and situations where relfection of solar energy are important,
honeybee-radiance should be used."
-
EM August 1, 2022
    Args:
        _setttings: The Settings to use for the shading calculations. Connect a 
            'HBPH - Shading Factor Settings - LBT Rad'
            
        _shading_surfaces: A flat list of all the surfaces to consider when calculating 
            the detailed shading factors. At the least, these should include all of the 
            building surfaces 'punched' with the apertures and all the aperture side
            'reveals'. This may also include additional site or building shading surfaces
            as desired. Use the 'HBPH - Create Building Shading' to generate 'punched' building shading.
        
        _hb_rooms: The Honeybee Rooms with apertures.
        
        _run: Set True to run the simulation.
    
    Returns:
        legend_: The Ladybug Legend for output / visualizations.
        
        winter_radiation_shaded_mesh_: (kWh) The colored mesh showing the winter-period 
            incident solar radiation on the apertures for output / visualizations.
        
        summer_radiation_shaded_mesh_: (kWh) The colored mesh showing the summer-period 
            incident solar radiation on the apertures for output / visualizations.
            
        hb_rooms_: The Honeybe Rooms with the shading factors added to all the apertures.
"""

import Rhino
from System import Object
from Grasshopper import DataTree
from Grasshopper.Kernel.Data import GH_Path
import Grasshopper.Kernel as ghK

from honeybee_ph_rhino.gh_compo_io import ghio_lbt_shading, ghio_win_shade_surfaces

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add Shading Factors - LBT Rad"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='AUG_1_2022')
if DEV:
    reload(ghio_lbt_shading)
    reload(ghio_win_shade_surfaces)


cpus = None


if not _settings:
    msg = 'Please input _settings to calculate Radiation results.'
    ghenv.Component.AddRuntimeMessage( ghK.GH_RuntimeMessageLevel.Warning, msg )

if not _hb_rooms:
    msg = 'Please input Honeybee Rooms to calculate Radiation results.'
    ghenv.Component.AddRuntimeMessage( ghK.GH_RuntimeMessageLevel.Warning, msg )

if not _run:
    msg = 'Please set _run to True in order to calculate Radiation results.'
    ghenv.Component.AddRuntimeMessage( ghK.GH_RuntimeMessageLevel.Warning, msg )


if _run and _settings and _hb_rooms:
    hb_rooms_ = []
    
    # ---------------------------------------------------------------------------
    # Create the context shading mesh geometry
    shade_mesh = ghio_lbt_shading.create_shading_mesh(
        _shading_surfaces,
        _settings.mesh_params
    )
    
    # deconstruct the sky-matrix and get the sky dome vectors. Winter (w) and Summer (s)
    # ---------------------------------------------------------------------------
    w_sky_vecs, w_total_sky_rad = ghio_lbt_shading.deconstruct_sky_matrix(_settings.winter_sky_matrix)
    s_sky_vecs, s_total_sky_rad = ghio_lbt_shading.deconstruct_sky_matrix(_settings.summer_sky_matrix)
    
    
    # Calc window surface shaded and unshaded radiation
    #---------------------------------------------------------------------------
    lb_window_meshes = []
    winter_radiation_shaded_ = DataTree[Object]()
    winter_radiation_shaded_detailed_ = DataTree[Object]()
    winter_radiation_unshaded_ = DataTree[Object]()
    summer_radiation_shaded_ = DataTree[Object]()
    summer_radiation_shaded_detailed_ = DataTree[Object]()
    summer_radiation_unshaded_ = DataTree[Object]()
    mesh_by_window = DataTree[Object]()
    
    inset_window_surfaces = ghio_win_shade_surfaces.create_inset_aperture_surfaces(_hb_rooms)
    win_count = 0
    for room in _hb_rooms:
        new_room = room.duplicate()
        
        for face in new_room.faces:
            for aperture in face.apertures:
                window_surface = ghio_win_shade_surfaces.create_inset_aperture_surface(aperture)

                # Build the meshes
                # ----------------------------------------------------------------------
                pts, nrmls, win_msh, win_msh_bck, rh_msh = ghio_lbt_shading.build_window_meshes(window_surface, _settings.grid_size, _settings.mesh_params)
                lb_window_meshes.append(win_msh)
                
                
                # Solve Winter
                # ----------------------------------------------------------------------
                args_winter = (shade_mesh, win_msh_bck, pts, w_sky_vecs, nrmls, cpus)
                
                int_matrix_s, int_matrix_u, angles_s, angles_u = ghio_lbt_shading.generate_intersection_data(*args_winter)
                w_rads_shaded, face_areas = ghio_lbt_shading.calc_win_radiation(int_matrix_s, angles_s, w_total_sky_rad, win_msh)
                w_rads_unshaded, face_areas = ghio_lbt_shading.calc_win_radiation(int_matrix_u, angles_u, w_total_sky_rad, win_msh)
                
                winter_rad_shaded = sum(w_rads_shaded)/sum(face_areas)
                winter_rad_unshaded = sum(w_rads_unshaded)/sum(face_areas)
                
                winter_radiation_shaded_detailed_.AddRange(w_rads_shaded, GH_Path(win_count))
                winter_radiation_shaded_.Add(winter_rad_shaded, GH_Path(win_count))
                winter_radiation_unshaded_.Add(winter_rad_unshaded, GH_Path(win_count))
                
                
                # Solve Summer
                # ----------------------------------------------------------------------
                args_summer = (shade_mesh, win_msh_bck, pts, s_sky_vecs, nrmls, cpus)
                
                int_matrix_s, int_matrix_u, angles_s, angles_u = ghio_lbt_shading.generate_intersection_data(*args_summer)
                s_rads_shaded, face_areas = ghio_lbt_shading.calc_win_radiation(int_matrix_s, angles_s, s_total_sky_rad, win_msh)
                s_rads_unshaded, face_areas = ghio_lbt_shading.calc_win_radiation(int_matrix_u, angles_u, s_total_sky_rad, win_msh)
                
                summer_rad_shaded = sum(s_rads_shaded)/sum(face_areas)
                summer_rad_unshaded = sum(s_rads_unshaded)/sum(face_areas)
                
                summer_radiation_shaded_detailed_.AddRange(s_rads_shaded, GH_Path(win_count))
                summer_radiation_shaded_.Add(summer_rad_shaded, GH_Path(win_count))
                summer_radiation_unshaded_.Add(summer_rad_unshaded, GH_Path(win_count))
                
                
                mesh_by_window.Add(rh_msh, GH_Path(win_count) )
                
                
                # Set the aperture shading factors
                # ----------------------------------------------------------------------
                aperture.properties.ph.winter_shading_factor = winter_rad_shaded / winter_rad_unshaded
                aperture.properties.ph.summer_shading_factor = summer_rad_shaded / summer_rad_unshaded
                
                
                win_count += 1
                
        # -- Add the new room to the output set
        # ----------------------------------------------------------------------
        hb_rooms_.append(new_room)
    
    # Create the mesh and legend outputs
    # --------------------------------------------------------------------------
    # Flatten the radiation data trees
    winter_rad_vals = [item for branch in winter_radiation_shaded_detailed_.Branches for item in branch]
    summer_rad_vals = [item for branch in summer_radiation_shaded_detailed_.Branches for item in branch]
    
    # Create the single window Mesh
    joined_window_mesh = ghio_lbt_shading.create_window_mesh( lb_window_meshes )
    
    winter_graphic, title = ghio_lbt_shading.create_graphic_container('Winter', winter_rad_vals, joined_window_mesh, _settings.legend_par)
    winter_radiation_shaded_mesh_, legend_ = ghio_lbt_shading.create_rhino_mesh(winter_graphic, joined_window_mesh)
    
    summer_graphic, title = ghio_lbt_shading.create_graphic_container('Summer', summer_rad_vals, joined_window_mesh, _settings.legend_par)
    summer_radiation_shaded_mesh_, legend_ = ghio_lbt_shading.create_rhino_mesh(summer_graphic, joined_window_mesh)
    
else:
    hb_rooms_ = _hb_rooms

