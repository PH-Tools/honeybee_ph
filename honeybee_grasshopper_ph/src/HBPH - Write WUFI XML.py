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
Convert an HBJSON file into a new WUFI-XML file which can then be opened using 
WUFI-Passive. This will read in the HBJSON, rebuild the HB-Model before converting the 
Model into a WUFI-Passive file.
-
EM May 22, 2022
    Args:
        _filename: (str) The filename for the WUFI XML file.
        
        _save_folder: (str) The folder path to save the WUFI XML file to.
        
        _hb_json_file: (str) The path to the HBJSON file to convert into WUFI XML.
        
        _write_xml: (bool) Set True to run. 
            
    Returns:
        xml_file_: The full path to the output WUFI XML file.
"""


import os
import json

try:  # import the core honeybee dependencies
    from honeybee.config import folders as hb_folders
except ImportError as e:
    raise ImportError('Failed to import honeybee:\t{}'.format(e))

import PHX.run

# ------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Write WUFI XML"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='MAY_22_2022')
if DEV:
    reload(PHX.run)

# ------------------------------------------------------------------------------
if _write_xml and _hb_json_file:
    d, f = PHX.run.convert_hbjson_to_WUFI_XML(_hb_json_file, _filename, _save_folder)
    xml_file_ = os.path.join(d, f)
