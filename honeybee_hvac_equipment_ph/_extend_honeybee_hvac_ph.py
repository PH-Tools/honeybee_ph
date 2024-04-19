# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Called during __init__ to extend the HB-base class 'properties' with a new '_hvac_equipment_ph' attribute."""

from honeybee.properties import RoomProperties

from .properties.room import RoomPhHvacEquipmentProperties


# Step 1)
# set a private ""._hvac_equipment_ph" attribute on each relevant HB-Core Property class to None


setattr(RoomProperties, "_hvac_equipment_ph", None)


# Step 2)
# create methods to define the public .ph property instances on each obj.properties container


def room_hvac_equipment_ph_properties(self):
    if self._ph is None:
        self._ph = RoomPhHvacEquipmentProperties(self.host)
    return self._ph


# Step 3)
# add public .ph property methods to the Properties classes


setattr(RoomProperties, "hvac_equipment_ph", property(room_hvac_equipment_ph_properties))
