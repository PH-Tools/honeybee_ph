# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing"""

from honeybee.properties import _Properties
from ladybug_geometry.geometry3d.pointvector import Point3D


class Point3DPhProperties(object):
    """PH Properties Object for LBT Point3D Objects"""

    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    def duplicate(self, new_host=None):
        # type: (Point3DPhProperties, Any) -> Point3DPhProperties
        _host = new_host or self._host
        new_properties_obj = Point3DPhProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "LBT-Point3D Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        # type: (Point3DPhProperties, bool) -> dict[str, dict]
        base = {"_PH": {}}
        base["_PH"]["type"] = "Point3DPhProperties" if not abridged else "Point3DPhPropertiesAbridged"

        return base

    @classmethod
    def from_dict(cls, data, host):
        # type: (Point3DPhProperties, dict, Any) -> Point3DPhProperties
        assert data["type"] == "Point3DPhProperties", "Expected Point3DPhProperties. Got {}.".format(
            data["type"])

        new_prop = cls(host)
        new_prop.id_num = data.get("id_num", 0)

        return new_prop


class Point3DProperties(_Properties):
    """Properties container for PH Vertix Objects"""

    def __repr__(self):
        return "Point3DProperties: {!r}".format(self.host)


class PH_Point3D(Point3D):
    """Subclass Point3D so it can have properties"""

    __slots__ = ("_properties",)

    def __init__(self, _x, _y, _z):
        super(PH_Point3D, self).__init__(x=_x, y=_y, z=_z)
        self._properties = Point3DProperties(self)

    @property
    def properties(self):
        return self._properties

    def __repr__(self):
        return "PH_Point3D ({}, {}, {})".format(self.x, self.y, self.z)
