# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Hot-Water-Heater GH-Component inputs node configuration."""

from honeybee_ph_rhino.gh_io import ComponentInput

inputs_electric = {
    1: ComponentInput(_name='display_name',
                      _description='(str) An optional name for the HW-Heater.'),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) The % of total HW energy covered by this device.'),
    3: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) Is the boiler installed inside the conditioned space? default=True.'),
}

inputs_boiler_oil_gas = {
    1: ComponentInput(_name='display_name',
                      _description='(str) An optional name for the HW-Heater.'),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) The % of total HW energy covered by this device.'),
    3: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) Is the boiler installed inside the conditioned space? default=True.'),
    4: ComponentInput(_name='fuel',
                      _description='Input: "1-Gas" or "2-Oil"'),
    5: ComponentInput(_name='condensing',
                      _description='(bool) Is the boiler a more-efficient "condensing" boiler? default=True.'),
    6: ComponentInput(_name='effic_at_30_perc_load',
                      _description='(float) Boiler efficiency (%) at 30% of peak-load.'),
    7: ComponentInput(_name='effic_at_nominal_load',
                      _description='(float) Boiler efficiency (%) at nominal output.'),
    8: ComponentInput(_name='avg_return_temp_at_30_perc_load',
                      _description='(float) Boiler efficiency (%) at nominal output.'),
    9: ComponentInput(_name='avg_boiler_temp_at_70_55',
                      _description='(float) Average boiler temp. at 77C / 55C.'),
    10: ComponentInput(_name='avg_boiler_temp_at_55_45',
                       _description='(float) Average boiler temp. at 55C / 45C.'),
    11: ComponentInput(_name='avg_boiler_temp_at_35_28',
                       _description='(float) Average boiler temp. at 35C / 28C.'),
}

inputs_boiler_wood = {
    1: ComponentInput(_name='display_name',
                      _description='(str) An optional name for the HW-Heater.'),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) The % of total HW energy covered by this device.'),
    3: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) Is the boiler installed inside the conditioned space? default=True.'),
    4: ComponentInput(_name='fuel',
                      _description='Input: "1-Pellets" or "2-Logs"'),
    5: ComponentInput(_name='effic_in_basic_cycle',
                      _description='(float) The efficiency of the heat generator in basic cycle. Standard Pellet=0.72, Standard Log=0.60'),
    6: ComponentInput(_name='effic_in_const_operation',
                      _description='(float) The efficiency of the heat generator in constant operation. Standard Pellet=0.80, Standard Log=0.70'),
    7: ComponentInput(_name='avg_frac_heat_released',
                      _description='(float) The average fraction of heat output released to heating circuit. Standard Pellet=0.50, Standard Log=0.40'),
    8: ComponentInput(_name='on_off_temp_diff',
                      _description='(float) The temperature difference (deg K) between power-on and power-off. Standard Pellet=10K, Standard Log=30K'),
}

inputs_district = {
    1: ComponentInput(_name='display_name',
                      _description='(str) An optional name for the HW-Heater.'),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) The % of total HW energy covered by this device.'),
    3: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) Is the boiler installed inside the conditioned space? default=True.'),
    4: ComponentInput(_name='energy_carrier',
                      _description='Energy Carrier for the district heat.'),
    5: ComponentInput(_name='solar_fraction',
                      _description='(float) The solar fraction for the space heating.'),
    6: ComponentInput(_name='util_fact_heat_transfer',
                      _description='(float) Utilization Factor of heat-transfer station.'),
}

inputs_heat_pump_annual = {
    1: ComponentInput(_name='display_name',
                      _description='(str) An optional name for the HW-Heater.'),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) The % of total HW energy covered by this device.'),
    3: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) Is the boiler installed inside the conditioned space? default=True.'),
    4: ComponentInput(_name='annual_COP',
                      _description='(float) Annual Coefficient of Performance (COP).'),
    5: ComponentInput(_name='annual_system_perf_ratio',
                      _description='(float) Annual system performance ratio of heat generator.'),
    6: ComponentInput(_name='annual_energy_factor',
                      _description='(float) OPTIONAL - Annual energy-factor (EF) of the heat pump.'),
}

inputs_heat_pump_monthly = {
    1: ComponentInput(_name='display_name',
                      _description='(str) An optional name for the HW-Heater.'),
    2: ComponentInput(_name='percent_coverage',
                      _description='(float) The % of total HW energy covered by this device.'),
    3: ComponentInput(_name='in_conditioned_space',
                      _description='(bool) Is the boiler installed inside the conditioned space? default=True.'),
    4: ComponentInput(_name='rated_COP_at_T1',
                      _description='(float) The rated Coefficient of Performance (COP) at temperature T1'),
    5: ComponentInput(_name='rated_COP_at_T2',
                      _description='(float) The rated Coefficient of Performance (COP) at temperature T2'),
    6: ComponentInput(_name='temp_T1',
                      _description='(float) Temperature T1 (deg C)'),
    7: ComponentInput(_name='temp_T2',
                      _description='(float) Temperature T2 (deg C)'),
}


input_groups = {
    1: inputs_electric,
    2: inputs_boiler_oil_gas,
    3: inputs_boiler_wood,
    4: inputs_district,
    5: inputs_heat_pump_annual,
    6: inputs_heat_pump_monthly,
}

valid_heater_types = ["1-Electric", "2-Boiler (gas/oil)",
                      "3-Boiler (wood)", "4-District", "5-HeatPump", "6-HeatPump"]


def get_component_inputs(_heater_type):
    # type: (str) -> dict
    """Select the component input-node group based on the 'type' specified"""

    if '1' in str(_heater_type):
        return input_groups[1]
    elif '2' in str(_heater_type):
        return input_groups[2]
    elif '3' in str(_heater_type):
        return input_groups[3]
    elif '4' in str(_heater_type):
        return input_groups[4]
    elif '5' in str(_heater_type):
        return input_groups[5]
    elif '6' in str(_heater_type):
        return input_groups[6]
    else:
        return input_groups[1]
