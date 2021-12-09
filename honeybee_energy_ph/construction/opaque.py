# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Subclassing """

from honeybee.properties import FaceProperties, _Properties
from honeybee_energy.construction.opaque import OpaqueConstruction


class OpaqueConstructionPhProperties(FaceProperties):
    def __init__(self, *args, **kwargs):
        super(OpaqueConstructionPhProperties, self).__init__(*args, **kwargs)
        self.id_num = 0


class OpaqueConstructionProperties(_Properties):
    def __repr__(self):
        return "PH_OpaqueConstructionProperties: {!r}".format(self.host)


class PH_OpaqueConstruction(OpaqueConstruction):
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
        # type: (OpaqueConstruction) -> PH_OpaqueConstruction
        obj = cls(
            _hb_construction.identifier,
            _hb_construction.materials,
        )

        return obj

    def __repr__(self):
        return "PH_OpaqueConstruction: {}".format(self.display_name)
