# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HBPH-Cooling System GH-Component inputs node configuration."""

from copy import copy
# Note: Use copy so that specific equipments can overwrite base with their own hints

from GhPython import Component
from Grasshopper.Kernel.Parameters import Hints

from honeybee_ph_rhino.gh_io import input_to_int, ComponentInput


class InputTypeNotFoundError(Exception):
    def __init__(self, _in):
        self.msg = 'Error: cooling type ID: "{}" is not a valid equip type.'.format(_in)
        super(InputTypeNotFoundError, self).__init__(self.msg)


# -----------------------------------------------------------------------------
# Setup the component input node groups
inputs_base = {
    1: ComponentInput(_name='display_name',
                      _description='(str) Optional display name for the cooling system.',
                      _type_hint=Component.NewStrHint()),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) default=1.0 The fraction of total cooling supplied by this system (0-1)',
                      _type_hint=Component.NewFloatHint()),
}

inputs_ventilation = copy(inputs_base)
inputs_ventilation.update({
    3: ComponentInput(_name='annual_COP',
                      _description='(float) The Annual COP (W/W) of the equipment.',
                      _type_hint=Component.NewFloatHint()),
    4: ComponentInput(_name='single_speed',
                      _description='(bool) Cyclical operation works through an on/off regulation of the compressor. If this is set to False, then the assumption is that the unit has a VRF (variant refrigerant flow), which  works by modulating the efficiency of the compressor.',
                      _type_hint=Hints.GH_BooleanHint_CS()),
    5: ComponentInput(_name='min_coil_temp',
                      _description='(float) Deg. C',
                      _type_hint=Component.NewFloatHint()),
    6: ComponentInput(_name='capacity',
                      _description='(float) Maximum kW output.',
                      _type_hint=Component.NewFloatHint()),
})


inputs_recirculation = copy(inputs_base)
inputs_recirculation.update({
    3: ComponentInput(_name='annual_COP',
                      _description='(float) The Annual COP (W/W) of the equipment.',
                      _type_hint=Component.NewFloatHint()),
    4: ComponentInput(_name='single_speed',
                      _description='(bool) Cyclical operation works through an on/off regulation of the compressor. If this is set to False, then the assumption is that the unit has a VRF (variant refrigerant flow), which  works by modulating the efficiency of the compressor.',
                      _type_hint=Hints.GH_BooleanHint_CS()),
    5: ComponentInput(_name='min_coil_temp',
                      _description='(float) Deg. C',
                      _type_hint=Component.NewFloatHint()),
    6: ComponentInput(_name='capacity',
                      _description='(float) Maximum kW output.',
                      _type_hint=Component.NewFloatHint()),
    7: ComponentInput(_name='flow_rate_m3_hr',
                      _description='(float) The maximum airflow rate in m3/hr',
                      _type_hint=Component.NewFloatHint()),
    8: ComponentInput(_name='flow_rate_variable',
                      _description='(bool) VAV system: The volume flow changes proportionally  to the cooling capacity, thereby reducing the  temperature remains constant (usually better dehumidification)',
                      _type_hint=Hints.GH_BooleanHint_CS()),
})

inputs_dehumidification = copy(inputs_base)
inputs_dehumidification.update({
    3: ComponentInput(_name='annual_COP',
                      _description='(float) The Annual COP (W/W) of the equipment.',
                      _type_hint=Component.NewFloatHint()),
    4: ComponentInput(_name='useful_heat_loss',
                      _description='If this is set to True, then the waste heat from the dehumidification unit will be considered as an internal heat gain. On the contrary, dehumidification has no influence on the thermal balance.',
                      _type_hint=Component.NewFloatHint()),
})

inputs_panel = copy(inputs_base)
inputs_panel.update({
    3: ComponentInput(_name='annual_COP',
                      _description='(float) The Annual COP (W/W) of the equipment.',
                      _type_hint=Component.NewFloatHint()),
})


# -----------------------------------------------------------------------------

input_groups = {
    1: inputs_ventilation,
    2: inputs_recirculation,
    3: inputs_dehumidification,
    4: inputs_panel,
}

valid_cooling_types = [
    "1-ventilation",
    "2-recirculation",
    "3-dehumidification",
    "4-panel",
]

# -----------------------------------------------------------------------------


def get_component_inputs(_cooling_type):
    # type: (str) -> dict
    """Select the component input-node group based on the 'cooling_type' specified"""

    if not _cooling_type:
        return {}

    input_type_id = input_to_int(_cooling_type)
    if not input_type_id:
        raise InputTypeNotFoundError(input_type_id)

    try:
        return input_groups[input_type_id]
    except KeyError:
        raise InputTypeNotFoundError(input_type_id)
