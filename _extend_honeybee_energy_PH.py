# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-


# TODO: Extend the extension.... hmmm.....


# I think that it may be as simple as:
"""Like in HBE"""
# https://github.com/ladybug-tools/honeybee-energy/blob/31e88614b747458403bf6de85a8f016157125056/honeybee_energy/_extend_honeybee.py#L29
# set a hidden energy attribute on each core geometry Property class to None
# define methods to produce energy property instances on each Property instance

from honeybee_energy.properties.face import FaceEnergyProperties
from honeybee_energy.properties.aperture import ApertureProperties

from honeybee_energy_ph.construction import opaque, window

from honeybee_energy_ph.opaque import *
from honeybee_energy_ph.window import *

FaceProperties._energy._ph = None
ApertureProperties._energy._ph = None


def face_ph_properties(self):
    if self._energy._ph is None:
        self._energy._ph = OpaqueConstructionPHProperties()
    return FaceEnergyProperties._energy._ph


""" I'm not kneejerk seeing a reason why this shouldn't work? Am I missing something?
Not 100% sure how to test this correctly sans beating around an invisible bush for a 
secret hatch that may or may not exist?
"""
