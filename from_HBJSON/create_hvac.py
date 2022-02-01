# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions to create PHX-HVAC objects from Honeybee-Energy HVAC"""

from PHX import mech_equip
from honeybee_ph import space


def build_phx_ventilator(_space: space.Space) -> mech_equip.PhxVentilator:
    """Returns a new Fresh-Air Ventilator built from the hb-energy hvac paramaters.

    This will look at the Space's Host-Room .properties.energy.hvac for data.

    Arguments:
    ----------
        *_space (space.Space): The Passive House Space to use as the source.

    Returns:
    --------
        * mech_equip.Ventilator: The new Passive House Ventilator created.
    """

    space_ventilator = mech_equip.PhxVentilator()

    # -- Setup the basic system and unit params based on the Honeybee-Energy IdeaAirSystem
    hb_hvac = _space.host.properties.energy.hvac
    space_ventilator.name = f'Ventilator: {hb_hvac.sensible_heat_recovery*100 :0.0f}%-HR,'\
        f' {hb_hvac.latent_heat_recovery*100 :0.0f}%-MR'
    space_ventilator.heat_recovery_efficiency = hb_hvac.sensible_heat_recovery
    space_ventilator.moisture_recovery_efficiency = hb_hvac.latent_heat_recovery

    # -- The, try and pull out any PH-Specific System params (if any) and set those
    ph_vent_system = _space.host.properties.energy.hvac.properties.ph.ventilation_system
    if ph_vent_system is not None:
        space_ventilator.name = ph_vent_system.ventilation_unit.name
        space_ventilator.fan_power = ph_vent_system.ventilation_unit.electric_efficiency
        space_ventilator.frost_protection_reqd = ph_vent_system.ventilation_unit.frost_protection_reqd
        space_ventilator.frost_temp = ph_vent_system.ventilation_unit.temperature_below_defrost_used
        space_ventilator.in_conditioned_space = ph_vent_system.ventilation_unit.in_conditioned_space

    return space_ventilator
