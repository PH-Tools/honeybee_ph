# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""HB-Room Passive-House-HVAC-Equipment Properties."""

try:
    from typing import Any, Dict, Optional
except ImportError:
    pass  # Python2.7

try:
    from ladybug_geometry import geometry3d
except ImportError as e:
    raise ImportError("\nFailed to import ladybug_geometry:\n\t{}".format(e))

try:
    from honeybee.properties import RoomProperties
except ImportError as e:
    raise ImportError("\nFailed to import honeybee:\n\t{}".format(e))


# -----------------------------------------------------------------------------


class RoomPhHvacEquipmentProperties(object):
    def __init__(self, _host):
        # type: (RoomProperties) -> None
        self._host = _host
        self.id_num = 0

    @property
    def host(self):
        # type: () -> RoomProperties
        return self._host

    def duplicate(self, new_host=None, include_spaces=True):
        # type: (Any, bool) -> RoomPhHvacEquipmentProperties
        _host = new_host or self._host
        new_obj = RoomPhHvacEquipmentProperties(_host)
        new_obj.id_num = self.id_num
        return new_obj

    def to_dict(self, abridged=False):
        # type: (bool) -> Dict[str, Any]
        d = {}

        if abridged == False:
            d["type"] = "RoomPhHvacEquipmentProperties"
            d["id_num"] = self.id_num
        else:
            d["type"] = "RoomPhHvacEquipmentPropertiesAbridged"

        return {"ph_hvac": d}

    @classmethod
    def from_dict(cls, _input_dict, host):
        # type: (Dict[str, Any], RoomProperties) -> RoomPhHvacEquipmentProperties
        assert (
            _input_dict["type"] == "RoomPhHvacEquipmentProperties"
        ), "Expected RoomPhHvacEquipmentProperties. Got {}.".format(_input_dict["type"])
        new_prop = cls(host)
        new_prop.id_num = _input_dict.get("id_num", 0)
        return new_prop

    def apply_properties_from_dict(self, room_prop_dict):
        # type: (Dict[str, Any]) -> None
        """Apply properties from a RoomPhPropertiesAbridged dictionary."""
        pass

    def scale(self, factor, origin=None):
        # type: (float, Optional[geometry3d.Point3D]) -> None
        """Scale the room, and all the spaces in the room by a specified factor."""
        pass

    def __str__(self):
        return "{}(host={!r})".format(self.__class__.__name__, self.host)

    def __repr__(self):
        return str(self)

    def ToString(self):
        return self.__repr__()
