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
EM September 7, 2022
    Args:
        _setttings: The Settings to use for the shading calculations. Connect a 
            'HBPH - Shading Factor Settings - LBT Rad'
            
        _shading_surfaces_winter: (List) A flat list of all the surfaces to consider when calculating 
            the detailed shading factors for WINTER. At the least, these should include all of the 
            building surfaces 'punched' with the apertures and all the aperture side
            'reveals'. This may also include additional site or building shading surfaces
            as desired. Use the 'HBPH - Create Building Shading' to generate 'punched' building shading.
        
        _shading_surfaces_summer: (List) A flat list of all the surfaces to consider when calculating 
            the detailed shading factors for SUMMER. At the least, these should include all of the 
            building surfaces 'punched' with the apertures and all the aperture side
            'reveals'. This may also include additional site or building shading surfaces
            as desired. Use the 'HBPH - Create Building Shading' to generate 'punched' building shading.
        
        _hb_rooms: (List[room.Room]) The Honeybee Rooms with apertures.
        
        _run: (bool) Set True to run the simulation.
    
    Returns:
        legend_: The Ladybug Legend for output / visualizations.
        
        winter_radiation_shaded_mesh_: (kWh) The colored mesh showing the winter-period 
            incident solar radiation on the apertures for output / visualizations.
        
        summer_radiation_shaded_mesh_: (kWh) The colored mesh showing the summer-period 
            incident solar radiation on the apertures for output / visualizations.
            
        hb_rooms_: The Honeybe Rooms with the shading factors added to all the apertures.
"""

import Grasshopper.Kernel as ghK
from honeybee_ph_rhino.gh_compo_io import ghio_lbt_shading

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Add Shading Factors - LBT Rad"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='SEP_07_2022')
if DEV:
    reload(ghio_lbt_shading)


# ------------------------------------------------------------------------------
if not _settings:
    msg = 'Please input _settings to calculate Radiation results.'
    ghenv.Component.AddRuntimeMessage( ghK.GH_RuntimeMessageLevel.Warning, msg )

if not _hb_rooms:
    msg = 'Please input Honeybee Rooms to calculate Radiation results.'
    ghenv.Component.AddRuntimeMessage( ghK.GH_RuntimeMessageLevel.Warning, msg )

if not _run:
    msg = 'Please set _run to True in order to calculate Radiation results.'
    ghenv.Component.AddRuntimeMessage( ghK.GH_RuntimeMessageLevel.Warning, msg )


# ------------------------------------------------------------------------------
if _run and _settings and _hb_rooms:
    # -- Setup the Interface Object
    IShadingLBTRadiation_ = ghio_lbt_shading.IShadingLBTRadiation(
            _settings,
            _shading_surfaces_winter,
            _shading_surfaces_summer,
            _hb_rooms,
    )
    
    # -- Run
    (
        legend_,
        winter_radiation_shaded_mesh_,
        summer_radiation_shaded_mesh_,
        hb_rooms_
    ) = IShadingLBTRadiation_.run()
    
else:
    hb_rooms_ = _hb_rooms

