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
Create a new HBPH Window Frame. If only a single HBPH Frame Element is input (to the 'top') that
frame element will be used for all sides. Otherwise, input the various frame elements as needed.

-
EM July 2, 2022
    Args:
        _name_: (str)
        
        _top: (PhWindowFrameElement) Then HBPH Window Frame Element to use for the 'top'
            element of the full window frame.
            
        _right: (PhWindowFrameElement) Then HBPH Window Frame Element to use for the 'right'
            element of the full window frame.
            
        _bottom: (PhWindowFrameElement) Then HBPH Window Frame Element to use for the 'bottom'
            element of the full window frame.
            
        _left: (PhWindowFrameElement) Then HBPH Window Frame Element to use for the 'left'
            element of the full window frame.
    
    Returns:
        frame_: A new HBPH WindowFrame which can be used to build an HBPH Window Constrution.
"""

try:
    from honeybee_ph_utils import preview
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_utils:\t{}'.format(e))

try:
    from honeybee_ph_rhino.gh_compo_io import ghio_ph_frame
except ImportError as e:
    raise ImportError('Failed to import honeybee_ph_rhino:\t{}'.format(e))


# -------------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Create PH Window Frame"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='JUL_02_2022')

if DEV:
    reload(preview)
    #reload(ghio_ph_frame)


# -------------------------------------------------------------------------------------
ghio_frame = ghio_ph_frame.IPhWindowFrame()
ghio_frame.display_name = _name_
ghio_frame.top = _top
ghio_frame.right = _right
ghio_frame.bottom = _bottom
ghio_frame.left = _left

frame_ = ghio_frame.create_HBPH_Object()

# -------------------------------------------------------------------------------------
preview.object_preview(frame_)