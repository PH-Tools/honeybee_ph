# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Equipment GH-Component inputs node configuration."""
from copy import copy
# Use copy so that specific equipments can overwrite base with their own hints

from honeybee_ph_rhino.gh_io import ComponentInput

inputs_base = {
    1: ComponentInput(_name='display_name', _description='(str)'),
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

input_groups = {
    1: inputs_dishwasher,
}

valid_equipment_types = ["1-dishwasher", ]


def get_component_inputs(_equipment_type):
    # type: (str) -> dict
    """Select the component input-node group based on the 'type' specified"""

    if '1' in str(_equipment_type):
        return input_groups[1]
    else:
        return input_groups[1]
