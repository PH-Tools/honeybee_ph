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
Convert an existing HBJSON file to a Passive House Exchange (PHX) model and write out 
the model data to a PHPP document. 
NOTE:
    - You must have a valid PHPP document to write to. The PHPP is not part of the 
    honeybee-ph plugin and must be purchased from PHI or your local reseller. For more 
    information, see: "https://passivehouse.com/04_phpp/04_phpp.htm"
    - The PHPP document you would like to write to should be open alongside Rhino, 
    and must be the the 'active' excel document. To ensure best results and least 
    likelihood of conflicts, it is recommended to close all other excel documents 
    on your system except the PHPP.
    - Once the PHPP file is open, set _write to True to run the writer. 
    - IMPORTANT: This component simply writes the data to the PHPP file. Once writen, 
    be sure to save your PHPP file with the new data to the appropriate location on 
    your computer.
-
EM May 22, 2022
    Args:
        _hbjson_file: (str) The full file path to the HBJSON you would like to write 
            out to PHPP.
        
        _phpp_version_: (str) Optional 4-letter code for the PHPP version to use.
        Currently supported versions include
        - "ENSI" (English SI units) [default]
        - "ENIP" (English IP units)
        - "ESSI" (Espanol SI units)
        - "DESI" (Deutsch SI units)
            
            
        _write: (bool) Set True to run the PHPP writer.
            
    Returns:
        hb_rooms_ (List[Room]) A list of the Honeybee Rooms with the ph-style occupancy set.
"""

import os
import honeybee.config
import PHX.run
import Grasshopper.Kernel as ghK

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Write to PHPP"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='MAY_22_2022')
if DEV:
    reload(PHX.run)

#-------------------------------------------------------------------------------
if os.name != 'nt':
    msg = "Error: This PHPP writer is only supported on Windows OS. It looks like "\
        "you are running '{}'?".format(os.name)
    ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Error, msg)


#-------------------------------------------------------------------------------
shape_file = os.path.join(
    honeybee.config.folders.python_package_path,
    "PHX",
    "to_phpp",
    "phpp_localization",
    "{}.json".format(_phpp_version_ or "ENSI")
)

if _write and _hbjson_file:
    PHX.run.write_hbjson_to_phpp(_hbjson_file, shape_file)
else:
    msg = "Open a valid PHPP file in Excel, and set _write to True."
    ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)
