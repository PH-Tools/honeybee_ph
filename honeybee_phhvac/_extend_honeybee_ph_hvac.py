# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Called during __init__ to extend the HB-base class 'properties' with a new '_ph_hvac' attribute."""

from honeybee.properties import (
    ModelProperties,
    RoomProperties,
    FaceProperties,
    ShadeProperties,
    ApertureProperties,
    DoorProperties,
)

from .properties.model import ModelPhHvacProperties
from .properties.room import RoomPhHvacProperties
from .properties.face import FacePhHvacProperties
from .properties.shade import ShadePhHvacProperties
from .properties.aperture import AperturePhHvacProperties
from .properties.door import DoorPhHvacProperties


# -----------------------------------------------------------------------------
# Step 1)
# set a private 'ph_hvac' attribute on each relevant HB-Core Property class to None


setattr(ModelProperties, "_ph_hvac", None)
setattr(RoomProperties, "_ph_hvac", None)
setattr(FaceProperties, "_ph_hvac", None)
setattr(ShadeProperties, "_ph_hvac", None)
setattr(ApertureProperties, "_ph_hvac", None)
setattr(DoorProperties, "_ph_hvac", None)


# -----------------------------------------------------------------------------
# Step 2)
# create methods to define the public 'ph_hvac' property instances on each obj.properties container


def model_ph_hvac_properties(self):
    # type: (ModelProperties) -> ModelPhHvacProperties
    if self._ph_hvac is None:
        self._ph_hvac = ModelPhHvacProperties(self.host)
    return self._ph_hvac


def room_ph_hvac_properties(self):
    # type: (RoomProperties) -> RoomPhHvacProperties
    if self._ph_hvac is None:
        self._ph_hvac = RoomPhHvacProperties(self.host)
    return self._ph_hvac


def face_ph_hvac_properties(self):
    # type: (FaceProperties) -> RoomPhHvacProperties
    if self._ph_hvac is None:
        self._ph_hvac = FacePhHvacProperties(self.host)
    return self._ph_hvac


def shade_ph_hvac_properties(self):
    # type: (ShadeProperties) -> RoomPhHvacProperties
    if self._ph_hvac is None:
        self._ph_hvac = ShadePhHvacProperties(self.host)
    return self._ph_hvac


def aperture_ph_hvac_properties(self):
    # type: (ApertureProperties) -> RoomPhHvacProperties
    if self._ph_hvac is None:
        self._ph_hvac = AperturePhHvacProperties(self.host)
    return self._ph_hvac


def door_ph_hvac_properties(self):
    # type: (DoorProperties) -> RoomPhHvacProperties
    if self._ph_hvac is None:
        self._ph_hvac = DoorPhHvacProperties(self.host)
    return self._ph_hvac


# -----------------------------------------------------------------------------
# Step 3)
# add public 'ph_hvac' property methods to the Properties classes


setattr(ModelProperties, "ph_hvac", property(model_ph_hvac_properties))
setattr(RoomProperties, "ph_hvac", property(room_ph_hvac_properties))
setattr(FaceProperties, "ph_hvac", property(face_ph_hvac_properties))
setattr(ShadeProperties, "ph_hvac", property(shade_ph_hvac_properties))
setattr(ApertureProperties, "ph_hvac", property(aperture_ph_hvac_properties))
setattr(DoorProperties, "ph_hvac", property(door_ph_hvac_properties))

# -----------------------------------------------------------------------------
# Step 4_
# Add a public Setter


def model_ph_hvac_properties_setter(self, value):
    # type: (ModelProperties, ModelPhHvacProperties) -> None
    if isinstance(value, ModelPhHvacProperties):
        setattr(self, "_ph_hvac", value)


def room_ph_hvac_properties_setter(self, value):
    # type: (RoomProperties, RoomPhHvacProperties) -> None
    if isinstance(value, RoomPhHvacProperties):
        setattr(self, "_ph_hvac", value)


def face_ph_hvac_properties_setter(self, value):
    # type: (FaceProperties, FacePhHvacProperties) -> None
    if isinstance(value, FacePhHvacProperties):
        setattr(self, "_ph_hvac", value)


def shade_ph_hvac_properties_setter(self, value):
    # type: (ShadeProperties, ShadePhHvacProperties) -> None
    if isinstance(value, ShadePhHvacProperties):
        setattr(self, "_ph_hvac", value)


def aperture_ph_hvac_properties_setter(self, value):
    # type: (ApertureProperties, AperturePhHvacProperties) -> None
    if isinstance(value, AperturePhHvacProperties):
        setattr(self, "_ph_hvac", value)


def door_ph_hvac_properties_setter(self, value):
    # type: (DoorProperties, DoorPhHvacProperties) -> None
    if isinstance(value, DoorPhHvacProperties):
        setattr(self, "_ph_hvac", value)


setattr(ModelProperties, "ph_hvac", ModelProperties.ph_hvac.setter(model_ph_hvac_properties_setter))
setattr(RoomProperties, "ph_hvac", RoomProperties.ph_hvac.setter(room_ph_hvac_properties_setter))
setattr(FaceProperties, "ph_hvac", FaceProperties.ph_hvac.setter(face_ph_hvac_properties_setter))
setattr(ShadeProperties, "ph_hvac", ShadeProperties.ph_hvac.setter(shade_ph_hvac_properties_setter))
setattr(ApertureProperties, "ph_hvac", ApertureProperties.ph_hvac.setter(aperture_ph_hvac_properties_setter))
setattr(DoorProperties, "ph_hvac", DoorProperties.ph_hvac.setter(door_ph_hvac_properties_setter))
