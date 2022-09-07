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
Input PH-Style monthly average solar radiation values (kWh/m2) for the different orientations. This data 
will be used to configure the 'Climate' inputs in the Passive House models. Note that this data should
represent monthly average values. Information on climate data can be found at:
-
    - PHI: https://passipedia.org/planning/climate_data_tool
    - PHIUS: https://www.phius.org/climate-data
-
Note also that this component will *NOT* reset any of the Honeybee EnergyPlus climate, and you will need to set
that separately using a normal EPW file with hourly data.
-
EM September 7, 2022
    Args:
        _north_: (List[float]) A list of 12 monthly average radiation (kWh/m2) values for the NORTH. If 
            none are input, all values will be set to 0.

        _east_: (List[float]) A list of 12 monthly average radiation (kWh/m2) values for the EAST. If 
            none are input, all values will be set to 0.

        _south_: (List[float]) A list of 12 monthly average radiation (kWh/m2) values for the SOUTH. If 
            none are input, all values will be set to 0.

        _west_: (List[float]) A list of 12 monthly average radiation (kWh/m2) values for the WEST. If 
            none are input, all values will be set to 0.

        _global_: (List[float]) A list of 12 monthly average radiation (kWh/m2) values for the GLOBAL (Horiz.). If 
            none are input, all values will be set to 0.

    Returns:
        monthly_radiation_: A new HBPH Monthly-Radiation object which can be passed to an "HBPH - PH Climate Data"
            component.
"""

from honeybee_ph_rhino.gh_compo_io import ghio_climate
from honeybee_ph_utils import preview

# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - PH Climate Monthly Radiation"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='SEP_07_2022')

if DEV:
    from honeybee_ph import site
    from honeybee_ph_utils import units
    reload(units)
    from honeybee_ph_rhino.gh_compo_io import ghio_validators
    reload(ghio_validators)
    reload(site)
    reload(ghio_climate)

# -------------------------------------------------------------------------------------
IClimateMonthlyRad= ghio_climate.IClimateMonthlyRadiation(
        _north_,
        _east_,
        _south_,
        _west_,
        _global_,
    )

monthly_radiation_ = IClimateMonthlyRad.create_hbph_obj()

# -------------------------------------------------------------------------------------
preview.object_preview(monthly_radiation_)