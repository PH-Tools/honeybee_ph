# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""This is called during __init__ and extends the base honeybee class Properties with a new ._ph slot"""

# -- honeybee_energy properties objects
from honeybee_energy.schedule.ruleset import ScheduleRulesetProperties
from honeybee_ph.properties.space import SpaceProperties
from honeybee_energy.properties.extension import OpaqueConstructionProperties, WindowConstructionProperties

# -- hjoneynee_energy_ph properties objects
from honeybee_energy_ph.properties.ruleset import ScheduleRulesetPhProperties
from honeybee_energy_ph.properties.space import SpaceEnergyProperties
from honeybee_energy_ph.properties.construction.opaque import OpaqueConstructionPhProperties
from honeybee_energy_ph.properties.construction.window import WindowConstructionPhProperties

# Step 1)
# set a private ._ph attribute on each relevant HB-Energy Property class to None
setattr(SpaceProperties, '_energy', None)
setattr(ScheduleRulesetProperties, '_ph', None)
setattr(OpaqueConstructionProperties, '_ph', None)
setattr(WindowConstructionProperties, '_ph', None)

# Step 2)
# create methods to define the public .property.<extension> @property instances on each obj.properties container


def space_energy_properties(self):
    if self._energy is None:
        self._energy = SpaceEnergyProperties(self.host)
    return self._energy


def schedule_ruleset_ph_properties(self):
    if self._ph is None:
        self._ph = ScheduleRulesetPhProperties(self.host)
    return self._ph


def opaque_construction_ph_properties(self):
    if self._ph is None:
        self._ph = OpaqueConstructionPhProperties()
    return self._ph


def window_construction_ph_properties(self):
    if self._ph is None:
        self._ph = WindowConstructionPhProperties()
    return self._ph


# Step 3)
# add public .energy or .ph @property methods to the appropriate Properties classes
setattr(SpaceProperties, 'energy', property(space_energy_properties))
setattr(ScheduleRulesetProperties, 'ph', property(schedule_ruleset_ph_properties))
setattr(OpaqueConstructionProperties, 'ph', property(opaque_construction_ph_properties))
setattr(WindowConstructionProperties, 'ph', property(window_construction_ph_properties))
