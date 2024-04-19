# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Called during __init__ to extend the HB-base class 'properties' with a new '_ph_hvac' attribute."""

from honeybee.properties import RoomProperties

from .properties.room import RoomPhHvacEquipmentProperties


# Step 1)
# set a private 'ph_hvac' attribute on each relevant HB-Core Property class to None


setattr(RoomProperties, "_ph_hvac", None)


# Step 2)
# create methods to define the public 'ph_hvac' property instances on each obj.properties container


def room_ph_hvac_properties(self):
    # type: (RoomProperties) -> RoomPhHvacEquipmentProperties
    if self._ph_hvac is None:
        self._ph_hvac = RoomPhHvacEquipmentProperties(self.host)
    return self._ph_hvac


# Step 3)
# add public 'ph_hvac' property methods to the Properties classes


setattr(RoomProperties, "ph_hvac", property(room_ph_hvac_properties))


# Step 4_
# Add a public Setter


def room_ph_hvac_properties_setter(self, value):
    # type: (RoomProperties, RoomPhHvacEquipmentProperties) -> None
    if isinstance(value, RoomPhHvacEquipmentProperties):
        self._ph_hvac = value


setattr(RoomProperties, "ph_hvac", RoomProperties.ph_hvac.setter(room_ph_hvac_properties_setter))
