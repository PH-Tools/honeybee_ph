# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing Ladybug Point3D Object to allow for .properties"""

from honeybee import properties
from ladybug_geometry.geometry3d.pointvector import Point3D as LB_Point3D


class Point3DPhProperties(object):
    """PH Properties Object for LBT Point3D Objects"""

    def __init__(self):
        self.id_num = 0


class Point3DProperties(properties._Properties):
    """Properties for LBT Point3D Objects"""

    def __init__(self, host):
        super(Point3DProperties, self).__init__(host)
        self._ph = Point3DPhProperties()

    @property
    def ph(self):
        return self._ph

    def __repr__(self):
        return "{}(host={!r})".format(self.__class__.__name__, self.host)


class PH_Point3D(LB_Point3D):
    """Subclass Ladybug's Point3D in order to add .properties"""

    __slots__ = ("_properties",)

    def __init__(self, _x, _y, _z):
        super().__init__(x=_x, y=_y, z=_z)
        self._properties = Point3DProperties(self)

    @property
    def properties(self):
        return self._properties

    def __repr__(self):
        return "PH_Point3D ({}, {}, {})".format(self.x, self.y, self.z)
