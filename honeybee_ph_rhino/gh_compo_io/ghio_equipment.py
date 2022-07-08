# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Equipment GH-Component inputs node configuration."""

from copy import copy
# Note: Use copy so that specific equipments can overwrite base with their own hints

from GhPython import Component
from Grasshopper.Kernel.Parameters import Hints

from honeybee_ph_rhino.gh_io import ComponentInput
from honeybee_ph_utils.input_tools import input_to_int


class InputTypeNotFoundError(Exception):
    def __init__(self, _in):
        self.msg = 'Error: Equip. type ID: "{}" is not a valid equip type.'.format(_in)
        super(InputTypeNotFoundError, self).__init__(self.msg)


# -----------------------------------------------------------------------------
# Setup the component input node groups
inputs_base = {
    2: ComponentInput(_name='comment',
                      _description='(str) User defined comment / note.',
                      _type_hint=Component.NewStrHint()),
    3: ComponentInput(_name='reference_quantity',
                      _description='() some WUFI stuff.'),
    4: ComponentInput(_name='quantity',
                      _description='(int) The total number of appliances / pieces of equipment included.',
                      _type_hint=Hints.GH_IntegerHint_CS()),
    5: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) default=True, Set False if the appliance is outside and the waste heat from the appliance does not count towards internal-gains in the space.',
                      _type_hint=Hints.GH_BooleanHint_CS()),
    6: ComponentInput(_name='reference_energy_norm',
                      _description='() some other WUFI stuff.',
                      _type_hint=Component.NewStrHint()),
    7: ComponentInput(_name='energy_demand',
                      _description='(float) usually kWh/yr',
                      _type_hint=Component.NewFloatHint()),
    8: ComponentInput(_name='energy_demand_per_use',
                      _description='(float) usually kWh/use',
                      _type_hint=Component.NewFloatHint()),
    9: ComponentInput(_name='combined_energy_factor',
                      _description='(float)',
                      _type_hint=Component.NewFloatHint()),
}

inputs_dishwasher = copy(inputs_base)
inputs_dishwasher.update({
    10: ComponentInput(_name='capacity_type',
                       _description='Input "1-Standard" or ',
                       _type_hint=Component.NewStrHint()),
    11: ComponentInput(_name='capacity',
                       _description='(float)',
                       _type_hint=Component.NewFloatHint()),
    12: ComponentInput(_name='water_connection',
                       _description='Input either -\n "1-DHW Connection"\n "2-Cold Water Connection"',
                       _type_hint=Component.NewStrHint()),
})

inputs_clothes_washer = copy(inputs_base)
inputs_clothes_washer.update({
    10: ComponentInput(_name='capacity',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
    11: ComponentInput(_name='modified_energy_factor',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
    12: ComponentInput(_name='water_connection',
                       _description='Input either -\n "1-DHW Connection"\n "2-Cold Water Connection"',
                       _type_hint=Component.NewStrHint()),
    13: ComponentInput(_name='utilization_factor',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
})

inputs_clothes_dryer = copy(inputs_base)
inputs_clothes_dryer.update({
    10: ComponentInput(_name='dryer_type',
                       _description='Input either -\n "1-CLOTHES LINE"\n "2-DRYING CLOSET (COLD!)"\n "3-DRYING CLOSET (COLD!) IN EXTRACT AIR"\n "4-CONDENSATION DRYER"\n "5-ELECTRIC EXHAUST AIR DRYER"\n "6-GAS EXHAUST AIR DRYER"\n ',
                       _type_hint=Component.NewStrHint()),
    11: ComponentInput(_name='gas_consumption',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
    12: ComponentInput(_name='gas_efficiency_factor',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
    13: ComponentInput(_name='field_utilization_factor_type',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
    14: ComponentInput(_name='field_utilization_factor',
                       _description='',
                       _type_hint=Component.NewFloatHint()),
})

inputs_refrigerator = copy(inputs_base)
inputs_refrigerator.update({})

inputs_freezer = copy(inputs_base)
inputs_freezer.update({})

inputs_fridge_freezer = copy(inputs_base)
inputs_fridge_freezer.update({})

inputs_cooktop = copy(inputs_base)
inputs_cooktop.update({
    10: ComponentInput(_name='cooktop_type',
                       _description='Input either -\n "1-ELECTRICITY"\n "2-NATURAL GAS"\n "3-LPG",',
                      _type_hint=Component.NewStrHint()),
})

input_Phius_MEL = copy(inputs_base)
input_Phius_MEL.update({})

inputs_Phius_Lighting_Int = copy(inputs_base)
inputs_Phius_Lighting_Int.update({
    10: ComponentInput(_name='frac_high_efficiency',
                       _description='The percentage of lighting which is "high efficiency."',
                       _type_hint=Component.NewFloatHint()),
})


inputs_Phius_Lighting_Ext = copy(inputs_base)
inputs_Phius_Lighting_Ext.update({
    10: ComponentInput(_name='frac_high_efficiency',
                       _description='The percentage of lighting which is "high efficiency."',
                       _type_hint=Component.NewFloatHint()),
})


inputs_Phius_Lighting_Garage = copy(inputs_base)
inputs_Phius_Lighting_Garage.update({
    10: ComponentInput(_name='frac_high_efficiency',
                       _description='The percentage of lighting which is "high efficiency."',
                       _type_hint=Component.NewFloatHint()),
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
