# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing """

from honeybee.properties import FaceProperties, _Properties
from honeybee_energy.construction.opaque import OpaqueConstruction


class OpaqueConstructionPHProperties(FaceProperties):
    def __init__(self, *args, **kwargs):
        super(OpaqueConstructionPHProperties, self).__init__(*args, **kwargs)
        self.id_num = 0


class OpaqueConstructionProperties(_Properties):
    def __repr__(self):
        return "PHX_OpaqueConstructionProperties: {!r}".format(self.host)


class PHX_OpaqueConstruction(OpaqueConstruction):
    """Subclass honeybee_energy's OpaqueConstruction so it can have .properties"""

    __slots__ = ("properties",)

    def __init__(self, *args, **kwargs):
        super(PHX_OpaqueConstruction, self).__init__(*args, **kwargs)
        self.properties = OpaqueConstructionProperties(self)

    @classmethod
    def from_hb_construction(cls, _hb_construction):
        # type: (OpaqueConstruction) -> PHX_OpaqueConstruction
        obj = cls(
            _hb_construction.identifier,
            _hb_construction.materials,
        )

        return obj

    def __repr__(self):
        return "PHX_OpaqueConstruction: {}".format(self.display_name)
