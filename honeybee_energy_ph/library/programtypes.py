# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Find Phius program data and build HBE-Programs."""

try:
    from honeybee.typing import clean_ep_string
except ImportError as e:
    raise ImportError('\nFailed to import honeybee:\n\t{}'.format(e))

try:
    from honeybee_energy.load import lighting, people, equipment
    from honeybee_energy.schedule.ruleset import ScheduleRuleset
    from honeybee_energy.programtype import ProgramType
    from honeybee_energy.lib.scheduletypelimits import schedule_type_limit_by_identifier
    from honeybee_energy.lib.programtypes import program_type_by_identifier, \
        building_program_type_by_identifier
except ImportError as e:
    raise ImportError('\nFailed to import honeybee_energy:\n\t{}'.format(e))

from honeybee_ph_standards.programtypes import PHIUS_programs
from honeybee_energy_ph.properties import ruleset


class MissingBaseProgramError(Exception):
    def __init__(self, _data):
        self.msg = 'Error: The Phius data set for "{}" appears to missing '\
            'a Honeybee base-program?'.format(_data['name'])
        super(MissingBaseProgramError, self).__init__(self.msg)


def _clean_str(_str):
    # type: (str) -> str
    if not _str:
        return ''
    else:
        return str(_str).lstrip().rstrip().upper().replace(' ', '_').replace('-', '_')


def load_data_from_Phius_standards(_search_key, _search_field='name', _protocol=''):
    # type: (str, str, str) -> list[dict[str, dict]]
    """Returns a list of Phius program data as dicts.

    Arguments:
    ----------
        * _search_key (str): The key to search the Phius library for.
        * _search_field (str): default='name' | The dict field to search.
        * _protocol (str): Optional extra flag to filter by the specific 'protocol'

    Returns:
    --------
        * (list[dict]): A list of the Phius data found in the library.
    """
    if not _search_key:
        return []

    prog_data = []
    _search_key = _clean_str(_search_key)
    _protocol = _clean_str(_protocol)
    for data in PHIUS_programs.PHIUS_library.values():
        if _search_key not in _clean_str(data[_search_field]):
            continue
        if not _protocol:
            prog_data.append(data)
        else:
            if _protocol in _clean_str(data['protocol']):
                prog_data.append(data)

    return prog_data


def build_hb_people_from_Phius_data(_data):
    # type: (dict) -> people.People
    """Returns a new HBE-People Object with attributes based on the input data dict

    Arguments:
    ----------
        * _data (dict): The "people" element from a full Phius data dict.

    Returns:
    --------
        * (people.People): A new HB-People object.
    """
    # -------------------------------------------------------------------------
    # -- Build the People Schedule and set attributes
    ph_sched_ph_prop = ruleset.ScheduleRulesetPhProperties.from_days_per_year(
        _data['schedule']['annual_utilization_days'],
        _host=None
    )
    ph_sched_ph_prop.daily_operating_periods.add_period_to_collection(
        ruleset.DailyOperationPeriod.from_start_end_hours(
            _data['schedule']['start_hour'],
            _data['schedule']['end_hour'],
            _data['schedule']['relative_utilization_factor'],
            'operating'
        )
    )
    ppl_sched = ScheduleRuleset.from_constant_value(
        _data['schedule']['name'],
        ph_sched_ph_prop.annual_average_operating_fraction,
        schedule_type_limit_by_identifier('Fractional')
    )
    ph_sched_ph_prop._host = ppl_sched._properties
    ppl_sched._properties._ph = ph_sched_ph_prop

    # -------------------------------------------------------------------------
    # -- Build the HBE-People and set attributes
    hb_people = people.People(
        _data['loads']['identifier'],
        _data['loads']['people_per_area'],
        ppl_sched
    )

    return hb_people


def build_hb_lighting_from_Phius_data(_data):
    # type: (dict) -> lighting.Lighting
    """Returns a new HBE-Lighting Object with attributes based on the input data dict

    Arguments:
    ----------
        * _data (dict): The "lighting" element from a full Phius data dict.

    Returns:
    --------
        * (lighting.Lighting): A new HB-Lighting object.
    """
    # -------------------------------------------------------------------------
    # -- Build the Lighting Schedule and set attributes
    ph_sched_ph_prop = ruleset.ScheduleRulesetPhProperties.from_days_per_year(
        _data['schedule']['annual_utilization_days'],
        _host=None
    )
    ph_sched_ph_prop.daily_operating_periods.add_period_to_collection(
        ruleset.DailyOperationPeriod.from_operating_hours(
            _data['schedule']['daily_operating_hours'],
            _data['schedule']['relative_utilization_factor'],
            'operating'
        )
    )
    lighting_sched = ScheduleRuleset.from_constant_value(
        _data['schedule']['name'],
        ph_sched_ph_prop.annual_average_operating_fraction,
        schedule_type_limit_by_identifier('Fractional')
    )
    ph_sched_ph_prop._host = lighting_sched._properties
    lighting_sched._properties._ph = ph_sched_ph_prop

    # -------------------------------------------------------------------------
    # -- Build the HBE-Lighting and set attributes
    # -- Phius standard datasets are all in IP units (W/ft2)
    # -- if any data is found with W/ft2 inputs, convert them
    try:
        # Convert W/ft2 to W/M2
        w_m2 = _data['loads']['watts_per_ft2'] * 0.092903
    except KeyError:
        w_m2 = _data['loads']['watts_per_m2']
    
    hb_lighting = lighting.Lighting(
        _data['loads']['name'],
        w_m2,
        lighting_sched,
        0.0,
        0.32,
        0.25
    )

    # -- Set LightingPhProperties attributes
    hb_lighting.properties.ph.target_lux = _data['loads']['target_lux']
    hb_lighting.properties.ph.target_lux_height = _data['loads']['target_lux_height']

    return hb_lighting


def build_hb_elec_equip_from_Phius_data(_data):
    # type: (dict) -> equipment.ElectricEquipment
    """Returns a new HBE-Equipment Object with attributes based on the input data dict

    Arguments:
    ----------
        * _data (dict): The "elec_equipment" element from a full Phius data dict.

    Returns:
    --------
        * (people.People): A new HB-People object.
    """
    # -------------------------------------------------------------------------
    # -- Build the Equipment Schedule and set attributes
    ph_sched_ph_prop = ruleset.ScheduleRulesetPhProperties(_host=None)
    ph_sched_ph_prop.daily_operating_periods.add_period_to_collection(
        ruleset.DailyOperationPeriod.from_annual_utilization_factor(
            _data['schedule']['annual_utilization_factor'],
            'operating'
        )
    )
    equip_sched = ScheduleRuleset.from_constant_value(
        _data['schedule']['name'],
        ph_sched_ph_prop.annual_average_operating_fraction,
        schedule_type_limit_by_identifier('Fractional')
    )
    ph_sched_ph_prop._host = equip_sched._properties
    equip_sched._properties._ph = ph_sched_ph_prop

    # -------------------------------------------------------------------------
    # -- Build the HBE-Equipment and set attributes

    # -- Phius standard datasets are all in IP units (W/ft2)
    # -- if any data is found with W/ft2 inputs, convert them
    try:
        # Convert W/ft2 to W/M2
        w_m2 = _data['loads']['watts_per_ft2'] * 0.092903
    except KeyError:
        w_m2 = _data['loads']['watts_per_m2']

    hb_elec_equip = equipment.ElectricEquipment(
        _data['loads']['identifier'],
        w_m2,
        equip_sched
    )

    return hb_elec_equip


def build_hb_program_from_Phius_data(_data):
    # type: (dict) -> ProgramType
    """Return a new HB-Program with attributes based on an input Phius dataset

    Arguments:
    ---------
        * _data (dict): The full Phius datadict

    Returns:
    --------
        * (ProgramType): The new Honeybee-Energy ProgramType.
    """

    # -- Sort out the base-program
    base_program = _data['hb_base_program']

    if not base_program:
        raise MissingBaseProgramError(_data)
    try:
        base_program_ = building_program_type_by_identifier(base_program)
    except ValueError:
        base_program_ = program_type_by_identifier(base_program)

    program = base_program_.duplicate()
    program.identifier = clean_ep_string(
        "Phius_{}".format(_data['name'].replace(' ', '_')))
    program.display_name = "{}::{}".format(_data['protocol'], _data['name'])

    # -- Build and assign the sub-programs
    program.people = build_hb_people_from_Phius_data(_data['people'])
    program.lighting = build_hb_lighting_from_Phius_data(_data['lighting'])
    program.electric_equipment = build_hb_elec_equip_from_Phius_data(
        _data['elec_equipment'])

    # -- Inherit the rest from the base-program
    # program.gas_equipment = _gas_equip_
    # program.service_hot_water = _hot_water_
    # program.infiltration = _infiltration_
    # program.ventilation = _ventilation_
    # program.setpoint = _setpoint_

    return program
