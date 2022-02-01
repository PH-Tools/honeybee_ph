# -*- coding: utf-8 -*-
# -*- Python Version: 3.10 -*-

"""Functions to create PhX-HVAC objects from Honeybee-Energy HVAC"""

from PHX import mech_equip
from honeybee_ph import space


def build_phx_ventilator(_space: space.Space) -> mech_equip.Ventilator:
    """Returns a new Fresh-Air Ventilator built from the hb-energy hvac paramaters.

    This will look at the Space's Host-Room .properties.energy.hvac for data.

    Arguments:
    ----------
        *_space (space.Space): The Passive House Space to use as the source.

    Returns:
    --------
        * mech_equip.Ventilator: The new Passive House Ventilator created.
    """

    space_ventilator = mech_equip.Ventilator()

    hb_hvac = _space.host.properties.energy.hvac
    space_ventilator.name = f'Ventilator: {hb_hvac.sensible_heat_recovery*100 :0.0f}%-HR,'\
        f' {hb_hvac.latent_heat_recovery*100 :0.0f}%-MR'
    space_ventilator.heat_recovery_efficiency = hb_hvac.sensible_heat_recovery
    space_ventilator.moisture_recovery_efficiency = hb_hvac.latent_heat_recovery

    return space_ventilator
