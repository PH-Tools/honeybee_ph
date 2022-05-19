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
Enter the relevant Phius Certification threshold data for the building-segment.
-
EM May 20, 2022
    Args:
        _certification_type: Input either -
            "1-Passive House"
            "2-EnerPHit"
            "3-PHI Low Energy Building"
            "4-Other"

        _certification_class: Input either -
            "1-Classic"
            "2-Plus"
            "3-Premium"

        _primary_energy_type: Input either -
            "1-PE (non-renewable)"
            "2-PER (renewable)"

        _enerphit_type: Input either -
            "1-Component method"
            "2-Energy demand method"

        _retrofit: Input either -
            "1-New building"
            "2-Retrofit"
            "3-Step-by-step retrofit"

    Returns:
        phi_certification_: The PHI Certification Settings object to 
            assign to one or more Building Segments.
"""


from honeybee_ph_rhino import gh_io
from honeybee_ph_utils import preview, enumerables
from honeybee_ph import phi


#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - PHI Certification"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='MAY_20_2022')
if DEV:
    reload(enumerables)
    reload(gh_io)
    reload(preview)
    reload(phi)


#-------------------------------------------------------------------------------

phi_certification_ =  phi.PhiCertification()
phi_certification_.certification_type = gh_io.input_to_int(_certification_type)
phi_certification_.certification_class = gh_io.input_to_int(_certification_class)
phi_certification_.primary_energy_type = gh_io.input_to_int(_primary_energy_type)
phi_certification_.enerphit_type = gh_io.input_to_int(_enerphit_type)
phi_certification_.retrofit_type = gh_io.input_to_int(_retrofit)


preview.object_preview(phi_certification_)