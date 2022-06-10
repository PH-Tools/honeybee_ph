# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""This is called during __init__ and extends the base honeybee class Properties with a new ._ph slot"""

from honeybee.properties import (
    ModelProperties,
    RoomProperties,
    FaceProperties,
    ApertureProperties,
    ShadeProperties
)

from .properties.space import SpaceProperties, SpacePhProperties
from .properties.model import ModelPhProperties
from .properties.room import RoomPhProperties
from .properties.face import FacePhProperties
from .properties.aperture import AperturePhProperties
from .properties.shade import ShadePhProperties

# Step 1)
# set a private ._ph attribute on each relevant HB-Core Property class to None

setattr(ModelProperties, '_ph', None)
setattr(RoomProperties, '_ph', None)
setattr(FaceProperties, '_ph', None)
setattr(ApertureProperties, '_ph', None)
setattr(SpaceProperties, '_ph', None)
setattr(ShadeProperties, '_ph', None)

# Step 2)
# create methods to define the public .ph property instances on each obj.properties container


def model_ph_properties(self):
    if self._ph is None:
        self._ph = ModelPhProperties(self.host)
    return self._ph


def room_ph_properties(self):
    if self._ph is None:
        self._ph = RoomPhProperties(self.host)
    return self._ph


def face_ph_properties(self):
    if self._ph is None:
        self._ph = FacePhProperties(self.host)
    return self._ph


def aperture_ph_properties(self):
    if self._ph is None:
        self._ph = AperturePhProperties(self.host)
    return self._ph


def space_ph_properties(self):
    if self._ph is None:
        self._ph = SpacePhProperties(self.host)
    return self._ph


def shade_ph_properties(self):
    if self._ph is None:
        self._ph = ShadePhProperties(self.host)
    return self._ph


# Step 3)
# add public .ph property methods to the Properties classes
setattr(ModelProperties, 'ph', property(model_ph_properties))
setattr(RoomProperties, 'ph', property(room_ph_properties))
setattr(FaceProperties, 'ph', property(face_ph_properties))
setattr(ApertureProperties, 'ph', property(aperture_ph_properties))
setattr(SpaceProperties, 'ph', property(space_ph_properties))
setattr(ShadeProperties, 'ph', property(shade_ph_properties))
