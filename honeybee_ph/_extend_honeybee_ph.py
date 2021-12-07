# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""""""

from honeybee.properties import (
    ModelProperties,
    RoomProperties,
    FaceProperties,
    ApertureProperties,
)
from .model import ModelPhProperties
from .room import RoomPhProperties
from .face import FacePhProperties
from .aperture import AperturePhProperties


# Step 1)
# set a private ._ph attribute on each relevant HB-Core Property class to None

ModelProperties._ph = None
RoomProperties._ph = None
FaceProperties._ph = None
ApertureProperties._ph = None

# Step 2)
# create methods to define the ._PH property instances on each obj.properties container


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


# Step 3)
# add public .PH property methods to the Properties classes

ModelProperties.ph = property(model_ph_properties)
RoomProperties.ph = property(room_ph_properties)
FaceProperties.ph = property(face_ph_properties)
ApertureProperties.ph = property(aperture_ph_properties)
