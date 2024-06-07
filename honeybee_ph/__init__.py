# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Package: Honeybee-PH Classes and functions to allow for Passive-House data within Honeybee.

These classes are designed to be used within a Honeybee-editing environment, such as Rhino or 
Grasshopper. These classes will allow for Passive House specific data to be added to certain 
relevant Honeybee entities and logged for later use.
"""

# load all functions that extends honeybee core library
# Make sure the load `honeybee_energy` before anything else to avoid import errors.
import honeybee_energy._extend_honeybee

import honeybee_ph._extend_honeybee_ph
