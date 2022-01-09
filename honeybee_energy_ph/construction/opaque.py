# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing """

from honeybee import properties
from honeybee_energy.construction import opaque


class OpaqueConstructionPhProperties:
    def __init__(self):
        self.id_num = 0

    def __repr__(self):
        return "{}(id_num={!r})".format(self.__class__.__name__, self.id_num)


class OpaqueConstructionProperties(properties._Properties):

    def __init__(self, host):
        super(OpaqueConstructionProperties, self).__init__(host)
        self._ph = OpaqueConstructionPhProperties()

    @property
    def ph(self):
        return self._ph

    def __repr__(self):
        return "{}(host={!r})".format(self.__class__.__name__, self.host)


class PH_OpaqueConstruction(opaque.OpaqueConstruction):
    """Subclass honeybee_energy's OpaqueConstruction so it can have .properties"""

    __slots__ = ("_properties",)

    def __init__(self, *args, **kwargs):
        super(PH_OpaqueConstruction, self).__init__(*args, **kwargs)
        self._properties = OpaqueConstructionProperties(self)

    @property
    def properties(self):
        return self._properties

    @classmethod
    def from_hb_construction(cls, _hb_construction):
        # type: (opaque.OpaqueConstruction) -> PH_OpaqueConstruction
        obj = cls(
            _hb_construction.identifier,
            _hb_construction.materials,
        )

        return obj

    def __repr__(self):
        return "PH_OpaqueConstruction: {}".format(self.display_name)
