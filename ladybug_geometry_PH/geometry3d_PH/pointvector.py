# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""""""

from honeybee.properties import _Properties
from ladybug_geometry.geometry3d.pointvector import Point3D


class Point3DPHProperties(object):
    def __init__(self, _host):
        self._host = _host
        self.id_num = 0

    def duplicate(self, new_host=None):
        _host = new_host or self._host
        new_properties_obj = Point3DPHProperties(_host)
        new_properties_obj.id_num = self.id_num

        return new_properties_obj

    def ToString(self):
        return self.__repr__()

    def __repr__(self):
        return "LBT-Point3D Passive House Properties: [host: {}]".format(self.host.display_name)

    def to_dict(self, abridged=False):
        base = {'_PH': {}}
        base['_PH']['type'] = 'Point3DPHProperties' if not \
            abridged else 'Point3DPHPropertiesAbridged'

        return base

    @classmethod
    def from_dict(cls, data, host):
        assert data['type'] == 'Point3DPHProperties', \
            'Expected Point3DPHProperties. Got {}.'.format(data['type'])

        new_prop = cls(host)
        new_prop.id_num = data.get('id_num', 0)

        return new_prop


class PHXVertixProperties(_Properties):
    def __repr__(self):
        return "PHXVertixProperties: {!r}".format(self.host)


class PHX_Vertix(Point3D):
    """Subclass Point3D so it can have properties"""

    __slots__ = ("properties",)

    def __init__(self, _x, _y, _z):
        super(PHX_Vertix, self).__init__(x=_x, y=_y, z=_z)
        self.properties = PHXVertixProperties(self)

    def __repr__(self):
        return "PHX_Vertix ({}, {}, {})".format(self.x, self.y, self.z)
