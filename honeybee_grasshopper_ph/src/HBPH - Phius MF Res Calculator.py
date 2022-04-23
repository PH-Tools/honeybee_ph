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
Calculate the Phius Multifamily Elec. Equipment Residential values (MEL and Lighting). The results of this 
component should match the Phius Multifamily Calculator.
Note also that for this to work properly, each dwelling unit (apt) should be its own Honeybee-Room.
-
The resulting elec_equipment_ objects can be added to the Honeybee-Rooms by using a "Add PH Equipment"
component and passing them to the 'equipment_' inputs. Note that this component will only calcuate the values
in the Phius Multifamily Workbook. These include MEL, Interior-Lighting, Exterior-Lighting, and Garage-Lighting.
This does NOT include the other residential appliances (fridge, cooking, etc..). Be sure to add those 
to the Residential Honeybee-Rooms in addition to the elec_equipment_ created by this component.
-
EM April 22, 2022

    Args:
        int_light_HE_frac_: (float) default=1.0 | The % (0-1.0) of interior lighting
            that is 'high efficiency'
            
        ext_light_HE_frac_: (float) default=1.0 default=1.0 | The % (0-1.0) of exterior
            lighting that is 'high efficiency'
        
        garage_light_HE_frac_: (float) default=1.0 | The % (0-1.0) of garage lighting
            that is 'high efficiency'
            
        _hb_rooms: (list[room.Room]): A list of the Honeybee Rooms to calculate the Phius Multifamily 
            Elec. Equipment for. 
            
    Returns:
        res_data_by_story_: (For Error-Checking) This is the input data for the residential stories. This 
            data can be copy/pasted into the Phius MF Claculator "Dwelling Units" B5 for vertification.
        
        res_totals_: (For Error-Checking) This is the computed residential story energy consumption. This
            data should match the values computed in the Phius MF Calculator "Dwelling Units" Columns J:N
            
        non_res_program_data_: (For Error-Checking) This is the input data for the non-residential programs
            found on the Honeybee-Rooms. This can be copy/pasted into the Phius MF Calculator worksheet 
            "Common Areas" "Default Space Types" section for verification.
        
        non_res_room_data_: (For Error-Checking) This is the input data for the non-residential spaces found
            in the Honeybee-Rooms. This can be copy/pasted intpo the Phius MF Calculator worksheet "Common Areas"
            "Rooms Table" section for verification.
        
        non_res_totals_: (For Error-Checking) This is the computed non-residential room energy consumption. This
            data should match the values computed in the Phius MF Calculator worksheet "Common Areas" columns H:M
            
        elec_equipment_: The PH-Electric Equipment objects for the MEL, Interior-Lighting, Exterior-Lighting 
            and Garage-Lighting. This equipment can be added to the Honeybee-Rooms by using an 'Add PH Equipment'
            component and passing these objects into the 'equipment_' input node.
            
        hb_res_rooms_: The residential HB-Rooms.
        
        hb_nonres_rooms_: The non-residential HB-Rooms.
"""

import Grasshopper.Kernel as ghK
from honeybee_energy_ph.load import phius_mf
from honeybee_energy_ph.load import ph_equipment
from honeybee_ph_rhino.gh_compo_io import ghio_phius_mf
import honeybee_ph_utils.preview

#-------------------------------------------------------------------------------
import honeybee_ph_rhino._component_info_
reload(honeybee_ph_rhino._component_info_)
ghenv.Component.Name = "HBPH - Phius MF Res Calculator"
DEV = True
honeybee_ph_rhino._component_info_.set_component_params(ghenv, dev='APR_22_2022')
if DEV:
    reload(phius_mf)
    reload(honeybee_ph_utils.preview)
    reload(ghio_phius_mf)


if _hb_rooms:
    # ------------------------------------------------------------------------------
    # -- Break out the Res from the non-Res HB-Rooms
    hb_res_rooms_ = [ rm for rm in _hb_rooms 
        if rm.properties.energy.people.properties.ph.is_dwelling_unit]
    hb_nonres_rooms_ = [ rm for rm in _hb_rooms 
        if not rm.properties.energy.people.properties.ph.is_dwelling_unit]
    
    if not hb_res_rooms_:
        msg = "Warning: No Residential HB-Rooms found?"
        ghenv.Component.AddRuntimeMessage(ghK.GH_RuntimeMessageLevel.Warning, msg)

    # Calculate the Elec. Energy use for the residential HB-Rooms
    # ------------------------------------------------------------------------------
    # -- Check the inputs for errors, display warnings
    ghio_phius_mf.check_inputs(hb_res_rooms_, ghenv)


    # ------------------------------------------------------------------------------
    # -- Determine the Input Res Honeybee Room attributes by story

    rooms_by_story = ghio_phius_mf.sort_rooms_by_story( hb_res_rooms_ )
    phius_stories = [phius_mf.PhiusResidentialStory(room_list) for room_list in rooms_by_story]
    floor_area_by_story_m2_ = [story.total_floor_area_m2 for story in phius_stories]
    floor_area_by_story_ft2_ = [story.total_floor_area_ft2 for story in phius_stories]
    num_dwellings_by_story_ = [story.total_number_dwellings for story in phius_stories]
    num_bedrooms_by_story_ = [story.total_number_bedrooms for story in phius_stories]


    # ------------------------------------------------------------------------------
    # -- Calculate the total Res. Elec. Energy Consumption

    mel_by_story = [story.mel for story in phius_stories]
    lighting_int_by_story = [story.lighting_int for story in phius_stories]
    lighting_ext_by_story = [story.lighting_ext for story in phius_stories]
    lighting_garage_by_story = [story.lighting_garage for story in phius_stories]

    total_dwelling_units = sum(story.total_number_dwellings for story in phius_stories)
    total_res_mel = sum(mel_by_story)
    total_res_int_lighting = sum(lighting_int_by_story)
    total_res_ext_lighting = sum(lighting_ext_by_story)
    total_res_garage_lighting = sum(lighting_garage_by_story)
    
    # -- Collect for output preview
    res_data_by_story_ = [
        ",".join([
            str(story.story_number),
            str(story.total_floor_area_ft2),
            str(story.total_number_dwellings),
            str(story.total_number_bedrooms)
        ])
        for story in phius_stories]
        
    res_totals_ = [
        ",".join([
            str(story.design_occupancy),
            str(story.mel),
            str(story.lighting_int),
            str(story.lighting_ext),
            str(story.lighting_garage),
        ])
        for story in phius_stories]
    res_totals_.insert(0, 
            str("FLOOR-Design Occupancy, FLOOR-Televisions + Mis. Elec. Loads (kWh/yr), FLOOR-Interior Lighting (kWh/yr), FLOOR-Exterior Lighting (kWh/yr), Garage Lighting (kWh/yr)"))
    
    # ------------------------------------------------------------------------------
    # -- Calculate the Non-Res Elec. Energy Consumption
    total_nonres_mel = 0
    total_nonres_int_lighting = 0
    if hb_nonres_rooms_:
        prog_collection = phius_mf.PhiusNonResProgramCollection()

        # -- Build a new Phius Non-Res-Space for each PH-Space found
        non_res_spaces = []
        for hb_room in hb_nonres_rooms_:
            for space in hb_room.properties.ph.spaces:                
                new_nonres_space = phius_mf.PhiusNonResRoom.from_ph_space(space)
                
                prog_collection.add_program(new_nonres_space.program_type)
                
                non_res_spaces.append(new_nonres_space)


        # -- Calc total MEL
        total_nonres_mel = sum( sp.total_mel_kWh for sp in non_res_spaces )
        
        # -- Calc total Lighting
        total_nonres_int_lighting = sum( sp.total_lighting_kWh for sp in non_res_spaces )
        
        # -- Collect the program data for preview / output
        non_res_program_data_ = prog_collection.to_phius_mf_workbook()
         
        non_res_room_data_ = [
            sp.to_phius_mf_workbook() for sp in 
            sorted(non_res_spaces, key=lambda x: x.name)
            ]
        non_res_totals_ = [
            sp.to_phius_mf_workbook_results() for sp in
            sorted(non_res_spaces, key=lambda x: x.name)
            ]
        non_res_totals_.insert(0, 
            str("Lighting Power Density (W/sf), Usage (days/year), Daily Usage (hrs/day), MELCOMM (kWh/yr.sf), LIGHTCOMM (kWh/yr), MELCOMM (kWh/yr)"))
        
    
    # ------------------------------------------------------------------------------
    # -- Calculate the Elec. Energy average per Honeybee-Room
    total_hb_rooms = len(hb_res_rooms_) + len(hb_nonres_rooms_)
    bldg_avg_mel = (total_res_mel + total_nonres_mel) / total_hb_rooms
    bldg_avg_lighting_int = (total_res_int_lighting + total_nonres_int_lighting) / total_hb_rooms
    bldg_avg_lighting_ext = total_res_ext_lighting / total_hb_rooms
    bldg_avg_lighting_garage = total_res_garage_lighting / total_hb_rooms


    # ------------------------------------------------------------------------------
    # -- Create the new Phius MF Elec Equip

    elec_equipment_ = []
    mel = ph_equipment.PhCustomAnnualMEL(_defaults=True)
    mel.energy_demand = bldg_avg_mel
    mel.comment = "MEL - Phius MF Calculator"
    elec_equipment_.append(mel)

    lighting_int = ph_equipment.PhCustomAnnualLighting(_defaults=True)
    lighting_int.energy_demand = bldg_avg_lighting_int
    lighting_int.comment = "Interior Lighting - Phius MF Calculator"
    elec_equipment_.append(lighting_int)

    lighting_ext = ph_equipment.PhCustomAnnualLighting(_defaults=True)
    lighting_ext.energy_demand = bldg_avg_lighting_ext
    lighting_ext.comment = "Exterior Lighting - Phius MF Calculator"
    elec_equipment_.append(lighting_ext)

    lighting_garage = ph_equipment.PhCustomAnnualLighting(_defaults=True)
    lighting_garage.energy_demand = bldg_avg_lighting_garage
    lighting_garage.comment = "Garage Lighting - Phius MF Calculator"
    lighting_garage.in_conditioned_space = False
    elec_equipment_.append(lighting_garage)  


    # ------------------------------------------------------------------------------
    # -- Previews
    #honeybee_ph_utils.preview.object_preview(mel)
    #honeybee_ph_utils.preview.object_preview(lighting_int)
    #honeybee_ph_utils.preview.object_preview(lighting_ext)
    #honeybee_ph_utils.preview.object_preview(lighting_garage)