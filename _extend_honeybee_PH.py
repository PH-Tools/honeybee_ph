# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""""""

from honeybee.properties import ModelProperties, RoomProperties, \
    FaceProperties, ApertureProperties
from honeybee_PH.model import ModelPHProperties
from honeybee_PH.room import RoomPHProperties
from honeybee_PH.face import FacePHProperties
from honeybee_PH.aperture import AperturePHProperties

# Step 1)
# set a private ._PH attribute on each relevant HB-Core Property class to None

ModelProperties._PH = None
RoomProperties._PH = None
FaceProperties._PH = None
ApertureProperties._PH = None

# Step 2)
# create methods to define the ._PH property instances on each obj.properties container


def model_PH_properties(self):
    if self._PH is None:
        self._PH = ModelPHProperties(self.host)
    return self._PH


def room_PH_properties(self):
    if self._PH is None:
        self._PH = RoomPHProperties(self.host)
    return self._PH


def face_PH_properties(self):
    if self._PH is None:
        self._PH = FacePHProperties(self.host)
    return self._PH


def aperture_PH_properties(self):
    if self._PH is None:
        self._PH = AperturePHProperties(self.host)
    return self._PH


# Step 3)
# add public .PH property methods to the Properties classes

ModelProperties.PH = property(model_PH_properties)
RoomProperties.PH = property(room_PH_properties)
FaceProperties.PH = property(face_PH_properties)
ApertureProperties.PH = property(aperture_PH_properties)
