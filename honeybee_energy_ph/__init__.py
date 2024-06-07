# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Package: Honeybee-PH-Energy

These classes are designed to be used within a Honeybee-editing environment, such as Rhino or 
Grasshopper. These classes will allow for the extension of the Honeybee-Energy objects in order
to add relevant Passive House fields and functions.
"""

# load all functions that extends honeybee core library
# Make sure the load `honeybee_energy` before anything else to avoid import errors.
import honeybee_energy._extend_honeybee

import honeybee_energy_ph._extend_honeybee_energy_ph
