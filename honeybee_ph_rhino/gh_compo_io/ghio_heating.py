# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""PH-Heating System GH-Component inputs node configuration."""

from copy import copy
# Note: Use copy so that specific equipments can overwrite base with their own hints

from honeybee_ph_rhino.gh_io import input_to_int, ComponentInput


class InputTypeNotFoundError(Exception):
    def __init__(self, _in):
        self.msg = 'Error: Heating type ID: "{}" is not a valid equip type.'.format(_in)
        super(InputTypeNotFoundError, self).__init__(self.msg)


# -----------------------------------------------------------------------------
# Setup the component input node groups
inputs_base = {
    1: ComponentInput(_name='display_name', _description='(str) Optional display name for the heating system.'),
    2: ComponentInput(_name='percent_coverage', _description='(float) default=1.0 The fraction of total heating supplied by this system (0-1)'),
}

inputs_direct_electric = copy(inputs_base)
inputs_direct_electric.update({})

inputs_fossil_boiler = copy(inputs_base)
inputs_fossil_boiler.update({
    3: ComponentInput(_name='fuel', _description='Select Fuel type: "1-Natural-Gas" or "2-Oil"'),
})

inputs_wood_boiler = copy(inputs_base)
inputs_wood_boiler.update({
    3: ComponentInput(_name='fuel', _description='Select Fuel type: "3-Logs" or "4-Pellets"'),
})

inputs_district_heat = copy(inputs_base)
inputs_district_heat.update({
    3: ComponentInput(_name='energy_carrier', _description='Select Energy Carrier.'),
})

inputs_heat_pump_annual = copy(inputs_base)
inputs_heat_pump_annual.update({
    3: ComponentInput(_name='annual_COP', _description='COP: watts-out/watts-in'),
})

inputs_heat_pump_monthly = copy(inputs_base)
inputs_heat_pump_monthly.update({
    3: ComponentInput(_name='monthly_COPS', _description='(list[float]): A List of COP values.'),
    4: ComponentInput(_name='monthly_temps', _description='(list[float]): A List of temp [deg C] values.'),
})

# -----------------------------------------------------------------------------

input_groups = {
    1: inputs_direct_electric,
    2: inputs_fossil_boiler,
    3: inputs_wood_boiler,
    4: inputs_district_heat,
    5: inputs_heat_pump_annual,
    6: inputs_heat_pump_monthly,
}

valid_heating_types = [
    "1-direct_electric",
    "2-fossil_boiler",
    "3-wood_boiler",
    "4-district_heat",
    "5-heat_pump_annual",
    "6-heat_pump_monthly", ]

# -----------------------------------------------------------------------------


def get_component_inputs(_heating_type):
    # type: (str) -> dict
    """Select the component input-node group based on the 'heating_type' specified"""

    if not _heating_type:
        return {}

    input_type_id = input_to_int(_heating_type)
    if not input_type_id:
        raise InputTypeNotFoundError(input_type_id)

    try:
        return input_groups[input_type_id]
    except KeyError:
        raise InputTypeNotFoundError(input_type_id)
