# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Equipment GH-Component inputs node configuration."""
from copy import copy
# Note: Use copy so that specific equipments can overwrite base with their own hints

from honeybee_ph_rhino.gh_io import input_to_int, ComponentInput


class InputTypeNotFoundError(Exception):
    def __init__(self, _in):
        self.msg = 'Error: Equip. type ID: "{}" is not a valid equip type.'.format(_in)
        super(InputTypeNotFoundError, self).__init__(self.msg)


# -----------------------------------------------------------------------------
# Setup the component input node groups
inputs_base = {
    2: ComponentInput(_name='comment', _description='(str) User defined comment / note.'),
    3: ComponentInput(_name='reference_quantity', _description='()'),
    4: ComponentInput(_name='quantity', _description='(int) The total number of equipments used.'),
    5: ComponentInput(_name='in_conditioned_space', _description='(bool) default=True'),
    6: ComponentInput(_name='reference_energy_norm', _description='()'),
    7: ComponentInput(_name='energy_demand', _description='(float)'),
    8: ComponentInput(_name='energy_demand_per_use', _description='(float)'),
    9: ComponentInput(_name='combined_energy_factor', _description='(float)'),
}

inputs_dishwasher = copy(inputs_base)
inputs_dishwasher.update({
    10: ComponentInput(_name='capacity_type', _description='Input "1-Standard" or '),
    11: ComponentInput(_name='capacity', _description='(float)'),
    12: ComponentInput(_name='water_connection', _description='Input "1-DHW Connection" or "2-Cold Water Connection"'),
})

inputs_clothes_washer = copy(inputs_base)
inputs_clothes_washer.update({
    10: ComponentInput(_name='capacity', _description=''),
    11: ComponentInput(_name='modified_energy_factor', _description=''),
    12: ComponentInput(_name='connection', _description=''),
    13: ComponentInput(_name='utilization_factor', _description=''),
})

inputs_clothes_dryer = copy(inputs_base)
inputs_clothes_dryer.update({
    10: ComponentInput(_name='dryer_type', _description=''),
    11: ComponentInput(_name='gas_consumption', _description=''),
    12: ComponentInput(_name='gas_efficiency_factor', _description=''),
    13: ComponentInput(_name='field_utilization_factor_type', _description=''),
    14: ComponentInput(_name='field_utilization_factor', _description=''),
})

inputs_refrigerator = copy(inputs_base)
inputs_refrigerator.update({})

inputs_freezer = copy(inputs_base)
inputs_freezer.update({})

inputs_fridge_freezer = copy(inputs_base)
inputs_fridge_freezer.update({})

inputs_cooktop = copy(inputs_base)
inputs_cooktop.update({
    10: ComponentInput(_name='cooktop_type', _description=''),
})

input_Phius_MEL = copy(inputs_base)
input_Phius_MEL.update({})

inputs_Phius_Lighting_Int = copy(inputs_base)
inputs_Phius_Lighting_Int.update({
    10: ComponentInput(_name='frac_high_efficiency', _description=''),
})


inputs_Phius_Lighting_Ext = copy(inputs_base)
inputs_Phius_Lighting_Ext.update({
    10: ComponentInput(_name='frac_high_efficiency', _description=''),
})


inputs_Phius_Lighting_Garage = copy(inputs_base)
inputs_Phius_Lighting_Garage.update({
    10: ComponentInput(_name='frac_high_efficiency', _description=''),
})

inputs_Custom_Elec = copy(inputs_base)
inputs_Custom_Lighting = copy(inputs_base)
inputs_Custom_MEL = copy(inputs_base)

# -----------------------------------------------------------------------------

input_groups = {
    1: inputs_dishwasher,
    2: inputs_clothes_washer,
    3: inputs_clothes_dryer,
    4: inputs_refrigerator,
    5: inputs_freezer,
    6: inputs_fridge_freezer,
    7: inputs_cooktop,
    13: input_Phius_MEL,
    14: inputs_Phius_Lighting_Int,
    15: inputs_Phius_Lighting_Ext,
    16: inputs_Phius_Lighting_Garage,
    11: inputs_Custom_Elec,
    17: inputs_Custom_Lighting,
    18: inputs_Custom_MEL,
}

valid_equipment_types = ["1-dishwasher", "2-clothes_washer", "3-clothes_dryer",
                         "4-fridge", "5-freezer", "6-fridge_freezer", "7-cooking", "13-PHIUS_MEL",
                         "14-PHIUS_Lighting_Int", "15-PHIUS_Lighting_Ext", "16-PHIUS_Lighting_Garage",
                         "11-Custom_Electric_per_Year", "17-Custom_Electric_Lighting_per_Year",
                         "18-Custom_Electric_MEL_per_Use", ]
# "21-Commercial_Dishwasher", "22-Commercial_Refrigerator", "23-Commercial_Cooking", "24-Commercial_Custom"]


# -----------------------------------------------------------------------------

def get_component_inputs(_equipment_type):
    # type: (str) -> dict
    """Select the component input-node group based on the 'type' specified"""

    if not _equipment_type:
        return {}

    input_type_id = input_to_int(_equipment_type)
    if not input_type_id:
        raise InputTypeNotFoundError(input_type_id)

    try:
        return input_groups[input_type_id]
    except KeyError:
        raise InputTypeNotFoundError(input_type_id)
