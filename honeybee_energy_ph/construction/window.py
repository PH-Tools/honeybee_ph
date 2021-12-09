# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

""" """

from honeybee.properties import FaceProperties, _Properties
from honeybee_energy.construction.window import WindowConstruction as HB_WindowConstruction


class WindowConstructionPhProperties(FaceProperties):
    def __init__(self, *args, **kwargs):
        super(WindowConstructionPhProperties, self).__init__(*args, **kwargs)
        self.id_num = 0


class WindowConstructionProperties(_Properties):
    def __repr__(self):
        return "PH_WindowConstructionProperties: {!r}".format(self.host)


class PH_WindowConstruction(HB_WindowConstruction):
    """Subclass honeybee_energy's WindowConstruction so it can have .properties"""

    __slots__ = ("_properties",)

    def __init__(self, *args, **kwargs):
        super(PH_WindowConstruction, self).__init__(*args, **kwargs)
        self._properties = WindowConstructionProperties(self)

    @property
    def properties(self):
        return self._properties

    @classmethod
    def from_hb_construction(cls, _hb_construction):
        # type: (Type[PH_WindowConstruction], HB_WindowConstruction) -> PH_WindowConstruction
        obj = cls(
            _hb_construction.identifier,
            _hb_construction.materials,
        )

        return obj

    def __repr__(self):
        return "PH_WindowConstruction: {}".format(self.display_name)
